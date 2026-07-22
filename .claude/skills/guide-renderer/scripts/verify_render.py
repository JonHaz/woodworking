#!/usr/bin/env python3
"""verify_render.py — check a rendered master build document against its verified spec.

The render gate. It does for a guide what verify_cutlist.py does for a design: turns
"the model rendered it faithfully" from a hope into a mechanical check. It compares the
emitted HTML/SVG against the spec cut-verifier already passed and reports where they
disagree.

Hard boundary — it does ZERO cut-list arithmetic. All yield and stack-up math lives in
verify_cutlist.py; this script only compares what is on the page to what is in the spec.
A number a figure needs that is not in the spec is a spec gap, reported as such, never
computed here.

Findings carry a level:
  fail  — a real defect; gates (exit 1).
  warn  — advisory; gates only under --strict.
  info  — a census note (e.g. a figure with no machine-readable scale). Never gates;
          this is the evidence base for deciding what the spec schema still lacks.

Checks:
  R (structure, spec-free): R-ENV envelope, R-NET self-containment, R-SVG svg attrs,
     R-PRINT print contract, R-PALETTE house palette, R-SCALE declared figure scale.
  N (numbers vs spec):      N-FINISHED finished dims, N-KERF kerf stated, N-STOCK every
     stock dimension appears on the page.
  G (geometry vs spec):     G-SCALE derive a cut diagram's scale from its sheet outline,
     G-RIP every rip_plan crosscut appears as a drawn rect at that scale.

Parsing note: the masters are quirks-mode fragments (no doctype/html/head/body, an
undefined &nbsp;, raw & in the fonts URL), so xml.etree cannot read them. Structure is
parsed with html.parser; rects are pulled from the raw svg text with a regex.

Exit codes:  0 = clean (no fail; no warn under --strict)   1 = findings gate   2 = usage/parse error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

TOL = 0.02  # inches; covers the shipped masters' hand-rounding (155.3 vs 155.25 at 4.5px/in)

# the 18 house palette tokens, byte-identical across all three shipped masters
PALETTE_TOKENS = [
    "--paper", "--ink", "--graphite", "--rule", "--blue", "--blue-soft",
    "--wood", "--wood-soft", "--warn", "--good",
    "--top", "--shelf", "--side", "--div", "--str", "--waste", "--rail", "--rung",
]

ALLOWED_HOST = "fonts.googleapis.com"


# --------------------------------------------------------------------------- #
# document model
# --------------------------------------------------------------------------- #
class _DocParser(HTMLParser):
    """Collects prose text (outside style/script/svg), style text, comments, external
    references, and the doctype/html/head/body presence flags."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.prose: list[str] = []
        self.style: list[str] = []
        self.comments: list[str] = []
        self.refs: list[str] = []          # (kind:attr) external references from tags
        self.saw_doctype = False
        self.saw_html = False
        self.saw_head = False
        self.saw_body = False
        self.first_tag: str | None = None
        self._skip_depth = 0               # inside style/script/svg
        self._in_style = False

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype"):
            self.saw_doctype = True

    def handle_starttag(self, tag, attrs):
        if self.first_tag is None:
            self.first_tag = tag
        if tag == "html":
            self.saw_html = True
        elif tag == "head":
            self.saw_head = True
        elif tag == "body":
            self.saw_body = True
        if tag in ("style", "script", "svg"):
            self._skip_depth += 1
            if tag == "style":
                self._in_style = True
        d = dict(attrs)
        if tag == "link" and d.get("href"):
            self.refs.append(d["href"])
        if tag in ("script", "img", "iframe", "audio", "video", "source") and d.get("src"):
            self.refs.append(d["src"])

    def handle_endtag(self, tag):
        if tag in ("style", "script", "svg") and self._skip_depth > 0:
            self._skip_depth -= 1
            if tag == "style":
                self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.style.append(data)
        elif self._skip_depth == 0:
            self.prose.append(data)

    def handle_comment(self, data):
        self.comments.append(data)


# --------------------------------------------------------------------------- #
# number normalization
# --------------------------------------------------------------------------- #
_UNI_FRAC = re.compile(r"(\d+)?\s*([¼-¾⅐-⅞])")
_MIXED = re.compile(r"(\d+)[-\s](\d+)/(\d+)")
_FRAC = re.compile(r"(\d+)/(\d+)")
_NUM = re.compile(r"\d+\.\d+|\d+")


def _sub_unifrac(m: "re.Match") -> str:
    whole = int(m.group(1)) if m.group(1) else 0
    frac = unicodedata.numeric(m.group(2))
    return f"{whole + frac:g}"


def normalize_numbers(text: str) -> str:
    """Rewrite unicode and ascii fractions to decimals so they compare numerically.
    e.g. '⅛' -> '0.125', '54-1/8' -> '54.125', '1/8' -> '0.125'."""
    text = _UNI_FRAC.sub(_sub_unifrac, text)
    text = _MIXED.sub(lambda m: f"{int(m[1]) + int(m[2]) / int(m[3]):g}", text)
    text = _FRAC.sub(lambda m: f"{int(m[1]) / int(m[2]):g}", text)
    return text


def numbers_in(text: str) -> list[float]:
    return [float(t) for t in _NUM.findall(normalize_numbers(text))]


def present(value: float, pool: set[float], tol: float = TOL) -> bool:
    return any(abs(value - p) <= tol for p in pool)


# --------------------------------------------------------------------------- #
# svg extraction (regex on raw source — html.parser mangles nested void tags)
# --------------------------------------------------------------------------- #
_SVG = re.compile(r"<svg\b[^>]*>.*?</svg>", re.S | re.I)
_ATTR = lambda name: re.compile(r'\b' + name + r'\s*=\s*"([^"]*)"', re.I)
_VIEWBOX = _ATTR("viewBox")
_WIDTH = _ATTR("width")
_HEIGHT = _ATTR("height")
_DATASCALE = _ATTR("data-scale")
_RECT = re.compile(r"<rect\b[^>]*>", re.I)


def svg_blocks(source: str) -> list[str]:
    return _SVG.findall(source)


def svg_tag(block: str) -> str:
    return block[: block.index(">") + 1]


def rects(block: str) -> list[tuple]:
    """Return (w_px, h_px) for every rect that declares both."""
    out = []
    for r in _RECT.findall(block):
        w = _WIDTH.search(r)
        h = _HEIGHT.search(r)
        if w and h:
            try:
                out.append((float(w.group(1)), float(h.group(1))))
            except ValueError:
                pass
    return out


# --------------------------------------------------------------------------- #
# findings helper
# --------------------------------------------------------------------------- #
def finding(kind: str, level: str, where: str, detail: str) -> dict:
    return {"kind": kind, "level": level, "where": where, "detail": detail}


# --------------------------------------------------------------------------- #
# R — structure
# --------------------------------------------------------------------------- #
def check_envelope(source: str, doc: _DocParser) -> list[dict]:
    out = []
    head = source.lstrip()
    if not head.lower().startswith('<meta charset="utf-8">'):
        out.append(finding("R-ENV", "fail", "top of file",
                            'master must open with <meta charset="utf-8">'))
    for flag, name in ((doc.saw_doctype, "<!doctype>"), (doc.saw_html, "<html>"),
                       (doc.saw_head, "<head>"), (doc.saw_body, "<body>")):
        if flag:
            out.append(finding("R-ENV", "fail", name,
                               f"master is a fragment; {name} must not appear"))
    if not source.rstrip().endswith("</div>"):
        out.append(finding("R-ENV", "fail", "end of file",
                            "master must end with the closing </div> of .sheet"))
    return out


def check_network(doc: _DocParser) -> list[dict]:
    out = []
    style = "".join(doc.style)
    urls = re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", style)
    urls += re.findall(r"@import\s+url\(\s*['\"]?([^'\")]+)", style)
    urls += doc.refs
    seen: set[str] = set()
    external = [u for u in urls
                if (u.startswith("http://") or u.startswith("https://"))
                and not (u in seen or seen.add(u))]
    allowed = [u for u in external if ALLOWED_HOST in u]
    disallowed = [u for u in external if ALLOWED_HOST not in u]
    for u in disallowed:
        out.append(finding("R-NET", "fail", u,
                           "only the Google Fonts @import may reference the network"))
    if not allowed:
        out.append(finding("R-NET", "warn", "fonts",
                           "no Google Fonts @import found; confirm fonts are intended"))
    if "system-ui" not in style and "sans-serif" not in style:
        out.append(finding("R-NET", "warn", "font stacks",
                           "no system-ui/sans-serif fallback; file will not print without the webfont"))
    return out


def check_svg_attrs(blocks: list[str]) -> list[dict]:
    out = []
    for i, b in enumerate(blocks, 1):
        tag = svg_tag(b)
        if not _VIEWBOX.search(tag):
            out.append(finding("R-SVG", "fail", f"figure {i}", "svg has no viewBox"))
        if _WIDTH.search(tag) or _HEIGHT.search(tag):
            out.append(finding("R-SVG", "fail", f"figure {i}",
                               "svg declares width/height; it must scale by viewBox only"))
    return out


def check_print(doc: _DocParser) -> list[dict]:
    out = []
    style = "".join(doc.style)
    flat = re.sub(r"\s+", "", style)
    if "@page" not in flat:
        out.append(finding("R-PRINT", "fail", "@page",
                           "no @page rule; printed margins are undefined"))
    if "print-color-adjust:exact" not in flat:
        out.append(finding("R-PRINT", "fail", "print-color-adjust",
                           "no print-color-adjust:exact; legend swatches drop in default print"))
    if "break-inside:avoid" not in flat:
        out.append(finding("R-PRINT", "fail", "break-inside",
                           "no modern break-inside:avoid; figures may split across pages"))
    return out


def check_palette(doc: _DocParser) -> list[dict]:
    out = []
    style = "".join(doc.style)
    missing = [t for t in PALETTE_TOKENS if not re.search(re.escape(t) + r"\s*:", style)]
    if missing:
        out.append(finding("R-PALETTE", "warn", ":root",
                           f"palette tokens not defined: {', '.join(missing)}"))
    return out


def check_scale_declared(source: str, blocks: list[str]) -> list[dict]:
    """Census: which figures declare a machine-readable scale. Info-level by design —
    the shipped masters keep scale in HTML comments, which this flags as the gap that
    motivates a data-scale attribute."""
    out = []
    undeclared = [i for i, b in enumerate(blocks, 1) if not _DATASCALE.search(svg_tag(b))]
    if undeclared:
        out.append(finding("R-SCALE", "info", "figures " + ",".join(map(str, undeclared)),
                           f"{len(undeclared)}/{len(blocks)} figures declare no machine-readable "
                           "data-scale (scale lives only in a comment or the caption)"))
    return out


# --------------------------------------------------------------------------- #
# N — numbers vs spec
# --------------------------------------------------------------------------- #
def check_finished(spec: dict, pool: set[float]) -> list[dict]:
    out = []
    fin = spec.get("finished") or {}
    for k in ("width", "depth", "height"):
        if k in fin and not present(float(fin[k]), pool):
            out.append(finding("N-FINISHED", "fail", k,
                               f"finished {k} {fin[k]} does not appear on the page"))
    return out


def check_kerf(spec: dict, pool: set[float]) -> list[dict]:
    out = []
    kerf = float(spec.get("kerf", 0.125))
    if not present(kerf, pool):
        out.append(finding("N-KERF", "warn", "kerf",
                           f"spec kerf {kerf} is stated nowhere in the guide"))
    return out


def check_stock(spec: dict, pool: set[float]) -> list[dict]:
    out = []
    wanted: set[float] = set()
    ss = spec.get("sheet_stock") or {}
    for p in ss.get("parts", []):
        wanted.add(round(float(p["w"]), 4))
        wanted.add(round(float(p["d"]), 4))
    st = spec.get("stick_stock") or {}
    for p in st.get("parts", []):
        wanted.add(round(float(p["length"]), 4))
    missing = sorted(v for v in wanted if not present(v, pool))
    if missing:
        out.append(finding("N-STOCK", "warn", "cut lists",
                           f"stock dimensions not found on the page: {missing}"))
    return out


# --------------------------------------------------------------------------- #
# G — geometry vs spec
# --------------------------------------------------------------------------- #
def _derive_scale(rs: list[tuple], sw: float, sl: float) -> "float | None":
    """Derive px/in from a rect matching the full sheet in either orientation."""
    if not rs:
        return None
    big = max(rs, key=lambda t: t[0] * t[1])
    for a, b in ((big[0], big[1]), (big[1], big[0])):
        cand = a / sl
        if abs(b / cand - sw) <= TOL * cand:
            return cand
    return None


def check_geometry(spec: dict, blocks: list[str]) -> list[dict]:
    """Derive each sheet diagram's px/in scale from its sheet outline, then confirm every
    rip_plan crosscut is drawn as a rect *somewhere* across the diagrams.

    The check is a union, not per-figure, on purpose: the schema does not say which sheet
    a strip lands on (rip_plan carries no sheet index), so a per-figure test would flag a
    crosscut as missing merely because it lives on another sheet. That missing mapping is
    itself reported by check_schema_gaps."""
    out = []
    ss = spec.get("sheet_stock")
    if not ss:
        return out
    sw, sl = float(ss["sheet"][0]), float(ss["sheet"][1])
    rip = ss.get("rip_plan", [])
    if not rip:
        return out
    crosscuts = sorted({round(float(c), 4) for strip in rip for c in strip["crosscuts"]})

    drawn: set[float] = set()
    for i, b in enumerate(blocks, 1):
        scale = _derive_scale(rects(b), sw, sl)
        if scale is None:
            continue
        out.append(finding("G-SCALE", "info", f"figure {i}",
                           f"derived scale {scale:g} px/in from the sheet outline"))
        for (w, h) in rects(b):
            drawn.add(round(w / scale, 4))
            drawn.add(round(h / scale, 4))
    if not drawn:
        out.append(finding("G-SCALE", "info", "sheet diagrams",
                           "no figure carried a derivable sheet outline; geometry unverified"))
        return out
    unmatched = [c for c in crosscuts if not present(c, drawn)]
    if unmatched:
        out.append(finding("G-RIP", "warn", "sheet diagrams",
                           f"rip_plan crosscuts drawn nowhere at the derived scale: {unmatched}"))
    return out


def check_schema_gaps(spec: dict) -> list[dict]:
    """Census of what the render gate *cannot* check because the spec lacks the field.
    This is the evidence base for the Stage 4 schema extension — each info finding is a
    requirement, not a defect in this guide."""
    out = []
    ss = spec.get("sheet_stock") or {}
    rip = ss.get("rip_plan", [])
    if rip:
        if any("width" not in strip for strip in rip):
            out.append(finding("G-GAP", "info", "rip_plan",
                               "strips carry no rip width; a strip's cross-dimension can only "
                               "be inferred, so a generated diagram cannot place it exactly"))
        bare = any(not isinstance(c, dict) for strip in rip for c in strip["crosscuts"])
        if bare:
            out.append(finding("G-GAP", "info", "rip_plan.crosscuts",
                               "crosscuts are bare numbers with no part reference; a diagram "
                               "cannot label which part a cut yields without dimension-guessing"))
        out.append(finding("G-GAP", "info", "rip_plan",
                           "strips carry no sheet index; the diagram-to-sheet grouping cannot "
                           "be verified against the spec"))
    if any("id" not in p for p in ss.get("parts", [])):
        out.append(finding("G-GAP", "info", "sheet_stock.parts",
                           "sheet parts have no id; a drawn rect can only be matched to a part "
                           "by dimension, which is ambiguous when two parts share a dimension"))
    st = spec.get("stick_stock") or {}
    if any("id" not in p for p in st.get("parts", [])):
        out.append(finding("G-GAP", "info", "stick_stock.parts",
                           "stick parts have no id; two distinct parts can share a length "
                           "(the stove-shelf fence and stretcher both 31 in) and be indistinguishable"))
    return out


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
def run(spec: dict, source: str) -> list[dict]:
    doc = _DocParser()
    doc.feed(source)
    blocks = svg_blocks(source)
    pool = set(round(v, 4) for v in numbers_in("".join(doc.prose)))

    findings: list[dict] = []
    findings += check_envelope(source, doc)
    findings += check_network(doc)
    findings += check_svg_attrs(blocks)
    findings += check_print(doc)
    findings += check_palette(doc)
    findings += check_scale_declared(source, blocks)
    findings += check_finished(spec, pool)
    findings += check_kerf(spec, pool)
    findings += check_stock(spec, pool)
    findings += check_geometry(spec, blocks)
    findings += check_schema_gaps(spec)
    return findings


def _counts(findings: list[dict]) -> dict:
    c = {"fail": 0, "warn": 0, "info": 0}
    for f in findings:
        c[f["level"]] = c.get(f["level"], 0) + 1
    return c


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", required=True, help="path to the verified design spec (.json)")
    ap.add_argument("--guide", required=True, help="path to the rendered master (.html)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--strict", action="store_true",
                    help="treat warn findings as gating (exit 1)")
    args = ap.parse_args(argv)

    spec_path = Path(args.spec)
    guide_path = Path(args.guide)
    for p in (spec_path, guide_path):
        if not p.exists():
            print(f"error: file not found: {p}", file=sys.stderr)
            return 2
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"error: could not parse spec: {e}", file=sys.stderr)
        return 2
    if not isinstance(spec, dict):
        print("error: spec must be a mapping/object", file=sys.stderr)
        return 2
    try:
        source = guide_path.read_text(encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        print(f"error: could not read guide: {e}", file=sys.stderr)
        return 2

    findings = run(spec, source)
    counts = _counts(findings)
    gating = counts["fail"] + (counts["warn"] if args.strict else 0)

    if args.format == "json":
        print(json.dumps({
            "spec": spec.get("project", str(spec_path)),
            "guide": guide_path.name,
            "ok": gating == 0,
            "counts": counts,
            "findings": findings,
        }, indent=2))
    else:
        print(f"verify-render: {guide_path.name}")
        order = {"fail": 0, "warn": 1, "info": 2}
        for f in sorted(findings, key=lambda x: order.get(x["level"], 3)):
            print(f"  [{f['level'].upper():4}] {f['kind']}: {f['where']}")
            print(f"         {f['detail']}")
        verdict = "ALL CHECKS PASS" if gating == 0 else f"{gating} GATING FINDING(S)"
        print(f"\n{verdict}  (fail={counts['fail']} warn={counts['warn']} info={counts['info']})")
    return 0 if gating == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit the shop inventory for unconfirmed tools and unmeasured stock.

Reads the two OKF inventory files (``tools.md`` and ``materials-on-hand.md``),
parses their GitHub-style markdown tables, and reports the gaps that undercut
build planning:

  * tools whose Status is ``inferred`` (a guess, not verified) or blank/unknown
  * dimensional-lumber rows whose size cell is not a real measurement

``confirmed`` and ``wanted`` tools are treated as *resolved* — ``confirmed``
means Jon verified it, ``wanted`` is a deliberate "don't own it" decision. The
gap this catches is the unverified middle: ``inferred`` entries that
``build-planner`` is forced to treat as likely-but-verify.

Exit codes: 0 = census complete (nothing to confirm) · 1 = findings ·
2 = usage/parse error. Run from the repo root, or pass explicit paths.
"""

import argparse
import json
import os
import re
import sys

# A status is "resolved" when Jon has made a decision about it: he owns it
# (confirmed), plans to buy it (wanted), or has verified he does not own it
# (not owned). The only real gap is `inferred` — a guess nobody has checked.
RESOLVED_STATUSES = {"confirmed", "wanted", "not owned"}
TALLY_KEYS = ("confirmed", "inferred", "wanted", "not owned", "unknown")
# a measurement cell looks like "54 1/8 x 1 1/2 x 3 1/2" — needs a digit and a
# dimension separator (x or the unicode multiplication sign).
_SEP = re.compile(r"[x×]", re.IGNORECASE)
_DIGIT = re.compile(r"\d")


def _split_row(line):
    """Split a markdown table row into stripped cell strings."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_divider(cells):
    """True for the |---|---| header divider row."""
    return all(re.fullmatch(r":?-{2,}:?", c) is not None for c in cells if c)


def parse_tables(text):
    """Yield (headers, rows) for each markdown table in *text*."""
    lines = text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < n and _is_divider(_split_row(lines[i + 1])):
            headers = _split_row(line)
            rows = []
            j = i + 2
            while j < n and lines[j].strip().startswith("|"):
                cells = _split_row(lines[j])
                if not _is_divider(cells):
                    rows.append(cells)
                j += 1
            yield headers, rows
            i = j
        else:
            i += 1


def _col_index(headers, *names):
    """Index of the first header whose lowercased text contains any of *names*."""
    lowered = [h.lower() for h in headers]
    for name in names:
        for idx, h in enumerate(lowered):
            if name in h:
                return idx
    return None


def audit_tools(path):
    """Return (findings, tally) for the tools inventory file."""
    findings = []
    tally = {k: 0 for k in TALLY_KEYS}
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for headers, rows in parse_tables(text):
        status_i = _col_index(headers, "status")
        tool_i = _col_index(headers, "tool", "what", "item")
        if status_i is None:
            continue
        for cells in rows:
            if status_i >= len(cells):
                continue
            status = cells[status_i].strip().lower()
            # normalize bold markers (**confirmed**) and "not-owned" spellings
            status = status.replace("*", "").replace("-", " ")
            status = " ".join(status.split())
            name = cells[tool_i].strip() if tool_i is not None and tool_i < len(cells) else cells[0].strip()
            if status in tally:
                tally[status] += 1
            else:
                tally["unknown"] += 1
            if status not in RESOLVED_STATUSES:
                findings.append({
                    "file": path,
                    "kind": "unconfirmed-tool",
                    "item": name,
                    "status": status or "(blank)",
                })
    return findings, tally


def audit_materials(path):
    """Return findings for stock rows that carry no real measurement."""
    findings = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for headers, rows in parse_tables(text):
        size_i = _col_index(headers, "size", "dimension")
        if size_i is None:
            continue
        item_i = _col_index(headers, "what", "item", "material")
        for cells in rows:
            if size_i >= len(cells):
                continue
            size = cells[size_i]
            measured = bool(_DIGIT.search(size)) and bool(_SEP.search(size))
            if not measured:
                name = cells[item_i].strip() if item_i is not None and item_i < len(cells) else cells[0].strip()
                findings.append({
                    "file": path,
                    "kind": "unmeasured-stock",
                    "item": name or "(row)",
                    "size": size or "(blank)",
                })
    return findings


def render_text(tools_findings, tally, mat_findings, tools_path, mat_path):
    out = []
    total = len(tools_findings) + len(mat_findings)
    resolved = tally["confirmed"] + tally["wanted"] + tally["not owned"]
    counted = sum(tally.values())
    out.append("Shop inventory audit")
    out.append("=" * 20)
    out.append(
        f"Tools: {counted} listed — {tally['confirmed']} confirmed, "
        f"{tally['wanted']} wanted, {tally['not owned']} not owned, "
        f"{tally['inferred']} inferred, {tally['unknown']} unknown status."
    )
    if tools_findings:
        out.append("")
        out.append(f"Unconfirmed tools ({len(tools_findings)}) in {tools_path}:")
        for f in tools_findings:
            out.append(f"  - {f['item']}  [{f['status']}]")
    if mat_findings:
        out.append("")
        out.append(f"Unmeasured stock ({len(mat_findings)}) in {mat_path}:")
        for f in mat_findings:
            out.append(f"  - {f['item']}  (size: {f['size']})")
    out.append("")
    if total == 0:
        out.append(f"CENSUS COMPLETE — {resolved} tools resolved, all stock measured.")
    else:
        out.append(
            f"{total} ITEM(S) NEED CONFIRMATION — interview Jon to resolve them, "
            "then update the inventory files and re-run."
        )
    return "\n".join(out)


def run(tools_path, mat_path):
    tools_findings, tally = ([], {k: 0 for k in TALLY_KEYS})
    mat_findings = []
    if os.path.exists(tools_path):
        tools_findings, tally = audit_tools(tools_path)
    if os.path.exists(mat_path):
        mat_findings = audit_materials(mat_path)
    return tools_findings, tally, mat_findings


def main(argv=None):
    p = argparse.ArgumentParser(description="Audit the shop tool/material inventory.")
    p.add_argument("--tools", default="knowledge/shop/tools.md",
                   help="path to the tools inventory (default: knowledge/shop/tools.md)")
    p.add_argument("--materials", default="knowledge/shop/materials-on-hand.md",
                   help="path to the materials inventory (default: knowledge/shop/materials-on-hand.md)")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args(argv)

    if not os.path.exists(args.tools) and not os.path.exists(args.materials):
        sys.stderr.write(
            f"error: neither {args.tools} nor {args.materials} exists — "
            "run from the repo root or pass --tools/--materials.\n"
        )
        return 2

    try:
        tools_findings, tally, mat_findings = run(args.tools, args.materials)
    except Exception as exc:  # noqa: BLE001 - surface any parse error as exit 2
        sys.stderr.write(f"error: {exc}\n")
        return 2

    total = len(tools_findings) + len(mat_findings)
    if args.format == "json":
        print(json.dumps({
            "tools_path": args.tools,
            "materials_path": args.materials,
            "tally": tally,
            "unconfirmed_tools": tools_findings,
            "unmeasured_stock": mat_findings,
            "total_findings": total,
            "census_complete": total == 0,
        }, indent=2))
    else:
        print(render_text(tools_findings, tally, mat_findings, args.tools, args.materials))

    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())

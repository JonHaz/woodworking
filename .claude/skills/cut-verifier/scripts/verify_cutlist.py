#!/usr/bin/env python3
"""verify_cutlist.py — deterministic geometry & yield check for a woodworking spec.

Re-derives a proposed design's numbers from scratch and reports whether they
close. Encodes lessons 1-4 of knowledge/methods/lessons-learned.md:

  1. Captured panels lose 2x material thickness (a part that fits *between* two
     0.75-in walls must be span - 2*0.75 wide).  -> captured_checks
  2. (Face-frame encroachment is a captured_check with walls set accordingly.)
  3. Allow ~1/8-in kerf per cut in yield math.   -> stick_stock / sheet_stock
  4. Firm counts (sheets/sticks from yield) are separated from estimates
     (screws/glue/pads).                          -> parts kind, report

Input is a JSON spec (see references/spec-schema.md). YAML is accepted if
PyYAML is installed, but JSON is the canonical, dependency-free format.

Exit codes:  0 = all checks pass   1 = one or more checks fail   2 = usage/spec error
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

EPS = 1e-6  # dimensions are exact fractions of an inch; tolerate float noise only


# --------------------------------------------------------------------------- #
# spec loading
# --------------------------------------------------------------------------- #
def load_spec(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ModuleNotFoundError:
            raise SystemExit(
                "spec is YAML but PyYAML is not installed; convert to JSON or "
                "`pip install pyyaml`"
            )
        return yaml.safe_load(text)
    return json.loads(text)


def approx(a: float, b: float, tol: float = EPS) -> bool:
    return abs(a - b) <= tol


# --------------------------------------------------------------------------- #
# checks — each returns a list of finding dicts
# --------------------------------------------------------------------------- #
def check_stackups(spec: dict) -> list[dict]:
    """Every ordered list of segments must sum to its finished dimension."""
    out = []
    for su in spec.get("stackups", []):
        name = su.get("name", "?")
        segs = su.get("segments", [])
        target = su["equals"]
        total = sum(segs)
        ok = approx(total, target)
        out.append(
            {
                "check": "stackup",
                "name": name,
                "ok": ok,
                "detail": f"{' + '.join(_fmt(s) for s in segs)} = {_fmt(total)}"
                + ("" if ok else f"  (expected {_fmt(target)}, off by {_fmt(total - target)})"),
                "corrected": None if ok else target,
            }
        )
    return out


def check_captured(spec: dict) -> list[dict]:
    """A captured part = span - walls*thickness. Flags lesson #1 / #2 errors."""
    out = []
    default_t = spec.get("material_thickness", 0.75)
    for c in spec.get("captured_checks", []):
        name = c.get("name", "?")
        span = c["span"]
        walls = c.get("walls", 2)
        t = c.get("thickness", default_t)
        actual = c["actual"]
        expected = span - walls * t
        ok = approx(actual, expected)
        out.append(
            {
                "check": "captured",
                "name": name,
                "ok": ok,
                "detail": f"fits between {walls}x{_fmt(t)} in a {_fmt(span)} span "
                f"-> should be {_fmt(expected)}; spec says {_fmt(actual)}"
                + ("" if ok else "  << does not fit"),
                "corrected": None if ok else expected,
            }
        )
    return out


def _ffd_bins(pieces: list[float], stock_lengths: list[float], kerf: float):
    """First-fit-decreasing 1-D cutting: place `pieces` into bins whose
    capacities are drawn from stock_lengths (each usable once, longest first).
    A cut consumes piece length + kerf. Returns (placed_all, bins_used_detail,
    leftover_pieces)."""
    pieces = sorted(pieces, reverse=True)
    # bins: list of [remaining, original_length, [pieces...]]
    bins: list[list] = []
    stock = sorted(stock_lengths, reverse=True)
    stock_idx = 0
    leftover = []
    for p in pieces:
        need = p + kerf
        placed = False
        for b in bins:
            if b[0] + EPS >= need:
                b[0] -= need
                b[2].append(p)
                placed = True
                break
        if not placed:
            # open a new bin from remaining stock
            if stock_idx < len(stock):
                cap = stock[stock_idx]
                stock_idx += 1
                if cap + EPS >= need:
                    bins.append([cap - need, cap, [p]])
                else:
                    leftover.append(p)  # piece longer than any stock
            else:
                leftover.append(p)
    return (len(leftover) == 0, bins, leftover)


def check_sticks(spec: dict) -> list[dict]:
    """1-D cutting feasibility for linear stock (2x4s, etc.)."""
    out = []
    ss = spec.get("stick_stock")
    if not ss:
        return out
    kerf = spec.get("kerf", 0.125)
    # explode parts and stock into flat piece / length lists
    pieces = []
    for p in ss.get("parts", []):
        pieces += [p["length"]] * p["qty"]
    on_hand = []
    for s in ss.get("on_hand", []):
        on_hand += [s["length"]] * s["qty"]
    new = []
    for s in ss.get("new", []):
        new += [s["length"]] * s["qty"]

    total_needed = sum(pieces)
    # Prefer on-hand first (CLAUDE.md: allocate on-hand before buying).
    ok_onhand, bins_oh, leftover_after_oh = _ffd_bins(pieces, on_hand, kerf)
    # place whatever's left onto NEW stock
    ok_all, bins_new, leftover = _ffd_bins(leftover_after_oh, new, kerf)
    new_sticks_used = len(bins_new)
    new_provided = len(new)

    detail = (
        f"{len(pieces)} pieces, {_fmt(total_needed)} lin in needed; "
        f"kerf {_fmt(kerf)}/cut. On-hand used: {len(bins_oh)}/{len(on_hand)}. "
        f"New sticks needed: {new_sticks_used}"
    )
    if new_provided:
        detail += f" (spec provides {new_provided})"
    ok = ok_all and (new_provided == 0 or new_sticks_used <= new_provided)
    if not ok_all:
        detail += f"; UNPLACED pieces: {[_fmt(x) for x in leftover]}"
    elif new_provided and new_sticks_used > new_provided:
        detail += "; NOT ENOUGH new stock provided"
    out.append(
        {
            "check": "stick_yield",
            "name": ss.get("name", "linear stock"),
            "ok": ok,
            "detail": detail,
            "corrected": None if ok else new_sticks_used,
        }
    )
    return out


def check_sheets(spec: dict) -> list[dict]:
    """Sheet-goods yield. Area lower-bound (necessary) with a kerf allowance,
    plus an optional per-strip 1-D crosscut check when a rip_plan is given.
    2-D packing is advisory — a passing area check is necessary, not sufficient."""
    out = []
    sh = spec.get("sheet_stock")
    if not sh:
        return out
    kerf = spec.get("kerf", 0.125)
    sw, sl = sh["sheet"]
    count = sh.get("count")
    parts = sh.get("parts", [])
    # required area with a per-part kerf pad (approximate a saw line around each part)
    req_area = 0.0
    for p in parts:
        pad_w = p["w"] + kerf
        pad_d = p["d"] + kerf
        req_area += pad_w * pad_d * p["qty"]
    sheet_area = sw * sl
    min_sheets = math.ceil(req_area / sheet_area - EPS)
    detail = (
        f"parts need ~{_fmt(req_area)} sq in (kerf-padded); "
        f"sheet = {_fmt(sw)}x{_fmt(sl)} = {_fmt(sheet_area)} sq in; "
        f"area lower bound = {min_sheets} sheet(s)"
    )
    ok = True
    if count is not None:
        detail += f"; spec claims {count}"
        if count < min_sheets:
            ok = False
            detail += " << below area lower bound (cannot fit)"
        else:
            detail += " (packing advisory — verify with rip_plan or cut diagram)"
    out.append(
        {
            "check": "sheet_area",
            "name": sh.get("name", "sheet goods"),
            "ok": ok,
            "detail": detail,
            "corrected": None if ok else min_sheets,
        }
    )
    # optional strong check: each declared strip's crosscuts fit its length
    for strip in sh.get("rip_plan", []):
        length = strip.get("length", sl)
        crosscuts = strip["crosscuts"]
        used = sum(crosscuts) + kerf * len(crosscuts)
        ok_s = used <= length + EPS
        out.append(
            {
                "check": "rip_strip",
                "name": strip.get("name", "strip"),
                "ok": ok_s,
                "detail": f"crosscuts {[_fmt(c) for c in crosscuts]} + kerf = "
                f"{_fmt(used)} vs strip length {_fmt(length)}"
                + ("" if ok_s else " << overruns strip"),
                "corrected": None if ok_s else length,
            }
        )
    return out


def report_firmness(spec: dict) -> list[dict]:
    """Not a pass/fail check — surfaces the firm-vs-estimate split (lesson #4)."""
    firm, estimate = [], []
    for p in spec.get("parts", []):
        (estimate if p.get("kind") == "hardware" else firm).append(p.get("name", "?"))
    note = []
    if firm or estimate:
        note.append(
            {
                "check": "firmness",
                "name": "firm vs estimate",
                "ok": True,
                "detail": f"FIRM (from yield math): {', '.join(firm) or '-'} | "
                f"ESTIMATE (round up): {', '.join(estimate) or '-'}",
                "corrected": None,
            }
        )
    return note


def _fmt(x: float) -> str:
    if isinstance(x, (int,)) or (isinstance(x, float) and x.is_integer()):
        return str(int(x))
    return f"{x:g}"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def run(spec: dict) -> list[dict]:
    findings = []
    findings += check_stackups(spec)
    findings += check_captured(spec)
    findings += check_sticks(spec)
    findings += check_sheets(spec)
    findings += report_firmness(spec)
    return findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec", help="path to the design spec (.json, or .yaml with PyYAML)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    path = Path(args.spec)
    if not path.exists():
        print(f"error: spec not found: {path}", file=sys.stderr)
        return 2
    try:
        spec = load_spec(path)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"error: could not parse spec: {e}", file=sys.stderr)
        return 2
    if not isinstance(spec, dict):
        print("error: spec must be a mapping/object", file=sys.stderr)
        return 2

    findings = run(spec)
    failed = [f for f in findings if not f["ok"]]

    if args.format == "json":
        print(
            json.dumps(
                {
                    "spec": spec.get("project", str(path)),
                    "pass": len(failed) == 0,
                    "failed": len(failed),
                    "findings": findings,
                },
                indent=2,
            )
        )
    else:
        proj = spec.get("project", path.name)
        print(f"cut-verifier: {proj}")
        for f in findings:
            mark = "PASS" if f["ok"] else "FAIL"
            print(f"  [{mark}] {f['check']}: {f['name']}")
            print(f"         {f['detail']}")
        print(
            f"\n{'ALL CHECKS PASS' if not failed else str(len(failed)) + ' CHECK(S) FAILED'}"
        )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

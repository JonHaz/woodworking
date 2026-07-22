#!/usr/bin/env python3
"""test_verify_render.py — regression test for the render gate.

Two assertions, no test runner (the repo has none; this mirrors the two existing scripts
and runs as a bare `python3 test_verify_render.py`):

  1. Baseline. Each shipped master's finding set must equal evals/baseline-findings.json.
     The baseline is intentionally non-empty — it records the known gaps. This fails on
     drift in EITHER direction: a NEW finding fails (a regression), and a listed finding
     that stops appearing ALSO fails (fix it, then delete its line from the baseline). No
     one can quietly regress and no one can quietly ignore.

  2. Fail-firing. The seeded-defect fixture must trip every gating check family, proving
     the checks have teeth and a green run means something.

Exit codes:  0 = all assertions pass   1 = a mismatch   2 = usage/setup error
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / ".claude" / "skills" / "guide-renderer"
sys.path.insert(0, str(SKILL / "scripts"))

import verify_render as vr  # noqa: E402

PAIRS = [
    ("projects/2026-stackable-cubby-benches/design/cubby_bench_3ft.spec.json",
     "projects/2026-stackable-cubby-benches/guides/cubby_bench_3ft_master.html"),
    ("projects/2026-stackable-cubby-benches/design/cubby_bench_4ft.spec.json",
     "projects/2026-stackable-cubby-benches/guides/cubby_bench_4ft_master.html"),
    ("projects/2026-freestanding-stove-shelf/design/stove_shelf.spec.json",
     "projects/2026-freestanding-stove-shelf/guides/stove_shelf_master.html"),
]

EXPECTED_FAIL_KINDS = {"R-ENV", "R-NET", "R-SVG", "R-PRINT", "N-FINISHED"}


def _triples(findings: list) -> list:
    return sorted([f["kind"], f["level"], f["where"]] for f in findings)


def check_baseline() -> list:
    problems = []
    baseline = json.loads((SKILL / "evals" / "baseline-findings.json").read_text())["guides"]
    for spec_rel, guide_rel in PAIRS:
        name = guide_rel.split("/")[-1]
        spec = json.loads((ROOT / spec_rel).read_text(encoding="utf-8"))
        src = (ROOT / guide_rel).read_text(encoding="utf-8")
        got = _triples(vr.run(spec, src))
        want = sorted(map(list, baseline.get(name, {}).get("findings", [])))
        if got == want:
            continue
        got_s = {tuple(t) for t in got}
        want_s = {tuple(t) for t in want}
        for extra in sorted(got_s - want_s):
            problems.append(f"{name}: NEW finding not in baseline: {extra}")
        for gone in sorted(want_s - got_s):
            problems.append(f"{name}: baseline finding no longer appears (fixed? remove it): {gone}")
    return problems


def check_fail_firing() -> list:
    spec = json.loads((SKILL / "examples" / "broken.spec.json").read_text(encoding="utf-8"))
    src = (SKILL / "examples" / "broken_master.html").read_text(encoding="utf-8")
    fired = {f["kind"] for f in vr.run(spec, src) if f["level"] == "fail"}
    missing = EXPECTED_FAIL_KINDS - fired
    if missing:
        return [f"broken fixture did not fire expected fail checks: {sorted(missing)}"]
    return []


def main() -> int:
    problems = check_baseline() + check_fail_firing()
    if problems:
        print("verify_render tests FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("verify_render tests OK "
          f"({len(PAIRS)} masters match baseline; fail-firing covers {len(EXPECTED_FAIL_KINDS)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

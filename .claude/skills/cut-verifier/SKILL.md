---
name: cut-verifier
description: Deterministically verify that a woodworking design's numbers close before any cut list or shopping list is trusted. Use whenever a build spec, cut list, or panel layout needs checking — "does this cut list close", "verify my dimensions", "will these parts fit", "check the stack-up", "did I allocate my 2x4s right", "how many sheets do I really need". Recomputes width/depth/height stack-ups, captured-panel widths (a shelf between two 3/4-in sides is 1.5 in narrower), kerf-aware sheet and stick yields, and the firm-vs-estimate split — the checks behind lessons 1-4 of knowledge/methods/lessons-learned.md. build-planner calls this as a gate before presenting anything. Do not use for generating a design (that is build-planner) or for updating the knowledge base after a build (that is shop-close-out).
---

Numbers that do not close are the failure this whole repo exists to prevent — a
36-in shelf specified inside a 36-in bench, a divider mark that makes unequal
openings, a shopping list that ignores the 2x4 offcuts already on the shelf. This
skill turns the hard-won rules in `knowledge/methods/lessons-learned.md` into a
deterministic script so the arithmetic is machine-checked, not model-estimated.

The check is deliberately mechanical: it re-derives the design from a small
structured spec and reports pass or fail with the exact failing number and its
correction. It never "rounds to make it work."

## When to use this skill

- Any time `build-planner` has produced a design and is about to present a cut list,
  shopping sheet, or cut diagram — run this first, as a gate.
- When Jon asks to sanity-check a cut list or panel layout he wrote or is unsure about.
- When a build came out wrong ("my openings are uneven", "the shelf doesn't fit")
  and you need to find which number was off.
- Before adding anything to a shopping list, to confirm on-hand stock was allocated first.

Do not use this skill to *design* a piece (that is `build-planner`) or to log a
finished build into the knowledge base (that is `shop-close-out`).

## How to use this skill

1. **Get the spec into the schema.** The design must be expressed as the JSON spec
   in `references/spec-schema.md`. If `build-planner` produced one, use it; otherwise
   translate the cut list into a spec (list every stack-up, every captured panel, and
   the stock on hand). Missing a stack-up means it goes unchecked — be complete.
2. **Run the script:**
   `python3 scripts/verify_cutlist.py <spec.json> --format text`
   Use `--format json` when another skill or agent consumes the result.
3. **Read the exit code, not just the text.** `0` = every check closes; `1` = at least
   one failed; `2` = the spec could not be parsed. Never present a cut list built on a
   spec that exited `1`.
4. **On failure, report the correction, not just the error.** Each failing finding
   carries the corrected value (e.g. "shelf should be 34.5, spec says 36"). Hand that
   back to `build-planner` to fix the design, then re-run until it exits `0`.
5. **Surface the firm-vs-estimate split** in what you report to Jon: sheet and stick
   counts are firm; screws, glue, and pads are estimates to round up.

## Reference map

| File | When to load |
|---|---|
| `references/spec-schema.md` | Whenever you build or read a spec — the field-by-field contract. |
| `examples/cubby-bench-3ft.json` | A complete, passing reference spec to copy from. |
| `examples/broken-shelf.json` | Shows what failing checks look like (captured + stack-up + yield). |
| `scripts/verify_cutlist.py` | The check itself; run it, do not reimplement its math in prose. |

## Common output template

Report to Jon in this shape:

- **Verdict:** `ALL CHECKS PASS` or `N CHECK(S) FAILED` (mirror the script's exit code).
- **Failures first,** each as: what was checked → the wrong number → the corrected number.
- **Yield summary:** sheets and sticks needed (firm), on-hand stock consumed, new stock to buy.
- **Firm vs estimate** line for the shopping list.
- If it passed: one line confirming which stack-ups and captured panels were verified,
  so the pass is legible rather than a bare "OK".

## Non-negotiable principles

- **Never present numbers the script has not blessed.** If you changed a dimension,
  re-run. A cut list is only as trustworthy as its last `exit 0`.
- **On-hand before new, always.** The stick check consumes on-hand stock first; if a
  shopping list adds new material the check says is unnecessary, that is a finding.
- **Kerf is not optional.** ~1/8 in per cut is in the yield math; a plan that assumes
  zero kerf will short you on the tight rips (the 13.5-in divider strip is the classic).
- **A passing area check is necessary, not sufficient** for sheet goods. If the layout
  is tight, back it with a `rip_plan` or a to-scale cut diagram before buying.

## Gotchas

- **An empty spec passes trivially.** No stack-ups and no captured checks means nothing
  is verified. Completeness of the spec is your responsibility, not the script's.
- **The spec is per-design for geometry but whole-run for stock.** Stack-ups and captured
  checks describe one unit; `stick_stock`/`sheet_stock` describe the full quantity being
  built. Mixing those up produces a spec that passes but describes nothing real.
- **YAML needs PyYAML.** If a `.yaml` spec errors on load, convert it to `.json` — the
  canonical format has no dependencies.

# The render gate (`verify_render.py`)

What `cut-verifier` is to the numbers, this is to the rendering: a mechanical check that a
master matches the spec it was rendered from. It **compares, it never computes** — all
cut-list arithmetic stays in `verify_cutlist.py`, which must exit `0` on the same spec
first. A number a figure needs that is not in the spec is a spec gap, reported as one,
never derived here.

## Finding levels

| Level | Gates? | Meaning |
|---|---|---|
| `fail` | yes (exit 1) | a real defect in the guide |
| `warn` | only under `--strict` | advisory — probably wrong, occasionally a false positive |
| `info` | never | a census note: a gap in the spec schema, not a defect in this guide |

## Checks

**R — structure (no spec needed)**

- `R-ENV` (fail) — the master is a quirks-mode fragment: opens with `<meta charset="utf-8">`,
  carries no doctype/`<html>`/`<head>`/`<body>`, ends with the `.sheet` closing `</div>`.
- `R-NET` (fail/warn) — self-containment. The Google Fonts `@import` is the only sanctioned
  network reference; any other external URL fails. Warns if no `system-ui`/`sans-serif`
  fallback is in the font stacks.
- `R-SVG` (fail) — every `<svg>` scales by `viewBox` alone, with no `width`/`height`
  attribute. (Widths legitimately vary between figures — 520, 480, 420 — so width is not
  checked, only its absence as an attribute.)
- `R-PRINT` (fail) — the print contract is present: `@page`, `print-color-adjust:exact`,
  and modern `break-inside:avoid`. See `print-contract.md`.
- `R-PALETTE` (warn) — the 18 house palette tokens are defined in `:root`.
- `R-SCALE` (info) — which figures declare a machine-readable `data-scale`. The shipped
  masters keep scale in HTML comments, so today this lists every figure. It is the census
  that motivates emitting `data-scale` from the diagram generator.

**N — numbers vs spec**

- `N-FINISHED` (fail) — `finished.{width,depth,height}` each appear on the page.
- `N-KERF` (warn) — the spec's kerf value is stated somewhere (normalized: `⅛` = `1/8` =
  `0.125`).
- `N-STOCK` (warn) — every distinct sheet part `w`/`d` and stick part `length` appears in a
  cut list.

**G — geometry vs spec**

- `G-SCALE` (info) — for each sheet cut diagram, the px/in scale derived from its full-sheet
  outline rect. Deriving a *rendering* scale is allowed; deriving a *dimension* is not.
- `G-RIP` (warn) — every `rip_plan` crosscut is drawn as a rect at the derived scale,
  somewhere across the diagrams. The check is a union across figures, not per-figure,
  because the schema does not record which sheet a strip lands on (see `G-GAP`).
- `G-GAP` (info) — the census of what the gate *cannot* check because the spec lacks the
  field: rip widths, part references on crosscuts, sheet indices, part ids. Each `G-GAP` is
  a requirement for the additive schema extension, not a defect.

## Baseline discipline

`evals/baseline-findings.json` records the expected finding set for the three shipped
masters. It is **non-empty on purpose** — the honest day-one state has open `info` gaps.

`test_verify_render.py` fails on drift in **either** direction: a new finding is a
regression; a baseline finding that stops appearing means it was fixed, and its line must
be removed from the baseline in the same change. Nobody can quietly regress and nobody can
quietly ignore. The file is expected to shrink as the schema extension and the generator
close the `info` gaps.

Run the test with `python3 scripts/test_verify_render.py` (exit 0/1) — no pytest, matching
the repo's script idiom.

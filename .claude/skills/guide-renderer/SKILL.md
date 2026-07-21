---
name: guide-renderer
description: Render and check the house-style, print-ready HTML/SVG master build document for a woodworking project from a design spec cut-verifier has already passed. Use when a verified design needs its guide produced, when an existing master needs checking against its spec, or when a guide's print behaviour, figure scales, or house styling are in question — "render the build guide", "make the print-ready master", "does this guide match the spec", "why does this print badly", "check the cut diagram against the rip plan". Produces ONE self-contained master per size/variant containing the shopping list, cut lists with to-scale cut diagrams, the build-and-assembly sequence, and safety callouts. It renders numbers, it never invents or re-derives them. Do not use for designing a piece (that is build-planner), for cut-list arithmetic (that is cut-verifier), or for coaching a build at the bench (that is build-companion).
---

A master build document is the artifact Jon carries into the shop and cuts from. It is
the only place the design becomes physical, so two things have to hold at once: every
number on the page must trace back to a spec `cut-verifier` blessed, and the page must
survive contact with a printer.

The rendering itself is judgement — which figures a build needs, at what scale, in what
order. That stays with the model. What does *not* stay with the model is checking the
result: whether the cut diagram matches the `rip_plan`, whether the shopping counts match
`sheet_stock`, whether the file is still self-contained. Those are mechanical, and
`scripts/verify_render.py` does them so a rendered guide is verified rather than assumed.

## When to use this skill

- `build-planner` has a spec that exited `0` on `cut-verifier` and the guides are next.
- An existing master needs re-checking after a spec change, a correction, or a rev bump.
- A guide prints badly — pages breaking mid-figure, a section splitting from its heading.
- You are about to hand-edit a shipped master and want the check to catch a regression.

Do not use this skill to design a piece (`build-planner`), to do cut-list arithmetic
(`cut-verifier`), or to coach the physical build (`build-companion`).

## How to use this skill

1. **Confirm the spec passed first.** Run
   `python3 .claude/skills/cut-verifier/scripts/verify_cutlist.py <spec.json>` and require
   `exit 0`. A guide built on an unverified spec is exactly the failure this repo exists
   to prevent. The spec lives in the project's `design/` folder.
2. **Render the master** into `projects/<year>-<name>/guides/` following
   `references/house-visual-system.md` and `references/print-contract.md`. One
   self-contained file per size/variant — never a scattered set.
3. **Check the render:**
   `python3 scripts/verify_render.py --spec <spec.json> --guide <master.html> --format text`
   Use `--format json` when another skill or agent consumes the result.
   *(Not yet built — see "Status" below. Until it lands, check by hand against
   `references/print-contract.md` and the spec's `rip_plan`/`sheet_stock`/`stick_stock`.)*
4. **Read the exit code, not just the text.** `0` = every check passes; `1` = at least one
   failed; `2` = a file could not be parsed. Do not hand a master back on a `1`.
5. **Report what you assumed.** List the files written, the scale used per figure, and any
   place the spec was silent and you made a documentation-only assumption — never a
   dimension. Return control to `build-planner`.

## Reference map

| File | When to load |
|---|---|
| `references/print-contract.md` | Whenever you write or fix a `@media print` block — the rules and why each exists. |
| `.claude/skills/cut-verifier/references/spec-schema.md` | The field-by-field contract for the spec you are rendering from. |
| `projects/2026-stackable-cubby-benches/guides/` | The reference masters. Read one before rendering a new one — this is the visual system until it is extracted. |
| `scripts/verify_render.py` | The render gate. **Not yet built** — see Status. |

## Status

This skill is being built in stages. What exists today: the procedure above, the print
contract, and the trigger evals. Still to come, in order — a canonical style block
extracted from the three shipped masters, then `scripts/verify_render.py` as the render
gate, then machine-readable per-figure scale declarations derived by that gate rather than
hand-guessed. Until the gate exists, steps 3–4 are a manual check.

## Common output template

Report to Jon in this shape:

- **Files written** — full paths, one per size/variant.
- **Verdict** — mirror `verify_render.py`'s exit code, failures first.
- **Figure scales** — each figure and the px-per-inch it was drawn at.
- **Assumptions** — anything documentation-only the spec did not cover. If you found
  yourself wanting to assume a *dimension*, that is a stop-and-report, not an assumption.

## Non-negotiable principles

- **Render, never re-derive.** If a number looks wrong, stop and report it to
  `build-planner`. Silently "correcting" a dimension is the worst failure mode available
  to this capability, because the result looks authoritative and prints cleanly.
- **One master per size/variant.** Lesson 13 exists because the cubby set first shipped as
  seven files with the same cut list in five of them.
- **Self-contained.** Inline all CSS and all SVG. The Google-Fonts `@import` is the single
  sanctioned network reference and must ship with a `system-ui` fallback so the file
  prints without a network.
- **Every figure states its scale**, and every part in a cut figure carries its dimensions
  as text. A builder reads numbers off the page; they must never need to measure it.

## Gotchas

- **Figure scales are per-figure and that is correct.** A 96-inch sheet and a 1/8-inch
  roundover cannot share a scale on a 520-unit canvas. The invariant is that each figure
  *declares* its own scale and is internally consistent — not that all figures agree.
  Any "1 in = 4 px" house constant is fiction; the shipped masters use ten different scales.
- **SVG `fill` and CSS `background` print differently.** Part fills inside a diagram are
  SVG presentation attributes and print by default; legend swatches use CSS `background`
  and vanish without `print-color-adjust`. See `references/print-contract.md`.
- **The masters are quirks-mode fragments** — no doctype, no `<html>`, `<head>` or `<body>`.
  That is deliberate. It also means `xml.etree` cannot parse them; use `html.parser`.
- **The verifier compares, it never computes.** All cut-list math belongs to
  `verify_cutlist.py`. If you find yourself wanting the render gate to do arithmetic, the
  number belongs in the spec instead.

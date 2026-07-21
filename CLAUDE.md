# Instructions for Claude

This repo is Jon's DIY woodworking build system. Follow these rules in every
session that touches it.

## Skills and agents (the build pipeline)

Work flows through focused capabilities, not one monolith. Route to the
right one for the stage:

| Stage | Capability | Kind | Use when |
|---|---|---|---|
| FOUNDATION | `shop-inventory` | skill + script | Confirm what tools and materials Jon actually owns; resolve `inferred` entries. |
| PLAN | `project-intake` | skill | A vague idea needs scoping into a feasible brief. |
| DESIGN | `build-planner` | skill (orchestrator) | Turn a scoped build into a dimensioned design. |
| DESIGN | `cut-verifier` | agent + script | Confirm the numbers close before anything is presented. |
| BUILD | `guide-renderer` | agent | Render the house-style print-ready HTML/SVG guides. |
| BUILD | `build-companion` | skill | Coach the build at the bench; recover from off-spec cuts. |
| LOOP | `shop-close-out` | skill | Feed a finished build back into the knowledge base. |

Pipeline order: **project-intake → build-planner → cut-verifier (gate) →
guide-renderer → build-companion → shop-close-out**, all resting on the
`shop-inventory` foundation. `build-planner` is the orchestrator: it emits
a structured design spec (schema:
`.claude/skills/cut-verifier/references/spec-schema.md`), gates it through
`cut-verifier` (never present a cut list the verifier has not passed), then
delegates guides to `guide-renderer`. `build-companion` then coaches the physical
build, delegating any off-spec recovery math back to `cut-verifier`. The
verifier's script is the source of truth for cut-list math — do not hand-estimate
stack-ups or yields. `shop-inventory` keeps `tools.md`/`materials-on-hand.md`
honest so the "confirmed tools only" rule below has teeth.

## Before generating ANY build plan, cut list, or design

Read, in order:

1. `knowledge/shop/tools.md` — design only around tools marked `confirmed`.
   If a better approach needs an unowned tool, offer it as a clearly labeled
   alternative, never as the default plan. If the entries you need are still
   `inferred` (unverified), run `shop-inventory` to confirm them with Jon first.
2. `knowledge/shop/materials-on-hand.md` — allocate on-hand stock **before**
   adding anything to a shopping list. State which on-hand pieces the plan
   consumes.
3. `knowledge/methods/lessons-learned.md` — apply every relevant lesson
   (kerf allowances, captured-panel math, spacer-block layout, top fastening,
   etc.). These exist because they were once gotten wrong.

## Design conventions

- Dimensions in inches; sheet goods assumed 4×8 unless noted; allow ~1/8 in
  saw kerf per cut in all yield math.
- Verify every cut list closes on the finished dimensions before presenting it
  — run `cut-verifier` (`.claude/skills/cut-verifier/scripts/verify_cutlist.py`)
  on the design spec. An `exit 0` is required, not optional.
- Deliverables: dimensioned markdown spec in `design/`, plus print-ready,
  self-contained HTML guides in `guides/` (build sequence, cut diagrams to
  scale, shopping sheet with check-off boxes, assembly guide). Match the
  visual style of `projects/2026-stackable-cubby-benches/guides/`.
- Firm numbers (sheet/stick counts from yield math) vs. estimates (screws,
  glue, pads) must be labeled as such.
- Safety callouts are required where relevant: two-person lifts, mechanical
  top fastening, stacking limits, strap-to-wall guidance.

## After a project milestone or close-out

Run the `shop-close-out` skill, which performs this ritual:

1. Update `knowledge/shop/materials-on-hand.md` (consume used stock, add
   leftovers with measured sizes).
2. Append new lessons to `knowledge/methods/lessons-learned.md`.
3. Add or update the project concept doc in `knowledge/projects/`.
4. Record the change in `knowledge/log.md` (newest date first, ISO dates).
5. If a new tool was acquired, add it to `knowledge/shop/tools.md` as
   `confirmed`.

## Knowledge format (OKF v0.1)

`knowledge/` is an Open Knowledge Format bundle
(spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf).

- Every concept `.md` needs YAML frontmatter with at least a `type` field;
  include `title`, `description`, `tags`, and `timestamp` when possible.
- `index.md` files are directory listings (no frontmatter, except the bundle
  root which declares `okf_version`). Keep them current when adding concepts.
- `log.md` is the chronological history: `## YYYY-MM-DD` headings, newest
  first, `**Update**` / `**Creation**` style entries.
- Use bundle-relative links (starting with `/`) between concepts.

## Tone and safety

Treat structural and safety claims conservatively. If a request would produce
something unsafe to sit on, stack, or lift, say so and fix the design rather
than silently complying.

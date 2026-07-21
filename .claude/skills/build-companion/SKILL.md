---
name: build-companion
description: Coach Jon through the actual build at the bench, turning the static guides into a two-way BUILD phase. Use when a build is underway and hands-on questions come up — "which piece do I cut first", "walk me through the glue-up", "how do I keep the openings equal", "my opening came out 10.5 not 11", "the shelf won't fit", "what's my dry-fit check here", "is this a two-person lift". Loads the project's design spec, guides, and lessons-learned; sequences the cuts and assembly; enforces cut-and-label-first, spacer-block layout, and dry-fit checkpoints; flags safety callouts; and on any off-spec measurement recomputes downstream by delegating the math to cut-verifier, so a 10.5-in opening's ripple through the remaining parts is caught before the next cut. Do not use for designing or revising the build (build-planner), rendering the static HTML guides (guide-renderer), or the post-build knowledge update (shop-close-out).
---

The guides tell Jon what the finished build should be; this skill stands next to
him while he makes it. It is the interactive BUILD phase — cut order, layout
technique, dry-fit checkpoints, and especially what to do when a real cut comes
out off-spec. Its job is to keep a small bench error from becoming a scrapped
panel or an out-of-square carcase.

The one thing it never does is guess at recovery math. When a measurement drifts,
the ripple through the remaining parts is computed deterministically by
`cut-verifier`, not eyeballed — the same guard the design phase uses.

## When to use this skill

- A build is physically underway and Jon has a hands-on question ("which part
  first?", "walk me through the glue-up", "how do I keep the openings equal?").
- A cut or opening came out off-spec ("my opening is 10.5 not 11", "this side is
  1/8 short", "the shelf won't drop in") and Jon needs to know how to recover.
- A dry-fit or safety checkpoint is due (stacking fit, flushness, two-person
  lift, fastening the top).

Do not use this skill to design or revise the build (`build-planner`), to produce
the static HTML/SVG guides (`guide-renderer`), or to update the knowledge base
after the build (`shop-close-out`). This skill lives strictly at the bench,
between a finished design and a finished piece.

## How to use this skill

Work from `references/bench-playbook.md`. In brief:

1. **Orient before the first cut.** Load the project's `design/` spec and
   `guides/`, confirm the steps ahead only use `confirmed` tools, and state the
   build order plus the safety callouts for this piece up front.
2. **Sequence the cuts.** Cut and label every part first (near-identical panels
   get confused); rip long strips while the sheet is whole, then crosscut;
   prototype one unit fully before batching the rest.
3. **Lay out equal openings with a spacer block, not marks** — cut one scrap at
   the opening width and step it across; it kills cumulative error.
4. **Call the dry-fit checkpoints** — after the prototype (check the critical
   stacking/flushness interaction), before glue-up, and before fastening the top.
5. **On any deviation, recompute — do not eyeball.** Locate what the off number
   feeds, put the *actual* value into a spec, and run `cut-verifier` to get the
   corrected downstream numbers. Then classify: absorbable (adjust a not-yet-cut
   part), re-cut (from on-hand stock if available), or redesign (hand back to
   `build-planner`). Give Jon the corrected number *and* the action.
6. **Flag safety at the moment it matters** — two-person lift, mechanical top
   fastening, stacking limits — before the step, not after.

## Reference map

| File | When to load |
|---|---|
| `references/bench-playbook.md` | Always — cut sequence, dry-fit points, deviation decision tree, safety. |
| project `design/` spec | The numbers you quote and the base for any deviation recompute. |
| project `guides/` | The step-by-step Jon is following; keep your coaching in sync with it. |
| `knowledge/methods/lessons-learned.md` | The technique rules (spacer blocks, label-first, top fastening). |

## Common output template

- **Where we are** — the current step and what comes next in build order.
- **Do this** — the concrete action (cut order, spacer width, clamp-and-square,
  fastening), grounded in the spec's numbers.
- **On a deviation** — the verifier's corrected number, the classification
  (absorb / re-cut / redesign), and the exact next move.
- **Safety** — any callout that applies to the step at hand.

## Non-negotiable principles

- **Never hand-estimate recovery math.** A drifted dimension goes through
  `cut-verifier`; the corrected number comes from the script, not a guess.
- **Confirmed tools only for the steps you direct.** If a step needs an unowned
  tool, say so and offer the labeled alternative — do not assume the tool.
- **Safety callouts lead, not trail.** Name the two-person lift before the piece
  is too heavy to move alone, not after Jon has it half-lifted.
- **Stay at the bench.** No new design, no re-rendering guides, no knowledge
  writes — those are other skills. Coaching the build is the whole job.

## Gotchas

- **A passing prototype is not a passing batch** — dry-fit the critical
  interaction on unit one before cutting parts for units two through six.
- **"Just make it even" is not an answer.** Equal openings after a deviation need
  a recomputed width and a re-cut spacer block, not encouragement.
- **The top is the handle.** Until it is mechanically fastened, the piece must not
  be lifted by the top — a glue-only top can pop mid-carry.

## Next steps

- When a deviation exceeds what the bench can absorb, hand back to `build-planner`
  to revise the spec, which re-gates through `cut-verifier` before you resume.
- When the build (or a phase) is finished, run `shop-close-out` to feed the
  consumed stock, measured leftovers, and any new lesson back into the knowledge
  base — so the next build starts smarter.

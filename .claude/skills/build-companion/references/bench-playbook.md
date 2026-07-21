# Bench playbook

The at-the-bench sequence and the deviation-response logic for coaching a build
in progress. Ground every answer in the project's own design spec and guides
plus `knowledge/methods/lessons-learned.md` — this playbook is the technique
layer, the spec is the numbers.

## Before the first cut — orient

1. **Load the design.** Open the project's `design/` spec (the JSON the verifier
   passed) and the `guides/` HTML. The spec's stack-ups and captured checks are
   the source of truth for every number you quote at the bench.
2. **Confirm the tools for the steps ahead.** Cross-check the cuts against
   `knowledge/shop/tools.md`; any step that needs a tool not `confirmed` gets
   flagged now, not mid-cut. (If the tool picture is stale, that is a
   `shop-inventory` job.)
3. **State the plan of attack** in build order, and the safety callouts that
   apply to this piece up front (see the safety section).

## Cut sequence

- **Cut and label everything first** (lesson 6). A 3-ft cubby bench has twelve
  plywood parts and several near-identical panels; unlabeled parts get confused
  fast. Write the part name on painter's tape as each piece comes off the saw.
- **Prototype one, then batch** (lesson 7). Build the first unit completely,
  dry-fit the critical interaction, and only then cut parts for the rest.
- **Rip long, crosscut short.** Full-length rips (the 17-in and 13.5-in strips)
  come first while the sheet is whole; crosscut those strips to length after.
- **Kerf is real** (lesson 3). Remind Jon that ~1/8 in disappears per cut — a
  48-in sheet does not yield three clean 16-in rips.

## Equal openings — spacer blocks, not marks

For any run of equal openings (cubby dividers), use the spacer-block method
(lesson 5): cut one scrap block at the exact opening width and step it across to
position each divider. This eliminates cumulative tape-measure error and the
awkward fractions (11-1/16) that creep in from marking. Cut the spacer from
scrap, verify it once against the spec's opening width, then trust it.

## Dry-fit checkpoints

Dry-fit (clamp, no glue) at these moments before committing:

- **After the prototype unit** — check the critical interaction the design
  depends on: stacking nesting (lesson 10), side-by-side flushness, that a
  captured shelf actually drops between its sides.
- **Before glue-up** — every joint held with clamps, panel labels visible,
  openings checked with the spacer block.
- **Before fastening the top** — confirm the top sits flush and overhang (if any)
  is even, because the top gets mechanically fastened and is hard to move after.

## Glue-up and fastening

- Square the assembly under clamps before any screw goes in; measure the two
  diagonals — equal diagonals mean square.
- **Mechanically fasten the seat/bench top from inside** (lesson 8) — screws, not
  brads or glue alone. The top is the lifting handle; a top attached by glue
  alone can pop mid-carry and drop the piece.
- Countersink and drive; fill and sand exposed plywood edges (no edge banding,
  house preference).

## Deviation response — the core of this skill

When a real cut or opening comes out off-spec, do not eyeball whether it still
works. Walk this decision tree:

1. **Locate what the off number feeds.** Is it a *captured* dimension (a shelf
   between two sides), one segment of a *stack-up* that must hit a finished
   dimension, or one opening in a run that must sum to a fixed width?
2. **Recompute downstream deterministically — hand it to `cut-verifier`.**
   Build a small spec (or edit the project spec) with the *actual* measured value
   in place of the planned one, and run:
   `python3 ../cut-verifier/scripts/verify_cutlist.py <adjusted-spec.json>`
   Let the script tell you whether the stack-up still closes and what the
   corrected number is. Never hand-estimate the ripple — that is the mistake the
   verifier exists to prevent.
3. **Classify and advise:**
   - **Absorbable** — the error can be taken up in a not-yet-cut part. Example:
     an opening came out 10.5 instead of 11, so the remaining openings must be
     re-divided; the verifier gives the new per-opening width. Adjust the spacer
     block and continue.
   - **Re-cut** — the off part is a captured or visible finished dimension that
     nothing downstream can absorb (an 11-in-too-narrow side). Re-cut from stock;
     check `materials-on-hand.md` has the stock, or it becomes a shopping item.
   - **Redesign** — the deviation breaks a finished dimension or a stacking
     interaction that cannot be recovered at the bench. Stop and hand back to
     `build-planner` to revise the spec, then re-verify.
4. **Give the corrected number, then the action.** "Your last two openings now
   split 23 in → 11.5 in each; re-cut the spacer to 11.5 and step from the left
   side" beats "just make them even."

### Worked example — "my opening came out 10.5 not 11"

A 36-in bench, 3 openings of 11 with four 3/4-in walls (0.75×4 + 11×3 = 36). The
first opening landed at 10.5. The 0.5 in has to go somewhere: the remaining
width for the last two openings is 36 − 0.75×4 − 10.5 = 22.5 in, so each becomes
11.25 in (not 11). Feed the actual 10.5 into the width stack-up and let
`cut-verifier` confirm 0.75, 10.5, 0.75, 11.25, 0.75, 11.25, 0.75 = 36 closes,
then re-cut the spacer block to 11.25 for the remaining dividers.

## Safety callouts — say them before the step, not after

- **Two-person lift** for a finished 3-ft plywood bench (~45–50 lb, lesson 11).
  Flag it before the piece is complete so a second person is on hand.
- **Stacking limits** (lessons 10–11): max 3 high unstrapped, like-size on
  like-size; wider on the bottom and strapped if mixed. Never the 6-high stack.
- **Top is the handle** (lesson 8): if the top is not yet mechanically fastened,
  do not lift the piece by it.

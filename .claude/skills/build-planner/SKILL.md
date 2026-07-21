---
name: build-planner
description: Design DIY woodworking builds grounded in Jon's real shop, then orchestrate verification and print-ready output. Use whenever Jon wants to design, plan, revise, or spec a physical build — "design a bench", "plan garage shelves", "make it 4 ft wide", "give me a cut list", "redo this for plywood not MDF", "spec a bookshelf for this wall". Loads confirmed tools, on-hand materials, and past lessons; emits a structured design spec; gates it through cut-verifier before presenting anything; and hands the passing spec to guide-renderer for house-style guides. Pairs with project-intake (scoping a vague idea first) and shop-close-out (updating the knowledge base after). Do not use for a bare number or fit check on an existing cut list (that is cut-verifier), or for logging a finished build (that is shop-close-out).
---

Plan builds from the shop's real constraints, not generic assumptions. This skill is
the **design orchestrator**: it decides the design, but delegates the two things that
must not be model-estimated — the arithmetic (to `cut-verifier`) and the print-ready
guides (to `guide-renderer`). Its own job is the design judgment and the hand-offs.

## When to use this skill

- Jon wants a new piece designed, or an existing design revised ("make it 4 ft wide",
  "add a drawer", "redo this for plywood not MDF").
- A `project-intake` brief has been produced and it is time to turn the scope into a
  real, dimensioned design.
- Any request that ends in a cut list, cut diagram, shopping sheet, or assembly guide.

Do not use this skill for a bare "does this cut list close?" check on numbers Jon
already has — that is `cut-verifier` directly. Do not use it to update the knowledge
base after a build — that is `shop-close-out`.

## How to use this skill

1. **Load shop context (required, in order):**
   - `knowledge/shop/tools.md` — design only around `confirmed` tools; treat `inferred`
     as likely-but-verify; offer `wanted`-tool approaches only as labeled alternatives.
   - `knowledge/shop/materials-on-hand.md` — allocate on-hand stock **before** adding
     purchases; state exactly which pieces the plan consumes.
   - `knowledge/methods/lessons-learned.md` — apply every relevant lesson.
2. **Clarify only what changes the design** — target dimensions, load/use, finish,
   quantity. Skip anything the knowledge base or a `project-intake` brief already answers.
3. **Design, then emit a structured spec.** Produce the design and express it as the
   JSON spec defined in `references/spec-schema.md`: every W/D/H stack-up, every
   captured panel, and the actual stock on hand. Save it in the project's `design/` folder.
4. **Gate on `cut-verifier` — do not present anything until it passes.** Spawn the
   `cut-verifier` agent (or run its script) on the spec. If it exits `1`, fix the design
   using the corrected numbers it returns and re-run. Only an `exit 0` spec earns a cut list.
5. **Delegate the guides to `guide-renderer`.** Hand the passing spec to the
   `guide-renderer` agent, which produces **one self-contained HTML master build
   document per size/variant** (shopping list, to-scale cut diagrams, the build +
   assembly sequence, and safety — all in one file).
6. **Write the dimensioned markdown spec** to `projects/<year>-<name>/design/` and the
   guides to `projects/<year>-<name>/guides/`. Separate firm counts from estimates and
   flag safety callouts (two-person lifts, mechanical top fastening, stacking limits).
7. **Point to the next step.** After a build milestone, `shop-close-out` updates the
   knowledge base so the design compounds.

## Reference map

| File | When to load |
|---|---|
| `knowledge/shop/tools.md` | Every design — the confirmed-tool constraint. |
| `knowledge/shop/materials-on-hand.md` | Every design — allocate on-hand first. |
| `knowledge/methods/lessons-learned.md` | Every design — apply the relevant lessons. |
| `references/spec-schema.md` | When emitting the spec to verify (mirrors cut-verifier's contract). |
| `projects/2026-stackable-cubby-benches/guides/` | The house style `guide-renderer` matches (the per-size masters). |

## Common output template

- A dimensioned markdown spec in `design/` with a finished-dimensions table and cut lists.
- A **verifier verdict line** ("cut-verifier: ALL CHECKS PASS — width, height, base-depth
  stack-ups and 3 captured panels closed") so the numbers are visibly blessed.
- The house-style HTML master(s) in `guides/` — one per size/variant — produced by `guide-renderer`.
- A shopping summary splitting firm counts (sheets, sticks) from estimates (screws, glue, pads),
  naming which on-hand stock the plan consumes.

## House constraints

- No edge banding — fill and sand plywood edges (owner preference); banding only as a
  labeled alternative for a natural, unpainted finish.
- Benches/seating: mechanically fasten tops from inside; flag two-person lifts;
  stacking max 3 high unless strapped.
- Prefer designs buildable with a circular/table saw + drill; call out any step that
  assumes a tool not marked `confirmed`.
- Dimensions in inches; sheet goods 4×8 unless noted; ~1/8 in kerf per cut in yield math.

## Next steps

- **Before designing**, if the request is a vague idea rather than a scoped build, run
  `project-intake` first to produce a brief and check feasibility. If the tools the
  design leans on are still `inferred`, run `shop-inventory` to confirm them.
- **Before presenting**, always gate on `cut-verifier`.
- **At the bench**, once the guides are rendered and Jon starts building, `build-companion`
  coaches the physical build and handles off-spec cuts (it delegates recovery math back
  to `cut-verifier`).
- **After a build milestone**, run `shop-close-out` to update materials, lessons, the
  project concept doc, and the log.

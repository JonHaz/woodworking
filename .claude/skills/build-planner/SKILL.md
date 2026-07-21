---
name: build-planner
description: Generate DIY woodworking build plans, cut lists, and shop documents grounded in Jon's actual tools, on-hand materials, and past lessons. Use whenever the request involves designing, planning, revising, or documenting a physical build (benches, shelves, storage, furniture, shop fixtures) — including cut lists, shopping lists, cut diagrams, or assembly guides.
---

# Build Planner

Plan builds from the shop's real constraints, not generic assumptions.

## Workflow

1. **Load shop context (required, in order):**
   - `knowledge/shop/tools.md` — design only around `confirmed` tools;
     `inferred` = verify with the user; `wanted`-tool approaches only as
     labeled alternatives.
   - `knowledge/shop/materials-on-hand.md` — allocate on-hand stock before
     adding purchases; state exactly which pieces the plan consumes.
   - `knowledge/methods/lessons-learned.md` — apply every relevant lesson.
2. **Clarify only what changes the design** (target dimensions, load/use,
   finish, quantity). Skip questions the knowledge base already answers.
3. **Design + verify.** Close every stack-up (W/D/H) against finished
   dimensions; account for material thickness on captured panels; allow
   ~1/8 in kerf in yield math; separate firm counts from estimates.
4. **Produce documents** in the house style (see
   `projects/2026-stackable-cubby-benches/guides/` for reference):
   - Dimensioned markdown spec → `projects/<year>-<name>/design/`
   - Print-ready self-contained HTML → `projects/<year>-<name>/guides/`:
     build guide, to-scale cut diagrams, check-off shopping sheet, assembly
     guide. Include safety callouts (lifting, fastening, stacking).
5. **Close the loop.** After milestones: update materials inventory, append
   lessons, update/create the `knowledge/projects/` concept doc, and add a
   `knowledge/log.md` entry (OKF v0.1 conventions — frontmatter with `type`,
   ISO-dated log, bundle-relative links).

## House constraints

- No edge banding — fill and sand plywood edges (owner preference).
- Benches/seating: mechanically fasten tops from inside; flag two-person
  lifts; stacking max 3 high unless strapped.
- Prefer designs buildable with a circular/table saw + drill; call out any
  step that assumes more.

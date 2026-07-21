# Knowledge Bundle Update Log

## 2026-07-21
* **Update**: Stove shelf design → **Rev 2** — re-pointed the anti-tip magnet
  tether to the range's **magnetic black rear backguard** (confirmed magnetic
  from the range side-profile photo), replacing the earlier "steel side panel"
  target. The legs' front faces sit against the backguard (leg depth 3.5 = rear
  gap 3.5), so magnets recess into the leg fronts and pull directly to it —
  promoted from optional to the reliable primary anti-tip measure. Updated the
  design spec, HTML master, and concept-doc stability note. No wood dimensions
  changed; cut list re-verified `exit 0`.
* **Creation**: Added [Freestanding rear stove shelf (2026)](/projects/freestanding-stove-shelf.md)
  — a liftable red-oak shelf on two legs bridging the gap behind a 30-in range;
  concealed 3/8-in dowels, no visible screws, hidden floating-top reveal, raised
  rear fence. Design complete and **cut-verified** (`exit 0`: 5 stack-ups,
  rear-stretcher captured check, 2-board 1×4 yield). Scaffolded
  `projects/2026-freestanding-stove-shelf/` with a Rev 1 design spec, the verifier
  JSON, and one self-contained `stove_shelf_master.html`. Corrected the brief's
  leg height (12.25 → 11.125 in with the floating riser) so the height stack-up
  closes; nested the fence + stretcher from a shared rip to hold the build at 2
  boards. No on-hand stock consumed (red oak is a purchase).
* **Creation**: Added [Red oak stock (Lowe's)](/shop/red-oak-stock.md) — the
  purchasable red oak S4S sizes and lengths (from owner photos) with
  nominal-to-actual conversions, as a sourcing reference for future builds.
* **Update**: Appended lessons **14–17** to
  [lessons learned](/methods/lessons-learned.md) — edge-glued solid tops
  (dowels are alignment, not strength), overall-vs-part height, sharing one
  ripped blank to save a board, and forward-tip disclosure for tall
  shallow-footprint pieces.
* **Update**: Consolidated the cubby-bench guide set into **one self-contained
  master build doc per size** — `cubby_bench_3ft_master.html` and
  `cubby_bench_4ft_master.html` — replacing the seven scattered guides (both-sizes
  master plan; 3-ft build/assembly/plywood-diagram/2×4-diagram/shopping-sheet; 4-ft
  build guide). Generated the previously-missing 4-ft cut diagrams, shopping list,
  and assembly steps, all cut-verified (`exit 0`: 8 rails @45 + 16 rungs @11 from 6
  new sticks; 4 sheets). Codified the format as the standing deliverable contract in
  `.claude/agents/guide-renderer.md` (+ `CLAUDE.md`, `build-planner`): future plans
  emit one `<name>_master.html` per size, not a file set.
* **Update**: Reconciled documentation drift across the 2026 cubby-bench guide
  set (see [project concept](/projects/cubby-benches-2026.md)). Made
  *fill-and-sand* the finish method everywhere — removed edge banding from the
  design spec (now Rev 3), the master build plan, and both build guides — to match
  the standing no-banding preference. Corrected Phase-1 2×4 sourcing to **3 new
  sticks + 8 on-hand 54-1/8 offcuts** (was "7 new") in the design spec, master
  plan, and 3-ft build guide, so on-hand stock is consumed first. Fixed the 3-ft
  build guide's Step-5 divider mark (24 in → **22.75 in** / 11-in spacer) so the
  three cubbies come out equal. Corrected the "2 spare rungs" wording to zero
  spare in the 2×4 cut diagram and cut/shopping sheet. Corrected the plywood
  cut-diagram illustration in the 3-ft build guide (Fig. 3) and the cut/shopping
  sheet to draw 5 dividers per 13.5-in strip (was 4), matching the authoritative
  plywood cut diagram (5 + 5 + 2 = 12).
* **Initialization**: Created the OKF v0.1 bundle structure (shop / methods / projects).
* **Creation**: Added [Shop tools](/shop/tools.md) inventory, seeded as inferred from cubby-bench build sessions — pending owner confirmation.
* **Creation**: Added [Materials on hand](/shop/materials-on-hand.md) with measured 2×4/2×2 offcut stock and Phase 1 allocations.
* **Creation**: Added [Build-planning lessons learned](/methods/lessons-learned.md) (12 lessons from the cubby-bench design review).
* **Creation**: Added [Stackable modular cubby benches (2026)](/projects/cubby-benches-2026.md) project concept — Phase 1 in progress.

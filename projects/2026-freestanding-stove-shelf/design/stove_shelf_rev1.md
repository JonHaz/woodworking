# Freestanding Rear Stove Shelf — Revision 1

**cut-verifier: ALL CHECKS PASS** — `verify_cutlist.py stove_shelf.spec.json` → `exit 0`
(5 stack-ups close, rear-stretcher captured check closes, parts pack into 2 red oak
1×4×6 boards; 120.25 lin in, 2 new sticks).

A premium, liftable red-oak shelf that bridges the gap behind a 30" electric range. Rests
on two legs, **no wall/counter fasteners, no visible screws** — concealed 3/8" dowels, glue
only. Redesigned from the Etsy reference to be stronger and more furniture-like: a two-board
edge-glued top, legs inset from the front with a hidden floating reveal, a concealed rear
stretcher, and a raised rear fence.

## Design decisions (resolve the brief)

1. **Leg height corrected 12.25 → 11.125 in.** The brief's 12.25" is the *overall* height,
   not the leg. With the top resting on the legs, `overall = leg + riser + top`, so a 12.25"
   leg would give 13.0" overall and 1.0" clearance (target is 0.25"). See stack-up below.
2. **Tooling: full confirmed shop** (table saw / track saw + router) — `knowledge/shop/tools.md`
   marks these `confirmed`, overriding the brief's "no table saw" line. Enables the exact
   6.75" top rip, clean stretcher/fence rips, and a routed reveal + roundover.
3. **Top depth 6.75 in:** two 1×4 (3.5") edge-glued → 7.0", ripped to 6.75".
4. **Floating top:** a hidden 3/8"-tall setback riser between each leg and the shelf gives a
   real shadow reveal (stretch goal). Underside chamfer is the no-risk fallback.
5. **Raised rear fence** (per the reference photo) kept, and nested onto 2 boards via a shared rip.

## Finished dimensions

| Dimension | Size |
|---|---:|
| Overall width | 31 in |
| Overall depth | 6.75 in |
| Overall height | 12.25 in |
| Clear opening under shelf | 11.5 in |
| Clearance over cooktop grates | ~0.25 in |
| Side overhang (each side of 30 in range) | ~0.5 in |
| Leg inset from shelf front | 0.75 in |
| Floating reveal (shadow gap) | 0.375 in |

Stack-up checks (all verified `exit 0`):
- Height: `11.125 leg + 0.375 riser + 0.75 top = 12.25 in` ✓
- Opening: `11.125 leg + 0.375 riser = 11.5 in` ✓
- Clearance: `11.25 grate height + 0.25 gap = 11.5 in opening` ✓
- Width: `0.5 + 30 + 0.5 = 31 in` ✓
- Top glue-up (pre-rip): `3.5 + 3.5 = 7.0 in` → ripped to 6.75 in ✓

## Cut list

All parts from red oak 1×4 S4S (actual 0.75 × 3.5 in). Grain runs along the length.

| Part | Qty | Size (L × W × T, in) | Notes |
|---|---:|---|---|
| Top board | 2 | 31 × 3.5 × 0.75 | Edge-glue the pair → 7.0", then **rip to 6.75"** wide |
| Leg | 2 | 11.125 × 3.5 × 0.75 | Full board width = 3.5" leg depth |
| Rear stretcher | 1 | 29.5 × 1.5 × 0.75 | Captured between legs (`31 − 2×0.75`) |
| Back fence | 1 | 31 × 1.5 × 0.75 | On shelf back edge, full width |
| Floating riser | 2 | 2.5 × 0.75 × 0.375 | Hidden spacer; from offcut |

The **rear stretcher and back fence are ripped from one shared 31" blank** (two 1.5"-wide
strips out of a single 3.5"-wide length), then the stretcher is crosscut to 29.5". This is
why the fence does not cost a third board.

## Material optimization

**Firm: 2 red oak 1×4×6 (72") boards required.** One 6' board is impossible — parts total
120.25 lin in (with kerf) > 72". Verified packing:

| Board | Parts placed | Leftover |
|---|---|---:|
| 1 | top (31) + top (31) + riser (2.5) + riser (2.5) | ~4.5 in |
| 2 | fence/stretcher blank (31) + leg (11.125) + leg (11.125) | ~18 in |

**Buy 3 boards** — 2 required + 1 for grain/color-matching the glued top and defect
insurance (estimate, not required). No on-hand red oak exists
(`knowledge/shop/materials-on-hand.md`), so nothing on hand is consumed; the cubby-earmarked
offcuts are untouched.

## Dowel locations & joinery

Concealed 3/8" fluted dowels throughout; glue only; no screws.

- **Leg → top (3 per leg, ~1 in long):** across the 3.5" leg depth at ~0.875 / 1.75 / 2.625 in
  from the leg's back face (step a scrap spacer block — lesson #5). Each dowel runs from the
  leg's top (end grain) **through the pre-drilled riser** and into the shelf underside (long
  grain — the strong anchor). Legs are inset 0.75" from the shelf front.
- **Rear stretcher → legs (2 per end):** into the inner faces of the legs, positioned a few
  inches below the top, behind the shelf.
- **Back fence → shelf (3–4, alignment):** into the shelf's back edge; glue carries the load.
- **Top edge-glue (3–4, alignment only):** a properly jointed long-grain edge joint is
  stronger than the wood; dowels/biscuits only keep the two boards coplanar during glue-up.

Dowel count ~18 (estimate — buy a pack).

## Floating-top reveal (stretch goal)

**Primary — hidden setback riser.** A 0.375"-tall block (~0.75 × 2.5") sits between each leg
top and the shelf underside, **inset from the leg's front and back faces** so a 3/8" shadow
gap shows on the visible faces — the top reads as floating. Height re-closes:
`11.125 leg + 0.375 riser + 0.75 top = 12.25` ✓. The 3 leg→top dowels pass through it.

**Fallback — underside chamfer.** Rout a deep chamfer on the top's underside perimeter so the
visible edge reads thinner and appears to float. No height change, no extra joint, subtler
effect. Use if you'd rather skip the risers.

## Edge profile

**1/8" router roundover** on all exposed edges and corners (top faces + ends, leg outer edges,
fence top). Ease the reveal edges by hand. No sharp edges anywhere.

## Glue-up & assembly sequence

1. **Mill & label.** Crosscut all parts to length on the miter saw; label each (lesson #6).
   Select the two best-matched boards for the top.
2. **Edge-glue the top.** Joint the mating edges, add alignment dowels, glue and clamp the two
   1×4s into a 7.0"-wide panel. Cauls keep it flat; wipe squeeze-out.
3. **Rip the top to 6.75".** Once cured, rip one edge clean on the table saw/track saw to
   6.75" finished depth; this also trues the panel.
4. **Rip the fence/stretcher strips.** Rip the shared 31" blank into two 1.5" strips; crosscut
   one to 29.5" (stretcher).
5. **Drill dowels.** Jig-drill: leg tops (end grain), shelf underside, risers (through), leg
   inner faces (stretcher), shelf back edge + fence.
6. **Dry-fit** the whole bridge (legs + risers + top + stretcher); check square and the 11.5"
   opening before glue.
7. **Glue legs + risers to the top.** Dowel and glue both legs (through the risers) to the
   shelf underside, inset 0.75" from the front. Clamp; verify the reveal is even.
8. **Glue in the rear stretcher** between the legs.
9. **Glue on the back fence** along the shelf's back edge.
10. **Rout the 1/8" roundover** on all exposed edges; sand to 220.
11. **Finish** (schedule below); add silicone feet and optional magnets last.

## Weight & stability analysis

Red oak ≈ 45 lb/ft³ (0.026 lb/in³):

| Part | Volume (in³) | Weight (lb) |
|---|---:|---:|
| Top (6.75 finished) | 156.9 | 4.08 |
| Legs (2) | 58.4 | 1.52 |
| Rear stretcher | 33.2 | 0.86 |
| Back fence | 34.9 | 0.91 |
| Risers (2) | 1.4 | 0.04 |
| **Finished (bare)** | **284.8** | **~7.4** |

~7.5 lb with finish and feet. **Center of gravity sits ~2.9" behind the front feet.**

**Tipping.** The base is only 3.5" deep (leg depth) while the shelf is 11.5" up — the piece
is inherently **tippy forward**. The wall behind arrests backward tip only.
- Vertical load on the 3/4" front overhang: tips at **~28 lb** — not a concern.
- Horizontal bump at shelf height: tips at only **~1.8 lb empty** (~3 lb with jars kept to the
  back). **This is the real weakness** — disclose and mitigate.

## Anti-tip recommendations (in order of effectiveness)

1. **Rare-earth magnets to the range's steel side panel** — a mechanical tether; holding force
   far exceeds the ~2 lb tip threshold and converts "tips over" into "needs real force."
   Biggest single win (confirm the range side is magnetic; keep magnets away from heat).
2. **Load discipline** — heavy jars to the **back, over the legs**; never on the front overhang.
3. **Silicone feet at the front and back extremes of each leg** — friction stops the base
   kicking out (slide-then-tip) and maximizes the effective footprint.
4. If magnets aren't viable, consider **deepening the leg footprint** (a discreet forward foot)
   — a geometric fix, at some cost to the clean look and the 3.5" gap fit.

## Finish schedule

- **Primary: General Finishes High Performance (Satin), water-based topcoat.** Sand to 220;
  raise grain with a damp rag and knock back at 320; 3 thin coats, scuff-sand 320–400 between;
  cure hard before use. Grease- and moisture-resistant, wipes clean.
- **Alternative: Rubio Monocoat Pure (hardwax-oil), single coat.** Natural matte look, easy
  spot-repair; re-oil occasionally near the cooktop.

## Optional enhancements — evaluated

| Idea | Verdict |
|---|---|
| Clear silicone feet | **Yes** — friction + protects the counter; part of the anti-tip set. |
| Rare-earth magnets to range | **Yes (optional)** — best anti-tip tether if the side panel is magnetic. |
| Rear lip / groove for jars | **Included** as the raised back fence (positive stop, matches the reference). |
| Shadow line / floating top | **Included** — the hidden setback riser (3/8" reveal). |

## Suggested improvements

- **Aesthetics:** book-match the two top boards for a continuous grain; the 3/8" reveal + 3/4"
  front inset give the floating, furniture read.
- **Manufacturability:** all crosscuts on the miter saw; only two rip operations (top to 6.75",
  the shared strip blank); dowel jig keeps joinery repeatable.
- **Rigidity:** the rear stretcher fights racking; the edge-glued top is a stiff spanning
  member; risers add glue area at the leg tops.
- **Cleaning:** 1/8" roundovers and a film/oil finish wipe clean; no sharp corners to trap grease.

## Safety summary

- **Forward-tip risk on a hot cooktop** — use magnets + load discipline + feet (above). ⚠
- **The shelf is the lifting handle** — the glued leg→top dowel joints carry the legs when you
  lift the piece off; lift with two hands, don't yank a front corner (lesson #8 applied to a
  glue-only joint). ⚠
- Keep combustibles off the shelf directly over active burners; the shelf clears the grates by
  only ~0.25".

## Final outcome check

- Bridges the 3.5" gap behind a 30" range, ~0.5" overhang each side ✓
- No wall/counter fasteners; lifts off as one unit ✓
- No visible screws (concealed dowels, glue only) ✓
- Clears the cooktop by ~0.25" (opening 11.5") ✓
- 2 boards firm (buy 3 for grain/defects) ✓
- Cut list cut-verified `exit 0` ✓

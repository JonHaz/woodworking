---
type: Playbook
title: Build-planning lessons learned
description: Hard-won rules from past projects; every new build plan must apply the relevant ones.
tags: [methods, planning, cut-lists, safety]
timestamp: 2026-07-21T00:00:00Z
---

Each lesson records what went wrong (or almost did) and the rule that
prevents it. Append, don't rewrite — history is the point.

# Cut-list math

1. **Captured panels lose 2× material thickness.** A shelf that fits *between*
   two 3/4-in sides must be 1 1/2 in narrower than the finished width (the
   cubby-bench draft listed a 36 in shelf inside a 36 in bench — impossible).
   Always verify width, depth, and height stack-ups close on the finished
   dimensions before presenting a cut list.
2. **Face frames encroach on openings.** A 1 1/2-in frame member centered on a
   3/4-in divider steals 3/8 in per side of clear opening. If bins or fixed
   opening sizes matter, do the encroachment math up front — or skip the face
   frame (current preference: no face frame, fill + sand edges).
3. **Allow ~1/8-in kerf per cut.** A 48-in sheet minus two 17-in rips leaves
   ~13 3/4 in, not 14 — a 13.5-in third rip fits, a 14-in part does not.
4. **Label firm vs. estimated quantities.** Sheet and stick counts from yield
   math are firm; screws/glue/pads are estimates to round up.

# Shop technique

5. **Spacer blocks beat measured marks** for equal openings (cut one scrap
   spacer at the opening width, step it across). Eliminates cumulative error
   and awkward fractions like 11-1/16.
6. **Cut and label everything first**; near-identical panels get confusing
   fast (a 3-ft cubby bench has twelve plywood parts).
7. **Prototype one, then batch.** Build the first unit fully, dry-fit the
   critical interaction (stacking, side-by-side flushness), then batch the
   rest.

# Structure & safety

8. **Mechanically fasten seat/bench tops from inside** (screws, not
   brads/glue alone) — the top is the lifting handle; a popped top mid-carry
   drops the piece.
9. **Modular units interoperate through shared section dimensions.** The 3-ft
   and 4-ft benches align because depth (17), height (18.5), and overhang (0)
   are identical; only width varies.
10. **Recessed bases nest.** A base inset 1.5 in all around must travel 1.5 in
    before it can slide off the unit below. Stack like-with-like; mixed sizes
    lose self-centering (wider on bottom + strap). Max 3 high unstrappd; never
    6.
11. **Weight limits stacking practicality.** ~45–50 lb (3-ft, plywood) is a
    two-person lift; MDF (~70 lb) was rejected for repeated moving.

# Documentation

12. **Print-ready HTML guides with to-scale SVG diagrams** are the house
    style: title block, spec strip, numbered steps with figures, check-off
    boxes on shopping/cut sheets, safety callouts flagged.
13. **One consolidated master per size beats a scattered guide set.** The 2026
    cubby set first shipped as seven separate files (build guide, assembly, two
    cut diagrams, shopping sheet, plus a both-sizes plan) — the same cut list
    lived in five of them and the CSS in all seven, so any fix had to land in
    many places and the 4-ft set was left half-finished. The house deliverable is
    now **one self-contained `<name>_master.html` per size** (shopping → cut →
    build → assemble → safety in one printable file), which removes the
    duplication and the "which doc is right?" ambiguity. Supersedes the
    multi-file framing in lesson 12.

# Solid stock & freestanding pieces

*(From the 2026 freestanding stove shelf — the first solid-hardwood, glue-only,
freestanding build.)*

14. **A jointed long-grain edge glue-up is stronger than the wood — dowels are
    alignment, not strength.** Gluing narrow boards into a wide top (the shelf's
    two 1×4s → a 6.75-in top) needs no reinforcement to *hold*; add dowels or
    biscuits only to keep the faces coplanar during clamp-up (matters more with
    no planer to flatten afterward). Rip the cured panel to final width to true
    it.
15. **Don't conflate overall height with a part height.** The brief listed "leg
    height 12.25 in," but that was the *overall* height — with the top resting on
    the legs, `leg = overall − top (− riser)`. Solve part heights from the hard
    fit constraints (clear opening, cooktop clearance), and let the verifier's
    height stack-up catch the mix-up (`12.25 + 0.75 = 13.0 ≠ 12.25` fails).
16. **Two narrow parts can share one ripped blank — it can save a whole board.**
    The back fence (31 in) and rear stretcher (29.5 in) both rip from a single
    3.5-in-wide × 31-in blank as two 1.5-in strips, keeping the build to 2 boards
    instead of 3. The 1-D stick check can't see a rip, so model the shared blank
    as **one length** in `stick_stock` and spell out the rip in the cut list.
17. **Tall, shallow-footprint pieces tip forward — disclose the number, not just
    the weight.** A shelf 11.5 in up on a 3.5-in-deep base tips at only a ~1.8 lb
    horizontal bump (empty). Report the horizontal-bump threshold and mitigate
    with a tether (rare-earth magnets to an adjacent steel appliance), load
    discipline (weight to the back / over the legs), and feet at the footprint
    extremes. A wall behind arrests backward tip only.

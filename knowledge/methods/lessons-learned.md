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

---
type: Tool Inventory
title: Shop tools
description: Tools Jon owns; build plans must design around confirmed entries only.
tags: [shop, tools, capabilities]
timestamp: 2026-07-21T00:00:00Z
---

Status values: **confirmed** (Jon verified it) · **inferred** (implied by past
build sessions, needs verification) · **wanted** (doesn't own; candidate
purchase) · **not owned** (verified absent). AI assistants: design only around
`confirmed` tools; treat `inferred` as likely-but-verify; offer `wanted` /
`not owned`-tool approaches only as clearly labeled alternatives.

> **STATUS (2026-07-21):** Jon confirmed his saws, drill/impact driver, router,
> dowel jig, and the specialty power tools below. Still `inferred` and pending
> his confirmation: countersink bit, dedicated sander type, and clamp count/type.

# Cutting

| Tool | Status | Notes / capability |
|---|---|---|
| Table saw | confirmed | Primary ripping — the narrow full-length plywood rips (17 in and 13.5 in strips, 3 in stretcher strips) and general rip cuts. |
| Track saw + guide rail | confirmed | Breaking down full 4×8 sheets safely before/instead of the table saw, and straight-line rips where a full sheet is awkward. Resolves the old "table saw vs. circular + straightedge" question — Jon has both. |
| Miter saw | confirmed | Crosscutting the 2×4 base parts (33 in rails, 11 in rungs) and plywood part lengths. |
| Jigsaw | confirmed | Curved cuts, notches, and interior cutouts (e.g., optional handholds — the current design avoids them to keep sides flush). |

# Drilling, driving & joinery

| Tool | Status | Notes |
|---|---|---|
| Drill | confirmed | Pilot holes, countersinking, doweling, general drilling. |
| Impact driver | confirmed | Driving assembly screws and the 3 in construction (base) screws — faster and less cam-out than the drill. |
| Countersink bit | inferred | Assembly guide countersinks the base screws inside the cubbies — confirm owned. |
| Dowel jig | confirmed | Reinforced-joint option: dowels where a butt joint wants more than glue + screws. |
| Router | confirmed | Dados, rabbets, and grooves — enables *housed* shelf/divider joints (stronger than butt joints; the design spec notes this option, "add the dado depth to the captured part's dimension"). Edge profiles too, if ever wanted. |
| Pocket-hole jig | not owned | The guides mention pocket screws as an *optional* method for attaching the top and setting dividers — Jon has a dowel jig instead. Read those steps as "straight screws from inside with the drill, or dowels." No design should depend on pocket screws. |

# Other power tools

| Tool | Status | Notes |
|---|---|---|
| Angle grinder | confirmed | Metal cutting/grinding and sharpening — rarely needed for the plywood/2×4 furniture builds, but on hand. |
| Oscillating multi-tool | confirmed | Flush and plunge cuts, trimming proud edges/dowels, scribing to fit, and detail sanding with a pad attachment. |

# Layout & assembly

| Tool | Status | Notes |
|---|---|---|
| Tape measure, square, pencil | inferred | Standard layout. |
| Clamps (count/type unknown) | inferred | Assembly guide assumes clamping during glue-up — count/type still to confirm. |

# Finishing

| Tool | Status | Notes |
|---|---|---|
| Sander (type unknown) | inferred | Plywood edges are filled + sanded, no banding. The oscillating tool's sanding pad works for small areas, but a dedicated orbital/random-orbit sander is likely — confirm. |

# Explicit preferences (treat as standing constraints)

- **No edge banding** — fill and sand exposed plywood edges instead.
- **Reinforced joinery = dowels, not pocket screws.** Jon owns a dowel jig, not a
  pocket-hole jig. Primary joinery stays butt joints with glue + straight screws;
  reach for dowels when a joint needs more. With a router on hand, dado/rabbet
  housed joints are also available for shelves/dividers if a build wants them.
- Print-ready, visual documentation preferred over prose.

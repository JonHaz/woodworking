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

> **STATUS (2026-07-21):** Jon confirmed the cutting tools and the joinery jig
> below. Still `inferred` and pending his confirmation: drill/driver +
> countersink, sander type, and clamp count/type.

# Cutting

| Tool | Status | Notes / capability |
|---|---|---|
| Table saw | confirmed | Primary ripping — the narrow full-length plywood rips (17 in and 13.5 in strips, 3 in stretcher strips) and general rip cuts. |
| Track saw + guide rail | confirmed | Breaking down full 4×8 sheets safely before/instead of the table saw, and straight-line rips where a full sheet is awkward on the table saw. Resolves the old "table saw vs. circular + straightedge" question — Jon has **both** a table saw and a track saw. |
| Miter saw | confirmed | Crosscutting the 2×4 base parts (33 in rails, 11 in rungs) and plywood part lengths. |

# Drilling & fastening

| Tool | Status | Notes |
|---|---|---|
| Drill/driver | inferred | Every assembly is glued and screwed; near-certain — confirm make if useful. |
| Countersink bit | inferred | Assembly guide countersinks the base screws inside the cubbies. |
| Dowel jig | confirmed | Owned reinforced-joint option. Use dowels where a butt joint wants more than glue + screws. |
| Pocket-hole jig | not owned | The build guides mention pocket screws as an *optional* method for attaching the top and setting dividers — Jon does **not** own a pocket-hole jig (he has the dowel jig above). Read those steps as "straight screws driven from inside with the drill, or dowels." No design should depend on pocket screws. |

# Layout & assembly

| Tool | Status | Notes |
|---|---|---|
| Tape measure, square, pencil | inferred | Standard layout. |
| Clamps (count/type unknown) | inferred | Assembly guide assumes clamping during glue-up — count/type still to confirm. |

# Finishing

| Tool | Status | Notes |
|---|---|---|
| Sander (type unknown) | inferred | Plywood edges are filled + sanded, no banding. Orbital? Block? — to confirm. |

# Explicit preferences (treat as standing constraints)

- **No edge banding** — fill and sand exposed plywood edges instead.
- **Reinforced joinery = dowels, not pocket screws.** Jon owns a dowel jig, not
  a pocket-hole jig. Primary joinery stays butt joints with glue + straight
  screws; reach for dowels (not pocket screws) when a joint needs more.
- Print-ready, visual documentation preferred over prose.

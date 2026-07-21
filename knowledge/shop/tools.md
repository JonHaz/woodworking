---
type: Tool Inventory
title: Shop tools
description: Tools Jon owns; build plans must design around confirmed entries only.
tags: [shop, tools, capabilities]
timestamp: 2026-07-21T00:00:00Z
---

Status values: **confirmed** (Jon verified it) · **inferred** (implied by past
build sessions, needs verification) · **wanted** (doesn't own; candidate
purchase). AI assistants: design only around `confirmed` tools; treat
`inferred` as likely-but-verify; offer `wanted`-tool approaches only as
labeled alternatives.

> **ACTION NEEDED:** everything below is `inferred` from the cubby-bench
> sessions. Jon — please edit statuses, add makes/models if useful, and add
> anything missing (sander? router? clamp count? jigsaw?).

# Cutting

| Tool | Status | Notes / capability implied |
|---|---|---|
| Saw capable of ripping 4×8 sheet goods | inferred | Cubby-bench plan rips 17 in and 13.5 in full-length strips — table saw, or circular saw + straightedge guide. **Which?** Affects how cut diagrams are drawn. |
| Saw for crosscutting 2×4s | inferred | Base rails/rungs (33 in, 11 in cuts). Miter saw or circular saw. |

# Drilling & fastening

| Tool | Status | Notes |
|---|---|---|
| Drill/driver | inferred | All assemblies use screws. |
| Countersink bit | inferred | Called for in assembly guide. |
| Pocket-hole jig | inferred | Listed as "optional" in the assembly guide — confirm whether owned. |

# Layout & assembly

| Tool | Status | Notes |
|---|---|---|
| Tape measure, square, pencil | inferred | Standard layout. |
| Clamps (unknown count/type) | inferred | Assembly guide assumes clamping during glue-up. |

# Finishing

| Tool | Status | Notes |
|---|---|---|
| Sanding (method unknown) | inferred | Plywood edges are filled + sanded (no edge banding, per owner preference). Orbital sander? Block? |

# Explicit preferences (treat as standing constraints)

- **No edge banding** — fill and sand exposed plywood edges instead.
- Print-ready, visual documentation preferred over prose.

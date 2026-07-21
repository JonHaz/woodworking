---
type: Material Inventory
title: Materials on hand
description: Lumber and sheet-good stock in the shop, with planned allocations; consume this before buying.
tags: [shop, materials, lumber, inventory]
timestamp: 2026-07-21T00:00:00Z
---

Rule for build planning: allocate from this list **first**, then shopping
list. When a project consumes stock, update this file and note it in
[/log.md](/log.md).

# Dimensional lumber (as measured 2026-07)

| Qty | Size (L × W × H, in) | What it is | Status / allocation |
|---:|---|---|---|
| 8 | 54 1/8 × 1 1/2 × 3 1/2 | True 2×4 offcuts | **Earmarked — cubby benches Phase 1**: each cut `33 + 11` → 8 base rails + 8 rungs. See [project doc](/projects/cubby-benches-2026.md). |
| 8 | 101 1/2 × 1 1/2 × 1 1/2 | Long 2×2 rip strips | Available. Optional substitute for base rungs (sit ~2 in below shelf — loses mid-span shelf backing; structurally acceptable for cubby bases). |
| 4 | 53 3/8 × 1 1/2 × 1 5/8 | Ripped strips (non-standard height) | Available, unallocated. Too short (height) for 2×4-on-edge base parts. |

# Sheet goods

| Qty | Material | Status |
|---:|---|---|
| 0 | 3/4 in plywood 4×8 | None on hand. Phase 1 requires 4 sheets (purchase). |

# Consumables (track loosely)

Wood glue, assembly screws (1 1/4–2 in), construction screws (3 in), rubber
anti-slip pads — quantities per active project shopping sheets; restock when low.

# Update protocol

After each build session that consumes or creates stock: adjust quantities,
re-measure meaningful offcuts (anything ≥ 24 in dimensional or ≥ 12 × 12
sheet), date the change, and add a `log.md` entry.

---
name: shop-inventory
description: Confirm and maintain the shop's real tool and material inventory so every design is grounded in what Jon actually owns, not guesses. Use for a deliberate inventory census — "confirm my tools", "I own a table saw", "which tools are you still guessing at", "promote these to confirmed", "add a router to my shop", "I have six bar clamps", "re-measure my offcuts", "took stock of the shop today". Reads knowledge/shop/tools.md and materials-on-hand.md, runs an audit script that flags every still-inferred tool and unmeasured leftover, interviews Jon only for the gaps, and writes back correct status values (confirmed, inferred, wanted) under OKF v0.1 — which unblocks build-planner's design-only-around-confirmed-tools guarantee. Do not use for the post-build feedback ritual (that is shop-close-out), designing a build (build-planner), or scoping a new idea (project-intake).
---

`build-planner` promises to design only around tools Jon actually owns — a
promise only as trustworthy as the statuses in `tools.md`. This skill is the
deliberate census that keeps those statuses honest: it turns `inferred` guesses
into verified facts (`confirmed`, `wanted`, or `not owned`), keeps the material
inventory measured and current, and re-runs on demand so the rest of the
pipeline can be trusted. The first census resolved most of Jon's tools; run it
again whenever the shop changes or an `inferred` straggler needs pinning down.

The work is a short, audit-driven interview, not a blank-page survey. A script
tells you exactly what is still unknown; you resolve those items with Jon and
write the answers back. You never guess a tool into `confirmed`.

## When to use this skill

- Jon wants to confirm what the repo *thinks* he owns ("which tools are you still
  guessing at?", "let's lock down my tool list").
- A tool was just acquired or retired ("I picked up a random-orbit sander",
  "add a router", "I don't actually have a pocket-hole jig").
- Stock needs a census outside a build — new lumber measured in, offcuts
  re-measured, quantities corrected.

Do not use this skill for the post-build knowledge update after a specific build
(consumed stock, leftovers, lessons) — that is `shop-close-out`. Do not use it to
design a build (`build-planner`) or scope a vague idea (`project-intake`).

## How to use this skill

Work the ordered ritual in `references/inventory-protocol.md`. In brief:

1. **Audit first — it sets the agenda.** Run
   `python3 scripts/audit_inventory.py --format text` from the repo root. It lists
   every tool not yet `confirmed`/`wanted` and every unmeasured stock row. That
   list is your interview agenda; skip anything already `confirmed`.
2. **Interview only for the gaps.** Group unknowns by category (cutting, drilling,
   layout, clamping, finishing) and ask compactly. Resolve the flagged items and
   stop — do not re-ask confirmed categories.
3. **Never promote `inferred` → `confirmed` without Jon.** That is his call and
   the entire point of the field. A wrong `confirmed` misleads every future
   design; an honest `inferred` does not.
4. **Measure materials or they do not count.** Every dimensional row needs a real
   size (`54 1/8 × 1 1/2 × 3 1/2`), not "some 2×4". Preserve allocation notes.
5. **Write back OKF-clean.** Edit statuses in place, bump the `timestamp`, drop
   the `ACTION NEEDED` banner once resolved, add make/model for confirmed tools,
   and log the change in `knowledge/log.md` (newest first).
6. **Re-run the audit to prove it.** Report the before/after tally ("8 inferred →
   6 confirmed, 1 wanted, 1 still unknown").

## Reference map

| File | When to load |
|---|---|
| `references/inventory-protocol.md` | Always — the status rules, interview structure, and write-back steps. |
| `scripts/audit_inventory.py` | Always — run it to find the gaps; do not eyeball the tables. |
| `knowledge/shop/tools.md` | The file being audited and edited. |
| `knowledge/shop/materials-on-hand.md` | The material side of the census. |

## Common output template

- **Audit result** — the tally line (confirmed / wanted / inferred / unknown) and
  the list of items needing confirmation.
- **Interview** — the compact questions asked, grouped by category.
- **Changes written** — each status promoted or corrected, each measurement added,
  with make/model where Jon gave one.
- **Log entry** — confirmation the dated `log.md` line was added.
- **Re-audit** — the after tally, and any item Jon genuinely could not resolve
  today (left honestly as `inferred`).

## Non-negotiable principles

- **Confirmed means verified by Jon.** Never infer a `confirmed`. Ask.
- **The audit script, not eyeballing.** It is deterministic and catches every
  unresolved row; a manual scan misses the eighth tool.
- **Measured stock only.** An offcut without a dimension is invisible to the next
  allocation — give it a real size or leave it in loose consumables.
- **Preserve allocations.** Never drop an `earmarked`/`allocation` note when
  editing a quantity; it is the only link between stock and a project.

## Gotchas

- **`wanted` and `not owned` are resolved, not gaps.** A tool Jon plans to buy or
  has verified he does not own is a decision, not an unknown — the audit treats
  `confirmed`, `wanted`, and `not owned` as done and only flags `inferred`/blank.
- **Do not design here.** This skill records what exists; it never sizes a part or
  proposes a build. If the conversation drifts to a design, hand to `build-planner`.

## Next steps

- The moment the census is clean, `build-planner` and `project-intake` can honor
  "confirmed tools only" for real — that is the payoff of running this.
- After a specific build finishes, run `shop-close-out` (not this skill) for the
  consumed-stock / leftovers / lessons ritual; it relies on the inventory this
  skill keeps honest.

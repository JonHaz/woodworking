---
name: shop-close-out
description: Run the post-build knowledge-update ritual so the woodworking repo compounds into a better resource after every project. Use at a build milestone or completion, or whenever Jon says "log this build", "update the shop", "I finished the benches", "close out this project", "I bought a new tool", "record what I have left over". Updates materials-on-hand (consume used stock, add measured leftovers), appends new lessons, updates the project concept doc's status, adds a newest-first ISO-dated log entry, and records any newly acquired tool as confirmed — all under OKF v0.1 conventions. Do not use for designing or revising a build (that is build-planner), or for scoping a new idea (that is project-intake).
---

The repo is only a compounding resource if every build feeds back into it. This skill
runs that feedback reliably — the exact ritual in `CLAUDE.md` under "After a project
milestone or close-out" — so the materials inventory, the lessons, the project status,
and the log never drift out of sync with what actually happened at the bench.

## When to use this skill

- A build (or a phase of one) is finished or hit a milestone worth recording.
- Jon reports leftover stock, a mistake worth capturing as a lesson, or a new tool.
- Any project's `status` needs to move (`planning` → `in-progress` → `complete`).

Do not use this skill to design or revise a build (`build-planner`) or to scope a new
idea (`project-intake`). This skill only writes to the knowledge base.

## How to use this skill

Work the checklist in `references/okf-closeout.md` in order. In brief:

1. **Materials** — update `knowledge/shop/materials-on-hand.md`: subtract the stock the
   build consumed, and add leftovers **with measured sizes** (a 54-1/8 offcut, not "a bit
   of 2×4"). Vague leftovers are useless to the next allocation.
2. **Lessons** — append any new lesson to `knowledge/methods/lessons-learned.md`. Record
   what went wrong (or nearly did) and the rule that prevents it. **Append, never rewrite**
   — the history is the point. Keep the numbering continuing from the last item.
3. **Project concept** — update (or create) the `knowledge/projects/` doc: move `status`,
   refresh the phase notes and key numbers, keep the documents list accurate.
4. **Log** — add an entry to `knowledge/log.md` under a `## YYYY-MM-DD` heading (today,
   **newest first**), using `**Update**` / `**Creation**` style and bundle-relative links.
5. **Tools** — if a tool was acquired, add it to `knowledge/shop/tools.md` as `confirmed`
   (make, model, capability). If a build confirmed a previously `inferred` tool, promote it.
6. **Indexes** — keep every touched `index.md` current (new concepts listed, descriptions fresh).

## Reference map

| File | When to load |
|---|---|
| `references/okf-closeout.md` | Always — the ordered checklist with the exact formats. |
| `knowledge/log.md` | To match the log entry style and confirm newest-first order. |
| `knowledge/projects/cubby-benches-2026.md` | The concept-doc frontmatter and section shape. |
| `knowledge/methods/lessons-learned.md` | To continue the lesson numbering and voice. |

## Common output template

A brief close-out summary for Jon:

- **Files touched** — each knowledge file changed, one line on what changed.
- **Inventory delta** — stock consumed and leftovers added (with sizes).
- **New lessons** — the numbers and one-line titles appended.
- **Status change** — the project's old → new `status`.
- **Log entry** — confirmation the dated entry was added, newest first.

## Non-negotiable principles

- **Measured leftovers only.** Every added offcut gets a real dimension.
- **Append lessons, never overwrite.** New numbers continue the sequence; old lessons stay.
- **Newest-first log, ISO dates.** Today's entry goes at the top under `## YYYY-MM-DD`.
- **OKF frontmatter stays valid.** Concept docs keep their `type` and other fields; links
  between concepts are bundle-relative (start with `/`).
- **Promote tools honestly.** Only mark a tool `confirmed` when Jon actually owns/used it;
  do not silently flip `inferred` entries without confirmation.

## Gotchas

- **Do not invent lessons.** Only append a lesson that a real build actually taught; a
  padded lessons file erodes trust in the ones that matter.
- **The concept doc and the log must agree.** If the log says Phase 1 is complete, the
  concept doc's `status` and phase notes must say so too.

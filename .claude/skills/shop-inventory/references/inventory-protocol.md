# Shop inventory protocol

The ordered ritual for taking or updating the shop census. The goal is a
`tools.md` and `materials-on-hand.md` that `build-planner` and `project-intake`
can trust literally: a `confirmed` tool is one Jon actually owns, and every
on-hand stock row carries a real measurement. Work these steps in order.

## 1. Run the audit first — let it set the agenda

```
python3 scripts/audit_inventory.py --format text
```

Run it from the repo root (it defaults to `knowledge/shop/tools.md` and
`knowledge/shop/materials-on-hand.md`). It prints every tool still `inferred`
(or blank/unknown) and every stock row missing a measurement. That list *is* the
interview agenda — do not ask about tools already resolved.

Exit `1` means the census still has `inferred` gaps. The first census resolved
most of Jon's tools, so this is usually a short list — a straggler like the
countersink bit, or the assumed layout tools. Exit `0` means nothing needs
confirming. Exit `2` means a path was wrong or a file could not be parsed.

## 2. Status values — the whole point of the file

| Status | Meaning | Who may set it |
|---|---|---|
| `confirmed` | Jon verified he owns it (ideally make/model). | Only after Jon says so. |
| `inferred` | Implied by a past build, **not** verified. A guess. | Set by planning, never a resting state. |
| `wanted` | Jon does not own it; a candidate purchase. | Jon's decision. |
| `not owned` | Jon verified he does **not** own it (e.g. pocket-hole jig). | Jon's decision; resolved, not a gap. |

`confirmed`, `wanted`, and `not owned` are all *resolved* — a decision has been
made. Only `inferred` (and blank) is an open gap the audit flags.

**Never silently flip `inferred` → `confirmed`.** That is Jon's call and the
entire value of the field. Ask; do not assume. A wrong `confirmed` is worse
than an honest `inferred`, because `build-planner` will design against it.

## 3. Interview only for the gaps

Group the audit's unconfirmed tools by category and ask compactly. Typical
categories and the questions that resolve them:

- **Cutting** — table saw or circular saw + straightedge? (this decides how cut
  diagrams are drawn) Miter saw for crosscuts? Jigsaw?
- **Drilling / fastening** — drill/driver make? Countersink bit? Pocket-hole jig
  (owned, or was it only ever "optional")?
- **Layout** — tape, square, pencil (assume yes unless Jon says otherwise).
- **Clamping** — how many clamps, what type/length? (glue-ups assume clamping)
- **Finishing** — random-orbit sander, or block only? (edges are filled + sanded)

Keep it to a short back-and-forth. The audit tells you exactly what is unknown;
resolve those and stop. Do not re-interview confirmed categories.

## 4. Materials — measured, or it does not count

Every dimensional-lumber row needs a real size (`54 1/8 × 1 1/2 × 3 1/2`), not a
vague "some 2×4." The audit flags any stock row whose size cell is not a
measurement. Re-measure meaningful offcuts (≥ 24 in dimensional, ≥ 12 × 12 in
sheet); smaller scraps can be tracked loosely under consumables.

Preserve any `allocation` / `earmarked` notes — those tie stock to a project and
must not be dropped when quantities change.

## 5. Write back — correct statuses, OKF-clean

- Edit the table cells in place; keep the table columns intact.
- Bump each file's frontmatter `timestamp` to the audit date.
- Remove the `> ACTION NEEDED` banner from `tools.md` once its inferred entries
  are resolved (it exists only to prompt the first census).
- For a newly acquired tool, add a row with `confirmed` status and make/model.
- Add a newest-first entry to `knowledge/log.md` under `## YYYY-MM-DD`:
  `**Update** — [tools.md](/shop/tools.md): confirmed table saw (DeWalt DWE7491),
  promoted 5 inferred entries; jigsaw marked wanted.`
- Keep `knowledge/shop/index.md` accurate if descriptions changed.

## 6. Re-run the audit to prove it

```
python3 scripts/audit_inventory.py --format text
```

A clean `exit 0` (or a smaller findings list with the remaining unknowns Jon
genuinely could not resolve today) is the close of the census. Report the
before/after tally to Jon: "8 inferred → 6 confirmed, 1 wanted, 1 still unknown
(pocket-hole jig)."

## Boundary with shop-close-out

This skill is the **deliberate census** — confirming what is owned, correcting
statuses, adding a tool the moment it is acquired, re-measuring stock. The
`shop-close-out` skill is the **post-build feedback ritual** — after a specific
build it consumes the stock that build used, adds the leftovers it produced,
and appends the lessons it taught. When both apply (a build just finished *and*
it introduced a new tool), `shop-close-out` runs the close-out and this skill
owns the standing tool/material truth it writes into.

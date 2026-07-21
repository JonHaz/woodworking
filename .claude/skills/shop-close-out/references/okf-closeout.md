# OKF close-out checklist

The ordered ritual for `shop-close-out`. Work top to bottom; each step names the file,
what to change, and the exact format to match. OKF v0.1 conventions throughout:
concept docs carry YAML frontmatter with at least a `type`; `index.md` files are plain
directory listings (no frontmatter, except the bundle root); links between concepts are
**bundle-relative** (start with `/`, e.g. `/shop/tools.md`).

## 1. Materials — `knowledge/shop/materials-on-hand.md`

- Subtract every piece the build consumed from the on-hand tables.
- Add leftovers **with measured dimensions and quantity** (e.g. `2×4 offcut — 40-3/8 in ×2`).
  Never "some 2×4 left"; the next allocation reads these numbers literally.
- If a whole category is exhausted, leave the row with qty `0` or remove it, but say which
  in the log entry.

## 2. Lessons — `knowledge/methods/lessons-learned.md`

- **Append only.** Continue the existing numbering under the right section
  (`# Cut-list math`, `# Shop technique`, `# Structure & safety`, `# Documentation`, or a
  new section if warranted).
- Each lesson = what went wrong (or nearly did) + the rule that prevents it. One tight
  paragraph. Keep the voice of the existing entries.
- Do not edit or renumber past lessons — history is the point.

## 3. Project concept — `knowledge/projects/<name>.md`

Update the existing doc (or create one if this project skipped intake). Frontmatter shape:

```yaml
---
type: Project
title: <human title>
description: <one line>
resource: https://github.com/JonHaz/woodworking/tree/main/projects/<year>-<name>
tags: [<materials>, <kind>, <active|complete>]
timestamp: <ISO-8601>
status: <planning | phase-N-in-progress | complete>
---
```

- Move `status` to reflect reality; update the `# Status` phase notes and `# Key numbers`.
- Keep the `# Documents (repo)` list pointing at the real files in `projects/…`.
- Under `# Lessons fed back`, reference the lesson numbers this build contributed.

## 4. Log — `knowledge/log.md`

- Add today's entry at the **top** (newest first) under a `## YYYY-MM-DD` heading; reuse
  the heading if one already exists for today.
- Use `**Update**` for changes and `**Creation**` for new concepts. Link with
  bundle-relative paths. Example:

```markdown
## 2026-08-14
* **Update**: Closed out Phase 1 of the [cubby benches](/projects/cubby-benches-2026.md):
  consumed 4 ply sheets + 3 new 2×4s + 8 on-hand offcuts; logged 6-3/4 in and 40-3/8 in
  leftovers in [materials](/shop/materials-on-hand.md); appended lesson #13 (label parts
  before glue-up). Project status → phase-2-planned.
```

## 5. Tools — `knowledge/shop/tools.md`

- If a tool was acquired, add a row with `confirmed` status, make/model, and the capability
  it unlocks.
- If a build *confirmed* a tool previously marked `inferred`, promote it to `confirmed`
  (only with Jon's confirmation — do not flip inferred rows silently).

## 6. Indexes — every touched `index.md`

- `knowledge/projects/index.md`, `knowledge/shop/index.md`, `knowledge/methods/index.md`:
  add any new concept as a bullet `* [Title](file.md) - one-line hook`, and refresh a
  description if it went stale. These are plain listings — no frontmatter.

## Final check

- Log, concept `status`, and materials all tell the **same** story about what was built
  and what is left.
- No angle-bracket `<...>` placeholders left in any file you wrote.
- Every inter-concept link starts with `/`.

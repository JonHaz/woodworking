---
name: project-intake
description: Turn a vague woodworking idea into a scoped, feasible project brief before any design work starts. Use whenever Jon floats a new build in loose terms — "I want a bench for the mudroom", "thinking about garage shelves", "could I build a coffee table", "need storage for the closet", "let's plan something new". Interviews only for the facts that change a design (dimensions, use/load, finish, quantity, budget, deadline), checks feasibility against confirmed tools and on-hand materials, scaffolds the project folder, writes an OKF concept doc, and hands off to build-planner. Do not use for designing or cutting an already-scoped build (that is build-planner), or for logging a finished build (that is shop-close-out).
---

A good build starts with a scoped brief, not a blank design. This skill is the front
door: it converts a loose idea into a short, concrete brief the `build-planner` can
design against, and it catches feasibility problems (a cut that needs an unowned tool,
a size that ignores on-hand stock) while they are still cheap to fix — before any panel
is dimensioned.

## When to use this skill

- Jon describes something he might build, in loose terms, with no dimensions yet.
- The tools or materials picture matters ("what can I build with what I have?").
- A project is starting and needs a folder, a concept doc, and a place in the log.

Do not use this skill when the build is already scoped and it is time to produce a
dimensioned design or cut list — hand to `build-planner`. Do not use it to log a
finished build — that is `shop-close-out`.

## How to use this skill

1. **Read the shop first.** Load `knowledge/shop/tools.md` and
   `knowledge/shop/materials-on-hand.md` so the interview and feasibility check are
   grounded in what Jon actually owns.
2. **Interview only for design-changing facts.** Ask the few things that move the design
   and stop: target dimensions (or the space it must fit), use and load (seating? heavy
   storage?), finish, quantity, budget ceiling, deadline. Do not ask what the knowledge
   base already answers, and do not drift into designing.
3. **Run a feasibility pass.** Flag anything that needs a tool not marked `confirmed`
   (offer it as a clearly labeled alternative, never the default), and note which on-hand
   stock the build could consume before buying anything.
4. **Scaffold the project folder.** Create `projects/<year>-<name>/` with `design/`,
   `guides/`, and `photos/` (copy the shape of `templates/project-template/`).
5. **Write the concept doc** to `knowledge/projects/<name>.md` using OKF v0.1 frontmatter
   (`type: Project`, `title`, `description`, `resource` repo URL, `tags`, `timestamp`,
   `status: planning`) and bundle-relative links. Add a one-line entry to
   `knowledge/projects/index.md` and a `**Creation**` line under today's date in
   `knowledge/log.md` (newest date first).
6. **Hand off to `build-planner`** to turn the brief into a verified design.

## Reference map

| File | When to load |
|---|---|
| `knowledge/shop/tools.md` | Always — the confirmed-tool feasibility check. |
| `knowledge/shop/materials-on-hand.md` | Always — what stock the build can use first. |
| `knowledge/projects/cubby-benches-2026.md` | The concept-doc format to match. |
| `templates/project-template/README.md` | The folder shape to scaffold. |

## Common output template

A short **project brief** Jon can approve at a glance:

- **What / why** — one or two sentences.
- **Scope** — dimensions (or the target space), use/load, finish, quantity, budget, deadline.
- **Feasibility** — buildable with confirmed tools? which steps (if any) need an
  unowned tool, and the labeled alternative; which on-hand stock it can consume first.
- **Open questions** — anything still unknown that will change the design.
- **Artifacts created** — the project folder path, the concept-doc path, the log entry.

Next: run `build-planner` to design the scoped build (it will emit a spec, gate it through
`cut-verifier`, and render the guides).

## Non-negotiable principles

- **Scope, do not design.** No cut lists, no part dimensions here — that is `build-planner`'s
  job. Intake ends at an approved brief and a scaffolded project.
- **Confirmed tools only in the default path.** Unowned-tool ideas are alternatives,
  clearly labeled, never the plan of record.
- **On-hand before new.** Name the stock the build could consume before it reaches a
  shopping list.
- **OKF discipline.** The concept doc, index line, and log entry all get written now, so
  the project is tracked from birth — not reconstructed later.

## Gotchas

- **Do not over-interview.** Three to six questions is usually enough; the design phase
  will surface the rest. A brief that stalls on every detail defeats the purpose.
- **`status: planning`** at intake. It moves to `in-progress` / `complete` later via
  `shop-close-out`, not here.

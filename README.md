# Woodworking

A personal DIY build system: past project archives, shop knowledge, and AI-ready
context so that every new build plan starts from what I actually own and what
I've already learned.

## How this repo works

Two halves:

1. **`knowledge/`** — an [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
   v0.1 bundle. Markdown files with YAML frontmatter describing the shop:
   tools owned, materials on hand, and lessons learned. This is the context an
   AI assistant reads **before** generating any build plan.
2. **`projects/`** — one folder per project, holding the final design docs and
   the print-ready HTML build guides (cut diagrams, shopping sheets, assembly
   guides).

`CLAUDE.md` tells Claude (Code, Cowork, or chat) how to use both halves.
`.claude/skills/build-planner/` packages the build-planning workflow as a
reusable skill.

## Repo map

```
woodworking/
├── README.md                  ← you are here
├── CLAUDE.md                  ← standing instructions for AI assistants
├── knowledge/                 ← OKF v0.1 knowledge bundle
│   ├── index.md               ← bundle index (progressive disclosure)
│   ├── log.md                 ← chronological update log
│   ├── shop/                  ← tools.md · materials-on-hand.md
│   ├── methods/               ← lessons-learned.md
│   └── projects/              ← one concept doc per project (summary + links)
├── projects/                  ← full project archives
│   └── 2026-stackable-cubby-benches/
│       ├── README.md
│       ├── design/            ← dimensioned design spec (markdown)
│       └── guides/            ← print-ready HTML: build guides, cut diagrams,
│                                shopping sheet, assembly guide
├── templates/
│   └── project-template/      ← starting structure for the next project
└── .claude/
    └── skills/
        └── build-planner/     ← Claude skill: plan builds from shop knowledge
```

## Workflow for a new project

1. Copy `templates/project-template/` → `projects/<year>-<name>/`.
2. Ask Claude for a build plan. Per `CLAUDE.md`, it reads
   `knowledge/shop/tools.md`, `knowledge/shop/materials-on-hand.md`, and
   `knowledge/methods/lessons-learned.md` first, and designs within them.
3. Iterate; save final designs and guides into the project folder.
4. Close out: add a concept doc in `knowledge/projects/`, append new
   lessons to `knowledge/methods/lessons-learned.md`, update
   `knowledge/shop/materials-on-hand.md` with leftovers, and log the change
   in `knowledge/log.md`.

## Current status

- **Active:** [Stackable cubby benches](projects/2026-stackable-cubby-benches/) —
  Phase 1 (six 3-ft benches) in progress; Phase 2 (four 4-ft) planned.
- **Tool inventory:** partially seeded from build sessions — needs owner
  confirmation. See [knowledge/shop/tools.md](knowledge/shop/tools.md).

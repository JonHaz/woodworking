# Design spec schema (the cut-verifier contract)

> Mirror of `.claude/skills/cut-verifier/references/spec-schema.md` — the canonical
> copy the verifier script parses. `build-planner` emits this format; `cut-verifier`
> consumes it. Keep the two in sync.

`build-planner` emits a design as a small JSON object; `cut-verifier` consumes it
and re-derives the numbers. This is the single interface between the two — keep it
stable. JSON is canonical (dependency-free); `.yaml`/`.yml` is accepted only if
PyYAML is installed.

Run: `python3 .claude/skills/cut-verifier/scripts/verify_cutlist.py <spec.json> [--format text|json]`
Exit `0` = every check closes · `1` = one or more checks fail · `2` = bad spec/usage.

## Top-level fields

| Field | Required | Meaning |
|---|---|---|
| `project` | recommended | Label echoed in output. |
| `units` | optional | Informational (default `in`). All numbers are inches. |
| `kerf` | optional | Saw kerf allowed per cut in yield math. Default `0.125`. |
| `material_thickness` | optional | Default panel thickness for captured checks. Default `0.75`. |
| `finished` | recommended | `{width, depth, height}` finished dimensions (documentation + sanity). |
| `stackups` | yes* | Dimension closure checks (see below). |
| `captured_checks` | yes* | Captured-panel width/height checks (lesson #1). |
| `parts` | recommended | Part list; `kind` drives the firm-vs-estimate split (lesson #4). |
| `stick_stock` | if linear stock | 1-D cutting feasibility for 2x4s etc. (lesson #3). |
| `sheet_stock` | if sheet goods | Sheet yield: area lower bound + optional rip-plan strip checks (lesson #3). |

\* Provide whichever apply to the design. A spec with no checks passes trivially —
so always include at least the `stackups` and `captured_checks` for a real design.

## stackups — every dimension must close (lesson #1)

Each entry is an ordered list of segments that must sum to a finished dimension.

```json
"stackups": [
  { "name": "width",  "equals": 36,   "segments": [0.75, 11, 0.75, 11, 0.75, 11, 0.75] },
  { "name": "height", "equals": 18.5, "segments": [3.5, 14.25, 0.75] }
]
```

A failing stackup reports the actual sum, the expected value, and the delta.

## captured_checks — panels that fit *between* walls (lesson #1 / #2)

A part captured between `walls` pieces of thickness `t` must equal `span - walls*t`.
This is the "36-in shelf can't fit inside a 36-in bench" guard.

```json
"captured_checks": [
  { "name": "bottom shelf", "actual": 34.5, "span": 36, "walls": 2 },
  { "name": "divider height", "actual": 13.5, "span": 14.25, "walls": 1 }
]
```

`thickness` defaults to `material_thickness`; set it per-check for mixed stock.

## stick_stock — 1-D cutting for linear stock (lesson #3)

Greedy first-fit-decreasing packing. **On-hand stock is consumed before new stock**,
and each cut consumes `length + kerf`.

```json
"stick_stock": {
  "parts":   [ {"length": 33, "qty": 12}, {"length": 11, "qty": 18} ],
  "on_hand": [ {"length": 54.125, "qty": 8} ],
  "new":     [ {"length": 96, "qty": 3} ]
}
```

Reports on-hand pieces used and how many **new** sticks are needed; fails if pieces
cannot be placed or more new stock is needed than provided.

## sheet_stock — sheet-goods yield (lesson #3)

`sheet` is `[width, length]`. The area check is a **necessary lower bound** (kerf-padded
per part). For a strong check, add a `rip_plan`: each strip lists its crosscuts, verified
1-D against the strip length.

```json
"sheet_stock": {
  "sheet": [48, 96], "thickness": 0.75, "count": 4,
  "parts": [ {"w": 36, "d": 17, "qty": 6} ],
  "rip_plan": [ { "name": "17-in strip", "length": 96, "crosscuts": [36, 34.5, 14.25] } ]
}
```

## parts — firm vs estimate (lesson #4)

`kind` is one of `sheet`, `stick`, or `hardware`. `sheet`/`stick` parts are reported
as **firm**; `hardware` (screws, glue, pads) as **estimate** (round up).

See `.claude/skills/cut-verifier/examples/` for a complete passing spec and a failing one.

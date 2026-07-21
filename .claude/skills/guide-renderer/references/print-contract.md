# Print contract (what a master must do on paper)

A master build document exists to be printed and carried into the shop. Everything below
is a rule the rendered file must satisfy, with the reason it exists. `verify_render.py`
enforces the mechanical ones.

## The block

```css
@page{size:letter portrait;margin:12mm 10mm}
@media print{
  body{background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .sheet{max-width:none;padding:0 8px}
  .step,figure,table,.spec{page-break-inside:avoid;break-inside:avoid}
  h2.sec{page-break-after:avoid;break-after:avoid}
  h2.sheetnum{page-break-after:avoid;break-after:avoid}
  h2,h3,figcaption{orphans:3;widows:3}
  p,li{orphans:2;widows:2}
}
```

Omit the `h2.sheetnum` line in a master that has no sheet-number headings (a one-sheet
project does not need them).

## Why each rule

**`@page` with an explicit size and margin.** Without it the browser picks, and the
printed margin varies by browser and by the user's last print dialog. A cut list that
reflows between two prints of the same file is a real hazard: the builder ticks a box on
page 3 and comes back to a different page 3. Letter portrait matches Jon's printer.

**`print-color-adjust:exact` (with the `-webkit-` prefix).** This one is narrower than it
looks, and the distinction matters:

| Mechanism | Where it is used | Prints by default? |
|---|---|---|
| SVG `fill="var(--top)"` | every part in every cut diagram | **Yes** — page content, unaffected by the "background graphics" toggle |
| CSS `background:var(--top)` | legend swatches, `.spec` strip, verdict badge, callout tints | **No** — dropped unless colour adjust is on |

So the cut diagrams were never at risk; the diagrams keep their colours regardless. What
was lost was the **legend key** — the nine swatches that say which tint means TOP versus
SHELF versus SIDE — plus the callout tints. That degrades gracefully (swatches carry a
`1.6px solid` border, labels are text, and every figcaption names the parts in prose),
which is why two benches got built without anyone noticing. Fix it anyway: a legend that
prints as nine identical white squares is a legend that does no work.

**Paired legacy and modern break properties.** `page-break-*` is deprecated but still what
some engines honour; `break-*` is the current spec. Ship both — they cost nothing and no
single property is reliable across Chrome, Safari and print-to-PDF.

**`break-inside:avoid` on `.step`, `figure`, `table`, `.spec`.** A step split from its
figure, or a cut-list table split mid-row, is the failure that sends someone back to the
screen. These are the units that must stay whole.

**`orphans`/`widows`.** Stops a heading stranded at a page foot and a single trailing line
carried to the next page.

## What the contract does *not* require

**Scale bars are not required, and were considered and rejected.** The SVGs carry no
`width`/`height` and print at `max-width:none`, so a figure's *absolute* printed size
varies with paper and margins. That sounds alarming and mostly is not: every part in every
cut figure carries its dimensions as text (`TOP 36 × 17`, `SHELF 34.5 × 17`, rip widths,
sheet size), and the assembly figures that carry no in-figure text state their numbers in
the figcaption. **No figure in any shipped master requires measuring off the page.** Adding
scale bars to thirty-eight figures would add clutter to solve a problem the labels already
solve.

What *is* required is that each figure's scale be **declared** — visibly in the caption or
machine-readably on the element — because the agent contract calls for it and because a
declared scale is what makes a figure checkable. Today most scales live in HTML comments,
which are invisible on paper and inconsistent in form. That is a real documentation gap
and is tracked separately from this print contract.

## Verifying

Print-to-PDF from Chrome **and** Safari, with "background graphics" off, and check:

1. No figure, table, `.step` or `.spec` strip splits across a page.
2. No `h2.sec` sits alone at the foot of a page.
3. The cut-diagram legend swatches show their tints.
4. Margins match between the two browsers.

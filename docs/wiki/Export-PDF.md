# Export PDF

`Plik / File → Export PDF (model)...` (Ctrl+P) produces a printable A4
sheet with your wing's plan and results — a physical reference you can
take to the workshop.

## Print-friendly by design

The PDF uses a **light background, dark ink** palette, independent of
GhostMEAN's dark on-screen theme. This is deliberate: it's meant to be
an actual printed sheet, not a screenshot of the app, so it shouldn't
waste ink or be hard to read on paper.

## What's on the page

- **The wing plan** — the same top-down drawing you see on screen (both
  halves, panel numbering, the M.A.C. line, CG markers, a total-span
  dimension line), using the exact same geometry as the on-screen
  preview and [Station View](Station-View). There's no separate
  "PDF version" of the geometry that could drift from what you see on
  screen.
- **The results table** — Wing Span, Area, Aspect Ratio, M.A.C., MAC
  position (X and Y), and CG at 25%/28%/30%/your custom percentage.
- **The title and every label**, in whichever interface language was
  selected when you exported — switch languages before exporting if you
  want the PDF in a specific one.

## Scale

The wing drawing uses a fixed scale (calibrated against a ~2000mm-span
reference wing), not an auto-fit-to-page scale — so a small wing prints
visibly small, and a large wing is scaled down just enough to stay on
the page, rather than every wing looking the same size regardless of how
big it actually is.

## If a panel has a discontinuity

A [real geometry step](Panel-Geometry) (Major ≠ previous panel's Minor)
is drawn on the PDF exactly as it is on screen — a visible jump in the
trailing edge — since the PDF and the screen preview share the same
drawing code.

## No data / bad data

If no panel is enabled, the PDF still generates — with a "no panel data"
placeholder where the drawing would be, and an empty results section,
rather than failing to export at all.

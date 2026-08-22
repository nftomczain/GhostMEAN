# Quick Start

The fastest path from opening GhostMEAN to a finished plan.

```text
1. Open GhostMEAN
2. Choose units (mm or in — top left)
3. Enter panel Major / Minor / Length / Sweep
4. Set CG (25/28/30% are always shown; set your own % if you want a 4th)
5. Check Station View (click 📐 on any panel)
6. Export PDF / CSV
```

## A concrete example

Try this exact wing — it's the reference example used throughout
GhostMEAN's own test suite, so you can check your results against known
numbers.

```text
Panel 1: 250 → 200 / 300 mm / 20°
Panel 2: 200 → 140 / 250 mm / 10°
Panel 3: 140 → 80  / 200 mm / 5°
```

Type Panel 1's numbers in, then instead of retyping Panel 2 and 3 by
hand, click the **⧉** button on Panel 1 — it copies Panel 1's `Minor`
into Panel 2's `Major` automatically (keeping the wing continuous), then
you just fill in the rest. Repeat for Panel 3.

With this wing enabled, you should see:

| Result | Value |
|---|---|
| Wing Span | 1500.000 mm |
| Area | 0.2640 m² |
| Aspect Ratio | 8.523 |
| M.A.C. | 189.621 mm |
| CG 25% | 47.405 mm |

If your numbers match, everything's working correctly.

## What to do next

- Click **📐** on Panel 2 or 3 to see [Station View](Station-View) —
  the exact Y/LE/TE/Chord geometry of that specific panel.
- Toggle **☑ Dimensions on preview** to see per-panel length arrows and
  a summary list below the wing.
- `Plik / File → Export PDF (model)...` for a printable A4 sheet.
- `Plik / File → Export stations (CSV)...` for the fully-resolved
  geometry, ready to use when building.
- If you see an orange **⚠** warning appear, that's normal — see
  [Validation & Warnings](Validation). It never blocks the calculation.

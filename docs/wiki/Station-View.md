# Station View

This is arguably GhostMEAN's most useful feature for actually *building*
a wing, not just calculating its M.A.C.

## What a station is

The wing outline is made of **stations** — spanwise cross-sections at
the root, at every panel boundary, and at the tip:

```text
Root (Nasada)
S1
S2
...
Tip (Końcówka)
```

For every station, GhostMEAN knows exactly:

| | Meaning |
|---|---|
| **Y** | Spanwise position, measured from the symmetry axis. |
| **LE** | Leading-edge position at this station. |
| **TE** | Trailing-edge position at this station. |
| **Chord** | The local chord length (TE − LE) at this station. |

## Two ways to see it

**The Stations table** (below the preview) shows this for the whole
wing at once — one row per station.

**The 📐 button** on every panel row opens *that specific panel's* exact
geometry in its own window:

```text
Y START / Y END
LE START / LE END
TE START / TE END
CHORD START / CHORD END
SWEEP (LE)
```

These are the numbers you actually need when building the physical wing
from a computed plan — no more re-deriving them by hand from Major/Minor/
Length/Sweep.

If the panel is disabled, the button tells you so instead of showing
empty or misleading data.

## One source of truth

This is the important part: **Station View, the on-screen drawing, the
PDF, and the M.A.C. calculation are all built from exactly the same
geometry.** There's no separate "display" version and "calculation"
version that could quietly drift apart. If Station View says Panel 2
starts at Y=300mm with a 200mm chord, that's the same 200mm chord the
M.A.C. engine used and the same one drawn on screen and in the PDF.

This also means [a real discontinuity](Panel-Geometry) shows up
consistently everywhere — the Stations table will show two entries at
the same Y (the end of one panel and the start of the next, with
different chords), matching the visible step in the drawing.

## Exporting stations

`Plik / File → Export stations (CSV)...` writes the fully-resolved
station geometry to a CSV file — see [CSV Format](CSV-Format) for the
exact columns. This is a **separate, one-way export**, not a project
file: it's meant to be used for building, not loaded back into
GhostMEAN. It always uses canonical, ASCII-safe (Polish) station labels
regardless of your selected interface language, since it's a
data-interchange format, not a localized artifact.

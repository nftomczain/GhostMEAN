# GhostMEAN

<p align="center">
  <img src="ghostmean/assets/icon.png" alt="GhostMEAN logo" width="220">
</p>

<p align="center"><em>🇵🇱 <a href="README.pl.md">Polska wersja</a></em></p>

**Mean Aerodynamic Chord Calculator** — open source, Linux/Debian, no
account, no cloud, no subscription. Your wing, your geometry, your data —
nothing ever leaves your computer.

## Field & result reference (what is what)

### Wing panels

A wing is up to 5 sequential panels (from root to tip), each defined by
four numbers. The program draws **one half** and automatically mirrors it
to the other side — the wing is always assumed symmetric.

| Field | Meaning |
|---|---|
| `✓ / ✗ Panel N` | Enables/disables the panel. A disabled panel keeps its values (they are not cleared) but is excluded from the calculation — you can re-enable it without retyping the numbers. |
| `Major` | Root chord (larger) of this panel — the wing width where the panel starts (closer to the symmetry axis). |
| `Minor` | Tip chord (smaller) of this panel — the wing width where the panel ends (further from the symmetry axis). |
| `Length` | Span of THIS panel, measured along the spanwise axis (perpendicular to the symmetry axis), **one side only** — not the whole wing. |
| `Sweep (LE)` | Leading-edge sweep of this panel. **Definition is locked and verified by tests** (see below). |

**Sweep (LE) — exact definition:**
- Measured from the **global spanwise axis** (perpendicular to the
  fuselage's axis of symmetry), **absolutely and independently for each
  panel** — angles are NEVER accumulated across panels. Panel 3 with a
  10° sweep is always at 10° from the spanwise axis, regardless of what
  sweep panels 1 and 2 have.
- `0°` means the leading edge runs parallel to the spanwise axis.
- A positive/negative value offsets the leading edge sideways (toward the
  trailing edge / toward the nose).
- **The chord never rotates** — it always stays perpendicular to the
  global spanwise axis, parallel to the root chord. Sweep only offsets
  the leading edge; the trailing edge falls out automatically (LE + local
  chord at that station), so on a tapered panel its effective sweep will
  differ from the LE sweep — that's expected, not a bug.

### Units

The `mm` / `in` switch at the top converts ALL panel fields live (nothing
needs to be retyped). Internally everything is computed in mm — the
display unit is only a presentation layer.

### Results

| Result | Meaning |
|---|---|
| `WING SPAN` | Total span, both sides (sum of all enabled panel lengths × 2). |
| `AREA` | Total area, both sides. |
| `ASPECT RATIO` | span² / area. |
| `M.A.C.` | Mean Aerodynamic Chord — computed by integrating the true chord distribution over the whole span (not just the single-trapezoid formula), so multi-panel wings with different taper per panel are handled correctly. |
| `MAC POSITION` — `X` | Leading-edge position of the M.A.C., measured from the root leading edge (wing centerline). |
| `MAC POSITION` — `Y` | Spanwise position of the M.A.C., measured from the symmetry axis. |
| `CG 25% / 28% / 30%` | The three most commonly used balance points in model aviation. The value is the distance **from the leading edge, measured at the MAC station** (i.e. exactly what you'd measure with a ruler on the physical wing where the M.A.C. falls) — it is not a global coordinate. |
| `CG (CUSTOM %)` | The same, but for a percentage you set yourself in the `CG — custom %:` field at the top. The program does not suggest this value on its own — you decide which extra % level to see. |

### Preview (top-down view)

| Element | Appearance |
|---|---|
| Wing outline | Light blue lines — leading edge, trailing edge, root, tips, both sides. |
| Symmetry axis | Thin dash-dot vertical line at the center — a reminder that this is always one geometry, mirrored. |
| Panel numbers | Small digits `1`, `2`, ... near the leading edge of each panel, on both sides. |
| M.A.C. line | Orange dashed vertical line where the mean aerodynamic chord falls. |
| CG markers | Green crosses on the M.A.C. line, one per level (25% / 28% / 30% / custom). Percentage labels are deliberately stacked vertically with a thin leader line back to the exact marker — at typical values (25–30%) the points sit very close together, and without this the labels would overlap. |
| Span dimension | A horizontal line with end ticks below the wing, labeled with the total span in the currently selected unit. |

### File menu

| Action | Shortcut | What it does |
|---|---|---|
| `Load data (CSV)...` | Ctrl+O | Loads all 5 panels (including disabled ones), the unit, and `CG — custom %` from a CSV file. |
| `Save data (CSV)...` | Ctrl+S | Saves the same. Data in the file is always stored in mm (regardless of the display unit), so the file is portable; the display unit is also remembered and restored on load. |
| `Export PDF (model)...` | Ctrl+P | A printable A4 sheet (light background, dark ink) with the wing plan and the results table — the same geometry as on screen. |

The filename is remembered between a CSV save and a PDF export — after
saving `wing.csv`, the PDF export dialog will default to `wing.pdf`, so
project names stay consistent.

## Changelog

### v0.3.1

- Renamed the `CG (CUSTOM %)` result label from the earlier "own %"
  wording (and likewise in the PDF) — the old wording implied the user
  had supplied that exact point, when it's really just an extra,
  adjustable percentage level. The input field itself (`CG — custom %:`)
  was left unchanged, since that one genuinely is user-entered.

### v0.3.0

- **Sweep — definition explicitly locked** (confirmed and verified with
  geometric tests): the LEADING-EDGE (LE) sweep of a given panel,
  measured from the global spanwise axis, ABSOLUTELY and independently
  per panel (no accumulation relative to the previous panel). `0°` = LE
  parallel to the spanwise axis. The chord stays perpendicular to the
  global spanwise axis — sweep only offsets the LE sideways. Documented
  directly in `geometry.py` (module docstring) and in the "Sweep (LE)"
  field tooltip in the GUI.
- **CG instead of a single AC**: `% MAC for AC` replaced by
  `CG — custom %` plus three fixed results **CG 25% / CG 28% / CG 30%**
  and **CG (custom %)** — each shown as the distance from the leading
  edge measured at the MAC station (exactly what you'd measure with a
  ruler on the wing).
- **MAC POSITION** now shows both X and Y (X = leading-edge position of
  the MAC from the root) — useful for your own CG calculations.
- **Expanded preview**: symmetry axis (dashed center line), panel
  numbering (1, 2, ... on each panel, both sides), a total-span dimension
  line below the wing, and 4 CG markers (25/28/30/custom%) on the MAC
  line with clear, de-overlapped labels (leader lines connect each label
  to its exact marker so closely-spaced percentages don't run together).
- Geometry drawing is still 100% shared between the screen and the PDF
  (`drawing.py`), so the PDF export has the same elements (symmetry axis,
  panel numbers, dimension, CG markers) in printable form.

### v0.2.1

- Unambiguously defined `Sweep`: the LEADING-EDGE (LE) sweep of a given
  panel, measured from the spanwise axis, independently per panel (not
  relative to the previous panel); the chord does not rotate — sweep only
  offsets the LE sideways. UI label changed to `Sweep (LE):`, full
  explanation in the tooltip.
- `MAC POSITION` results now also show `X` (leading-edge position of the
  MAC from the root), not just `Y` — useful for CG calculations.

### v0.2.0

- **Save data (CSV)** / **Load data (CSV)** (File menu, Ctrl+S / Ctrl+O):
  saves all 5 panels (including disabled ones, so nothing gets lost),
  the %MAC for AC, and the unit. Data is stored canonically in mm
  regardless of the currently selected GUI unit, so the file is
  portable; the display unit is also remembered and restored. Verified
  with a full round-trip (save → reset the GUI → load → identical values
  and identical M.A.C. result).
- **Export PDF (model)** (File menu, Ctrl+P): a printable A4 sheet
  (light background, dark ink — independent of the app's dark on-screen
  theme) with the top-down wing plan (same geometry as the on-screen
  preview, shared `drawing.py` module) and a results table.
- The filename is remembered between a CSV save and a PDF export — after
  saving `wing.csv`, the PDF save dialog defaults to `wing.pdf`, so names
  stay consistent.

### v0.1.3

- The panel checkbox had an invisible native indicator on the dark
  theme — replaced with a clear text-based marker instead: `✓ Panel N`
  (blue, bold) when enabled, `✗ Panel N` (red, bold) when disabled; the
  native box is hidden (`QCheckBox::indicator { width: 0; height: 0; }`)
  so it doesn't duplicate the text marker.

### v0.1.2

- Fixed the misleading impression that panels 2–5 "don't work": the
  logic was correct (the checkbox did enable the fields), but disabled
  fields looked nearly identical to enabled ones, so typing without
  first checking the checkbox looked like nothing happened — added a
  clear `:disabled` style (dimmed background/text) plus a tooltip
  explaining to check the "Panel N" checkbox first.

### v0.1.1

- The wing preview now uses the full available panel height (previously
  it kept to a fixed minimum, leaving empty space).
- Label renamed to `Length` in the panel row.
- Results redesigned in a "Ghost" style: uppercase captions, monospace
  values, `MAC POSITION` (Y) and `AERODYNAMIC CENTER` (X, Y) on separate,
  readable lines.
- Verified against a real two-panel wing (different chords and sweep per
  panel) — MAC/MAC position/AC results match a manual recomputation of
  the formulas to 3–4 decimal places; the calculations (`geometry.py`)
  were left unchanged.

### v0.1.0 — first version

- Up to 5 wing panels (each: enable/disable, Major Chord, Minor Chord,
  Panel Length, Sweep +/−).
- mm or inch units (switchable live, values converted).
- Automatically computed:
  - Wing Span
  - Area
  - Aspect Ratio
  - M.A.C. (Mean Aerodynamic Chord) — computed by **integrating the true
    chord distribution**, not just the single-trapezoid formula, so
    multi-panel wings with different taper per panel are handled
    correctly.
  - MAC position (spanwise and chordwise)
  - Aerodynamic Center at a given %MAC (25% by default)
- Graphical top-down wing preview (both halves, MAC line, AC marker).

## Running it

```bash
pip install -e .
ghostmean-gui
```

or without installing:

```bash
pip install PySide6
python -m ghostmean
```

## Accessibility

The interface was designed from the start for one-handed operation and
low vision:
- large fonts, high contrast (dark theme, light-blue accents)
- every control is a spin box with keyboard support (arrows/scroll wheel)
  — no core function requires precise mouse dragging or pressing several
  keys at once
- accessibleName labels on key fields for screen readers
- large, readable result numbers

## Math (summary)

For a panel with root chord `Cr`, tip chord `Ct`, and length `L`:

```
panel_MAC = (2/3) * Cr * (1+λ+λ²)/(1+λ),   λ = Ct/Cr
```

For the whole (multi-panel) wing, `MAC` and its position are computed by
integrating `c(y)²` and `c(y)·y` over the span — see the comment in
`ghostmean/geometry.py`. Verified against a known reference example
(11"/6" → MAC≈8.745") and against the rectangular-wing case (MAC =
constant chord).

## Roadmap

- Left/right half symmetry — currently always symmetric (a deliberate
  decision, see the v0.3.0 changelog entry); separate left/right panels
  would be a bigger future rebuild.
- Importing geometry from DXF/SVG (deliberately deferred — a much harder
  problem than CSV save/load, requiring recognition of the symmetry axis
  and panel boundaries from an arbitrary drawing).
- Flatpak / AppImage packaging (as in GhostPoster).

## License

MIT.
# GhostMEAN

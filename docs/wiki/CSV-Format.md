# CSV Format

GhostMEAN uses **two separate CSV formats** for two different purposes.
Don't mix them up — one is a project file, the other is a one-way export.

## 1. Panel data (project file — load/save)

This is what `Plik / File → Save data (CSV)...` and `Load data (CSV)...`
use. You can write one by hand, too — here's a ready-to-copy block for
the [Quick Start](Quick-Start) example:

```csv
# ghostmean_csv v1; ac_percent=25.0; unit=mm
panel,enabled,major_mm,minor_mm,length_mm,sweep_deg
1,True,250,200,300,20
2,True,200,140,250,10
3,True,140,80,200,5
4,False,200,150,300,0
5,False,200,150,300,0
```

| Column | Meaning |
|---|---|
| `panel` | 1 to 5. |
| `enabled` | `True`/`False` — disabled panels are still saved (with their values), just excluded from the calculation. |
| `major_mm`, `minor_mm`, `length_mm` | Always in **millimetres**, regardless of which unit the GUI was displaying — this keeps the file portable. |
| `sweep_deg` | Degrees, per the [locked Sweep definition](Panel-Geometry). |

The first line is a metadata comment (`# ghostmean_csv v1; ...`) storing
the CG custom-% target and the display unit that was active when you
saved — both are restored automatically on load. If it's missing (e.g.
you wrote the file by hand), GhostMEAN falls back to `ac_percent=25.0`
and `unit=mm` rather than failing to load.

## 2. Station export (one-way, for building)

This is what `Plik / File → Export stations (CSV)...` produces — see
[Station View](Station-View) for what a station is. **This file is not
meant to be loaded back into GhostMEAN** — it's the fully-resolved
geometry, ready to hand off to a build log or a CNC/laser-cutting
workflow.

```csv
station,y_mm,le_x_mm,te_x_mm,chord_mm
Nasada,0.000000,0.000000,250.000000,250.000000
S1,300.000000,0.000000,200.000000,200.000000
S2,550.000000,0.000000,140.000000,140.000000
Koncowka,750.000000,0.000000,80.000000,80.000000
```

Station labels here are always canonical, ASCII-safe Polish
(`Nasada`/`Koncowka`/`S1`...) regardless of your interface language —
diacritics are stripped (`Końcówka` → `Koncowka`) so the file opens
cleanly in tools that assume plain ASCII.

## Test fixtures

GhostMEAN's own test suite (`tests/fixtures/`) ships three example files
you can look at directly:

| File | What it's for |
|---|---|
| `test.csv` | A clean, continuous 3-panel wing (the [Quick Start](Quick-Start) example) — used to lock in the exact MAC value (189.621mm) as a regression check. |
| `test2.csv` | A single panel in **inches**, with sweep — checks unit handling and metadata round-tripping. |
| `test_err.csv` | **Deliberately broken**: zero chords, an inverted taper (Minor > Major), a zero-length panel, and a real Major/Minor discontinuity between two panels. Used to confirm GhostMEAN warns about all of it but never crashes — see [Validation & Warnings](Validation). |

If you want to stress-test your own build the way GhostMEAN's own
development did, loading `test_err.csv` is a good place to start.

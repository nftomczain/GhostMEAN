# GhostMEAN

**GhostMEAN calculates wing geometry from panel dimensions and produces
station data, drawings, and PDF plans for RC model aircraft.**

Open source. No account, no cloud, no subscription. Your wing, your
geometry, your data — nothing ever leaves your computer.

![GhostMEAN logo](https://raw.githubusercontent.com/nftomczain/GhostMEAN/main/ghostmean/assets/icon.png)

## What it does

- Computes **M.A.C.** (Mean Aerodynamic Chord), wing **Area**, and
  **Aspect Ratio** for wings built from up to 5 straight-tapered panels
  per side (mirrored automatically).
- Computes **CG balance points** at 25%, 28%, 30% MAC, plus any custom
  percentage you choose.
- **[Station View](Station-View)** — the exact geometry (Y / LE / TE /
  Chord) at every panel boundary, for building the physical wing from a
  computed plan.
- Live top-down preview, with dimensions, panel numbering, and CG
  markers.
- **[CSV](CSV-Format)** save/load for your project, plus a separate CSV
  export of the fully-resolved station geometry.
- **PDF export** of a printable model sheet.
- Interface in 6 languages: Polish, English, Russian, Spanish, German,
  French.
- Runs as a portable **AppImage** on Linux — no install needed.

## Get started

- New here? Start with **[Quick Start](Quick-Start)**.
- Building your first wing? See **[Panel Geometry](Panel-Geometry)**.
- Something not working? See **[Troubleshooting](Troubleshooting)**.

## Download

Get the latest release from the
[Releases page](https://github.com/nftomczain/GhostMEAN/releases).
See **[Installation](Installation)** for AppImage / pip / running from
source.

## Pages in this wiki

| Page | What's on it |
|---|---|
| [Installation](Installation) | AppImage, pip install, running from source, running the tests |
| [Quick Start](Quick-Start) | The fastest path from opening GhostMEAN to a finished PDF |
| [Panel Geometry](Panel-Geometry) | Major / Minor / Length / Sweep, continuity, and what a real discontinuity means |
| [Station View](Station-View) | The single source of truth behind the drawing, the CSV export, and the PDF |
| [CSV Format](CSV-Format) | The panel-data CSV format, and the separate station-export format |
| [Validation & Warnings](Validation) | Every warning GhostMEAN can show you, and why none of them ever block a calculation |
| [Export PDF](Export-PDF) | What's in the printable model sheet |
| [Troubleshooting](Troubleshooting) | AppImage won't start, CSV rejected, PDF looks wrong, display glitches, Windows portable |

## License

MIT.

"""
Station-table CSV export for GhostMEAN.

This is a SEPARATE, read-only data format from io_csv.py's panel-parameter
CSV (major/minor/length/sweep). This one exports the fully-resolved
geometry -- one row per boundary station (root, each panel junction, tip)
with the exact Y/LE/TE/chord numbers, in millimetres, ready to use for
building the physical wing. There is no matching "load" function: this
format is a derived export, not a round-trippable project file.

File shape:

    station,y_mm,le_x_mm,te_x_mm,chord_mm
    Nasada,0.000000,0.000000,250.000000,250.000000
    S1,300.000000,0.000000,200.000000,200.000000
    Koncowka,750.000000,0.000000,80.000000,80.000000
"""

import csv
import unicodedata
from pathlib import Path

from ghostmean.geometry import Station

STATIONS_CSV_FIELDS = ["station", "y_mm", "le_x_mm", "te_x_mm", "chord_mm"]


def _ascii_label(label: str) -> str:
    """Station labels are Polish ('Nasada', 'Końcówka') for on-screen/PDF
    use; the CSV keeps them ASCII-only so the file opens cleanly in tools
    that assume plain ASCII column values."""
    normalized = unicodedata.normalize("NFKD", label)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def save_stations_csv(path, stations: list[Station]) -> None:
    path = Path(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=STATIONS_CSV_FIELDS)
        writer.writeheader()
        for s in stations:
            writer.writerow({
                "station": _ascii_label(s.label),
                "y_mm": f"{s.y_mm:.6f}",
                "le_x_mm": f"{s.le_x_mm:.6f}",
                "te_x_mm": f"{s.te_x_mm:.6f}",
                "chord_mm": f"{s.chord_mm:.6f}",
            })

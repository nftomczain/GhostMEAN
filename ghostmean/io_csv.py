"""
CSV save/load for GhostMEAN wing panel data.

Canonical storage unit is always millimetres, regardless of which unit the
GUI happened to be displaying at save time -- that display unit (plus the
AC target %MAC) is stored separately as a metadata comment line, so a
save/load round-trip reproduces the exact same displayed numbers too, not
just the same underlying geometry.

File shape:

    # ghostmean_csv v1; ac_percent=25.0; unit=mm
    panel,enabled,major_mm,minor_mm,length_mm,sweep_deg
    1,True,200.000000,150.000000,300.000000,0.000000
    2,False,200.000000,150.000000,300.000000,0.000000
    ...
"""

import csv
from dataclasses import dataclass
from pathlib import Path

CSV_FIELDS = ["panel", "enabled", "major_mm", "minor_mm", "length_mm", "sweep_deg"]


@dataclass
class PanelRowData:
    enabled: bool
    major_mm: float
    minor_mm: float
    length_mm: float
    sweep_deg: float


@dataclass
class WingData:
    panels: list  # list[PanelRowData]
    ac_percent: float = 25.0
    unit: str = "mm"


def save_panels_csv(path, data: WingData) -> None:
    path = Path(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        f.write(f"# ghostmean_csv v1; ac_percent={data.ac_percent}; unit={data.unit}\n")
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for i, p in enumerate(data.panels, start=1):
            writer.writerow({
                "panel": i,
                "enabled": p.enabled,
                "major_mm": f"{p.major_mm:.6f}",
                "minor_mm": f"{p.minor_mm:.6f}",
                "length_mm": f"{p.length_mm:.6f}",
                "sweep_deg": f"{p.sweep_deg:.6f}",
            })


def load_panels_csv(path) -> WingData:
    path = Path(path)
    ac_percent = 25.0
    unit = "mm"
    with path.open("r", newline="", encoding="utf-8") as f:
        first_line = f.readline()
        if first_line.startswith("#"):
            for part in first_line.lstrip("#").split(";"):
                part = part.strip()
                if part.startswith("ac_percent="):
                    ac_percent = float(part.split("=", 1)[1])
                elif part.startswith("unit="):
                    unit = part.split("=", 1)[1].strip()
            rest = f.read()
        else:
            rest = first_line + f.read()

    reader = csv.DictReader(rest.splitlines())
    panels = []
    for row in reader:
        panels.append(PanelRowData(
            enabled=str(row["enabled"]).strip().lower() in ("1", "true", "yes"),
            major_mm=float(row["major_mm"]),
            minor_mm=float(row["minor_mm"]),
            length_mm=float(row["length_mm"]),
            sweep_deg=float(row["sweep_deg"]),
        ))
    if not panels:
        raise ValueError("Plik CSV nie zawiera żadnych wierszy paneli")
    return WingData(panels=panels, ac_percent=ac_percent, unit=unit)

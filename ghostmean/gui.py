"""
GhostMEAN GUI — Mean Aerodynamic Chord Calculator.

Design notes (accessibility-first, deliberately):
  - Large fonts, high-contrast dark theme, generous click targets.
  - Every control reachable and usable via keyboard alone (Tab / arrows /
    spin buttons) -- nothing here requires a simultaneous two-key chord or
    a precise mouse drag to operate the core workflow.
  - Spin boxes instead of free-drag sliders for every numeric input.
  - Output numbers are shown large and also announced via accessibleName
    for screen readers.
"""

import sys
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QDoubleSpinBox, QComboBox, QGroupBox, QCheckBox, QFrame,
    QScrollArea, QSizePolicy, QFileDialog, QMessageBox,
)

from ghostmean.geometry import WingPanel, compute_wing_metrics, cg_from_percent_mac
from ghostmean.units import to_mm, from_mm
from ghostmean.drawing import draw_wing_plan
from ghostmean.io_csv import save_panels_csv, load_panels_csv, WingData, PanelRowData
from ghostmean.export_pdf import export_wing_pdf

MAX_PANELS = 5

ICON_PATH = str(Path(__file__).parent / "assets" / "icon.png")

DARK_QSS = """
QWidget { background-color: #0b0f14; color: #e6f1fb; font-size: 13pt; }
QGroupBox {
    border: 2px solid #1c7fd6; border-radius: 8px; margin-top: 14px;
    font-weight: bold; color: #4fb3ff;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; }
QDoubleSpinBox, QComboBox {
    background-color: #14202b; border: 1px solid #2c6b9c; border-radius: 4px;
    padding: 4px; min-height: 30px; min-width: 90px; font-size: 13pt;
}
QDoubleSpinBox:focus, QComboBox:focus { border: 2px solid #4fc3ff; }
QDoubleSpinBox:disabled, QComboBox:disabled {
    background-color: #0c1116; border: 1px solid #1a2733; color: #3d5468;
}
QLabel#outputValue {
    font-size: 15pt; font-weight: bold; color: #4fc3ff;
    font-family: "DejaVu Sans Mono", "Consolas", monospace;
}
QLabel#outputCaption {
    font-size: 10pt; font-weight: bold; color: #6fa8c9;
}
QCheckBox { spacing: 8px; }
QCheckBox::indicator { width: 0px; height: 0px; }
"""


class WingPreview(QFrame):
    """Top-down (planform) preview of the wing, mirrored both sides, with
    the symmetry axis, panel numbers, MAC chord, CG markers (25/28/30% +
    custom), and a total-span dimension line."""

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(260)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAccessibleName("Podgląd skrzydła (widok z góry)")
        self.panels: list[WingPanel] = []
        self.metrics = None
        self.cg_targets = []
        self.unit = "mm"

    def update_data(self, panels, metrics, cg_targets, unit):
        self.panels = panels
        self.metrics = metrics
        self.cg_targets = cg_targets
        self.unit = unit
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0b0f14"))

        if not self.panels or self.metrics is None or self.metrics.span_mm <= 0:
            painter.setPen(QColor("#5c7a92"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Brak danych panelu")
            painter.end()
            return

        pen_outline = QPen(QColor("#4fc3ff"), 2)
        pen_mac = QPen(QColor("#ffb300"), 2, Qt.DashLine)
        pen_cg = QPen(QColor("#5cff8a"), 2)
        pen_axis = QPen(QColor("#3d5468"), 1, Qt.DashDotLine)
        pen_dim = QPen(QColor("#9fb8cc"), 1)
        label_font = QFont("Sans Serif", 8)
        draw_wing_plan(
            painter, self.width(), self.height(),
            self.panels, self.metrics, self.cg_targets,
            pen_outline, pen_mac, pen_cg, pen_axis, pen_dim,
            unit=self.unit, label_font=label_font,
        )
        painter.end()


SWEEP_TOOLTIP = (
    "Skos KRAWĘDZI NATARCIA (Leading Edge) tego panelu.\n"
    "Mierzony względem osi rozpiętości (prostopadłej do osi symetrii),\n"
    "NIEZALEŻNIE dla każdego panelu — NIE względem poprzedniego panelu.\n"
    "Cięciwa nie obraca się wraz ze skosem — zostaje równoległa do\n"
    "cięciwy nasadowej; skos przesuwa w bok tylko krawędź natarcia."
)


class PanelRow(QWidget):
    changed = Signal()

    def __init__(self, index: int):
        super().__init__()
        self.index = index
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.enabled = QCheckBox()
        self.enabled.setChecked(index == 0)
        self.enabled.setAccessibleName(f"Włącz panel {index + 1}")
        self._update_checkbox_label(self.enabled.isChecked())
        self.enabled.toggled.connect(self._update_checkbox_label)

        self.major = QDoubleSpinBox()
        self.minor = QDoubleSpinBox()
        self.length = QDoubleSpinBox()
        self.sweep = QDoubleSpinBox()

        for box, name, rng in (
            (self.major, "Cięciwa większa", (0, 10000)),
            (self.minor, "Cięciwa mniejsza", (0, 10000)),
            (self.length, "Długość panelu", (0.01, 10000)),
            (self.sweep, "Skos krawędzi natarcia (LE), względem osi rozpiętości", (-89, 89)),
        ):
            box.setRange(*rng)
            box.setDecimals(2)
            box.setAccessibleName(f"{name}, panel {index + 1}")
            box.valueChanged.connect(lambda _v: self.changed.emit())

        self.major.setValue(200.0)
        self.minor.setValue(150.0)
        self.length.setValue(300.0)
        self.sweep.setValue(0.0)
        self.sweep.setSuffix("°")

        self.enabled.toggled.connect(lambda _v: self.changed.emit())
        self.enabled.toggled.connect(self._sync_enabled_state)

        layout.addWidget(self.enabled, 2)
        layout.addWidget(QLabel("Major:"))
        layout.addWidget(self.major)
        layout.addWidget(QLabel("Minor:"))
        layout.addWidget(self.minor)
        layout.addWidget(QLabel("Długość:"))
        layout.addWidget(self.length)
        layout.addWidget(QLabel("Skos (LE):"))
        layout.addWidget(self.sweep)

        self._sync_enabled_state(self.enabled.isChecked())

    def _update_checkbox_label(self, on: bool):
        mark = "✓" if on else "✗"
        self.enabled.setText(f"{mark}  Panel {self.index + 1}")
        color = "#4fc3ff" if on else "#ff5c5c"
        self.enabled.setStyleSheet(f"QCheckBox {{ color: {color}; font-weight: bold; }}")

    def _sync_enabled_state(self, on: bool):
        for w in (self.major, self.minor, self.length, self.sweep):
            w.setEnabled(on)
        disabled_hint = "" if on else "\n\nZaznacz checkbox „Panel N”, aby edytować ten panel"
        generic_tip = "" if on else disabled_hint.strip()
        for w in (self.major, self.minor, self.length):
            w.setToolTip(generic_tip)
        self.sweep.setToolTip(SWEEP_TOOLTIP + disabled_hint)

    def to_panel_mm(self, unit: str) -> WingPanel | None:
        if not self.enabled.isChecked():
            return None
        return WingPanel(
            major_chord_mm=to_mm(self.major.value(), unit),
            minor_chord_mm=to_mm(self.minor.value(), unit),
            length_mm=to_mm(self.length.value(), unit),
            sweep_deg=self.sweep.value(),
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostMEAN — Mean Aerodynamic Chord Calculator")
        self.resize(1060, 780)
        if Path(ICON_PATH).exists():
            self.setWindowIcon(QIcon(ICON_PATH))

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        self._last_basename: str | None = None
        self._build_menu()

        # --- unit selector ---
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Jednostki:"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["mm", "in"])
        self.unit_combo.setAccessibleName("Wybór jednostek")
        self.unit_combo.currentTextChanged.connect(self._on_unit_changed)
        top_bar.addWidget(self.unit_combo)
        top_bar.addWidget(QLabel("CG — własny %:"))
        self.custom_cg_percent = QDoubleSpinBox()
        self.custom_cg_percent.setRange(0, 100)
        self.custom_cg_percent.setValue(25.0)
        self.custom_cg_percent.setSuffix(" %")
        self.custom_cg_percent.setAccessibleName("Własny docelowy procent MAC dla CG")
        self.custom_cg_percent.valueChanged.connect(self.recompute)
        top_bar.addWidget(self.custom_cg_percent)
        top_bar.addStretch()
        root.addLayout(top_bar)

        # --- panel table ---
        panels_box = QGroupBox("Panele skrzydła (do 5)")
        panels_layout = QVBoxLayout(panels_box)
        self._current_unit = "mm"
        self.rows: list[PanelRow] = []
        for i in range(MAX_PANELS):
            row = PanelRow(i)
            row.changed.connect(self.recompute)
            panels_layout.addWidget(row)
            self.rows.append(row)
        root.addWidget(panels_box)

        # --- outputs + preview ---
        mid = QHBoxLayout()

        outputs_box = QGroupBox("Wyniki")
        grid = QGridLayout(outputs_box)
        self.output_labels = {}
        fields = [
            ("span", "ROZPIĘTOŚĆ (WING SPAN)", "Rozpiętość (Wing Span)"),
            ("area", "POWIERZCHNIA (AREA)", "Powierzchnia (Area)"),
            ("ar", "WYDŁUŻENIE (ASPECT RATIO)", "Wydłużenie (Aspect Ratio)"),
            ("mac", "M.A.C.", "M.A.C."),
            ("mac_pos", "MAC POSITION", "Pozycja M.A.C. — X od krawędzi natarcia nasady, Y od osi symetrii"),
            ("cg25", "CG 25%", "CG przy 25% MAC, odległość od krawędzi natarcia na stacji MAC"),
            ("cg28", "CG 28%", "CG przy 28% MAC, odległość od krawędzi natarcia na stacji MAC"),
            ("cg30", "CG 30%", "CG przy 30% MAC, odległość od krawędzi natarcia na stacji MAC"),
            ("cg_custom", "CG (NIESTANDARDOWY %)", "CG przy niestandardowym (dowolnie ustawionym) procencie MAC"),
        ]
        for r, (key, caption, accessible_caption) in enumerate(fields):
            cap = QLabel(caption)
            cap.setObjectName("outputCaption")
            val = QLabel("—")
            val.setObjectName("outputValue")
            val.setAccessibleName(accessible_caption)
            grid.addWidget(cap, r, 0)
            grid.addWidget(val, r, 1)
            self.output_labels[key] = val
        mid.addWidget(outputs_box, 1)

        self.preview = WingPreview()
        preview_box = QGroupBox("Podgląd (widok z góry)")
        preview_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pv_layout = QVBoxLayout(preview_box)
        pv_layout.addWidget(self.preview)
        mid.addWidget(preview_box, 2)

        root.addLayout(mid, 1)

        self.recompute()

    def _build_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")

        load_action = file_menu.addAction("Wczytaj dane (CSV)...")
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._on_load_csv)

        save_action = file_menu.addAction("Zapisz dane (CSV)...")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._on_save_csv)

        file_menu.addSeparator()

        export_action = file_menu.addAction("Eksportuj PDF (model)...")
        export_action.setShortcut("Ctrl+P")
        export_action.triggered.connect(self._on_export_pdf)

    def _gather_wing_data(self) -> WingData:
        unit = self.unit_combo.currentText()
        panels_data = [
            PanelRowData(
                enabled=row.enabled.isChecked(),
                major_mm=to_mm(row.major.value(), unit),
                minor_mm=to_mm(row.minor.value(), unit),
                length_mm=to_mm(row.length.value(), unit),
                sweep_deg=row.sweep.value(),
            )
            for row in self.rows
        ]
        return WingData(panels=panels_data, ac_percent=self.custom_cg_percent.value(), unit=unit)

    def _apply_wing_data(self, data: WingData):
        idx = self.unit_combo.findText(data.unit)
        if idx >= 0:
            self.unit_combo.blockSignals(True)
            self.unit_combo.setCurrentIndex(idx)
            self.unit_combo.blockSignals(False)
            self._current_unit = data.unit

        for row, p in zip(self.rows, data.panels):
            row.enabled.blockSignals(True)
            row.enabled.setChecked(p.enabled)
            row.enabled.blockSignals(False)
            row._update_checkbox_label(p.enabled)
            row._sync_enabled_state(p.enabled)
            for box, mm_val in (
                (row.major, p.major_mm),
                (row.minor, p.minor_mm),
                (row.length, p.length_mm),
            ):
                box.blockSignals(True)
                box.setValue(from_mm(mm_val, data.unit))
                box.blockSignals(False)
            row.sweep.blockSignals(True)
            row.sweep.setValue(p.sweep_deg)
            row.sweep.blockSignals(False)

        self.custom_cg_percent.blockSignals(True)
        self.custom_cg_percent.setValue(data.ac_percent)
        self.custom_cg_percent.blockSignals(False)

        self.recompute()

    def _on_save_csv(self):
        default_name = f"{self._last_basename or 'skrzydlo'}.csv"
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz dane (CSV)", default_name, "CSV (*.csv)")
        if not path:
            return
        if not path.lower().endswith(".csv"):
            path += ".csv"
        try:
            save_panels_csv(path, self._gather_wing_data())
        except OSError as e:
            QMessageBox.critical(self, "Błąd zapisu", str(e))
            return
        self._last_basename = Path(path).stem
        self.statusBar().showMessage(f"Zapisano: {path}", 4000)

    def _on_load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wczytaj dane (CSV)", "", "CSV (*.csv)")
        if not path:
            return
        try:
            data = load_panels_csv(path)
        except (OSError, ValueError, KeyError) as e:
            QMessageBox.critical(self, "Błąd wczytywania", str(e))
            return
        self._apply_wing_data(data)
        self._last_basename = Path(path).stem
        self.statusBar().showMessage(f"Wczytano: {path}", 4000)

    def _on_export_pdf(self):
        default_name = f"{self._last_basename or 'skrzydlo'}.pdf"
        path, _ = QFileDialog.getSaveFileName(self, "Eksportuj PDF (model)", default_name, "PDF (*.pdf)")
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        unit = self.unit_combo.currentText()
        panels = [row.to_panel_mm(unit) for row in self.rows]
        panels = [p for p in panels if p is not None]
        metrics = compute_wing_metrics(panels)
        try:
            export_wing_pdf(path, panels, metrics, self.custom_cg_percent.value(), unit)
        except OSError as e:
            QMessageBox.critical(self, "Błąd eksportu", str(e))
            return
        self._last_basename = Path(path).stem
        self.statusBar().showMessage(f"Wyeksportowano: {path}", 4000)

    def _on_unit_changed(self, new_unit: str):
        old_unit = self._current_unit
        if new_unit == old_unit:
            return
        for row in self.rows:
            for box in (row.major, row.minor, row.length):
                mm_val = to_mm(box.value(), old_unit)
                box.blockSignals(True)
                box.setValue(from_mm(mm_val, new_unit))
                box.blockSignals(False)
        self._current_unit = new_unit
        self.recompute()

    def _cg_targets(self, verbose=False):
        c = self.custom_cg_percent.value()
        if verbose:
            return [("25% MAC", 25.0), ("28% MAC", 28.0), ("30% MAC", 30.0), (f"{c:.0f}% MAC", c)]
        return [("25%", 25.0), ("28%", 28.0), ("30%", 30.0), (f"{c:.0f}%", c)]

    def recompute(self):
        unit = self.unit_combo.currentText()
        panels = [row.to_panel_mm(unit) for row in self.rows]
        panels = [p for p in panels if p is not None]
        metrics = compute_wing_metrics(panels)

        def fmt(v_mm):
            return f"{from_mm(v_mm, unit):.3f} {unit}"

        if panels and metrics.area_mm2 > 0:
            self.output_labels["span"].setText(fmt(metrics.span_mm))
            if unit == "mm":
                area_val = metrics.area_mm2 / 1_000_000.0
                self.output_labels["area"].setText(f"{area_val:.4f} m²")
            else:
                area_val = metrics.area_mm2 / (25.4 * 25.4)
                self.output_labels["area"].setText(f"{area_val:.2f} in²")
            self.output_labels["ar"].setText(f"{metrics.aspect_ratio:.3f}")
            self.output_labels["mac"].setText(fmt(metrics.mac_mm))
            self.output_labels["mac_pos"].setText(f"X = {fmt(metrics.mac_le_x_mm)}\nY = {fmt(metrics.mac_y_mm)}")
            self.output_labels["cg25"].setText(fmt(cg_from_percent_mac(metrics, 25.0)))
            self.output_labels["cg28"].setText(fmt(cg_from_percent_mac(metrics, 28.0)))
            self.output_labels["cg30"].setText(fmt(cg_from_percent_mac(metrics, 30.0)))
            self.output_labels["cg_custom"].setText(
                fmt(cg_from_percent_mac(metrics, self.custom_cg_percent.value()))
            )
        else:
            for lbl in self.output_labels.values():
                lbl.setText("—")

        self.preview.update_data(panels, metrics, self._cg_targets(), unit)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_QSS)
    app.setFont(QFont("Sans Serif", 11))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

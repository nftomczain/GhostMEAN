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
    QScrollArea, QSizePolicy, QFileDialog, QMessageBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
)

from ghostmean.geometry import (
    WingPanel, compute_wing_metrics, cg_from_percent_mac,
    compute_stations, compute_panel_stations,
)
from ghostmean.units import to_mm, from_mm
from ghostmean.drawing import draw_wing_plan
from ghostmean.io_csv import save_panels_csv, load_panels_csv, WingData, PanelRowData
from ghostmean.export_pdf import export_wing_pdf
from ghostmean.io_stations import save_stations_csv
from ghostmean.i18n import tr, set_language, get_language, available_languages

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
QPushButton {
    background-color: #14202b; border: 1px solid #2c6b9c; border-radius: 4px;
    padding: 4px; min-height: 30px; font-size: 13pt; color: #4fc3ff;
}
QPushButton:hover { border: 1px solid #4fc3ff; }
QPushButton:pressed { background-color: #1c3040; }
QPushButton:disabled { color: #3d5468; border: 1px solid #1a2733; }
QLabel#warningBox {
    color: #ffb300; font-size: 10.5pt; padding: 4px;
}
QTableWidget {
    background-color: #0e1620; border: 1px solid #2c6b9c; border-radius: 4px;
    font-size: 10.5pt; gridline-color: #1c2e3d;
}
QHeaderView::section {
    background-color: #14202b; color: #6fa8c9; font-weight: bold;
    border: none; border-bottom: 1px solid #2c6b9c; padding: 4px;
}
QTableWidget::item { padding: 3px; }
QScrollBar:vertical {
    background: #0b0f14; width: 14px; margin: 0;
}
QScrollBar::handle:vertical {
    background: #2c6b9c; min-height: 24px; border-radius: 6px;
}
QScrollBar::handle:vertical:hover { background: #4fc3ff; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #0b0f14; height: 14px; margin: 0;
}
QScrollBar::handle:horizontal {
    background: #2c6b9c; min-width: 24px; border-radius: 6px;
}
QScrollBar::handle:horizontal:hover { background: #4fc3ff; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
"""


class WingPreview(QFrame):
    """Top-down (planform) preview of the wing, mirrored both sides, with
    the symmetry axis, panel numbers, MAC chord, CG markers (25/28/30% +
    custom), and a total-span dimension line."""

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(260)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAccessibleName(tr("preview_accessible"))
        self.panels: list[WingPanel] = []
        self.metrics = None
        self.cg_targets = []
        self.unit = "mm"
        self.show_panel_details = False

    def update_data(self, panels, metrics, cg_targets, unit, show_panel_details=False):
        self.panels = panels
        self.metrics = metrics
        self.cg_targets = cg_targets
        self.unit = unit
        self.show_panel_details = show_panel_details
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0b0f14"))

        if not self.panels or self.metrics is None or self.metrics.span_mm <= 0:
            painter.setPen(QColor("#5c7a92"))
            painter.drawText(self.rect(), Qt.AlignCenter, tr("preview_no_data"))
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
            show_panel_details=self.show_panel_details,
        )
        painter.end()


def style_toggle_checkbox(checkbox: QCheckBox, base_label: str, on: bool):
    """Every QCheckBox in the app has its native indicator hidden via QSS
    (invisible on the dark theme otherwise, see v0.1.3), so EVERY checkbox
    must compensate with this text-based ✓/✗ marker instead — otherwise it
    has no visible state at all (still clickable, just impossible to read).
    Use this for any new checkbox added to the app, not just panel rows."""
    mark = "✓" if on else "✗"
    checkbox.setText(f"{mark}  {base_label}")
    color = "#4fc3ff" if on else "#ff5c5c"
    checkbox.setStyleSheet(f"QCheckBox {{ color: {color}; font-weight: bold; }}")


class PanelRow(QWidget):
    changed = Signal()
    copy_to_next = Signal(int)
    show_stations = Signal(int)

    def __init__(self, index: int):
        super().__init__()
        self.index = index
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.enabled = QCheckBox()
        self.enabled.setChecked(index == 0)
        self.enabled.setAccessibleName(tr("panel_enable_accessible", n=index + 1))
        self._update_checkbox_label(self.enabled.isChecked())
        self.enabled.toggled.connect(self._update_checkbox_label)

        self.major = QDoubleSpinBox()
        self.minor = QDoubleSpinBox()
        self.length = QDoubleSpinBox()
        self.sweep = QDoubleSpinBox()

        for box, name_key, rng in (
            (self.major, "panel_major_name", (0, 10000)),
            (self.minor, "panel_minor_name", (0, 10000)),
            (self.length, "panel_length_name", (0, 10000)),
            (self.sweep, "panel_sweep_name", (-89, 89)),
        ):
            box.setRange(*rng)
            box.setDecimals(2)
            box.setAccessibleName(f"{tr(name_key)}, panel {index + 1}")
            box.valueChanged.connect(lambda _v: self.changed.emit())

        self.major.setValue(200.0)
        self.minor.setValue(150.0)
        self.length.setValue(300.0)
        self.sweep.setValue(0.0)
        self.sweep.setSuffix("°")

        self.enabled.toggled.connect(lambda _v: self.changed.emit())
        self.enabled.toggled.connect(self._sync_enabled_state)

        self.major_label = QLabel(tr("panel_major_label"))
        self.minor_label = QLabel(tr("panel_minor_label"))
        self.length_label = QLabel(tr("panel_length_label"))
        self.sweep_label = QLabel(tr("panel_sweep_label"))
        layout.addWidget(self.enabled, 2)
        layout.addWidget(self.major_label)
        layout.addWidget(self.major)
        layout.addWidget(self.minor_label)
        layout.addWidget(self.minor)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length)
        layout.addWidget(self.sweep_label)
        layout.addWidget(self.sweep)

        self.copy_btn = QPushButton("⧉")
        self.copy_btn.setFixedWidth(32)
        self.copy_btn.setToolTip(tr("panel_copy_tooltip", a=index + 1, b=index + 2))
        self.copy_btn.setAccessibleName(tr("panel_copy_accessible", a=index + 1, b=index + 2))
        self.copy_btn.clicked.connect(lambda: self.copy_to_next.emit(self.index))
        if index >= MAX_PANELS - 1:
            self.copy_btn.setEnabled(False)
            self.copy_btn.setToolTip(tr("panel_copy_no_next_tooltip"))
        layout.addWidget(self.copy_btn)

        self.stations_btn = QPushButton("📐")
        self.stations_btn.setFixedWidth(32)
        self.stations_btn.setToolTip(tr("panel_stations_tooltip", n=index + 1))
        self.stations_btn.setAccessibleName(tr("panel_stations_accessible", n=index + 1))
        self.stations_btn.clicked.connect(lambda: self.show_stations.emit(self.index))
        layout.addWidget(self.stations_btn)

        self._sync_enabled_state(self.enabled.isChecked())

    def retranslate(self):
        """Refresh this row's static text after a language change."""
        self._update_checkbox_label(self.enabled.isChecked())
        self.major_label.setText(tr("panel_major_label"))
        self.minor_label.setText(tr("panel_minor_label"))
        self.length_label.setText(tr("panel_length_label"))
        self.sweep_label.setText(tr("panel_sweep_label"))
        self.copy_btn.setToolTip(
            tr("panel_copy_no_next_tooltip") if self.index >= MAX_PANELS - 1
            else tr("panel_copy_tooltip", a=self.index + 1, b=self.index + 2)
        )
        self.stations_btn.setToolTip(tr("panel_stations_tooltip", n=self.index + 1))
        self._sync_enabled_state(self.enabled.isChecked())

    def _update_checkbox_label(self, on: bool):
        style_toggle_checkbox(self.enabled, tr("panel_label", n=self.index + 1), on)

    def _sync_enabled_state(self, on: bool):
        for w in (self.major, self.minor, self.length, self.sweep):
            w.setEnabled(on)
        disabled_hint = "" if on else tr("panel_disabled_hint")
        generic_tip = "" if on else disabled_hint.strip()
        for w in (self.major, self.minor, self.length):
            w.setToolTip(generic_tip)
        self.sweep.setToolTip(tr("sweep_tooltip") + disabled_hint)

    def to_panel_mm(self, unit: str) -> WingPanel | None:
        if not self.enabled.isChecked():
            return None
        return WingPanel(
            major_chord_mm=to_mm(self.major.value(), unit),
            minor_chord_mm=to_mm(self.minor.value(), unit),
            length_mm=to_mm(self.length.value(), unit),
            sweep_deg=self.sweep.value(),
        )

    def get_warnings(self) -> list[str]:
        """Non-blocking validation warnings for this panel, only checked
        while the panel is enabled (a disabled panel's values don't affect
        the model, so they're not worth flagging)."""
        if not self.enabled.isChecked():
            return []
        n = self.index + 1
        warnings = []
        if self.major.value() <= 0:
            warnings.append(tr("warn_major_le_zero", n=n))
        if self.minor.value() <= 0:
            warnings.append(tr("warn_minor_le_zero", n=n))
        if self.length.value() <= 0:
            warnings.append(tr("warn_length_le_zero", n=n))
        if self.minor.value() > self.major.value() > 0:
            warnings.append(tr("warn_minor_gt_major", n=n))
        if abs(self.sweep.value()) > 60:
            warnings.append(tr("warn_large_sweep", n=n, v=self.sweep.value()))
        return warnings

    def reset_default(self, enabled: bool):
        self.enabled.blockSignals(True)
        self.enabled.setChecked(enabled)
        self.enabled.blockSignals(False)
        self._update_checkbox_label(enabled)
        self._sync_enabled_state(enabled)
        for box, val in ((self.major, 200.0), (self.minor, 150.0), (self.length, 300.0), (self.sweep, 0.0)):
            box.blockSignals(True)
            box.setValue(val)
            box.blockSignals(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("window_title"))
        self.resize(1060, 820)
        if Path(ICON_PATH).exists():
            self.setWindowIcon(QIcon(ICON_PATH))

        # Wrapped in a scroll area so the full UI stays reachable on lower
        # resolutions / smaller windows instead of being clipped.
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll)

        central = QWidget()
        scroll.setWidget(central)
        root = QVBoxLayout(central)

        self._last_basename: str | None = None
        self._last_dir: str = ""
        self._build_menu()

        # --- unit selector ---
        top_bar = QHBoxLayout()
        self.units_label = QLabel(tr("topbar_units"))
        top_bar.addWidget(self.units_label)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["mm", "in"])
        self.unit_combo.setAccessibleName(tr("topbar_units_accessible"))
        self.unit_combo.currentTextChanged.connect(self._on_unit_changed)
        top_bar.addWidget(self.unit_combo)
        self.cg_custom_label = QLabel(tr("topbar_cg_custom"))
        top_bar.addWidget(self.cg_custom_label)
        self.custom_cg_percent = QDoubleSpinBox()
        self.custom_cg_percent.setRange(0, 100)
        self.custom_cg_percent.setValue(25.0)
        self.custom_cg_percent.setSuffix(" %")
        self.custom_cg_percent.setAccessibleName(tr("topbar_cg_custom_accessible"))
        self.custom_cg_percent.valueChanged.connect(self.recompute)
        top_bar.addWidget(self.custom_cg_percent)
        self.show_dims_checkbox = QCheckBox()
        self.show_dims_checkbox.setAccessibleName(tr("topbar_show_dims_accessible"))
        style_toggle_checkbox(self.show_dims_checkbox, tr("topbar_show_dims"), False)
        self.show_dims_checkbox.toggled.connect(
            lambda on: style_toggle_checkbox(self.show_dims_checkbox, tr("topbar_show_dims"), on)
        )
        self.show_dims_checkbox.toggled.connect(self.recompute)
        top_bar.addWidget(self.show_dims_checkbox)
        top_bar.addStretch()
        self.language_label = QLabel(tr("topbar_language"))
        top_bar.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.addItems(available_languages())
        self.language_combo.setCurrentText(get_language())
        self.language_combo.setAccessibleName(tr("topbar_language_accessible"))
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        top_bar.addWidget(self.language_combo)
        root.addLayout(top_bar)

        # --- panel table ---
        self.panels_box = QGroupBox(tr("panels_box_title"))
        panels_layout = QVBoxLayout(self.panels_box)
        self._current_unit = "mm"
        self.rows: list[PanelRow] = []
        for i in range(MAX_PANELS):
            row = PanelRow(i)
            row.changed.connect(self.recompute)
            row.copy_to_next.connect(self._on_copy_to_next)
            row.show_stations.connect(self._on_show_stations)
            panels_layout.addWidget(row)
            self.rows.append(row)
        root.addWidget(self.panels_box)

        # --- validation warnings ---
        self.warnings_label = QLabel("")
        self.warnings_label.setObjectName("warningBox")
        self.warnings_label.setWordWrap(True)
        self.warnings_label.hide()
        root.addWidget(self.warnings_label)

        # --- outputs + preview ---
        mid = QHBoxLayout()

        self.outputs_box = QGroupBox(tr("results_title"))
        grid = QGridLayout(self.outputs_box)
        self.output_labels = {}
        self.output_captions = {}
        fields = [
            ("span", "results_span", "results_span_accessible"),
            ("area", "results_area", "results_area_accessible"),
            ("ar", "results_ar", "results_ar_accessible"),
            ("mac", "results_mac", "results_mac"),
            ("mac_pos", "results_mac_pos", "results_mac_pos_accessible"),
            ("cg25", "results_cg25", "results_cg25_accessible"),
            ("cg28", "results_cg28", "results_cg28_accessible"),
            ("cg30", "results_cg30", "results_cg30_accessible"),
            ("cg_custom", "results_cg_custom", "results_cg_custom_accessible"),
        ]
        for r, (key, caption_key, accessible_key) in enumerate(fields):
            cap = QLabel(tr(caption_key))
            cap.setObjectName("outputCaption")
            val = QLabel("—")
            val.setObjectName("outputValue")
            val.setAccessibleName(tr(accessible_key))
            grid.addWidget(cap, r, 0)
            grid.addWidget(val, r, 1)
            self.output_labels[key] = val
            self.output_captions[key] = (cap, caption_key, accessible_key)
        mid.addWidget(self.outputs_box, 1)

        self.preview = WingPreview()
        self.preview_box = QGroupBox(tr("preview_title"))
        self.preview_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pv_layout = QVBoxLayout(self.preview_box)
        pv_layout.addWidget(self.preview)
        mid.addWidget(self.preview_box, 2)

        root.addLayout(mid, 2)

        self.stations_table = QTableWidget(0, 5)
        self._set_stations_headers()
        self.stations_table.verticalHeader().setVisible(False)
        self.stations_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.stations_table.setSelectionMode(QTableWidget.NoSelection)
        self.stations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stations_table.setAccessibleName(tr("stations_accessible"))
        self.stations_box = QGroupBox(tr("stations_title"))
        stations_layout = QVBoxLayout(self.stations_box)
        stations_layout.addWidget(self.stations_table)
        root.addWidget(self.stations_box)

        self.recompute()

    def _set_stations_headers(self):
        self.stations_table.setHorizontalHeaderLabels([
            tr("stations_header_station"), tr("stations_header_y"),
            tr("stations_header_le"), tr("stations_header_te"),
            tr("stations_header_chord"),
        ])

    def _on_language_changed(self, code: str):
        set_language(code)
        self.setWindowTitle(tr("window_title"))
        self.units_label.setText(tr("topbar_units"))
        self.unit_combo.setAccessibleName(tr("topbar_units_accessible"))
        self.cg_custom_label.setText(tr("topbar_cg_custom"))
        self.custom_cg_percent.setAccessibleName(tr("topbar_cg_custom_accessible"))
        style_toggle_checkbox(self.show_dims_checkbox, tr("topbar_show_dims"), self.show_dims_checkbox.isChecked())
        self.show_dims_checkbox.setAccessibleName(tr("topbar_show_dims_accessible"))
        self.language_label.setText(tr("topbar_language"))
        self.language_combo.setAccessibleName(tr("topbar_language_accessible"))
        self.panels_box.setTitle(tr("panels_box_title"))
        for row in self.rows:
            row.retranslate()
        self.outputs_box.setTitle(tr("results_title"))
        for key, (cap, caption_key, accessible_key) in self.output_captions.items():
            cap.setText(tr(caption_key))
            self.output_labels[key].setAccessibleName(tr(accessible_key))
        self.preview_box.setTitle(tr("preview_title"))
        self.preview.setAccessibleName(tr("preview_accessible"))
        self._set_stations_headers()
        self.stations_table.setAccessibleName(tr("stations_accessible"))
        self.stations_box.setTitle(tr("stations_title"))
        self._build_menu()
        self.recompute()

    def _build_menu(self):
        self.menuBar().clear()
        menubar = self.menuBar()
        file_menu = menubar.addMenu(tr("menu_file"))

        new_action = file_menu.addAction(tr("menu_new_project"))
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._on_new_project)

        file_menu.addSeparator()

        load_action = file_menu.addAction(tr("menu_load_csv"))
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._on_load_csv)

        save_action = file_menu.addAction(tr("menu_save_csv"))
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._on_save_csv)

        file_menu.addSeparator()

        export_action = file_menu.addAction(tr("menu_export_pdf"))
        export_action.setShortcut("Ctrl+P")
        export_action.triggered.connect(self._on_export_pdf)

        export_stations_action = file_menu.addAction(tr("menu_export_stations"))
        export_stations_action.setToolTip(tr("menu_export_stations_tooltip"))
        export_stations_action.triggered.connect(self._on_export_stations_csv)

    def _on_new_project(self):
        reply = QMessageBox.question(
            self, tr("new_project_title"), tr("new_project_body"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        self._reset_geometry()

    def _reset_geometry(self):
        for row in self.rows:
            row.reset_default(enabled=(row.index == 0))
        self.custom_cg_percent.blockSignals(True)
        self.custom_cg_percent.setValue(25.0)
        self.custom_cg_percent.blockSignals(False)
        idx = self.unit_combo.findText("mm")
        self.unit_combo.blockSignals(True)
        self.unit_combo.setCurrentIndex(idx)
        self.unit_combo.blockSignals(False)
        self._current_unit = "mm"
        self._last_basename = None
        self.recompute()
        self.statusBar().showMessage(tr("new_project_status"), 4000)

    def _on_copy_to_next(self, index: int):
        if index + 1 >= MAX_PANELS:
            return
        src = self.rows[index]
        dst = self.rows[index + 1]
        dst.major.setValue(src.minor.value())
        dst.minor.setValue(src.minor.value())
        dst.length.setValue(src.length.value())
        dst.sweep.setValue(src.sweep.value())
        if not dst.enabled.isChecked():
            dst.enabled.setChecked(True)
        self.statusBar().showMessage(tr("panel_copied_status", a=index + 1, b=index + 2), 3000)

    def _build_station_text(self, index: int):
        """Returns (title, body) for the Station View dialog, or None if
        the panel is disabled. Split out from _on_show_stations so the
        content can be tested without invoking the modal dialog."""
        pos = self._enabled_positions.get(index)
        if pos is None:
            return None
        start, end = self._panel_stations[pos]
        row = self.rows[index]
        unit = self.unit_combo.currentText()

        def fmt(v_mm):
            return f"{from_mm(v_mm, unit):9.3f} {unit}"

        body = (
            f"{tr('station_view_y_start'):12s} {fmt(start.y_mm)}\n"
            f"{tr('station_view_y_end'):12s} {fmt(end.y_mm)}\n"
            f"{tr('station_view_le_start'):12s} {fmt(start.le_x_mm)}\n"
            f"{tr('station_view_le_end'):12s} {fmt(end.le_x_mm)}\n"
            f"{tr('station_view_te_start'):12s} {fmt(start.te_x_mm)}\n"
            f"{tr('station_view_te_end'):12s} {fmt(end.te_x_mm)}\n"
            f"{tr('station_view_chord_start'):12s} {fmt(start.chord_mm)}\n"
            f"{tr('station_view_chord_end'):12s} {fmt(end.chord_mm)}\n"
            f"{tr('station_view_sweep'):12s} {row.sweep.value():9.3f}°"
        )
        return tr("station_view_panel_title", n=index + 1), body

    def _on_show_stations(self, index: int):
        result = self._build_station_text(index)
        if result is None:
            QMessageBox.information(
                self, tr("panel_label", n=index + 1),
                tr("station_view_disabled_body"),
            )
            return
        title, body = result
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title + tr("station_view_title_suffix"))
        box.setText(title)
        box.setInformativeText(body)
        box.setStyleSheet(
            "QLabel { font-family: 'DejaVu Sans Mono', 'Consolas', monospace; font-size: 12pt; }"
        )
        box.exec()

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
        default_name = f"{self._last_basename or tr('default_project_name')}.csv"
        start_path = str(Path(self._last_dir) / default_name) if self._last_dir else default_name
        path, _ = QFileDialog.getSaveFileName(self, tr("dialog_save_csv_title"), start_path, tr("filter_csv"))
        if not path:
            return
        if not path.lower().endswith(".csv"):
            path += ".csv"
        try:
            save_panels_csv(path, self._gather_wing_data())
        except OSError as e:
            QMessageBox.critical(self, tr("error_save_title"), str(e))
            return
        self._last_basename = Path(path).stem
        self._last_dir = str(Path(path).parent)
        self.statusBar().showMessage(tr("status_saved", path=path), 4000)

    def _on_load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("dialog_load_csv_title"), self._last_dir, tr("filter_csv"))
        if not path:
            return
        try:
            data = load_panels_csv(path)
        except (OSError, ValueError, KeyError) as e:
            QMessageBox.critical(self, tr("error_load_title"), str(e))
            return
        self._apply_wing_data(data)
        self._last_basename = Path(path).stem
        self._last_dir = str(Path(path).parent)
        self.statusBar().showMessage(tr("status_loaded", path=path), 4000)

    def _on_export_pdf(self):
        default_name = f"{self._last_basename or tr('default_project_name')}.pdf"
        start_path = str(Path(self._last_dir) / default_name) if self._last_dir else default_name
        path, _ = QFileDialog.getSaveFileName(self, tr("dialog_export_pdf_title"), start_path, tr("filter_pdf"))
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
            QMessageBox.critical(self, tr("error_export_title"), str(e))
            return
        self._last_basename = Path(path).stem
        self._last_dir = str(Path(path).parent)
        self.statusBar().showMessage(tr("status_exported_pdf", path=path), 4000)

    def _i18n_station_label(self, kind: str, **kw) -> str:
        """label_fn for geometry.compute_stations() -- translates the
        station labels shown on screen (Stations table / Station View)
        using the currently selected UI language."""
        if kind == "root":
            return tr("station_root")
        if kind == "tip":
            return tr("station_tip")
        if kind == "mid":
            return tr("station_mid", n=kw["n"])
        if kind == "mid_end":
            return tr("station_mid_end", n=kw["n"])
        if kind == "mid_start":
            return tr("station_mid_start", n=kw["n"], p=kw["p"])
        return ""

    def _on_export_stations_csv(self):
        default_name = f"{self._last_basename or tr('default_project_name')}{tr('stations_filename_suffix')}.csv"
        start_path = str(Path(self._last_dir) / default_name) if self._last_dir else default_name
        path, _ = QFileDialog.getSaveFileName(self, tr("dialog_export_stations_title"), start_path, tr("filter_csv"))
        if not path:
            return
        if not path.lower().endswith(".csv"):
            path += ".csv"
        if not self._stations:
            QMessageBox.warning(self, tr("no_geometry_title"), tr("no_geometry_body"))
            return
        # Canonical (Polish/ASCII-safe) labels for the CSV, independent of
        # the current UI language -- this is a data-interchange format
        # (like io_csv.py's panel CSV, always mm regardless of display
        # unit), not a localized artifact.
        unit = self.unit_combo.currentText()
        panels = [row.to_panel_mm(unit) for row in self.rows]
        panels = [p for p in panels if p is not None]
        canonical_stations = compute_stations(panels)
        try:
            save_stations_csv(path, canonical_stations)
        except OSError as e:
            QMessageBox.critical(self, tr("error_export_title"), str(e))
            return
        self._last_dir = str(Path(path).parent)
        self.statusBar().showMessage(tr("status_exported_stations", path=path), 4000)

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
        panels = []
        enabled_rows = []
        self._enabled_positions = {}
        for row in self.rows:
            p = row.to_panel_mm(unit)
            if p is not None:
                self._enabled_positions[row.index] = len(panels)
                panels.append(p)
                enabled_rows.append(row.index)
            else:
                self._enabled_positions[row.index] = None
        metrics = compute_wing_metrics(panels)
        self._stations = compute_stations(panels, label_fn=self._i18n_station_label)
        self._panel_stations = compute_panel_stations(panels)

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

        self._refresh_stations_table(unit)

        self.preview.update_data(
            panels, metrics, self._cg_targets(), unit,
            show_panel_details=self.show_dims_checkbox.isChecked(),
        )

        all_warnings = []
        for row in self.rows:
            all_warnings.extend(row.get_warnings())
        CONTINUITY_EPS_MM = 0.01
        for k in range(1, len(panels)):
            prev_minor = panels[k - 1].minor_chord_mm
            this_major = panels[k].major_chord_mm
            jump = this_major - prev_minor
            if abs(jump) > CONTINUITY_EPS_MM:
                all_warnings.append(
                    tr("warn_discontinuity",
                       b=enabled_rows[k] + 1, bm=this_major,
                       a=enabled_rows[k - 1] + 1, am=prev_minor, jump=jump)
                )
        if all_warnings:
            self.warnings_label.setText("⚠ " + "  •  ".join(all_warnings))
            self.warnings_label.show()
        else:
            self.warnings_label.setText("")
            self.warnings_label.hide()

    def _refresh_stations_table(self, unit: str):
        t = self.stations_table
        t.setRowCount(len(self._stations))
        for r, s in enumerate(self._stations):
            values = [
                s.label,
                f"{from_mm(s.y_mm, unit):.2f}",
                f"{from_mm(s.le_x_mm, unit):.2f}",
                f"{from_mm(s.te_x_mm, unit):.2f}",
                f"{from_mm(s.chord_mm, unit):.2f}",
            ]
            for c, text in enumerate(values):
                item = QTableWidgetItem(text)
                if c > 0:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                t.setItem(r, c, item)
        t.resizeRowsToContents()
        content_h = t.horizontalHeader().height() + 2 * t.frameWidth()
        for r in range(t.rowCount()):
            content_h += t.rowHeight(r)
        t.setFixedHeight(min(max(content_h, 70), 240))


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_QSS)
    app.setFont(QFont("Sans Serif", 11))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

"""
PDF / drawing tests -- "sprawdzić wszystkie 5 paneli / skok geometryczny /
wymiary / jednostki / krawędzie przy dużym sweepie / PDF bez danych".

These check that generation never raises and produces a plausible,
non-trivial PDF file. They do not do pixel-level image comparison (no
reference renderer to compare against) -- that's a reasonable gap to
leave for now per the "polish, don't rebuild" spirit of the v1.0 push.
"""

from pathlib import Path

import pytest

from ghostmean.geometry import WingPanel, compute_wing_metrics
from ghostmean.export_pdf import export_wing_pdf


def _make_panels(n, sweep=0.0):
    return [WingPanel(220 - i * 20, 200 - i * 20, 150, sweep) for i in range(n)]


class TestPdfPanelCounts:
    @pytest.mark.parametrize("n_panels", [1, 2, 3, 4, 5])
    def test_n_panels_export_succeeds(self, qapp, tmp_path, n_panels):
        panels = _make_panels(n_panels)
        metrics = compute_wing_metrics(panels)
        out = tmp_path / f"p{n_panels}.pdf"
        export_wing_pdf(out, panels, metrics, 25.0, "mm")
        assert out.exists()
        assert out.read_bytes()[:5] == b"%PDF-"
        assert out.stat().st_size > 1000


class TestPdfDiscontinuity:
    def test_real_geometry_jump_exports_without_error(self, qapp, tmp_path):
        panels = [WingPanel(250, 200, 300, 0), WingPanel(180, 140, 200, 0)]
        metrics = compute_wing_metrics(panels)
        out = tmp_path / "jump.pdf"
        export_wing_pdf(out, panels, metrics, 25.0, "mm")
        assert out.exists() and out.stat().st_size > 1000


class TestPdfUnits:
    @pytest.mark.parametrize("unit", ["mm", "in"])
    def test_export_in_both_units(self, qapp, tmp_path, unit):
        panels = _make_panels(2)
        metrics = compute_wing_metrics(panels)
        out = tmp_path / f"units_{unit}.pdf"
        export_wing_pdf(out, panels, metrics, 25.0, unit)
        assert out.exists() and out.stat().st_size > 1000


class TestPdfExtremeSweep:
    @pytest.mark.parametrize("sweep_deg", [-85, 85, 89.5])
    def test_extreme_sweep_exports_without_error(self, qapp, tmp_path, sweep_deg):
        panels = _make_panels(2, sweep=sweep_deg)
        metrics = compute_wing_metrics(panels)
        out = tmp_path / f"sweep_{sweep_deg}.pdf"
        export_wing_pdf(out, panels, metrics, 25.0, "mm")
        assert out.exists() and out.stat().st_size > 1000


class TestPdfNoOrBadData:
    def test_empty_panel_list_exports_placeholder_without_raising(self, qapp, tmp_path):
        metrics = compute_wing_metrics([])
        out = tmp_path / "empty.pdf"
        export_wing_pdf(out, [], metrics, 25.0, "mm")
        assert out.exists() and out.stat().st_size > 500

    def test_degenerate_panel_data_exports_without_raising(self, qapp, tmp_path):
        panels = [WingPanel(0, 0, 0.01, 89.9)]
        metrics = compute_wing_metrics(panels)
        out = tmp_path / "degenerate.pdf"
        export_wing_pdf(out, panels, metrics, 25.0, "mm")
        assert out.exists()


class TestDrawingSharedWithScreenPreview:
    """draw_wing_plan() backs both the on-screen preview and the PDF --
    a smoke test that it runs cleanly against an offscreen QPixmap for
    every panel count, independent of export_pdf.py's page layout."""

    @pytest.mark.parametrize("n_panels", [1, 2, 3, 4, 5])
    def test_draw_wing_plan_on_pixmap(self, qapp, n_panels):
        from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
        from ghostmean.drawing import draw_wing_plan

        panels = _make_panels(n_panels)
        metrics = compute_wing_metrics(panels)
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor("black"))
        painter = QPainter(pixmap)
        ok = draw_wing_plan(
            painter, 600, 400, panels, metrics,
            cg_targets=[("25%", 25.0)],
            pen_outline=QPen(QColor("blue")),
            pen_mac=QPen(QColor("orange")),
            pen_cg=QPen(QColor("green")),
            pen_axis=QPen(QColor("gray")),
            pen_dim=QPen(QColor("white")),
        )
        painter.end()
        assert ok is True

    def test_draw_wing_plan_returns_false_for_empty_panels(self, qapp):
        from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
        from ghostmean.drawing import draw_wing_plan

        metrics = compute_wing_metrics([])
        pixmap = QPixmap(600, 400)
        painter = QPainter(pixmap)
        ok = draw_wing_plan(
            painter, 600, 400, [], metrics, cg_targets=[],
            pen_outline=QPen(), pen_mac=QPen(), pen_cg=QPen(),
            pen_axis=QPen(), pen_dim=QPen(),
        )
        painter.end()
        assert ok is False

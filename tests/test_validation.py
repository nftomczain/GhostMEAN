"""
GUI-level validation tests -- non-blocking warnings must appear for bad
data, and bad data must never crash the app. Uses tests/fixtures/test_err.csv
(deliberately pathological: zero chords, inverted taper, zero length, a
real Major/Minor discontinuity) as the primary stress fixture.
"""

from pathlib import Path

from ghostmean.io_csv import load_panels_csv

FIXTURES = Path(__file__).parent / "fixtures"


class TestPanelRowWarnings:
    def test_clean_panel_has_no_warnings(self, qapp):
        from ghostmean.gui import PanelRow
        row = PanelRow(0)
        row.major.setValue(200)
        row.minor.setValue(150)
        row.length.setValue(300)
        row.sweep.setValue(10)
        assert row.get_warnings() == []

    def test_disabled_panel_has_no_warnings_even_if_bad(self, qapp):
        from ghostmean.gui import PanelRow
        row = PanelRow(0)
        row.enabled.setChecked(False)
        row.major.setValue(0)
        assert row.get_warnings() == []

    def test_major_zero_warns(self, qapp):
        from ghostmean.gui import PanelRow
        row = PanelRow(0)
        row.major.setValue(0)
        assert any("Major" in w for w in row.get_warnings())

    def test_minor_greater_than_major_warns(self, qapp):
        from ghostmean.gui import PanelRow
        row = PanelRow(0)
        row.major.setValue(100)
        row.minor.setValue(150)
        assert any("Minor" in w and "Major" in w for w in row.get_warnings())

    def test_large_sweep_warns(self, qapp):
        from ghostmean.gui import PanelRow
        row = PanelRow(0)
        row.sweep.setValue(75)
        assert len(row.get_warnings()) >= 1


class TestErrCsvDrivenValidation:
    """Load the deliberately-broken fixture straight into a live
    MainWindow and confirm: (a) it never crashes, (b) it produces
    warnings, (c) the app keeps computing something instead of freezing
    up."""

    def test_loading_test_err_csv_does_not_crash(self, qapp):
        from ghostmean.gui import MainWindow
        win = MainWindow()
        win.show()
        data = load_panels_csv(FIXTURES / "test_err.csv")
        win._apply_wing_data(data)  # must not raise
        qapp.processEvents()
        win.close()

    def test_loading_test_err_csv_produces_warnings(self, qapp):
        from ghostmean.gui import MainWindow
        win = MainWindow()
        win.show()
        data = load_panels_csv(FIXTURES / "test_err.csv")
        win._apply_wing_data(data)
        qapp.processEvents()
        assert win.warnings_label.text() != ""
        assert win.warnings_label.isVisible()
        win.close()

    def test_loading_test_err_csv_still_produces_a_result(self, qapp):
        """Even with garbage panel data, *some* MAC value should be
        computed and shown -- not a crash, not a frozen '—'."""
        from ghostmean.gui import MainWindow
        win = MainWindow()
        win.show()
        data = load_panels_csv(FIXTURES / "test_err.csv")
        win._apply_wing_data(data)
        qapp.processEvents()
        assert win.output_labels["mac"].text() != "—"
        win.close()

    def test_test_err_csv_discontinuity_is_flagged(self, qapp):
        """Panel 3 -> Panel 4 in the fixture is a genuine Major/Minor
        mismatch (100 -> 180) -- confirm the specific discontinuity
        warning text appears, not just *a* warning."""
        from ghostmean.gui import MainWindow
        win = MainWindow()
        win.show()
        data = load_panels_csv(FIXTURES / "test_err.csv")
        win._apply_wing_data(data)
        qapp.processEvents()
        assert "≠" in win.warnings_label.text()

    def test_pdf_export_survives_test_err_csv(self, qapp, tmp_path):
        from ghostmean.geometry import compute_wing_metrics
        from ghostmean.export_pdf import export_wing_pdf
        data = load_panels_csv(FIXTURES / "test_err.csv")
        from ghostmean.geometry import WingPanel
        panels = [WingPanel(p.major_mm, p.minor_mm, p.length_mm, p.sweep_deg)
                  for p in data.panels if p.enabled]
        metrics = compute_wing_metrics(panels)
        out = tmp_path / "err.pdf"
        export_wing_pdf(out, panels, metrics, data.ac_percent, data.unit)  # must not raise
        assert out.exists() and out.stat().st_size > 500


class TestNewProjectReset:
    def test_reset_clears_warnings(self, qapp):
        from ghostmean.gui import MainWindow
        win = MainWindow()
        win.show()
        win.rows[0].major.setValue(0)  # trigger a warning
        qapp.processEvents()
        assert win.warnings_label.text() != ""
        win._reset_geometry()
        qapp.processEvents()
        assert win.warnings_label.text() == ""
        win.close()

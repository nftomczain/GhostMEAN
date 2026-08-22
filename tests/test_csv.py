"""
CSV format tests -- "zamknąć format" checklist item.

Covers: round-trip fidelity, canonical-mm storage independent of display
unit, rounding precision, and malformed/error-path data that must produce
a controlled failure (a clear exception at the io_csv boundary) rather
than a crash -- the GUI layer turns those exceptions into a QMessageBox,
but that's out of scope for these pure-logic tests (see test_validation.py
for the GUI-level warning behaviour on the same kind of bad data).
"""

from pathlib import Path

import pytest

from ghostmean.geometry import compute_wing_metrics, compute_stations
from ghostmean.io_csv import save_panels_csv, load_panels_csv, WingData, PanelRowData
from ghostmean.io_stations import save_stations_csv, STATIONS_CSV_FIELDS

FIXTURES = Path(__file__).parent / "fixtures"


class TestPanelCsvRoundTrip:
    def test_save_then_load_is_lossless(self, tmp_path):
        data = WingData(
            panels=[
                PanelRowData(True, 260.0, 200.0, 220.0, 2.0),
                PanelRowData(True, 200.0, 90.0, 260.0, 12.0),
                PanelRowData(False, 200.0, 150.0, 300.0, 0.0),
                PanelRowData(False, 200.0, 150.0, 300.0, 0.0),
                PanelRowData(False, 200.0, 150.0, 300.0, 0.0),
            ],
            ac_percent=28.0,
            unit="in",
        )
        path = tmp_path / "roundtrip.csv"
        save_panels_csv(path, data)
        loaded = load_panels_csv(path)

        assert loaded.ac_percent == 28.0
        assert loaded.unit == "in"
        assert len(loaded.panels) == 5
        for original, back in zip(data.panels, loaded.panels):
            assert back.enabled == original.enabled
            assert back.major_mm == pytest.approx(original.major_mm)
            assert back.minor_mm == pytest.approx(original.minor_mm)
            assert back.length_mm == pytest.approx(original.length_mm)
            assert back.sweep_deg == pytest.approx(original.sweep_deg)

    def test_storage_is_canonical_mm_regardless_of_unit(self, tmp_path):
        """A file saved while the GUI was showing inches must still store
        raw millimetres on disk -- the 'unit' field is metadata for
        restoring the display, not a unit conversion applied to the
        numbers themselves."""
        data = WingData(panels=[PanelRowData(True, 254.0, 203.2, 300.0, 0.0)], unit="in")
        path = tmp_path / "canonical.csv"
        save_panels_csv(path, data)
        raw = path.read_text()
        assert "254.000000" in raw  # mm value, not "10.0" (inches)

    def test_disabled_panels_are_preserved(self, tmp_path):
        """Disabled panels must round-trip too -- v0.3.2 required this so
        re-enabling a panel after a save/load doesn't lose its numbers."""
        data = WingData(panels=[
            PanelRowData(False, 111.0, 22.0, 333.0, 4.0),
            PanelRowData(True, 250.0, 200.0, 300.0, 0.0),
        ])
        path = tmp_path / "disabled.csv"
        save_panels_csv(path, data)
        loaded = load_panels_csv(path)
        assert loaded.panels[0].enabled is False
        assert loaded.panels[0].major_mm == pytest.approx(111.0)

    def test_rounding_precision_is_six_decimals(self, tmp_path):
        data = WingData(panels=[PanelRowData(True, 200.123456789, 150.0, 300.0, 0.0)])
        path = tmp_path / "precision.csv"
        save_panels_csv(path, data)
        raw = path.read_text()
        assert "200.123457" in raw  # rounded to 6 decimals, not truncated garbage
        loaded = load_panels_csv(path)
        assert loaded.panels[0].major_mm == pytest.approx(200.123457, abs=1e-6)


class TestPanelCsvFixtureFiles:
    """Regression tests against the actual on-disk fixture files -- if the
    CSV format ever changes shape, these are the first things to break."""

    def test_test_csv_loads_and_matches_known_geometry(self):
        data = load_panels_csv(FIXTURES / "test.csv")
        assert data.unit == "mm"
        assert data.ac_percent == 25.0
        enabled = [p for p in data.panels if p.enabled]
        assert len(enabled) == 3
        assert enabled[0].major_mm == 250.0
        assert enabled[-1].minor_mm == 80.0

        from ghostmean.geometry import WingPanel
        wing_panels = [WingPanel(p.major_mm, p.minor_mm, p.length_mm, p.sweep_deg) for p in enabled]
        m = compute_wing_metrics(wing_panels)
        assert m.mac_mm == pytest.approx(189.621, abs=1e-3)

    def test_test2_csv_loads_as_continuous_5panel_wing(self):
        """test2.csv is a deliberately-continuous 5-panel wing
        (320→270→210→160→110→70mm) used as a more complex geometry
        regression example than test.csv's 3 panels."""
        data = load_panels_csv(FIXTURES / "test2.csv")
        assert data.unit == "mm"
        assert data.ac_percent == 28.0
        enabled = [p for p in data.panels if p.enabled]
        assert len(enabled) == 5

        from ghostmean.geometry import WingPanel, compute_stations
        wing_panels = [WingPanel(p.major_mm, p.minor_mm, p.length_mm, p.sweep_deg) for p in enabled]
        m = compute_wing_metrics(wing_panels)
        assert m.mac_mm == pytest.approx(215.681, abs=1e-3)
        assert m.span_mm == pytest.approx(2200.0)
        assert m.area_mm2 == pytest.approx(422500.0)

        # Fully continuous chain -- exactly 6 stations (root + 5 boundaries),
        # no discontinuity-induced duplicate entries.
        stations = compute_stations(wing_panels)
        assert len(stations) == 6

    def test_test_err_csv_loads_without_raising(self):
        """The file is full of pathological panel data (zero chords, an
        inverted taper, a zero-length panel, a real discontinuity) -- but
        it's syntactically valid CSV, so loading it must NOT raise. The
        resulting bad values are a GUI-validation concern (see
        test_validation.py), not a parse-time error."""
        data = load_panels_csv(FIXTURES / "test_err.csv")
        assert len(data.panels) == 5
        assert data.panels[0].major_mm == 0.0
        assert data.panels[1].minor_mm > data.panels[1].major_mm
        assert data.panels[2].length_mm == 0.0

    def test_test_err_csv_geometry_engine_does_not_crash(self):
        """Feed the pathological fixture straight into the geometry engine
        (bypassing the GUI's spinbox range clamping entirely) and confirm
        it still returns a result instead of raising."""
        from ghostmean.geometry import WingPanel
        data = load_panels_csv(FIXTURES / "test_err.csv")
        panels = [WingPanel(p.major_mm, p.minor_mm, p.length_mm, p.sweep_deg)
                  for p in data.panels if p.enabled]
        m = compute_wing_metrics(panels)  # must not raise
        stations = compute_stations(panels)  # must not raise
        assert len(stations) >= len(panels)


class TestPanelCsvErrorHandling:
    def test_empty_csv_raises_value_error(self, tmp_path):
        path = tmp_path / "empty.csv"
        path.write_text("# ghostmean_csv v1; ac_percent=25.0; unit=mm\npanel,enabled,major_mm,minor_mm,length_mm,sweep_deg\n")
        with pytest.raises(ValueError):
            load_panels_csv(path)

    def test_missing_file_raises_oserror(self, tmp_path):
        with pytest.raises(OSError):
            load_panels_csv(tmp_path / "does_not_exist.csv")

    def test_missing_column_raises_key_error(self, tmp_path):
        path = tmp_path / "missing_col.csv"
        path.write_text(
            "# ghostmean_csv v1; ac_percent=25.0; unit=mm\n"
            "panel,enabled,major_mm,minor_mm,length_mm\n"  # sweep_deg missing
            "1,True,200,150,300\n"
        )
        with pytest.raises(KeyError):
            load_panels_csv(path)

    def test_missing_metadata_comment_falls_back_to_defaults(self, tmp_path):
        """A CSV with no leading '# ghostmean_csv...' comment line should
        still load, defaulting ac_percent=25.0 and unit='mm', rather than
        crashing on a missing header."""
        path = tmp_path / "no_comment.csv"
        path.write_text(
            "panel,enabled,major_mm,minor_mm,length_mm,sweep_deg\n"
            "1,True,200,150,300,0\n"
        )
        data = load_panels_csv(path)
        assert data.ac_percent == 25.0
        assert data.unit == "mm"
        assert data.panels[0].major_mm == 200.0


class TestStationsCsvExport:
    def test_ascii_only_labels_regardless_of_language(self):
        """Station CSV export must always use canonical ASCII-safe labels,
        even if the caller passes stations that were labeled in another
        language upstream (the GUI enforces this by always recomputing
        stations with the default label_fn before export -- see
        gui.py's _on_export_stations_csv)."""
        from ghostmean.geometry import WingPanel
        stations = compute_stations([WingPanel(250, 200, 300, 0)])
        assert stations[0].label == "Nasada"
        assert stations[-1].label == "Końcówka"

    def test_export_writes_expected_columns(self, tmp_path):
        from ghostmean.geometry import WingPanel
        stations = compute_stations([WingPanel(250, 200, 300, 0)])
        path = tmp_path / "stations.csv"
        save_stations_csv(path, stations)
        header = path.read_text().splitlines()[0]
        assert header.split(",") == STATIONS_CSV_FIELDS

    def test_export_transliterates_polish_diacritics(self, tmp_path):
        from ghostmean.geometry import WingPanel
        stations = compute_stations([WingPanel(250, 200, 300, 0)])
        path = tmp_path / "stations_ascii.csv"
        save_stations_csv(path, stations)
        raw = path.read_text()
        assert "Końcówka" not in raw
        assert "Koncowka" in raw

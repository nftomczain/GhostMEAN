"""
Geometry tests -- the "ZERO niespodzianek" core of GhostMEAN.

Every reference number here traces back to either a hand-computed value
verified during development, or the user's own worked example (the
250->200->140->80 chain, lengths 300/250/200mm), so a regression here
means the actual math changed, not just a refactor.
"""

import math

import pytest

from ghostmean.geometry import (
    WingPanel, WingMetrics, compute_wing_metrics,
    compute_panel_stations, compute_stations,
    aerodynamic_center, cg_from_percent_mac, percent_mac_from_cg,
)

# The chain example used throughout development: 250->200->140->80mm
# chords at panel lengths 300/250/200mm, no sweep.
CHAIN_PANELS = [
    WingPanel(250, 200, 300, 0),
    WingPanel(200, 140, 250, 0),
    WingPanel(140, 80, 200, 0),
]


class TestPanelStations:
    def test_one_panel_uses_its_own_major_and_minor(self):
        pairs = compute_panel_stations([WingPanel(250, 200, 300, 0)])
        assert len(pairs) == 1
        start, end = pairs[0]
        assert start.chord_mm == 250
        assert end.chord_mm == 200
        assert start.y_mm == 0
        assert end.y_mm == 300

    def test_chain_example_matches_user_table(self):
        pairs = compute_panel_stations(CHAIN_PANELS)
        assert len(pairs) == 3
        # Root
        assert pairs[0][0].y_mm == 0 and pairs[0][0].chord_mm == 250
        # S1 (end of panel 1 / start of panel 2, continuous)
        assert pairs[0][1].y_mm == 300 and pairs[0][1].chord_mm == 200
        assert pairs[1][0].y_mm == 300 and pairs[1][0].chord_mm == 200
        # S2
        assert pairs[1][1].y_mm == 550 and pairs[1][1].chord_mm == 140
        assert pairs[2][0].y_mm == 550 and pairs[2][0].chord_mm == 140
        # Tip
        assert pairs[2][1].y_mm == 750 and pairs[2][1].chord_mm == 80

    def test_discontinuous_panel_uses_its_own_major_not_inherited(self):
        """The core v0.4.0 promise: user data is truth. Panel 2's Major
        (180) must be used even though panel 1's Minor was 200 -- no
        silent 'fixing'."""
        panels = [WingPanel(250, 200, 300, 0), WingPanel(180, 140, 200, 0)]
        pairs = compute_panel_stations(panels)
        assert pairs[1][0].chord_mm == 180  # panel 2's OWN major, not 200

    def test_sweep_offsets_le_consistently_across_panels(self):
        """Panel 2's LE start must exactly equal panel 1's LE end (sweep
        integration is continuous even though each panel's sweep angle is
        independent)."""
        panels = [WingPanel(250, 200, 300, 5), WingPanel(200, 140, 250, 10)]
        pairs = compute_panel_stations(panels)
        assert pairs[0][1].le_x_mm == pytest.approx(pairs[1][0].le_x_mm)
        expected_le1 = 300 * math.tan(math.radians(5))
        assert pairs[0][1].le_x_mm == pytest.approx(expected_le1)


class TestComputeStations:
    def test_empty_panels_returns_empty_list(self):
        assert compute_stations([]) == []

    def test_continuous_chain_regression(self):
        """Must produce exactly 4 entries (Root, S1, S2, Tip) -- no
        spurious duplicate/jump entries when panels are continuous."""
        stations = compute_stations(CHAIN_PANELS)
        assert [s.label for s in stations] == ["Nasada", "S1", "S2", "Końcówka"]
        assert [s.y_mm for s in stations] == [0, 300, 550, 750]
        assert [s.chord_mm for s in stations] == [250, 200, 140, 80]

    def test_discontinuity_inserts_real_jump(self):
        """The v0.4.1 'real fix': a genuine, visible 20mm step at Y=300,
        not smoothed away."""
        panels = [WingPanel(250, 200, 300, 0), WingPanel(180, 140, 200, 0)]
        stations = compute_stations(panels)
        assert len(stations) == 4  # Root, S1(end), S1(start), Tip
        assert stations[1].y_mm == stations[2].y_mm == 300
        assert stations[1].chord_mm == 200   # end of panel 1 (its own minor)
        assert stations[2].chord_mm == 180   # start of panel 2 (its own major)

    def test_custom_label_fn_used_instead_of_default(self):
        def en_labels(kind, **kw):
            return {"root": "Root", "tip": "Tip", "mid": f"S{kw.get('n')}"}.get(kind, "")
        stations = compute_stations(CHAIN_PANELS, label_fn=en_labels)
        assert stations[0].label == "Root"
        assert stations[-1].label == "Tip"

    def test_default_label_fn_unaffected_by_custom_calls(self):
        """Calling compute_stations with a custom label_fn must not leak
        into later calls without one (label_fn has no lingering global
        state)."""
        compute_stations(CHAIN_PANELS, label_fn=lambda kind, **kw: "X")
        stations = compute_stations(CHAIN_PANELS)
        assert stations[0].label == "Nasada"


class TestMacAndArea:
    def test_reference_example_11_6_inches(self):
        """Known aviation reference: 11in/6in chords -> MAC ~= 8.745in."""
        p = WingPanel(major_chord_mm=11 * 25.4, minor_chord_mm=6 * 25.4, length_mm=30 * 25.4)
        m = compute_wing_metrics([p])
        assert m.mac_mm / 25.4 == pytest.approx(8.745, abs=1e-3)

    def test_rectangular_wing_mac_equals_constant_chord(self):
        p = WingPanel(major_chord_mm=200, minor_chord_mm=200, length_mm=500, sweep_deg=10)
        m = compute_wing_metrics([p])
        assert m.mac_mm == pytest.approx(200)

    def test_chain_example_mac(self):
        """Locks in the exact value repeatedly verified through the whole
        development conversation (MAC = 189.621mm for the chain example)."""
        m = compute_wing_metrics(CHAIN_PANELS)
        assert m.mac_mm == pytest.approx(189.621, abs=1e-3)
        assert m.span_mm == 1500
        assert m.area_mm2 == pytest.approx(264000)

    def test_span_and_area_are_additive_across_panels(self):
        m = compute_wing_metrics(CHAIN_PANELS)
        expected_area = 2 * sum(p.area_mm2() for p in CHAIN_PANELS)
        assert m.area_mm2 == pytest.approx(expected_area)
        expected_span = 2 * sum(p.length_mm for p in CHAIN_PANELS)
        assert m.span_mm == pytest.approx(expected_span)

    def test_empty_panels_returns_zeroed_metrics(self):
        m = compute_wing_metrics([])
        assert m == WingMetrics(0, 0, 0, 0, 0, 0)


class TestCgAndAc:
    def test_cg_from_percent_mac_25_28_30(self):
        m = compute_wing_metrics(CHAIN_PANELS)
        assert cg_from_percent_mac(m, 25.0) == pytest.approx(m.mac_mm * 0.25)
        assert cg_from_percent_mac(m, 28.0) == pytest.approx(m.mac_mm * 0.28)
        assert cg_from_percent_mac(m, 30.0) == pytest.approx(m.mac_mm * 0.30)

    def test_percent_mac_from_cg_is_true_inverse(self):
        m = compute_wing_metrics(CHAIN_PANELS)
        for pct in (10, 25, 28, 30, 50, 75):
            cg_mm = cg_from_percent_mac(m, pct)
            assert percent_mac_from_cg(m, cg_mm) == pytest.approx(pct)

    def test_percent_mac_from_cg_zero_mac_returns_zero(self):
        m = WingMetrics(0, 0, 0, 0, 0, 0)
        assert percent_mac_from_cg(m, 50.0) == 0.0

    def test_aerodynamic_center_at_mac_y(self):
        m = compute_wing_metrics(CHAIN_PANELS)
        ac_x, ac_y = aerodynamic_center(m, 25.0)
        assert ac_y == pytest.approx(m.mac_y_mm)
        assert ac_x == pytest.approx(m.mac_le_x_mm + m.mac_mm * 0.25)


class TestPanelCounts:
    """v1.0 checklist: 1, 2, 3, 4, and 5 panels must all compute without
    error and produce internally consistent station counts."""

    @pytest.mark.parametrize("n_panels", [1, 2, 3, 4, 5])
    def test_n_panels_no_crash_and_consistent_station_count(self, n_panels):
        panels = [WingPanel(200 - i * 20, 180 - i * 20, 150, 0) for i in range(n_panels)]
        m = compute_wing_metrics(panels)
        stations = compute_stations(panels)
        pairs = compute_panel_stations(panels)
        assert len(pairs) == n_panels
        assert len(stations) == n_panels + 1  # continuous chain, no jumps
        assert m.span_mm == pytest.approx(n_panels * 150 * 2)
        assert m.mac_mm > 0


class TestSweepEdgeCases:
    @pytest.mark.parametrize("sweep_deg", [-80, -30, 0, 30, 80, 88.9])
    def test_various_sweeps_no_crash(self, sweep_deg):
        p = WingPanel(200, 150, 300, sweep_deg)
        m = compute_wing_metrics([p])
        stations = compute_stations([p])
        assert m.mac_mm > 0
        assert len(stations) == 2

    def test_zero_sweep_le_stays_on_axis(self):
        p = WingPanel(200, 150, 300, 0)
        pairs = compute_panel_stations([p])
        assert pairs[0][0].le_x_mm == 0
        assert pairs[0][1].le_x_mm == 0

    def test_negative_sweep_moves_le_opposite_direction(self):
        pos = compute_panel_stations([WingPanel(200, 150, 300, 20)])[0][1]
        neg = compute_panel_stations([WingPanel(200, 150, 300, -20)])[0][1]
        assert pos.le_x_mm == pytest.approx(-neg.le_x_mm)


class TestNoCrashOnPathologicalInput:
    """Everything here is deliberately invalid/degenerate input -- the
    engine must return *something* (possibly zeros) rather than raise."""

    def test_zero_major_and_minor(self):
        p = WingPanel(0, 0, 300, 0)
        m = compute_wing_metrics([p])
        assert m.mac_mm == 0

    def test_minor_greater_than_major(self):
        p = WingPanel(100, 200, 300, 0)  # reversed taper
        m = compute_wing_metrics([p])
        assert m.mac_mm > 0  # still computes a sane, positive MAC

    def test_extreme_sweep_near_90_degrees(self):
        p = WingPanel(200, 150, 300, 89.9)
        m = compute_wing_metrics([p])
        assert m.mac_mm > 0

    def test_tiny_length(self):
        p = WingPanel(200, 150, 0.01, 0)
        m = compute_wing_metrics([p])
        assert m.span_mm == pytest.approx(0.02)

    def test_all_panels_disabled_is_empty_list(self):
        # This is how the GUI represents "nothing enabled" -- an empty list.
        m = compute_wing_metrics([])
        stations = compute_stations([])
        assert m.area_mm2 == 0
        assert stations == []

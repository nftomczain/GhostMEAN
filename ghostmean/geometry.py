"""
Core geometry math for GhostMEAN.

A wing is modeled as a stack of up to 5 straight-tapered panels (one side,
mirrored automatically for the opposite semi-span). Each panel is defined by:

    major_chord_mm  -- chord at the panel root (inboard side)
    minor_chord_mm  -- chord at the panel tip (outboard side)
    length_mm       -- panel span (ONE side, perpendicular to root chord)
    sweep_deg       -- leading-edge sweep angle for THIS panel, degrees

SWEEP CONVENTION (confirmed/locked, do not change without updating every
caller and the UI tooltip in gui.py):
  - sweep_deg is the angle of the panel's OWN leading edge, measured from
    the spanwise axis (perpendicular to the wing's axis of symmetry).
  - Each panel's sweep is ABSOLUTE / independent -- it is measured from the
    global spanwise axis, NOT relative to the previous panel's direction.
    Sweep angles are never composed/accumulated across panels.
  - 0 degrees means the leading edge runs parallel to the spanwise axis.
    Positive/negative sets which way the leading edge is offset.
  - The chord itself never rotates -- it always stays perpendicular to the
    global spanwise axis (parallel to the root chord). Sweep only offsets
    the leading-edge x-position sideways as the panel's local coordinate
    advances along the span; the trailing edge position is a DERIVED
    quantity (leading edge x + local chord length at that station), so a
    tapered panel's effective trailing-edge sweep will generally differ
    from its leading-edge sweep -- this is expected, not a bug.

All internal math is done in millimetres. The GUI converts to/from inches
at the input/output boundary only (see units.py).

MAC is computed by integrating the true chord distribution c(y) rather than
just applying the single-trapezoid formula, so multi-panel wings with
different taper per panel are handled correctly:

    MAC       = (2/S) * sum_i  Li*(Cri^2 + Cri*Cti + Cti^2)/3
    y_MAC     = (2/S) * sum_i [ y0_i*Ai + Li^2*(Cri+2*Cti)/6 ]
    LE_x(MAC) = (2/S) * sum_i [ x0_i*Ai + Li^2*(Cri+2*Cti)/6 * tan(sweep_i) ]

where S is the FULL wing area (both sides), Ai = Li*(Cri+Cti)/2 is one
panel's area (one side), y0_i/x0_i are the panel's root position, and the
factor of 2 accounts for both semi-spans (symmetric wing assumed).
"""

from dataclasses import dataclass
import math


@dataclass
class WingPanel:
    major_chord_mm: float
    minor_chord_mm: float
    length_mm: float
    sweep_deg: float = 0.0

    def area_mm2(self) -> float:
        """One panel, one side."""
        return self.length_mm * (self.major_chord_mm + self.minor_chord_mm) / 2.0

    def taper_ratio(self) -> float:
        if self.major_chord_mm == 0:
            return 0.0
        return self.minor_chord_mm / self.major_chord_mm


@dataclass
class WingMetrics:
    span_mm: float          # full span, both sides
    area_mm2: float         # full area, both sides
    aspect_ratio: float
    mac_mm: float
    mac_y_mm: float          # spanwise position of MAC, measured from centerline
    mac_le_x_mm: float       # chordwise (leading-edge) position of the MAC, from root LE at centerline
    root_le_x_mm: float = 0.0  # kept for reference / future dihedral etc.


def compute_wing_metrics(panels: list[WingPanel]) -> WingMetrics:
    if not panels:
        return WingMetrics(0, 0, 0, 0, 0, 0)

    half_span = sum(p.length_mm for p in panels)
    half_area = sum(p.area_mm2() for p in panels)
    span = 2 * half_span
    area = 2 * half_area

    sum_c2 = 0.0     # sum of Li*(Cri^2+Cri*Cti+Cti^2)/3  -> feeds MAC
    sum_yc = 0.0      # sum of y0_i*Ai + Li^2*(Cri+2Cti)/6 -> feeds y_MAC
    sum_xc = 0.0      # sum of x0_i*Ai + tan(sweep)*Li^2*(Cri+2Cti)/6 -> feeds LE_x_MAC

    y0 = 0.0
    x0 = 0.0
    for p in panels:
        Cr, Ct, L = p.major_chord_mm, p.minor_chord_mm, p.length_mm
        Ai = p.area_mm2()
        theta = math.radians(p.sweep_deg)

        sum_c2 += L * (Cr * Cr + Cr * Ct + Ct * Ct) / 3.0
        moment = L * L * (Cr + 2 * Ct) / 6.0
        sum_yc += y0 * Ai + moment
        sum_xc += x0 * Ai + math.tan(theta) * moment

        # advance to next panel's root
        y0 += L
        x0 += L * math.tan(theta)

    if half_area <= 0:
        return WingMetrics(span, area, 0.0, 0.0, 0.0, 0.0)

    mac = sum_c2 / half_area
    mac_y = sum_yc / half_area
    mac_le_x = sum_xc / half_area
    ar = (span * span / area) if area > 0 else 0.0

    return WingMetrics(
        span_mm=span,
        area_mm2=area,
        aspect_ratio=ar,
        mac_mm=mac,
        mac_y_mm=mac_y,
        mac_le_x_mm=mac_le_x,
        root_le_x_mm=0.0,
    )


def aerodynamic_center(metrics: WingMetrics, percent_mac: float = 25.0):
    """Aerodynamic center as an absolute (x, y) point, at percent_mac of the MAC
    chord back from its leading edge. Returns (ac_x_mm, ac_y_mm)."""
    ac_x = metrics.mac_le_x_mm + metrics.mac_mm * (percent_mac / 100.0)
    return ac_x, metrics.mac_y_mm


def cg_from_percent_mac(metrics: WingMetrics, percent_mac: float) -> float:
    """Distance from the MAC leading edge to a target CG position, in mm."""
    return metrics.mac_mm * (percent_mac / 100.0)


def percent_mac_from_cg(metrics: WingMetrics, cg_from_le_mm: float) -> float:
    if metrics.mac_mm == 0:
        return 0.0
    return 100.0 * cg_from_le_mm / metrics.mac_mm


@dataclass
class Station:
    """A single spanwise cross-section of the wing outline -- the root, a
    panel boundary, or the tip. This is the canonical source for both the
    on-screen/PDF wing outline (see drawing.py) and the Station View /
    station table / station CSV export (v0.4.0)."""
    label: str
    y_mm: float       # spanwise position, one side, from the symmetry axis
    le_x_mm: float     # leading-edge x position at this station
    te_x_mm: float     # trailing-edge x position at this station
    chord_mm: float    # local chord length (te_x - le_x) at this station


def compute_panel_stations(panels: list[WingPanel]) -> list[tuple[Station, Station]]:
    """One (start, end) Station pair per panel -- always exactly
    len(panels) pairs, directly addressable by panel index. Each panel's
    start uses its OWN major_chord_mm and end its OWN minor_chord_mm,
    regardless of whether that matches the neighbouring panel -- GhostMEAN
    never substitutes a neighbour's value for the one the user entered.
    This is the source Station View / per-panel dimension labels / panel
    numbering should index by panel, rather than walking the flat outline
    from compute_stations() (which may contain extra points at a real
    discontinuity -- see below)."""
    pairs = []
    y, le = 0.0, 0.0
    for i, p in enumerate(panels):
        theta = math.radians(p.sweep_deg)
        start = Station(f"P{i + 1} start", y, le, le + p.major_chord_mm, p.major_chord_mm)
        y_end = y + p.length_mm
        le_end = le + p.length_mm * math.tan(theta)
        end = Station(f"P{i + 1} end", y_end, le_end, le_end + p.minor_chord_mm, p.minor_chord_mm)
        pairs.append((start, end))
        y, le = y_end, le_end
    return pairs


def compute_stations(panels: list[WingPanel]) -> list[Station]:
    """Flat, root-to-tip outline station list for drawing / the station
    table / CSV export.

    GHOST MEAN PRINCIPLE (locked, v0.4.0): the user's panel data is the
    truth -- the program never silently "fixes" a mismatch between one
    panel's Major and the previous panel's Minor. Each panel is drawn from
    its OWN Major/Minor (see compute_panel_stations() above). Normally
    this produces exactly one entry per boundary (root, each panel
    junction, tip) because consecutive panels agree. If they DON'T agree,
    a real step exists in the wing outline, and TWO entries are emitted at
    that boundary's Y -- the end of the previous panel and the start of
    the current one -- so the outline (and the station table) show the
    actual jump instead of smoothing over it. The GUI separately raises a
    non-blocking validation warning when this happens; it never blocks or
    alters the calculation."""
def _default_station_label(kind: str, **kw) -> str:
    """Fallback labels (Polish), used when compute_stations() is called
    without a label_fn -- keeps geometry.py usable/testable standalone,
    with no dependency on the i18n layer."""
    if kind == "root":
        return "Nasada"
    if kind == "tip":
        return "Końcówka"
    if kind == "mid":
        return f"S{kw['n']}"
    if kind == "mid_end":
        return f"S{kw['n']} (koniec P{kw['n']})"
    if kind == "mid_start":
        return f"S{kw['n']} (start P{kw['p']})"
    return ""


def compute_stations(panels: list[WingPanel], label_fn=None) -> list[Station]:
    """Flat, root-to-tip outline station list for drawing / the station
    table / CSV export.

    `label_fn(kind, **kw)` generates each station's display label; kind is
    one of "root", "tip", "mid" (kw: n), "mid_end" (kw: n), "mid_start"
    (kw: n, p) -- see _default_station_label() above for the reference
    implementation. Pass an i18n-aware label_fn from the UI layer to get
    translated station labels without geometry.py itself depending on the
    i18n package.

    GHOST MEAN PRINCIPLE (locked, v0.4.0): the user's panel data is the
    truth -- the program never silently "fixes" a mismatch between one
    panel's Major and the previous panel's Minor. Each panel is drawn from
    its OWN Major/Minor (see compute_panel_stations() above). Normally
    this produces exactly one entry per boundary (root, each panel
    junction, tip) because consecutive panels agree. If they DON'T agree,
    a real step exists in the wing outline, and TWO entries are emitted at
    that boundary's Y -- the end of the previous panel and the start of
    the current one -- so the outline (and the station table) show the
    actual jump instead of smoothing over it. The GUI separately raises a
    non-blocking validation warning when this happens; it never blocks or
    alters the calculation."""
    if not panels:
        return []
    label_fn = label_fn or _default_station_label

    pairs = compute_panel_stations(panels)
    root = pairs[0][0]
    stations = [Station(label_fn("root"), root.y_mm, root.le_x_mm, root.te_x_mm, root.chord_mm)]
    JUMP_EPS_MM = 1e-6
    for i, (start, end) in enumerate(pairs):
        if i > 0:
            prev_end = stations[-1]
            if abs(prev_end.te_x_mm - start.te_x_mm) > JUMP_EPS_MM:
                # real discontinuity: rename the boundary's two halves so
                # both are distinguishable, then insert the actual jump
                stations[-1] = Station(
                    label_fn("mid_end", n=i), prev_end.y_mm, prev_end.le_x_mm,
                    prev_end.te_x_mm, prev_end.chord_mm,
                )
                stations.append(Station(
                    label_fn("mid_start", n=i, p=i + 1), start.y_mm, start.le_x_mm,
                    start.te_x_mm, start.chord_mm,
                ))
        label = label_fn("tip") if i == len(panels) - 1 else label_fn("mid", n=i + 1)
        stations.append(Station(label, end.y_mm, end.le_x_mm, end.te_x_mm, end.chord_mm))
    return stations

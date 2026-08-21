"""
Shared wing-planform drawing logic.

Used by BOTH the on-screen preview widget and the PDF export, so the two
stay geometrically identical -- only the color palette differs (dark theme
on screen, print-friendly light theme in the PDF). The caller owns the
QPainter (begin/end, fillRect, render hints) and supplies QPen objects for
each element so each context can pick its own colors.

Station geometry itself (leading/trailing edge position and chord, per
panel and along the flat outline) is computed once in geometry.py's
compute_panel_stations() / compute_stations() -- this module only turns
those stations into pixels. Do not recompute boundary positions here;
import them. GHOST MEAN never "fixes" a mismatch between one panel's Major
and the previous panel's Minor -- a real discontinuity is drawn as an
actual step (see geometry.compute_stations() docstring), not smoothed
over.
"""

from PySide6.QtCore import Qt, QRectF

from ghostmean.geometry import cg_from_percent_mac, compute_stations, compute_panel_stations
from ghostmean.units import from_mm


def draw_wing_plan(
    painter, width, height, panels, metrics,
    cg_targets,
    pen_outline, pen_mac, pen_cg, pen_axis, pen_dim,
    unit="mm",
    pad=30,
    show_panel_numbers=True,
    show_dimensions=True,
    show_panel_details=False,
    label_font=None,
):
    """Paint the mirrored wing planform into `painter`'s coordinate space
    (width x height). Draws, in order: symmetry axis, outline, panel number
    labels, (optionally) per-panel dimension arrows above the leading edge,
    MAC line, CG markers (one per (label, percent) in cg_targets), a
    total-span dimension line, and (optionally) a per-panel legend listing
    Major/Minor/Length/Sweep by panel number -- kept as a list rather than
    positioned labels on the drawing itself, since with 3+ panels the
    labels crowd together near the root and become unreadable.

    Returns False (and draws nothing) if there is no valid geometry to show.
    """
    if not panels or metrics is None or metrics.span_mm <= 0:
        return False

    stations = compute_stations(panels)
    panel_pairs = compute_panel_stations(panels)

    if label_font is not None:
        painter.setFont(label_font)
    fm = painter.fontMetrics()
    legend_line_h = fm.height() + 4

    reserve_bottom = 44 if show_dimensions else 0
    if show_panel_details:
        reserve_bottom += legend_line_h * len(panels) + 10
    reserve_top = 30 if show_panel_details else 0
    w = width - 2 * pad
    h = max(height - 2 * pad - reserve_bottom - reserve_top, 10)

    # True chordwise depth needed (root-LE-to-tip-TE bounding box), computed
    # from the actual station data rather than a mac_mm+chord approximation.
    depth_mm = max(s.te_x_mm for s in stations) - min(s.le_x_mm for s in stations)
    depth_mm = max(depth_mm, 1e-6)

    # Fixed reference scale (mm-per-pixel), calibrated so a "large" wing
    # (REFERENCE_SPAN_MM / REFERENCE_DEPTH_MM) fills the box -- smaller
    # wings render visibly smaller instead of always being blown up to
    # fill the same space, and larger wings fall back to shrink-to-fit
    # (the second term below) so they never overflow the box, getting
    # progressively "tighter" the more they exceed the reference size.
    REFERENCE_SPAN_MM = 2000.0
    REFERENCE_DEPTH_MM = 350.0
    fixed_scale = min(w / REFERENCE_SPAN_MM, h / REFERENCE_DEPTH_MM)
    fit_scale = min(w / metrics.span_mm, h / depth_mm)
    scale = min(fixed_scale, fit_scale)
    scale = max(scale, 1e-6)

    cx = width / 2
    top_y = pad + reserve_top

    def X(y_span_signed):
        return cx + y_span_signed * scale

    def Y(x_chord):
        return top_y + x_chord * scale

    # --- symmetry axis (full drawing height) ---
    painter.setPen(pen_axis)
    painter.drawLine(X(0), top_y, X(0), top_y + h)

    # --- outline ---
    painter.setPen(pen_outline)

    def draw_side(sign):
        for i in range(len(stations) - 1):
            a, b = stations[i], stations[i + 1]
            painter.drawLine(X(sign * a.y_mm), Y(a.le_x_mm), X(sign * b.y_mm), Y(b.le_x_mm))
            painter.drawLine(X(sign * a.y_mm), Y(a.te_x_mm), X(sign * b.y_mm), Y(b.te_x_mm))
        first, last = stations[0], stations[-1]
        painter.drawLine(X(sign * last.y_mm), Y(last.le_x_mm), X(sign * last.y_mm), Y(last.te_x_mm))
        painter.drawLine(X(sign * first.y_mm), Y(first.le_x_mm), X(sign * first.y_mm), Y(first.te_x_mm))

    draw_side(1)
    draw_side(-1)

    # --- panel numbers (near the LE midpoint of each panel, both sides) ---
    if show_panel_numbers:
        painter.setPen(pen_outline)
        for i, (a, b) in enumerate(panel_pairs):
            y_mid = (a.y_mm + b.y_mm) / 2
            x_mid_le = (a.le_x_mm + b.le_x_mm) / 2
            label = str(i + 1)
            for sign in (1, -1):
                painter.drawText(QRectF(X(sign * y_mid) - 10, Y(x_mid_le) - 20, 20, 16),
                                  Qt.AlignCenter, label)

    # --- per-panel dimension arrow (length), above the leading edge ---
    if show_panel_details:
        painter.setPen(pen_dim)
        for i, p in enumerate(panels):
            a, b = panel_pairs[i]

            arrow_y = top_y - 18
            for sign in (1, -1):
                ya, yb = X(sign * a.y_mm), X(sign * b.y_mm)
                lo, hi = (ya, yb) if ya <= yb else (yb, ya)
                painter.drawLine(lo, arrow_y, hi, arrow_y)
                for xend, direction in ((lo, 1), (hi, -1)):
                    painter.drawLine(xend, arrow_y, xend + direction * 5, arrow_y - 4)
                    painter.drawLine(xend, arrow_y, xend + direction * 5, arrow_y + 4)

    # --- MAC line (dashed, both sides at mac_y) ---
    painter.setPen(pen_mac)
    for sign in (1, -1):
        yv = sign * metrics.mac_y_mm
        painter.drawLine(X(yv), Y(metrics.mac_le_x_mm), X(yv), Y(metrics.mac_le_x_mm + metrics.mac_mm))

    # --- CG markers along the MAC line ---
    painter.setPen(pen_cg)
    line_h = painter.fontMetrics().height() + 2
    cyp_first = Y(cg_from_percent_mac(metrics, cg_targets[0][1]) + metrics.mac_le_x_mm) if cg_targets else 0
    for i, (label, percent) in enumerate(cg_targets):
        cg_mm = cg_from_percent_mac(metrics, percent)
        cg_x = metrics.mac_le_x_mm + cg_mm
        cxp, cyp = X(metrics.mac_y_mm), Y(cg_x)
        for sign in (1, -1):
            cxp_s = X(sign * metrics.mac_y_mm)
            r = 5
            painter.drawLine(cxp_s - r, cyp, cxp_s + r, cyp)
            painter.drawLine(cxp_s, cyp - r, cxp_s, cyp + r)
        # labels stack vertically (offset by index) so close-together markers
        # (typical: 25/28/30% are only a few % of the MAC chord apart) don't
        # overlap each other -- a thin leader line ties each label back to
        # its exact marker point.
        label_y = cyp_first - line_h / 2 + i * line_h
        painter.drawLine(cxp + 6, cyp, cxp + 10, label_y + line_h / 2)
        painter.drawText(QRectF(cxp + 12, label_y, 60, line_h), Qt.AlignLeft | Qt.AlignVCenter, label)

    # --- total span dimension line ---
    if show_dimensions:
        painter.setPen(pen_dim)
        dim_y = top_y + h + 20
        left_x = X(-metrics.span_mm / 2)
        right_x = X(metrics.span_mm / 2)
        painter.drawLine(left_x, dim_y, right_x, dim_y)
        tick = 6
        painter.drawLine(left_x, dim_y - tick, left_x, dim_y + tick)
        painter.drawLine(right_x, dim_y - tick, right_x, dim_y + tick)
        span_disp = from_mm(metrics.span_mm, unit)
        text = f"Span: {span_disp:.1f} {unit}"
        painter.drawText(QRectF(left_x, dim_y + 4, right_x - left_x, 18), Qt.AlignCenter, text)

    # --- per-panel legend (Major/Minor/Length/Sweep by panel number) ---
    # A list under the wing rather than labels crowded onto the drawing --
    # with 3+ panels, positioned labels near the root overlap and become
    # unreadable; the panel numbers already drawn on the outline (above)
    # tie each list line to its shape unambiguously.
    if show_panel_details:
        painter.setPen(pen_dim)
        legend_top = (top_y + h + 44) if show_dimensions else (top_y + h + 10)
        for i, p in enumerate(panels):
            major_disp = from_mm(p.major_chord_mm, unit)
            minor_disp = from_mm(p.minor_chord_mm, unit)
            length_disp = from_mm(p.length_mm, unit)
            text = (
                f"Panel {i + 1}:  {major_disp:.0f}→{minor_disp:.0f} | "
                f"{length_disp:.0f}{unit} | {p.sweep_deg:.0f}°"
            )
            line_y = legend_top + i * legend_line_h
            painter.drawText(QRectF(pad, line_y, width - 2 * pad, legend_line_h),
                              Qt.AlignLeft | Qt.AlignVCenter, text)

    return True

"""
Shared wing-planform drawing logic.

Used by BOTH the on-screen preview widget and the PDF export, so the two
stay geometrically identical -- only the color palette differs (dark theme
on screen, print-friendly light theme in the PDF). The caller owns the
QPainter (begin/end, fillRect, render hints) and supplies QPen objects for
each element so each context can pick its own colors.
"""

import math

from PySide6.QtCore import Qt, QRectF

from ghostmean.geometry import cg_from_percent_mac
from ghostmean.units import from_mm


def compute_wing_outline(panels):
    """Leading- and trailing-edge points along ONE side (right), as
    (y_span_mm, x_chord_mm) pairs, y=0 at the root, x=0 at the root
    leading edge. Mirror y for the left side."""
    y0 = 0.0
    x0 = 0.0
    pts_le = [(0.0, 0.0)]
    pts_te = [(0.0, panels[0].major_chord_mm if panels else 0.0)]
    for p in panels:
        theta = math.radians(p.sweep_deg)
        y1 = y0 + p.length_mm
        x1 = x0 + p.length_mm * math.tan(theta)
        pts_le.append((y1, x1))
        pts_te.append((y1, x1 + p.minor_chord_mm))
        y0, x0 = y1, x1
    return pts_le, pts_te


def draw_wing_plan(
    painter, width, height, panels, metrics,
    cg_targets,
    pen_outline, pen_mac, pen_cg, pen_axis, pen_dim,
    unit="mm",
    pad=30,
    show_panel_numbers=True,
    show_dimensions=True,
    label_font=None,
):
    """Paint the mirrored wing planform into `painter`'s coordinate space
    (width x height). Draws, in order: symmetry axis, outline, panel number
    labels, MAC line, CG markers (one per (label, percent) in cg_targets),
    and a total-span dimension line at the bottom.

    Returns False (and draws nothing) if there is no valid geometry to show.
    """
    if not panels or metrics is None or metrics.span_mm <= 0:
        return False

    reserve_bottom = 44 if show_dimensions else 0
    w = width - 2 * pad
    h = max(height - 2 * pad - reserve_bottom, 10)
    scale = min(w / metrics.span_mm, h / (metrics.mac_mm + max(p.major_chord_mm for p in panels)))
    scale = max(scale, 1e-6)

    cx = width / 2
    top_y = pad

    def X(y_span_signed):
        return cx + y_span_signed * scale

    def Y(x_chord):
        return top_y + x_chord * scale

    if label_font is not None:
        painter.setFont(label_font)

    # --- symmetry axis (full drawing height) ---
    painter.setPen(pen_axis)
    painter.drawLine(X(0), top_y, X(0), top_y + h)

    # --- outline ---
    pts_le_right, pts_te_right = compute_wing_outline(panels)
    painter.setPen(pen_outline)

    def draw_side(sign):
        le = [(sign * y, x) for y, x in pts_le_right]
        te = [(sign * y, x) for y, x in pts_te_right]
        for i in range(len(le) - 1):
            painter.drawLine(X(le[i][0]), Y(le[i][1]), X(le[i + 1][0]), Y(le[i + 1][1]))
            painter.drawLine(X(te[i][0]), Y(te[i][1]), X(te[i + 1][0]), Y(te[i + 1][1]))
        painter.drawLine(X(le[-1][0]), Y(le[-1][1]), X(te[-1][0]), Y(te[-1][1]))
        painter.drawLine(X(le[0][0]), Y(le[0][1]), X(te[0][0]), Y(te[0][1]))

    draw_side(1)
    draw_side(-1)

    # --- panel numbers (near the LE midpoint of each panel, both sides) ---
    if show_panel_numbers:
        painter.setPen(pen_outline)
        for i, p in enumerate(panels):
            y0_local, x0_local = pts_le_right[i]
            y1_local, x1_local = pts_le_right[i + 1]
            y_mid = (y0_local + y1_local) / 2
            x_mid_le = (x0_local + x1_local) / 2
            label = str(i + 1)
            for sign in (1, -1):
                painter.drawText(QRectF(X(sign * y_mid) - 10, Y(x_mid_le) - 20, 20, 16),
                                  Qt.AlignCenter, label)

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

    return True

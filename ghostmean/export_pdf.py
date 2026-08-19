"""
PDF export of the wing model: planform drawing + a results summary table.

Deliberately print-friendly (white page, dark ink) regardless of the app's
dark on-screen theme -- this is meant to be an actual printed reference
sheet for the workshop, not a screenshot.
"""

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPdfWriter, QPageSize

from ghostmean.drawing import draw_wing_plan
from ghostmean.geometry import cg_from_percent_mac
from ghostmean.units import from_mm


def export_wing_pdf(path, panels, metrics, custom_cg_percent, unit="mm"):
    writer = QPdfWriter(str(path))
    writer.setPageSize(QPageSize(QPageSize.A4))
    writer.setResolution(150)

    painter = QPainter(writer)
    painter.setRenderHint(QPainter.Antialiasing)

    page_rect = painter.viewport()
    w, h = page_rect.width(), page_rect.height()

    painter.fillRect(0, 0, w, h, QColor("white"))

    # --- title ---
    painter.setFont(QFont("Sans Serif", 18, QFont.Bold))
    painter.setPen(QColor("#0b0f14"))
    painter.drawText(QRectF(0, 20, w, 50), Qt.AlignHCenter, "GhostMEAN — Model skrzydła")

    # --- planform drawing ---
    draw_top = 100
    draw_h = min(int(h * 0.42), 620)
    has_geometry = bool(panels) and metrics is not None and metrics.span_mm > 0
    cg_targets = [
        ("25%", 25.0), ("28%", 28.0), ("30%", 30.0),
        (f"{custom_cg_percent:.0f}%", custom_cg_percent),
    ]
    if has_geometry:
        pen_outline = QPen(QColor("#0b3d61"), 4)
        pen_mac = QPen(QColor("#c46a00"), 3, Qt.DashLine)
        pen_cg = QPen(QColor("#0e7a35"), 3)
        pen_axis = QPen(QColor("#9aa5ad"), 2, Qt.DashDotLine)
        pen_dim = QPen(QColor("#444444"), 2)
        label_font = QFont("Sans Serif", 11)
        painter.save()
        painter.translate(0, draw_top)
        draw_wing_plan(
            painter, w, draw_h, panels, metrics, cg_targets,
            pen_outline, pen_mac, pen_cg, pen_axis, pen_dim,
            unit=unit, pad=60, label_font=label_font,
        )
        painter.restore()
    else:
        painter.setPen(QColor("#888888"))
        painter.drawText(QRectF(0, draw_top, w, draw_h), Qt.AlignCenter, "Brak danych panelu")

    # --- results table ---
    def fmt(v_mm):
        return f"{from_mm(v_mm, unit):.3f} {unit}"

    lines = []
    if has_geometry and metrics.area_mm2 > 0:
        if unit == "mm":
            area_val, area_unit = metrics.area_mm2 / 1_000_000.0, "m²"
        else:
            area_val, area_unit = metrics.area_mm2 / (25.4 * 25.4), "in²"
        lines = [
            ("Rozpiętość (Wing Span)", fmt(metrics.span_mm)),
            ("Powierzchnia (Area)", f"{area_val:.4f} {area_unit}"),
            ("Wydłużenie (Aspect Ratio)", f"{metrics.aspect_ratio:.3f}"),
            ("M.A.C.", fmt(metrics.mac_mm)),
            ("MAC — pozycja X", fmt(metrics.mac_le_x_mm)),
            ("MAC — pozycja Y", fmt(metrics.mac_y_mm)),
            ("CG 25% MAC (od LE na stacji MAC)", fmt(cg_from_percent_mac(metrics, 25.0))),
            ("CG 28% MAC (od LE na stacji MAC)", fmt(cg_from_percent_mac(metrics, 28.0))),
            ("CG 30% MAC (od LE na stacji MAC)", fmt(cg_from_percent_mac(metrics, 30.0))),
            (f"CG {custom_cg_percent:.0f}% MAC (niestandardowy)", fmt(cg_from_percent_mac(metrics, custom_cg_percent))),
        ]

    painter.setFont(QFont("Sans Serif", 13))
    painter.setPen(QColor("#0b0f14"))
    y = draw_top + draw_h + 30
    col1_x = int(w * 0.08)
    col2_x = int(w * 0.60)
    for caption, value in lines:
        painter.drawText(QRectF(col1_x, y, col2_x - col1_x - 10, 30), Qt.AlignLeft | Qt.AlignVCenter, caption)
        painter.drawText(QRectF(col2_x, y, w - col2_x - col1_x, 30), Qt.AlignLeft | Qt.AlignVCenter, value)
        y += 34

    painter.end()

"""
The "About" dialog -- shows the supplied splash graphic (ghostmean/assets/
about_splash.png) as-is, with real, clickable overlay widgets placed over
the picture's own drawn boxes: the version box (filled live from
ghostmean.__version__, never hardcoded) and the three link boxes at the
bottom (Project Wiki, GitHub, Get Support), plus the Close button.

The graphic itself is NOT redrawn or recreated with QPainter -- per the
request, only functional links are added on top of the existing image.
Overlay coordinates below are measured against the source image's native
1447x865 resolution, then scaled together with the image to fit the
dialog's max height (770px).
"""

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtWidgets import QDialog, QLabel, QPushButton

from ghostmean import __version__
from ghostmean.i18n import tr

ASSETS_DIR = Path(__file__).parent / "assets"
SPLASH_PATH = ASSETS_DIR / "about_splash.png"

# Native resolution of about_splash.png, and the max dialog height it gets
# scaled to fit (per spec: 770px max height, aspect ratio preserved).
NATIVE_W, NATIVE_H = 1447, 865
MAX_H = 770
SCALE = MAX_H / NATIVE_H

WIKI_URL = "https://github.com/nftomczain/GhostMEAN/wiki"
GITHUB_URL = "https://github.com/nftomczain/GhostMEAN"
SUPPORT_URL = "https://github.com/nftomczain/GhostMEAN/discussions"

# (x, y, w, h) in the image's NATIVE pixel space -- measured against the
# supplied graphic's own drawn boxes. Scaled by SCALE before use.
_NATIVE_RECTS = {
    "version": (943, 625, 195, 50),
    "wiki": (578, 737, 178, 82),
    "github": (778, 737, 193, 82),
    "support": (993, 737, 193, 82),
    "close": (1208, 737, 193, 82),
}


def _scaled_rect(name: str):
    x, y, w, h = _NATIVE_RECTS[name]
    return (round(x * SCALE), round(y * SCALE), round(w * SCALE), round(h * SCALE))


_OVERLAY_BUTTON_QSS = """
QPushButton {
    background: transparent;
    border: none;
}
QPushButton:hover {
    background: transparent; #rgba(79, 195, 255, 40);
    border-radius: 6px;
}
"""

_VERSION_LABEL_QSS = """
QLabel {
    background: transparent;
    color: #4fc3ff;
    font-size: 16pt;
    font-weight: bold;
}
"""


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("about_window_title"))
        self.setModal(True)

        img_w = round(NATIVE_W * SCALE)
        img_h = round(NATIVE_H * SCALE)
        self.setFixedSize(img_w, img_h)
        self.setMaximumHeight(MAX_H)

        background = QLabel(self)
        if SPLASH_PATH.exists():
            pixmap = QPixmap(str(SPLASH_PATH))
            if pixmap.isNull():
                # File exists but isn't a valid/loadable image (corrupted,
                # truncated download, wrong format) -- fail loudly rather
                # than silently rendering a black dialog.
                background.setText(f"⚠ Could not load image:\n{SPLASH_PATH}")
            else:
                pixmap = pixmap.scaled(
                    img_w, img_h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
                )
                background.setPixmap(pixmap)
        else:
            # Missing file -- same principle: visible and diagnosable,
            # not a silent black dialog.
            background.setText(f"⚠ Missing file:\n{SPLASH_PATH}")
            background.setStyleSheet("QLabel { color: #ff8080; font-size: 11pt; }")
        background.setAlignment(Qt.AlignCenter)
        background.setGeometry(0, 0, img_w, img_h)
        background.lower()

        # --- version label, overlaid on the graphic's empty VERSION box ---
        # Deliberately left empty in the source graphic -- filled here,
        # live, from ghostmean.__version__ (single source of truth, same
        # value as the window title bar and `ghostmean --version`).
        vx, vy, vw, vh = _scaled_rect("version")
        self.version_label = QLabel(f"v{__version__}", self)
        self.version_label.setGeometry(vx, vy, vw, vh)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet(_VERSION_LABEL_QSS)
        self.version_label.setAccessibleName(tr("about_version_accessible"))

        # --- the three link boxes + Close, overlaid as real buttons ---
        self._make_overlay_button("wiki", tr("about_link_wiki_accessible"), self._open_wiki)
        self._make_overlay_button("github", tr("about_link_github_accessible"), self._open_github)
        self._make_overlay_button("support", tr("about_link_support_accessible"), self._open_support)
        self._make_overlay_button("close", tr("about_close"), self.accept)

    def _make_overlay_button(self, rect_name: str, accessible_name: str, slot):
        x, y, w, h = _scaled_rect(rect_name)
        btn = QPushButton("", self)
        btn.setGeometry(x, y, w, h)
        btn.setStyleSheet(_OVERLAY_BUTTON_QSS)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setAccessibleName(accessible_name)
        btn.setToolTip(accessible_name)
        btn.clicked.connect(slot)
        return btn

    def _open_wiki(self):
        QDesktopServices.openUrl(QUrl(WIKI_URL))

    def _open_github(self):
        QDesktopServices.openUrl(QUrl(GITHUB_URL))

    def _open_support(self):
        QDesktopServices.openUrl(QUrl(SUPPORT_URL))

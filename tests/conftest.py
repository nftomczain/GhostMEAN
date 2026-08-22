"""
Shared pytest fixtures for the GhostMEAN test suite.

QT_QPA_PLATFORM is forced to "offscreen" before PySide6 is imported
anywhere, so the whole suite runs headless (CI, SSH sessions, this sandbox
-- none of them have a real display). A single session-scoped QApplication
is created once and reused, since Qt does not support multiple
QApplication instances in one process.
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest


@pytest.fixture(scope="session")
def qapp():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture(autouse=True)
def _reset_language():
    """Every test starts and ends on the default language ("pl"), so
    tests that switch languages (e.g. i18n / GUI tests) can't leak state
    into unrelated tests that run after them."""
    from ghostmean.i18n import set_language, DEFAULT_LANGUAGE
    set_language(DEFAULT_LANGUAGE)
    yield
    set_language(DEFAULT_LANGUAGE)

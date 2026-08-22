"""
About dialog tests. QDesktopServices.openUrl is monkeypatched in the link
tests so nothing actually tries to launch a real browser in a headless
test environment.
"""

import pytest

from ghostmean import __version__
from ghostmean.i18n import available_languages, set_language


class TestAboutDialogLayout:
    def test_respects_max_height_770(self, qapp):
        from ghostmean.about_dialog import AboutDialog, MAX_H
        dlg = AboutDialog()
        assert MAX_H == 770
        assert dlg.height() == 770
        assert dlg.maximumHeight() == 770

    def test_exactly_four_overlay_buttons(self, qapp):
        from ghostmean.about_dialog import AboutDialog
        from PySide6.QtWidgets import QPushButton
        dlg = AboutDialog()
        assert len(dlg.findChildren(QPushButton)) == 4

    def test_all_overlay_buttons_have_accessible_names(self, qapp):
        from ghostmean.about_dialog import AboutDialog
        from PySide6.QtWidgets import QPushButton
        dlg = AboutDialog()
        for btn in dlg.findChildren(QPushButton):
            assert btn.accessibleName() != ""


class TestAboutDialogVersion:
    def test_version_label_shows_the_real_dynamic_version(self, qapp):
        """Never hardcoded -- must always match ghostmean.__version__,
        the same single source of truth used by the window title and
        `ghostmean --version`."""
        from ghostmean.about_dialog import AboutDialog
        dlg = AboutDialog()
        assert dlg.version_label.text() == f"v{__version__}"

    def test_version_label_has_accessible_name(self, qapp):
        from ghostmean.about_dialog import AboutDialog
        dlg = AboutDialog()
        assert dlg.version_label.accessibleName() != ""


class TestAboutDialogLinks:
    def test_wiki_button_opens_correct_url(self, qapp, monkeypatch):
        from ghostmean import about_dialog
        opened = []
        monkeypatch.setattr(
            about_dialog.QDesktopServices, "openUrl",
            staticmethod(lambda url: opened.append(url.toString())),
        )
        dlg = about_dialog.AboutDialog()
        dlg._open_wiki()
        assert opened == [about_dialog.WIKI_URL]

    def test_github_button_opens_correct_url(self, qapp, monkeypatch):
        from ghostmean import about_dialog
        opened = []
        monkeypatch.setattr(
            about_dialog.QDesktopServices, "openUrl",
            staticmethod(lambda url: opened.append(url.toString())),
        )
        dlg = about_dialog.AboutDialog()
        dlg._open_github()
        assert opened == [about_dialog.GITHUB_URL]

    def test_support_button_opens_correct_url(self, qapp, monkeypatch):
        from ghostmean import about_dialog
        opened = []
        monkeypatch.setattr(
            about_dialog.QDesktopServices, "openUrl",
            staticmethod(lambda url: opened.append(url.toString())),
        )
        dlg = about_dialog.AboutDialog()
        dlg._open_support()
        assert opened == [about_dialog.SUPPORT_URL]

    def test_close_button_accepts_the_dialog(self, qapp):
        from ghostmean.about_dialog import AboutDialog
        from PySide6.QtWidgets import QDialog, QPushButton
        from PySide6.QtTest import QTest
        from PySide6.QtCore import Qt
        dlg = AboutDialog()
        dlg.show()
        close_btn = sorted(dlg.findChildren(QPushButton), key=lambda b: b.geometry().x())[-1]
        QTest.mouseClick(close_btn, Qt.LeftButton)
        assert dlg.result() == QDialog.Accepted


class TestAboutDialogI18n:
    @pytest.mark.parametrize("lang", available_languages())
    def test_dialog_opens_in_every_language_without_raising(self, qapp, lang):
        set_language(lang)
        from ghostmean.about_dialog import AboutDialog
        dlg = AboutDialog()  # must not raise
        assert dlg.windowTitle() != ""
        assert "about_window_title" not in dlg.windowTitle()
        set_language("pl")

    def test_help_menu_about_action_opens_dialog(self, qapp, monkeypatch):
        """End-to-end: MainWindow's Help > About actually shows the
        dialog (patching exec() so the test doesn't block on a modal
        loop)."""
        from ghostmean.gui import MainWindow
        from ghostmean import about_dialog
        opened = []
        monkeypatch.setattr(
            about_dialog.AboutDialog, "exec",
            lambda self: opened.append(True),
        )
        win = MainWindow()
        win.show()
        win._on_open_about()
        assert opened == [True]

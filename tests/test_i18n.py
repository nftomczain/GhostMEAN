"""
i18n tests -- "jeden test, który przełącza wszystkie języki i sprawdza,
czy GUI się nie wysypuje przez brakujący klucz."

Two layers: (1) pure data checks (key sets / placeholders match across all
language files, no GUI needed), and (2) an actual live GUI test that cycles
every registered language on a real MainWindow instance and confirms it
never raises and never silently falls back to the raw key string
(which would show up as literal "some_key" text in the UI).
"""

import re

import pytest

from ghostmean.i18n import LANGUAGES, DEFAULT_LANGUAGE, tr, set_language, available_languages


class TestLanguageFilesConsistency:
    def test_all_languages_have_identical_key_sets(self):
        ref_keys = set(LANGUAGES[DEFAULT_LANGUAGE].keys())
        assert len(ref_keys) > 0
        for lang, strings in LANGUAGES.items():
            assert set(strings.keys()) == ref_keys, f"{lang} has mismatched keys"

    def test_all_languages_have_identical_placeholders(self):
        """A template with a different set of {..} placeholders than the
        reference would raise a KeyError at .format() time when used --
        catch that here instead of at runtime."""
        placeholder_re = re.compile(r"\{([a-zA-Z_]+)")
        ref = LANGUAGES[DEFAULT_LANGUAGE]
        for key, ref_val in ref.items():
            ref_placeholders = set(placeholder_re.findall(ref_val))
            for lang, strings in LANGUAGES.items():
                val_placeholders = set(placeholder_re.findall(strings[key]))
                assert val_placeholders == ref_placeholders, (
                    f"key={key} lang={lang}: expected {ref_placeholders}, got {val_placeholders}"
                )

    def test_no_empty_translations(self):
        for lang, strings in LANGUAGES.items():
            for key, val in strings.items():
                assert val != "", f"{lang}.{key} is empty"

    @pytest.mark.parametrize("lang", list(LANGUAGES.keys()))
    def test_every_key_formats_without_raising(self, lang):
        """Feed every key a full set of plausible kwargs and confirm
        .format() doesn't blow up -- catches typos like {n} vs {N} that
        the placeholder-set check above wouldn't catch if both languages
        happened to share the typo."""
        set_language(lang)
        sample_kwargs = dict(
            n=1, a=1, b=2, p=3, v=12.5, bm=200.0, am=180.0, jump=-20.0, pct=25,
            path="/tmp/x.csv", version="0.4.12",
        )
        for key in LANGUAGES[lang]:
            tr(key, **sample_kwargs)  # must not raise


class TestLiveLanguageSwitching:
    """Actually drives a real MainWindow through every registered
    language -- this is the closest thing to 'czy GUI się nie wysypuje'."""

    def test_cycle_all_languages_no_crash(self, qapp):
        from ghostmean.gui import MainWindow

        win = MainWindow()
        win.show()
        # Give it some real geometry so recompute() has actual work to do
        # while switching languages (an empty wing would skip several
        # label-update code paths).
        win.rows[0].major.setValue(250.0)
        win.rows[0].minor.setValue(200.0)
        win.rows[0].length.setValue(300.0)
        win.rows[1].enabled.setChecked(True)
        win.rows[1].major.setValue(200.0)
        win.rows[1].minor.setValue(140.0)
        qapp.processEvents()

        for lang in available_languages():
            win.set_language_by_code(lang)
            qapp.processEvents()
            # A raw, untranslated key would appear literally in these
            # widgets (e.g. "results_title" instead of "Wyniki"/"Results")
            # if a key were missing for this language -- assert that
            # never happens for a representative sample of widgets.
            assert win.outputs_box.title() != "results_title"
            assert win.panels_box.title() != "panels_box_title"
            assert win.stations_box.title() != "stations_title"
            assert "_" not in win.units_label.text().replace(" ", "")

        win.close()

    def test_mac_value_identical_across_all_languages(self, qapp):
        """Switching languages must never touch the underlying numbers."""
        from ghostmean.gui import MainWindow

        win = MainWindow()
        win.show()
        win.rows[0].major.setValue(250.0)
        win.rows[0].minor.setValue(200.0)
        win.rows[0].length.setValue(300.0)
        qapp.processEvents()
        before = win.output_labels["mac"].text()

        for lang in available_languages():
            win.set_language_by_code(lang)
            qapp.processEvents()
            assert win.output_labels["mac"].text() == before

        win.close()

    def test_station_labels_translate_per_language(self, qapp):
        from ghostmean.gui import MainWindow

        win = MainWindow()
        win.show()
        win.rows[0].major.setValue(250.0)
        win.rows[0].minor.setValue(200.0)
        win.rows[0].length.setValue(300.0)
        qapp.processEvents()

        expected_root = {
            "pl": "Nasada", "en": "Root", "ru": "Корень крыла",
            "es": "Raíz", "de": "Flügelwurzel", "fr": "Emplanture",
        }
        for lang, expected in expected_root.items():
            win.set_language_by_code(lang)
            qapp.processEvents()
            assert win.stations_table.item(0, 0).text() == expected

        win.close()

    def test_discontinuity_warning_translates_and_does_not_crash(self, qapp):
        from ghostmean.gui import MainWindow

        win = MainWindow()
        win.show()
        win.rows[0].major.setValue(250.0)
        win.rows[0].minor.setValue(200.0)
        win.rows[0].length.setValue(300.0)
        win.rows[1].enabled.setChecked(True)
        win.rows[1].major.setValue(180.0)  # discontinuous vs panel 1's minor (200)
        win.rows[1].minor.setValue(140.0)
        qapp.processEvents()

        for lang in available_languages():
            win.set_language_by_code(lang)
            qapp.processEvents()
            assert win.warnings_label.text() != ""
            assert "warn_discontinuity" not in win.warnings_label.text()

        win.close()

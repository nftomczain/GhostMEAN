"""
Minimal i18n layer for GhostMEAN.

Each language is one flat dict of key -> template string, in its own file
(pl.py, en.py, ...). To add a new language:

  1. Copy pl.py to e.g. de.py and translate every value (keep the {..}
     placeholders exactly as they are -- they're filled in with .format()).
  2. Register it in LANGUAGES below.
  3. Add it to the language QComboBox in gui.py (LANGUAGE_CHOICES).

Nothing else in the app needs to change -- every user-facing string goes
through tr(key, **kwargs), so a new language file is immediately usable
everywhere (GUI, PDF export) once registered here.

Scope note: the station labels generated inside geometry.compute_stations()
("Nasada", "Końcówka", "S1", ...) are NOT yet routed through this layer --
translating those would mean threading a translation callback into a
otherwise UI-independent geometry module, which is a bigger, separate
decision. They stay Polish/ASCII for now regardless of the selected UI
language.
"""

from ghostmean.i18n import pl, en, ru, es, de, fr

LANGUAGES = {
    "pl": pl.STRINGS,
    "en": en.STRINGS,
    "ru": ru.STRINGS,
    "es": es.STRINGS,
    "de": de.STRINGS,
    "fr": fr.STRINGS,
}
DEFAULT_LANGUAGE = "pl"

_current_language = DEFAULT_LANGUAGE


def set_language(code: str) -> None:
    global _current_language
    if code in LANGUAGES:
        _current_language = code


def get_language() -> str:
    return _current_language


def available_languages() -> list[str]:
    return list(LANGUAGES.keys())


def tr(key: str, **kwargs) -> str:
    """Look up `key` in the current language, falling back to the default
    language, then to the raw key itself (so a missing translation is
    visibly wrong rather than silently blank or crashing)."""
    strings = LANGUAGES.get(_current_language, LANGUAGES[DEFAULT_LANGUAGE])
    template = strings.get(key)
    if template is None:
        template = LANGUAGES[DEFAULT_LANGUAGE].get(key, key)
    return template.format(**kwargs) if kwargs else template

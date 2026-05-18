import locale
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# Pfad zum locales-Ordner auflösen
LOCALES_DIR = Path(__file__).parent / "locales"

# Zwischenspeicher für geladene Übersetzungen
_TRANSLATIONS_CACHE: Dict[str, Dict[str, Any]] = {}


def get_system_lang() -> str:
    """Ermittelt die Systemsprache. Standard: en."""
    try:
        # Versuche Systemsprache zu ermitteln
        lang_code = locale.getdefaultlocale()[0]
        if lang_code:
            lang_code = lang_code.split("_")[0].lower()
            return lang_code
    except Exception:
        pass

    # Fallback auf Umgebungsvariablen
    env_lang = os.environ.get("LANG", "en")
    if "_" in env_lang:
        return env_lang.split("_")[0].lower()
    if "." in env_lang:
        return env_lang.split(".")[0].lower()

    return env_lang.lower()


# Aktuelle Sprache festlegen
CURRENT_LANG = get_system_lang()


def set_language(lang: str) -> None:
    """Setzt die aktuelle Sprache manuell (primär für Tests)."""
    global CURRENT_LANG
    CURRENT_LANG = lang


def load_translations(lang: str) -> Dict[str, Any]:
    """Lädt die Übersetzungen aus der entsprechenden YAML-Datei."""
    if lang in _TRANSLATIONS_CACHE:
        return _TRANSLATIONS_CACHE[lang]

    file_path = LOCALES_DIR / f"{lang}.yaml"

    # Fallback auf Englisch, falls Sprache nicht existiert
    if not file_path.exists():
        file_path = LOCALES_DIR / "en.yaml"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            translations = yaml.safe_load(f)
            if not isinstance(translations, dict):
                return {}
            _TRANSLATIONS_CACHE[lang] = translations
            return translations
    except Exception:
        return {}


def _get_nested(data: Dict[str, Any], path: str) -> Optional[str]:
    """Sucht einen Wert in einem verschachtelten Dictionary mittels Punkt-Notation."""
    keys = path.split(".")
    current: Any = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return str(current) if current is not None else None


def _(key: str, **kwargs: Any) -> str:
    """Übersetzt einen Schlüssel (Punkt-Notation unterstützt) in die aktuelle Sprache."""
    translations = load_translations(CURRENT_LANG)

    # Suche in verschachtelter Struktur
    text = _get_nested(translations, key)

    # Fallback auf flache Suche oder den Key selbst
    if text is None:
        text = str(translations.get(key, key))

    if kwargs:
        return text.format(**kwargs)
    return text

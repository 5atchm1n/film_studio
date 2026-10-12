"""i18n: on-screen text is written in English; a film provides a FR dict (English → French).

FILM_LANG=en (default) or fr selects the language at render time.
"""

import os

LANGS = ("en", "fr")


def current_lang() -> str:
    lang = os.environ.get("FILM_LANG", "en")
    if lang not in LANGS:
        raise ValueError(f"FILM_LANG={lang} (expected one of {', '.join(LANGS)})")
    return lang


class Translator:
    """tr = Translator(FR); tr("TRUST") → "CONFIANCE" when FILM_LANG=fr, "TRUST" otherwise."""

    def __init__(self, fr: dict, lang: str | None = None):
        self.fr, self.lang = fr, lang or current_lang()

    def __call__(self, text: str) -> str:
        return self.fr.get(text, text) if self.lang == "fr" else text

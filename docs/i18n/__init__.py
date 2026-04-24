"""i18n support for ReportLab documentation generation."""
import os

_active_lang = 'en'

def set_language(lang):
    global _active_lang
    _active_lang = lang

def get_language():
    return _active_lang

def get_strings():
    """Return the active string catalog. Falls back to English for missing keys."""
    from docs.i18n import en as default
    if _active_lang == 'en':
        return default
    try:
        mod = __import__('docs.i18n.' + _active_lang.replace('-', '_'), fromlist=['_'])
        merged = {}
        for k in dir(default):
            if not k.startswith('_'):
                merged[k] = getattr(default, k)
        for k in dir(mod):
            if not k.startswith('_'):
                merged[k] = getattr(mod, k)
        return type('Strings', (), merged)()
    except ImportError:
        return default

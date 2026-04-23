#Copyright (c) 2025-2026, selcarpa
#see LICENSE for license details
"""Shared helpers for TTFont fallback test suite."""
import os, unittest
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Font paths
# ---------------------------------------------------------------------------
_projectRoot = os.path.dirname(os.path.dirname(__file__))
_srcFontsDir = os.path.join(_projectRoot, 'src', 'reportlab', 'fonts')
_testsResDir = os.path.join(_projectRoot, 'tests_resource')

veraPath = os.path.join(_srcFontsDir, 'Vera.ttf')
veraBdPath = os.path.join(_srcFontsDir, 'VeraBd.ttf')

notoSCPath = os.path.join(_testsResDir, 'NotoSansSC-Regular.ttf')
notoKRPath = os.path.join(_testsResDir, 'NotoSansKR-Bold.ttf')
gentiumBIPath = os.path.join(_testsResDir, 'Gentium-BoldItalic.ttf')
theanoDidotPath = os.path.join(_testsResDir, 'TheanoDidot-Regular.ttf')
emojiPath = os.path.join(_testsResDir, 'NotoEmoji-Regular.ttf')

# ---------------------------------------------------------------------------
# Availability checks
# ---------------------------------------------------------------------------
_has_all_external = all(
    os.path.isfile(p) for p in [notoSCPath, notoKRPath, gentiumBIPath, theanoDidotPath, emojiPath]
)

_missing_fonts = []
for _name, _path in [
    ('NotoSansSC-Regular.ttf', notoSCPath),
    ('NotoSansKR-Bold.ttf', notoKRPath),
    ('Gentium-BoldItalic.ttf', gentiumBIPath),
    ('TheanoDidot-Regular.ttf', theanoDidotPath),
    ('NotoEmoji-Regular.ttf', emojiPath),
]:
    if not os.path.isfile(_path):
        _missing_fonts.append(_name)

# ---------------------------------------------------------------------------
# Registration helpers
# ---------------------------------------------------------------------------
def registerVera():
    if 'Vera' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('Vera', veraPath))
    if 'VeraBd' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('VeraBd', veraBdPath))

def registerExternalFonts():
    """Register external test fonts. Returns True if all fonts are available."""
    if not _has_all_external:
        return False
    if 'NotoSC' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('NotoSC', notoSCPath))
    if 'NotoKR' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('NotoKR', notoKRPath))
    if 'GentiumBI' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('GentiumBI', gentiumBIPath))
    if 'TheanoDidot' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('TheanoDidot', theanoDidotPath))
    if 'NotoEmoji' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('NotoEmoji', emojiPath))
    return True

def skipUnlessExternalFonts():
    """Decorator for tests requiring external fonts."""
    return unittest.skipUnless(
        _has_all_external,
        'Missing font files in tests_resource/: %s. '
        'See tests_resource/README.md for setup instructions.' % ', '.join(_missing_fonts)
    )

#Copyright (c) 2025-2026, selcarpa
#see LICENSE for license details
__version__='3.3.0'
"""Core TTFont fallback tests — unicode2TT, hasGlyph, env var control, stringWidth.
Uses only internal Vera fonts; no external dependencies."""
from reportlab.lib.testutils import setOutDir, makeSuiteForClasses, printLocation
if __name__=='__main__':
    setOutDir(__name__)
import unittest, os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.rl_accel import unicode2TT, instanceStringWidthTTF
from _ttfont_fallback_helpers import registerVera, veraPath, veraBdPath

class Unicode2TTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registerVera()
        cls.font = pdfmetrics.getFont('Vera')
        cls.fontBd = pdfmetrics.getFont('VeraBd')

    def test_T01_basic(self):
        """Pure ASCII text returns single (font, text) pair"""
        result = unicode2TT("Hello", [self.font])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.font)
        self.assertEqual(result[0][1], "Hello")

    def test_T02_fallback_no_split(self):
        """Both fonts have ASCII → no split"""
        result = unicode2TT("AB", [self.font, self.fontBd])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.font)

    def test_T03_all_missing(self):
        """All fonts missing a glyph falls back to main font"""
        text = "你好"
        result = unicode2TT(text, [self.font, self.fontBd])
        self.assertTrue(len(result) >= 1)
        for fbFont, fbText in result:
            self.assertIs(fbFont, self.font)

    def test_T04_empty_text(self):
        """Empty text returns empty list"""
        result = unicode2TT("", [self.font])
        self.assertEqual(result, [])

    def test_T05_nbsp(self):
        """NBSP is treated as space"""
        text = "A B"
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], text)

    def test_T06_consecutive_same_font(self):
        """Consecutive same-font chars merged into single fragment"""
        result = unicode2TT("Hello World", [self.font])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Hello World")

    def test_T07_single_font(self):
        """Single font always returns single fragment"""
        result = unicode2TT("ABC", [self.font])
        self.assertEqual(len(result), 1)

    def test_long_ascii(self):
        """Long ASCII text stays as single fragment"""
        text = "The quick brown fox jumps over the lazy dog. " * 20
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], text)

    def test_repeated_missing_chars(self):
        """Many consecutive missing chars form a single fallback fragment"""
        text = "你好世界字体测试"
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.font)
        self.assertEqual(result[0][1], text)

    def test_mixed_ascii_missing_interleaved(self):
        """ASCII and missing chars produce alternating fragments"""
        text = "A你B好C世D"
        result = unicode2TT(text, [self.font])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)

    def test_all_spaces_and_nbsp(self):
        """Mix of spaces and NBSP"""
        text = "     "
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)

    def test_single_char(self):
        """Single character"""
        result = unicode2TT("X", [self.font])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "X")

    def test_single_missing_char(self):
        """Single missing character"""
        result = unicode2TT("你", [self.font])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.font)

    def test_control_chars(self):
        """Control characters (no glyph) fall back to main font"""
        text = "\x01\x02\x03"
        result = unicode2TT(text, [self.font])
        self.assertTrue(len(result) >= 1)

    def test_emoji_no_fallback_font(self):
        """Emoji chars with no emoji font in chain → all map to main font"""
        text = "Hi😀🎉"
        result = unicode2TT(text, [self.font])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)

    def test_long_mixed_with_nbsp(self):
        """Long text with NBSP interspersed"""
        text = "Hello World Test " * 10
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)


class HasGlyphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registerVera()
        cls.font = pdfmetrics.getFont('Vera')

    def test_existing_char_str(self):
        self.assertTrue(self.font.hasGlyph('A'))

    def test_existing_char_int(self):
        self.assertTrue(self.font.hasGlyph(ord('A')))

    def test_missing_char(self):
        self.assertFalse(self.font.hasGlyph(0x4F60))

    def test_nbsp(self):
        self.assertEqual(self.font.hasGlyph(' '), self.font.hasGlyph(' '))

    def test_ascii_range(self):
        """Check full printable ASCII range"""
        for code in range(32, 127):
            self.assertTrue(self.font.hasGlyph(code), 'Missing glyph U+%04X' % code)

    def test_multiple_missing_scripts(self):
        """Check CJK, Cyrillic, Emoji, Thai"""
        for code in [0x4F60, 0x597D, 0x4E16, 0x754C,
                     0x0401, 0x0410, 0x042F,
                     0x1F600,
                     0x0E01, 0x0E02]:
            self.assertFalse(self.font.hasGlyph(code), 'Unexpected glyph U+%04X' % code)

    def test_digits(self):
        for i in range(10):
            self.assertTrue(self.font.hasGlyph(str(i)))

    def test_punctuation(self):
        for ch in r'.,;:!?"''()-_+=[]{}|/<>@#$%^&*~`':
            self.assertTrue(self.font.hasGlyph(ch), 'Missing %r' % ch)


class EnvVarControlTest(unittest.TestCase):
    def setUp(self):
        registerVera()
        self.font = pdfmetrics.getFont('Vera')
        self._orig_env = os.environ.get('REPORTLAB_FONT_FALLBACK', None)

    def tearDown(self):
        if self._orig_env is None:
            os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        else:
            os.environ['REPORTLAB_FONT_FALLBACK'] = self._orig_env

    def test_T09_disabled_by_default(self):
        """substitutionFonts returns [] when env var not set"""
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        fb = TTFont('TestT09', veraPath)
        fb._substitutionFonts = [self.font]
        self.assertEqual(fb.substitutionFonts, [])

    def test_T10_enabled_by_env(self):
        """substitutionFonts returns actual list when env var is '1'"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        fb = TTFont('TestT10', veraPath)
        pdfmetrics.registerFont(fb)
        fb.substitutionFonts = [self.font]
        self.assertEqual(fb.substitutionFonts, [self.font])

    def test_T11_runtime_toggle(self):
        """Runtime toggle of env var changes behavior"""
        fb = TTFont('TestT11', veraPath)
        pdfmetrics.registerFont(fb)
        fb._substitutionFonts = [self.font]

        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        self.assertEqual(fb.substitutionFonts, [self.font])

        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        self.assertEqual(fb.substitutionFonts, [])

        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        self.assertEqual(fb.substitutionFonts, [self.font])


class StringWidthTest(unittest.TestCase):
    def setUp(self):
        registerVera()
        self._orig_env = os.environ.get('REPORTLAB_FONT_FALLBACK', None)

    def tearDown(self):
        if self._orig_env is None:
            os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        else:
            os.environ['REPORTLAB_FONT_FALLBACK'] = self._orig_env

    def test_T12_no_fallback(self):
        """Width without fallback matches original"""
        font = pdfmetrics.getFont('Vera')
        w1 = instanceStringWidthTTF(font, "Hello World", 10)
        w2 = pdfmetrics.stringWidth("Hello World", "Vera", 10)
        self.assertAlmostEqual(w1, w2, places=4)

    def test_T13_with_fallback_no_env(self):
        """Width with fallback set but env var off = same as original"""
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        font = pdfmetrics.getFont('Vera')
        w = pdfmetrics.stringWidth("Hello", "Vera", 10)
        font.substitutionFonts = [pdfmetrics.getFont('VeraBd')]
        w2 = pdfmetrics.stringWidth("Hello", "Vera", 10)
        self.assertAlmostEqual(w, w2, places=4)

    def test_T14_with_fallback_enabled(self):
        """Width with fallback enabled for ASCII text"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        font = pdfmetrics.getFont('Vera')
        fontBd = pdfmetrics.getFont('VeraBd')
        font.substitutionFonts = [fontBd]
        w = pdfmetrics.stringWidth("Hello", "Vera", 10)
        self.assertAlmostEqual(w, pdfmetrics.stringWidth("Hello", "Vera", 10), places=4)
        font.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)


def makeSuite():
    return makeSuiteForClasses(
        Unicode2TTTest,
        HasGlyphTest,
        EnvVarControlTest,
        StringWidthTest,
    )


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())
    printLocation()

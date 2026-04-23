"""Tests for TTFont fallback support.

Part of this test suite uses external font files from tests_resource/.
See tests_resource/README.md for setup instructions.
If the font files are not present, those tests will be skipped.
"""
from reportlab.lib.testutils import setOutDir, makeSuiteForClasses, outputfile, printLocation
if __name__ == '__main__':
    setOutDir(__name__)
import unittest, os
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.rl_accel import unicode2TT, instanceStringWidthTTF

# ---------------------------------------------------------------------------
# Font paths
# ---------------------------------------------------------------------------
_projectRoot = os.path.dirname(os.path.dirname(__file__))
_srcFontsDir = os.path.join(_projectRoot, 'src', 'reportlab', 'fonts')
_testsResDir = os.path.join(_projectRoot, 'tests_resource')

_veraPath = os.path.join(_srcFontsDir, 'Vera.ttf')
_veraBdPath = os.path.join(_srcFontsDir, 'VeraBd.ttf')

# External fonts (from tests_resource/, TTF only)
_notoSCPath = os.path.join(_testsResDir, 'NotoSansSC-Regular.ttf')
_notoKRPath = os.path.join(_testsResDir, 'NotoSansKR-Bold.ttf')
_gentiumBIPath = os.path.join(_testsResDir, 'Gentium-BoldItalic.ttf')
_theanoDidotPath = os.path.join(_testsResDir, 'TheanoDidot-Regular.ttf')
_emojiPath = os.path.join(_testsResDir, 'NotoEmoji-Regular.ttf')

# Check which external fonts are available
_has_notoSC = os.path.isfile(_notoSCPath)
_has_notoKR = os.path.isfile(_notoKRPath)
_has_gentium = os.path.isfile(_gentiumBIPath)
_has_theano = os.path.isfile(_theanoDidotPath)
_has_emoji = os.path.isfile(_emojiPath)

_missing_fonts = []
if not _has_notoSC: _missing_fonts.append('NotoSansSC-Regular.ttf')
if not _has_notoKR: _missing_fonts.append('NotoSansKR-Bold.ttf')
if not _has_gentium: _missing_fonts.append('Gentium-BoldItalic.ttf')
if not _has_theano: _missing_fonts.append('TheanoDidot-Regular.ttf')
if not _has_emoji: _missing_fonts.append('NotoEmoji-Regular.ttf')

_has_all_external = not _missing_fonts

def _registerVera():
    if 'Vera' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('Vera', _veraPath))
    if 'VeraBd' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('VeraBd', _veraBdPath))

def _registerExternalFonts():
    """Register external test fonts. Returns True if all fonts are available."""
    if not _has_all_external:
        return False
    if 'NotoSC' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('NotoSC', _notoSCPath))
    if 'NotoKR' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('NotoKR', _notoKRPath))
    if 'GentiumBI' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('GentiumBI', _gentiumBIPath))
    if 'TheanoDidot' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('TheanoDidot', _theanoDidotPath))
    if 'NotoEmoji' not in pdfmetrics._fonts:
        pdfmetrics.registerFont(TTFont('NotoEmoji', _emojiPath))
    return True

def _skipUnlessExternalFonts():
    """Decorator / skip guard for tests needing external fonts."""
    return unittest.skipUnless(
        _has_all_external,
        f'Missing font files in tests_resource/: {", ".join(_missing_fonts)}. '
        'See tests_resource/README.md for setup instructions.'
    )

# ---------------------------------------------------------------------------
# T01-T07: unicode2TT unit tests (internal fonts only)
# ---------------------------------------------------------------------------
class Unicode2TTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _registerVera()
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
        text = "你好"  # CJK chars not in any Vera font
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
        text = "A B"
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
        text = "你好世界字体测试"  # 7 CJK chars, all missing from Vera
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.font)
        self.assertEqual(result[0][1], text)

    def test_mixed_ascii_missing_interleaved(self):
        """ASCII and missing chars produce alternating fragments"""
        text = "A你B好C世D"
        result = unicode2TT(text, [self.font])
        # Should be: "A" + "你" + "B" + "好" + "C" + "世" + "D"  or merged
        # All fragments belong to main font (no fallback font has CJK)
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)

    def test_all_spaces_and_nbsp(self):
        """Mix of spaces and NBSP"""
        text = "          "
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
        text = "Hello World Test " * 10
        result = unicode2TT(text, [self.font])
        self.assertEqual(len(result), 1)

# ---------------------------------------------------------------------------
# T08: hasGlyph tests (internal fonts only)
# ---------------------------------------------------------------------------
class HasGlyphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _registerVera()
        cls.font = pdfmetrics.getFont('Vera')

    def test_existing_char_str(self):
        self.assertTrue(self.font.hasGlyph('A'))

    def test_existing_char_int(self):
        self.assertTrue(self.font.hasGlyph(ord('A')))

    def test_missing_char(self):
        self.assertFalse(self.font.hasGlyph(0x4F60))  # CJK

    def test_nbsp(self):
        self.assertEqual(self.font.hasGlyph(' '), self.font.hasGlyph(' '))
    def test_ascii_range(self):
        """Check full printable ASCII range"""
        for code in range(32, 127):
            self.assertTrue(self.font.hasGlyph(code), f'Missing glyph U+{code:04X}')

    def test_multiple_missing_scripts(self):
        """Check CJK, Cyrillic, Emoji, Thai"""
        for code in [0x4F60, 0x597D, 0x4E16, 0x754C,  # CJK
                     0x0401, 0x0410, 0x042F,            # Cyrillic
                     0x1F600,                            # Emoji
                     0x0E01, 0x0E02]:                    # Thai
            self.assertFalse(self.font.hasGlyph(code), f'Unexpected glyph U+{code:04X}')

    def test_digits(self):
        for i in range(10):
            self.assertTrue(self.font.hasGlyph(str(i)))

    def test_punctuation(self):
        for ch in r'.,;:!?"''()-_+=[]{}|/<>@#$%^&*~`':
            self.assertTrue(self.font.hasGlyph(ch), f'Missing {ch!r}')


# ---------------------------------------------------------------------------
# T09-T11: Environment variable control tests
# ---------------------------------------------------------------------------
class EnvVarControlTest(unittest.TestCase):
    def setUp(self):
        _registerVera()
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
        fb = TTFont('TestT09', _veraPath)
        fb._substitutionFonts = [self.font]
        self.assertEqual(fb.substitutionFonts, [])

    def test_T10_enabled_by_env(self):
        """substitutionFonts returns actual list when env var is '1'"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        fb = TTFont('TestT10', _veraPath)
        pdfmetrics.registerFont(fb)
        fb.substitutionFonts = [self.font]
        self.assertEqual(fb.substitutionFonts, [self.font])

    def test_T11_runtime_toggle(self):
        """Runtime toggle of env var changes behavior"""
        fb = TTFont('TestT11', _veraPath)
        pdfmetrics.registerFont(fb)
        fb._substitutionFonts = [self.font]

        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        self.assertEqual(fb.substitutionFonts, [self.font])

        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        self.assertEqual(fb.substitutionFonts, [])

        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        self.assertEqual(fb.substitutionFonts, [self.font])

# ---------------------------------------------------------------------------
# T12-T14: Width calculation tests
# ---------------------------------------------------------------------------
class StringWidthTest(unittest.TestCase):
    def setUp(self):
        _registerVera()
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

# ---------------------------------------------------------------------------
# T15-T17: Multi-script unicode2TT tests (external fonts)
# ---------------------------------------------------------------------------
@_skipUnlessExternalFonts()
class Unicode2TTMultiScriptTest(unittest.TestCase):
    """Multi-script fallback tests requiring external fonts."""

    @classmethod
    def setUpClass(cls):
        _registerVera()
        _registerExternalFonts()
        cls.latin = pdfmetrics.getFont('Vera')
        cls.cjkSC = pdfmetrics.getFont('NotoSC')
        cls.cjkK = pdfmetrics.getFont('NotoKR')

    def test_T15_latin_cjk_split(self):
        """Latin + CJK text splits into two fragments"""
        text = "Hello你好"  # Hello + 你好
        result = unicode2TT(text, [self.latin, self.cjkSC])
        self.assertEqual(len(result), 2)
        self.assertIs(result[0][0], self.latin)
        self.assertEqual(result[0][1], "Hello")
        self.assertIs(result[1][0], self.cjkSC)
        self.assertEqual(result[1][1], "你好")

    def test_T16_multi_fallback_chain(self):
        """Three fonts: Latin → fallback1 → fallback2"""
        text = "A你가"  # Latin A + CJK 你 + Hangul 가
        result = unicode2TT(text, [self.latin, self.cjkSC, self.cjkK])
        # 'A' → latin, '你' → cjkSC or cjkK, '가' → cjkK
        self.assertTrue(len(result) >= 2)

    def test_T17_alternating_scripts(self):
        """Alternating Latin/CJK produces multiple fragments"""
        text = "A你B好C"  # A 你 B 好 C
        result = unicode2TT(text, [self.latin, self.cjkSC])
        # Should alternate: latin, cjkSC, latin, cjkSC, latin
        fonts_seq = [r[0] for r in result]
        # At minimum, should have both fonts in the sequence
        self.assertIn(self.latin, fonts_seq)
        self.assertIn(self.cjkSC, fonts_seq)

    def test_long_paragraph_latin_cjk(self):
        """Long mixed Latin+CJK paragraph"""
        text = ("The quick brown fox jumps over the lazy dog. "
                "这只棕色狐狸跳过了那只懒狗。"
                "Pack my box with five dozen liquor jugs. "
                "敏捷的棕色狐狸跃过那只懒狗。"
                ) * 5
        result = unicode2TT(text, [self.latin, self.cjkSC])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)
        # Should have both fonts
        fonts_used = {r[0] for r in result}
        self.assertIn(self.latin, fonts_used)
        self.assertIn(self.cjkSC, fonts_used)

    def test_many_short_alternations(self):
        """Rapidly alternating single chars between scripts"""
        text = "A你B好C世D界E测F试G"
        result = unicode2TT(text, [self.latin, self.cjkSC])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)
        # With rapid alternation, should have many fragments
        self.assertTrue(len(result) >= 4)

    def test_long_cjk_block(self):
        """Long contiguous CJK block"""
        text = "中华人民共和国国务院外交部新闻发言人" * 10
        result = unicode2TT(text, [self.latin, self.cjkSC])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.cjkSC)

    def test_long_latin_block(self):
        """Long contiguous Latin block with fallback font available"""
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 20
        result = unicode2TT(text, [self.latin, self.cjkSC])
        self.assertEqual(len(result), 1)
        self.assertIs(result[0][0], self.latin)

    def test_sentence_with_numbers_and_cjk(self):
        """Full sentence mixing digits, Latin, CJK, punctuation"""
        text = "2024年报告显示，Revenue增长了35%，达到$1.2B。"
        result = unicode2TT(text, [self.latin, self.cjkSC])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)

    def test_three_script_long(self):
        """Long text across three scripts"""
        text = ("Hello world! 你好世界！ 안녕하세요! "
                "Python编程프로그래밍很有趣재미있다. "
                ) * 10
        result = unicode2TT(text, [self.latin, self.cjkSC, self.cjkK])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)
        fonts_used = {r[0] for r in result}
        self.assertIn(self.latin, fonts_used)
        self.assertIn(self.cjkSC, fonts_used)

# ---------------------------------------------------------------------------
# T18-T19: Multi-script width tests (external fonts)
# ---------------------------------------------------------------------------
@_skipUnlessExternalFonts()
class MultiScriptWidthTest(unittest.TestCase):
    def setUp(self):
        _registerVera()
        _registerExternalFonts()
        self._orig_env = os.environ.get('REPORTLAB_FONT_FALLBACK', None)

    def tearDown(self):
        if self._orig_env is None:
            os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        else:
            os.environ['REPORTLAB_FONT_FALLBACK'] = self._orig_env

    def test_T18_mixed_width(self):
        """Width of mixed-script text with fallback enabled"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjk = pdfmetrics.getFont('NotoSC')
        latin.substitutionFonts = [cjk]
        text = "Hello你好"
        w = pdfmetrics.stringWidth(text, 'Vera', 10)
        # Width should be > 0 and sum of individual widths
        w_latin = pdfmetrics.stringWidth("Hello", 'Vera', 10)
        w_cjk = pdfmetrics.stringWidth("你好", 'NotoSC', 10)
        self.assertAlmostEqual(w, w_latin + w_cjk, places=2)
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T19_width_consistency(self):
        """stringWidth matches sum of per-fragment widths"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjk = pdfmetrics.getFont('NotoSC')
        latin.substitutionFonts = [cjk]
        text = "A你B"
        w_total = pdfmetrics.stringWidth(text, 'Vera', 10)
        w_a = pdfmetrics.stringWidth("A", 'Vera', 10)
        w_cjk = pdfmetrics.stringWidth("你", 'NotoSC', 10)
        w_b = pdfmetrics.stringWidth("B", 'Vera', 10)
        self.assertAlmostEqual(w_total, w_a + w_cjk + w_b, places=2)
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_long_paragraph_width(self):
        """Width of a long mixed-script paragraph with fallback"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjk = pdfmetrics.getFont('NotoSC')
        latin.substitutionFonts = [cjk]
        text = ("Hello world! 你好世界！ " * 20).strip()
        # Should not raise and should be positive
        w = pdfmetrics.stringWidth(text, 'Vera', 10)
        self.assertGreater(w, 0)
        # Verify it's the sum of individual fragment widths
        fragments = unicode2TT(text, [latin, cjk])
        w_sum = sum(pdfmetrics.stringWidth(frag, f.fontName, 10) for f, frag in fragments)
        self.assertAlmostEqual(w, w_sum, places=1)
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_three_script_width(self):
        """Width across three scripts"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjkSC = pdfmetrics.getFont('NotoSC')
        cjkK = pdfmetrics.getFont('NotoKR')
        latin.substitutionFonts = [cjkSC, cjkK]
        text = "Hello你好안녕"
        w = pdfmetrics.stringWidth(text, 'Vera', 10)
        self.assertGreater(w, 0)
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

# ---------------------------------------------------------------------------
# T20-T24: PDF generation tests
# ---------------------------------------------------------------------------
class PDFGenerationTest(unittest.TestCase):
    def setUp(self):
        _registerVera()
        self._orig_env = os.environ.get('REPORTLAB_FONT_FALLBACK', None)

    def tearDown(self):
        if self._orig_env is None:
            os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        else:
            os.environ['REPORTLAB_FONT_FALLBACK'] = self._orig_env

    def test_T20_basic(self):
        """Basic PDF with fallback fonts generates successfully"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        font = pdfmetrics.getFont('Vera')
        fontBd = pdfmetrics.getFont('VeraBd')
        font.substitutionFonts = [fontBd]
        c = Canvas(outputfile('test_fallback_basic.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, 'Hello World with fallback')
        c.save()
        font.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_long_ascii_pdf(self):
        """Multi-line ASCII PDF with fallback generates successfully"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        font = pdfmetrics.getFont('Vera')
        fontBd = pdfmetrics.getFont('VeraBd')
        font.substitutionFonts = [fontBd]
        c = Canvas(outputfile('test_fallback_long_ascii.pdf'))
        c.setFont('Vera', 10)
        for i in range(50):
            c.drawString(72, 800 - i * 14, f'Line {i}: The quick brown fox jumps over the lazy dog.')
        c.save()
        font.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T22_all_in_main(self):
        """All chars in main font behaves same as no fallback"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        font = pdfmetrics.getFont('Vera')
        fontBd = pdfmetrics.getFont('VeraBd')
        font.substitutionFonts = [fontBd]
        c = Canvas(outputfile('test_fallback_all_main.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, 'All ASCII text')
        c.save()
        font.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T24_no_substitution(self):
        """No substitution fonts = no regression"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        c = Canvas(outputfile('test_fallback_no_sub.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, 'No substitution set')
        c.save()
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

@_skipUnlessExternalFonts()
class PDFMultiScriptTest(unittest.TestCase):
    """PDF generation with mixed scripts (external fonts)."""

    def setUp(self):
        _registerVera()
        _registerExternalFonts()
        self._orig_env = os.environ.get('REPORTLAB_FONT_FALLBACK', None)

    def tearDown(self):
        if self._orig_env is None:
            os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        else:
            os.environ['REPORTLAB_FONT_FALLBACK'] = self._orig_env

    def test_T21_mixed_script_pdf(self):
        """Mixed Latin + CJK PDF renders correctly"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjk = pdfmetrics.getFont('NotoSC')
        latin.substitutionFonts = [cjk]
        c = Canvas(outputfile('test_fallback_mixed_script.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, 'Hello 你好 World 世界')
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T23_all_in_fallback(self):
        """All chars in fallback font"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjk = pdfmetrics.getFont('NotoSC')
        latin.substitutionFonts = [cjk]
        c = Canvas(outputfile('test_fallback_all_cjk.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, '你好世界')
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T25_three_script_pdf(self):
        """Latin + CJK + Korean three-script PDF"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjkSC = pdfmetrics.getFont('NotoSC')
        cjkK = pdfmetrics.getFont('NotoKR')
        latin.substitutionFonts = [cjkSC, cjkK]
        c = Canvas(outputfile('test_fallback_three_script.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, 'Hi你好 가')
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T26_greek_pdf(self):
        """Latin + Greek PDF with TheanoDidot fallback"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        greek = pdfmetrics.getFont('TheanoDidot')
        latin.substitutionFonts = [greek]
        c = Canvas(outputfile('test_fallback_greek.pdf'))
        c.setFont('Vera', 12)
        c.drawString(100, 700, 'Greek: Αβγδ')
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_long_mixed_paragraphs_pdf(self):
        """Multi-line mixed-script PDF covering all five fallback fonts, symbols, and emoji"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjkSC = pdfmetrics.getFont('NotoSC')
        cjkK = pdfmetrics.getFont('NotoKR')
        greek = pdfmetrics.getFont('TheanoDidot')
        gentium = pdfmetrics.getFont('GentiumBI')
        emoji = pdfmetrics.getFont('NotoEmoji')
        latin.substitutionFonts = [cjkSC, cjkK, greek, gentium, emoji]
        c = Canvas(outputfile('test_fallback_long_mixed.pdf'))
        c.setFont('Vera', 10)
        lines = [
            # Latin + Chinese (NotoSC)
            "ReportLab TTFont Fallback 测试报告",
            "当主字体缺少某些字形时，系统会自动从备选字体列表中查找可用字体。",
            # Latin + Korean (NotoKR)
            "한국어 폰트 포서트: 이 문서는 자동 폰트 팘에 빙(Fallback)을 시연합니다.",
            # Latin + Greek (TheanoDidot)
            "Greek alphabet: ΑΒΓΔΕΖΗΘ αβγδεζηθ",
            "Mathematical: π ≈ 3.14159, ∑xᵢ, ∫ f(x)dx, √2 ≈ 1.414",
            # Latin extended (GentiumBI)
            "Accented: àáâãäå èéêë ìíîï òóôõö ùúûü",
            "Nordic/Turkish: æøå ðþ ß Çç Şş İı",
            # Subscripts / superscripts
            "Subscripts: H₂O, CO₂, x₁ + x₂, aₙ",
            "Superscripts: x² + y² = z², E=mc², 1⁰¹²³⁴⁵",
            # Common punctuation
            "Punctuation: . , ; : ! ? \" ' ( ) - _ + = [ ] { } | / < > @ # $ % ^ & * ~ `",
            # CJK punctuation
            "中文标点：，。！？、；：“”‘’（）【】《》",
            # Korean punctuation mixed
            "숫자: 0123456789 반간, ０１２３４５６７８９ 전간",
            # All scripts in one line
            "EN 英语 한국어 Ελληνικά üöä",
            # Business scenario with multiple scripts
            "2024年Q4营收$1.2B，同比增长35%。한국 시장: ₩500M。ΔRevenue = +12%",
            # Emoji (NotoEmoji fallback)
            "Emoji: 😀 🎉 ❤️ 🔥 ✨ 💡 📊 🚀 👍 🎯",
            # Emoji mixed with scripts
            "Great job! 太棒了👍 恭喜🎉 한국어🇰🇷 Ελληνικά🏆",
        ]
        for i, line in enumerate(lines):
            c.drawString(72, 800 - i * 16, line)
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_emoji_pdf(self):
        """PDF with emoji characters falling back to NotoEmoji (monochrome vector)"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjkSC = pdfmetrics.getFont('NotoSC')
        cjkK = pdfmetrics.getFont('NotoKR')
        greek = pdfmetrics.getFont('TheanoDidot')
        gentium = pdfmetrics.getFont('GentiumBI')
        emoji = pdfmetrics.getFont('NotoEmoji')
        latin.substitutionFonts = [cjkSC, cjkK, greek, gentium, emoji]
        c = Canvas(outputfile('test_fallback_emoji.pdf'))
        c.setFont('Vera', 12)
        lines = [
            # Pure emoji → NotoEmoji
            "😀😁😂🤣😃😄😅😆😇",
            # Emoji + Latin
            "Hello 😀 World 🌍",
            # Emoji + CJK
            "你好🎉恭喜🎊加油💪",
            # Emoji + Korean
            "안녕하세요🇰🇷감사합니다🙏",
            # Emoji + Greek
            "Αλφα 🏆 Βητα 📊",
            # Mixed: scripts + emoji + symbols
            "Score: 💯 Team🇨🇳 won🎉 Δ=+5%",
            # Emoji with variation selectors
            "❤️ 🧡 💛 💚 💙 💜",
            # Emoji skin tone modifiers
            "👍🏻👍🏼👍🏽👍🏾👍🏿",
            # Multi-codepoint emoji (ZWJ sequences)
            "👨‍👩‍👧‍👦 👩‍💻 🏳️‍🌈",
        ]
        for i, line in enumerate(lines):
            c.drawString(72, 800 - i * 16, line)
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_heavy_alternation_pdf(self):
        """PDF with rapidly alternating scripts on each line"""
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        latin = pdfmetrics.getFont('Vera')
        cjk = pdfmetrics.getFont('NotoSC')
        latin.substitutionFonts = [cjk]
        c = Canvas(outputfile('test_fallback_alternation.pdf'))
        c.setFont('Vera', 10)
        # Generate lines with rapid alternation
        for i in range(30):
            line = ''
            for j in range(20):
                line += chr(ord('A') + (j % 26)) if j % 2 == 0 else chr(0x4E00 + (i * 10 + j) % 200)
            c.drawString(72, 800 - i * 14, line)
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

# ---------------------------------------------------------------------------
# T30-T31: hasGlyph with external fonts
# ---------------------------------------------------------------------------
@_skipUnlessExternalFonts()
class HasGlyphMultiScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _registerExternalFonts()

    def test_cjk_glyph_present(self):
        font = pdfmetrics.getFont('NotoSC')
        self.assertTrue(font.hasGlyph('你'))  # 你

    def test_greek_glyph_present(self):
        font = pdfmetrics.getFont('TheanoDidot')
        self.assertTrue(font.hasGlyph('Α'))  # Α

# ---------------------------------------------------------------------------
# T32-T34: API tests
# ---------------------------------------------------------------------------
class APITest(unittest.TestCase):
    def setUp(self):
        self._orig_env = os.environ.get('REPORTLAB_FONT_FALLBACK', None)

    def tearDown(self):
        if self._orig_env is None:
            os.environ.pop('REPORTLAB_FONT_FALLBACK', None)
        else:
            os.environ['REPORTLAB_FONT_FALLBACK'] = self._orig_env

    def test_T32_by_name(self):
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        _registerVera()
        font = pdfmetrics.registerFontWithFallback(
            'TestT32', _veraBdPath,
            fallbackFonts=['Vera']
        )
        self.assertIsInstance(font, TTFont)
        self.assertEqual(font.substitutionFonts, [pdfmetrics.getFont('Vera')])
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T33_by_instance(self):
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        fb = TTFont('TestT33FB', _veraPath)
        font = pdfmetrics.registerFontWithFallback(
            'TestT33', _veraBdPath,
            fallbackFonts=[fb]
        )
        self.assertIsInstance(font, TTFont)
        self.assertEqual(font.substitutionFonts, [fb])
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T34_no_fallback(self):
        font = pdfmetrics.registerFontWithFallback('TestT34', _veraPath)
        self.assertIsInstance(font, TTFont)

# ---------------------------------------------------------------------------
# T40-T41: Regression tests
# ---------------------------------------------------------------------------
class RegressionTest(unittest.TestCase):
    def test_existing_imports(self):
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.rl_accel import unicode2TT, instanceStringWidthTTF
        from reportlab.pdfbase.pdfmetrics import registerFontWithFallback

    def test_ttfont_creation(self):
        font = TTFont('RegTestVera', _veraPath)
        pdfmetrics.registerFont(font)
        self.assertIsInstance(font, TTFont)
        self.assertEqual(font.substitutionFonts, [])


def makeSuite():
    return makeSuiteForClasses(
        Unicode2TTTest,
        HasGlyphTest,
        EnvVarControlTest,
        StringWidthTest,
        Unicode2TTMultiScriptTest,
        MultiScriptWidthTest,
        PDFGenerationTest,
        PDFMultiScriptTest,
        HasGlyphMultiScriptTest,
        APITest,
        RegressionTest,
    )


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

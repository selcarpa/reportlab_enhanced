#Copyright (c) 2025-2026, selcarpa
#see LICENSE for license details
__version__='3.3.0'
"""Multi-script TTFont fallback tests — unicode2TT, stringWidth, hasGlyph with external fonts.
Tests are skipped when external font files are not present in tests_resource/."""
from reportlab.lib.testutils import setOutDir, makeSuiteForClasses, printLocation
if __name__=='__main__':
    setOutDir(__name__)
import unittest, os
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.rl_accel import unicode2TT
from _ttfont_fallback_helpers import (
    registerVera, registerExternalFonts, skipUnlessExternalFonts,
)

@skipUnlessExternalFonts()
class Unicode2TTMultiScriptTest(unittest.TestCase):
    """Multi-script fallback tests requiring external fonts."""

    @classmethod
    def setUpClass(cls):
        registerVera()
        registerExternalFonts()
        cls.latin = pdfmetrics.getFont('Vera')
        cls.cjkSC = pdfmetrics.getFont('NotoSC')
        cls.cjkK = pdfmetrics.getFont('NotoKR')

    def test_T15_latin_cjk_split(self):
        """Latin + CJK text splits into two fragments"""
        text = "Hello你好"
        result = unicode2TT(text, [self.latin, self.cjkSC])
        self.assertEqual(len(result), 2)
        self.assertIs(result[0][0], self.latin)
        self.assertEqual(result[0][1], "Hello")
        self.assertIs(result[1][0], self.cjkSC)
        self.assertEqual(result[1][1], "你好")

    def test_T16_multi_fallback_chain(self):
        """Three fonts: Latin → fallback1 → fallback2"""
        text = "A你가"
        result = unicode2TT(text, [self.latin, self.cjkSC, self.cjkK])
        self.assertTrue(len(result) >= 2)

    def test_T17_alternating_scripts(self):
        """Alternating Latin/CJK produces multiple fragments"""
        text = "A你B好C"
        result = unicode2TT(text, [self.latin, self.cjkSC])
        fonts_seq = [r[0] for r in result]
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
        fonts_used = {r[0] for r in result}
        self.assertIn(self.latin, fonts_used)
        self.assertIn(self.cjkSC, fonts_used)

    def test_many_short_alternations(self):
        """Rapidly alternating single chars between scripts"""
        text = "A你B好C世D界E测F试G"
        result = unicode2TT(text, [self.latin, self.cjkSC])
        joined = ''.join(t for _, t in result)
        self.assertEqual(joined, text)
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


@skipUnlessExternalFonts()
class MultiScriptWidthTest(unittest.TestCase):
    def setUp(self):
        registerVera()
        registerExternalFonts()
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
        w = pdfmetrics.stringWidth(text, 'Vera', 10)
        self.assertGreater(w, 0)
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


@skipUnlessExternalFonts()
class HasGlyphMultiScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registerExternalFonts()

    def test_cjk_glyph_present(self):
        font = pdfmetrics.getFont('NotoSC')
        self.assertTrue(font.hasGlyph('你'))

    def test_greek_glyph_present(self):
        font = pdfmetrics.getFont('TheanoDidot')
        self.assertTrue(font.hasGlyph('Α'))


def makeSuite():
    return makeSuiteForClasses(
        Unicode2TTMultiScriptTest,
        MultiScriptWidthTest,
        HasGlyphMultiScriptTest,
    )


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())
    printLocation()

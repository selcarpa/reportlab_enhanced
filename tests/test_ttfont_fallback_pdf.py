#Copyright (c) 2025-2026, selcarpa
#see LICENSE for license details
__version__='3.3.0'
"""TTFont fallback PDF generation tests.
Internal-font tests always run; multi-script tests require external fonts."""
from reportlab.lib.testutils import setOutDir, makeSuiteForClasses, outputfile, printLocation
if __name__=='__main__':
    setOutDir(__name__)
import unittest, os
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from _ttfont_fallback_helpers import (
    registerVera, registerExternalFonts, skipUnlessExternalFonts,
)

# ---------------------------------------------------------------------------
# Internal fonts only
# ---------------------------------------------------------------------------
class PDFGenerationTest(unittest.TestCase):
    def setUp(self):
        registerVera()
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
            c.drawString(72, 800 - i * 14, 'Line %d: The quick brown fox jumps over the lazy dog.' % i)
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


# ---------------------------------------------------------------------------
# External fonts required
# ---------------------------------------------------------------------------
@skipUnlessExternalFonts()
class PDFMultiScriptTest(unittest.TestCase):
    """PDF generation with mixed scripts (external fonts)."""

    def setUp(self):
        registerVera()
        registerExternalFonts()
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
            "ReportLab TTFont Fallback 测试报告",
            "当主字体缺少某些字形时，系统会自动从备选字体列表中查找可用字体。",
            "한국어 폰트 포서트: 이 문서는 자동 폰트 팘에 빙(Fallback)을 시연합니다.",
            "Greek alphabet: ΑΒΓΔΕΖΗΘ αβγδεζηθ",
            "Mathematical: π ≈ 3.14159, ∑xᵢ, ∫ f(x)dx, √2 ≈ 1.414",
            "Accented: àáâãäå èéêë ìíîï òóôõö ùúûü",
            "Nordic/Turkish: æøå ðþ ß Çç Şş İı",
            "Subscripts: H₂O, CO₂, x₁ + x₂, aₙ",
            "Superscripts: x² + y² = z², E=mc², 1⁰¹²³⁴⁵",
            "Punctuation: . , ; : ! ? \" ' ( ) - _ + = [ ] { } | / < > @ # $ % ^ & * ~ `",
            "中文标点：，。！？、；：""''（）【】《》",
            "숫자: 0123456789 반간, ０１２３４５６７８９ 전간",
            "EN 英语 한국어 Ελληνικά üöä",
            "2024年Q4营收$1.2B，同比增长35%。한국 시장: ₩500M。ΔRevenue = +12%",
            "Emoji: 😀 🎉 ❤️ 🔥 ✨ 💡 📊 🚀 👍 🎯",
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
            "😀😁😂🤣😃😄😅😆😇",
            "Hello 😀 World 🌍",
            "你好🎉恭喜🎊加油💪",
            "안녕하세요🇰🇷감사합니다🙏",
            "Αλφα 🏆 Βητα 📊",
            "Score: 💯 Team🇨🇳 won🎉 Δ=+5%",
            "❤️ 🧡 💛 💚 💙 💜",
            "👍🏻👍🏼👍🏽👍🏾👍🏿",
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
        for i in range(30):
            line = ''
            for j in range(20):
                line += chr(ord('A') + (j % 26)) if j % 2 == 0 else chr(0x4E00 + (i * 10 + j) % 200)
            c.drawString(72, 800 - i * 14, line)
        c.save()
        latin.substitutionFonts = []
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)


def makeSuite():
    return makeSuiteForClasses(
        PDFGenerationTest,
        PDFMultiScriptTest,
    )


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())
    printLocation()

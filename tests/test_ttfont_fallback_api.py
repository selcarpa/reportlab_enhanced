#Copyright (c) 2025-2026, selcarpa
#see LICENSE for license details
__version__='3.3.0'
"""TTFont fallback API and regression tests."""
from reportlab.lib.testutils import setOutDir, makeSuiteForClasses, printLocation
if __name__=='__main__':
    setOutDir(__name__)
import unittest, os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from _ttfont_fallback_helpers import registerVera, veraPath, veraBdPath

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
        registerVera()
        font = pdfmetrics.registerFontWithFallback(
            'TestT32', veraBdPath,
            fallbackFonts=['Vera']
        )
        self.assertIsInstance(font, TTFont)
        self.assertEqual(font.substitutionFonts, [pdfmetrics.getFont('Vera')])
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T33_by_instance(self):
        os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
        fb = TTFont('TestT33FB', veraPath)
        font = pdfmetrics.registerFontWithFallback(
            'TestT33', veraBdPath,
            fallbackFonts=[fb]
        )
        self.assertIsInstance(font, TTFont)
        self.assertEqual(font.substitutionFonts, [fb])
        os.environ.pop('REPORTLAB_FONT_FALLBACK', None)

    def test_T34_no_fallback(self):
        font = pdfmetrics.registerFontWithFallback('TestT34', veraPath)
        self.assertIsInstance(font, TTFont)


class RegressionTest(unittest.TestCase):
    def test_existing_imports(self):
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.rl_accel import unicode2TT, instanceStringWidthTTF
        from reportlab.pdfbase.pdfmetrics import registerFontWithFallback

    def test_ttfont_creation(self):
        font = TTFont('RegTestVera', veraPath)
        pdfmetrics.registerFont(font)
        self.assertIsInstance(font, TTFont)
        self.assertEqual(font.substitutionFonts, [])


def makeSuite():
    return makeSuiteForClasses(
        APITest,
        RegressionTest,
    )


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())
    printLocation()

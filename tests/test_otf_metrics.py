# test_otf_metrics.py - 字体验证测试
# 测试字形数量、PostScript 名称

import os
import unittest

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')
OTF_FONT = os.path.join(FONT_DIR, 'SourceHanSansK-Light.otf')


class TestOTFMetrics(unittest.TestCase):
    """字体验证测试 (2 个测试用例)"""

    def setUp(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        self.font = OpenTypeFont('TestOTFMetrics', OTF_FONT)

    def test_glyph_count(self):
        """测试字形数量"""
        self.assertGreater(self.font.face.numGlyphs, 0)

    def test_postscript_name(self):
        """测试 PostScript 名称"""
        self.assertIsNotNone(self.font.face.name)
        self.assertTrue(len(self.font.face.name) > 0)


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(TestOTFMetrics)


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

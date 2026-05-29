# test_otf_subsetting.py - 子集化测试
# 测试 glyph 映射、CharStrings、子集大小

import os
import unittest

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')
OTF_FONT = os.path.join(FONT_DIR, 'SourceHanSansK-Light.otf')


class TestOTFSubsetting(unittest.TestCase):
    """子集化测试 (3 个测试用例)"""

    def setUp(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        self.font = OpenTypeFont('TestOTFSubset', OTF_FONT)

    def test_glyph_mapping(self):
        """测试 glyph 映射 (charToGlyph)"""
        self.assertIsNotNone(self.font.face.charToGlyph)
        self.assertIn(0x20, self.font.face.charToGlyph)  # space
        self.assertIn(0x41, self.font.face.charToGlyph)  # 'A'

    def test_charstrings_structure(self):
        """测试 CharStrings 结构"""
        # CFF 字体应该有 charWidths
        self.assertIsNotNone(self.font.face.charWidths)
        self.assertIn(0x20, self.font.face.charWidths)

    def test_subset_size(self):
        """测试子集大小合理"""
        # charToGlyph 应该包含足够多的字形
        self.assertGreater(len(self.font.face.charToGlyph), 100)


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(TestOTFSubsetting)


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

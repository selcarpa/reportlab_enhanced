# test_otf_asian.py - 亚洲 CJK 文本渲染测试
# 测试 CJK 渲染、Unicode 范围

import os
import unittest

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')
OTF_FONT = os.path.join(FONT_DIR, 'SourceHanSansK-Light.otf')


class TestOTFAsian(unittest.TestCase):
    """亚洲 CJK 文本渲染测试 (2 个测试用例)"""

    def test_cjk_rendering(self):
        """测试 CJK 字符渲染"""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        font = OpenTypeFont('TestCJKRender', OTF_FONT)
        pdfmetrics.registerFont(font)
        output_path = os.path.join(os.path.dirname(__file__), 'pdf-out', 'test_otf_asian.pdf')
        c = canvas.Canvas(output_path)
        c.setFont('TestCJKRender', 12)
        c.drawString(100, 700, '你好世界')
        c.save()
        self.assertTrue(os.path.exists(output_path))

    def test_unicode_range(self):
        """测试 Unicode 范围覆盖"""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        font = OpenTypeFont('TestUnicodeRange', OTF_FONT)
        # 检查 CJK 字符是否在 charToGlyph 中
        self.assertIn(0x4E2D, font.face.charToGlyph)  # '中'


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(TestOTFAsian)


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

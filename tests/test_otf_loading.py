# test_otf_loading.py - OTF/TTF 字体加载测试
# 测试字体加载验证、度量、宽度、cmap

import os
import unittest

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')
OTF_FONT = os.path.join(FONT_DIR, 'SourceHanSansK-Light.otf')
TTF_FONT = os.path.join(FONT_DIR, 'NotoSansKR-Bold.ttf')


class TestOTFLoading(unittest.TestCase):
    """OTF/TTF 字体加载测试 (4 个测试用例)"""

    def test_load_otf_font(self):
        """测试加载 OTF 字体文件"""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        font = OpenTypeFont('TestOTF', OTF_FONT)
        self.assertIsNotNone(font)
        self.assertTrue(getattr(font.face, 'isCFF', False))

    def test_load_ttf_font(self):
        """测试加载 TTF 字体文件仍然有效"""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        font = OpenTypeFont('TestTTF', TTF_FONT)
        self.assertIsNotNone(font)
        self.assertFalse(getattr(font.face, 'isCFF', False))

    def test_backward_compat_import(self):
        """测试旧导入路径仍然有效"""
        from reportlab.pdfbase.ttfonts import TTFont
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        font = TTFont('TestCompat', TTF_FONT)
        self.assertIsNotNone(font)

    def test_isinstance_check(self):
        """测试 isinstance 检查与旧类名"""
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase.openfonts import OpenTypeFont
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        font = TTFont('TestIsinstance', TTF_FONT)
        self.assertIsInstance(font, OpenTypeFont)
        self.assertIsInstance(font, TTFont)


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(TestOTFLoading)


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

# test_otf_rendering.py - PDF 渲染测试
# 测试 PDF 生成、FontFile3、Type1C 子类型

import os
import unittest

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')
OTF_FONT = os.path.join(FONT_DIR, 'SourceHanSansK-Light.otf')
TTF_FONT = os.path.join(FONT_DIR, 'NotoSansKR-Bold.ttf')


class TestOTFRendering(unittest.TestCase):
    """PDF 渲染测试 (3 个测试用例)"""

    def test_pdf_generation_ttf(self):
        """测试 TTF 字体 PDF 生成"""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        font = OpenTypeFont('TestTTFRender', TTF_FONT)
        pdfmetrics.registerFont(font)
        output_path = os.path.join(os.path.dirname(__file__), 'pdf-out', 'test_otf_rendering_ttf.pdf')
        c = canvas.Canvas(output_path)
        c.setFont('TestTTFRender', 12)
        c.drawString(100, 700, 'Hello World')
        c.save()
        self.assertTrue(os.path.exists(output_path))

    def test_fontfile3_structure(self):
        """测试 FontFile3 结构 (CFF 字体)"""
        # CFF 字体的 addObjects 应该创建 PDFType1CFont
        from reportlab.pdfbase.openfonts._font import OpenTypeFont
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        font = OpenTypeFont('TestFontFile3', OTF_FONT)
        self.assertTrue(getattr(font.face, 'isCFF', False))

    def test_type1c_font_dict_subtype(self):
        """Font dictionary Subtype for CFF fonts must be Type1."""
        from reportlab.pdfbase.pdfdoc import PDFType1CFont
        self.assertEqual(PDFType1CFont.Subtype, 'Type1')


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(TestOTFRendering)


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

# Tests for OpenType font support
# Tests OTF font loading, metrics extraction, and PDF rendering.

import os
import unittest
from io import BytesIO

# Test font paths
FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')
OTF_FONT = os.path.join(FONT_DIR, 'SourceHanSansK-Light.otf')
TTF_FONT = os.path.join(FONT_DIR, 'NotoSansKR-Bold.ttf')


class TestOTFLoading(unittest.TestCase):
    """Test OTF font loading and basic functionality."""
    
    def test_load_otf_font(self):
        """Test loading an OTF font file."""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        
        font = OpenTypeFont('TestOTF', OTF_FONT)
        self.assertIsNotNone(font)
        self.assertIsNotNone(font.face)
        self.assertTrue(getattr(font.face, 'isCFF', False))
    
    def test_load_ttf_font(self):
        """Test loading a TTF font file still works."""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        
        font = OpenTypeFont('TestTTF', TTF_FONT)
        self.assertIsNotNone(font)
        self.assertIsNotNone(font.face)
        self.assertFalse(getattr(font.face, 'isCFF', False))
    
    def test_backward_compat_import(self):
        """Test that old import path still works."""
        from reportlab.pdfbase.ttfonts import TTFont
        
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        
        font = TTFont('TestCompat', TTF_FONT)
        self.assertIsNotNone(font)
    
    def test_isinstance_check(self):
        """Test isinstance check works with old class name."""
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase.openfonts import OpenTypeFont
        
        if not os.path.exists(TTF_FONT):
            self.skipTest(f"Test font not found: {TTF_FONT}")
        
        font = TTFont('TestIsinstance', TTF_FONT)
        self.assertIsInstance(font, OpenTypeFont)
        self.assertIsInstance(font, TTFont)


class TestOTFMetrics(unittest.TestCase):
    """Test OTF font metrics extraction."""
    
    def setUp(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        
        self.font = OpenTypeFont('TestOTFMetrics', OTF_FONT)
    
    def test_font_name(self):
        """Test font name extraction."""
        self.assertIsNotNone(self.font.face.name)
        self.assertTrue(len(self.font.face.name) > 0)
    
    def test_char_widths(self):
        """Test character width extraction."""
        self.assertIsNotNone(self.font.face.charWidths)
        self.assertTrue(len(self.font.face.charWidths) > 0)
    
    def test_bbox(self):
        """Test bounding box extraction."""
        self.assertIsNotNone(self.font.face.bbox)
        self.assertEqual(len(self.font.face.bbox), 4)


class TestOTFRendering(unittest.TestCase):
    """Test OTF font rendering to PDF."""
    
    def test_render_basic(self):
        """Test basic OTF font rendering."""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        
        font = OpenTypeFont('TestOTFRender', OTF_FONT)
        pdfmetrics.registerFont(font)
        
        output_path = os.path.join(os.path.dirname(__file__), 'pdf-out', 'test_otf_rendering_basic.pdf')
        c = canvas.Canvas(output_path)
        c.setFont('TestOTFRender', 12)
        c.drawString(100, 700, 'Hello World')
        c.save()
        
        self.assertTrue(os.path.exists(output_path))
    
    def test_render_cjk(self):
        """Test CJK character rendering with OTF font."""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        
        if not os.path.exists(OTF_FONT):
            self.skipTest(f"Test font not found: {OTF_FONT}")
        
        font = OpenTypeFont('TestOTFCJK', OTF_FONT)
        pdfmetrics.registerFont(font)
        
        output_path = os.path.join(os.path.dirname(__file__), 'pdf-out', 'test_otf_cjk_rendering.pdf')
        c = canvas.Canvas(output_path)
        c.setFont('TestOTFCJK', 12)
        c.drawString(100, 700, '你好世界')
        c.save()
        
        self.assertTrue(os.path.exists(output_path))


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(
        TestOTFLoading,
        TestOTFMetrics,
        TestOTFRendering,
    )


if __name__ == '__main__':
    unittest.main()

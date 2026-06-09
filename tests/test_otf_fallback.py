# test_otf_fallback.py - OTF + TTF 混合 fallback 测试
# 覆盖 tests_resource 下所有字体，含 CFF/TTF 混合渲染

import os
import unittest

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'tests_resource')

ALL_FONTS = [
    ('CFF', 'SourceHanSans-Medium.otf'),
    ('CFF', 'SourceHanSansHW-Bold.otf'),
    ('CFF', 'SourceHanSansK-Light.otf'),
    ('CFF', 'SourceHanSansHWSC-Regular.otf'),
    ('CFF', 'SourceHanSansSC-Light.otf'),
    ('CFF', 'cmunss.otf'),
    ('CFF', 'eb-garamond.smallcaps-12-regular.otf'),
    ('CFF', 'LibertinusSerif-SemiboldItalic.otf'),
    ('TTF', 'Gentium-BoldItalic.ttf'),
    ('TTF', 'NotoEmoji-Regular.ttf'),
    ('TTF', 'NotoSansKR-Bold.ttf'),
    ('TTF', 'NotoSansSC-Regular.ttf'),
    ('TTF', 'TheanoDidot-Regular.ttf'),
]

ASCII_TEXT = 'Hello World 123'
CJK_TEXT = '\u4f60\u597d\u4e16\u754c'
MIXED_TEXT = CJK_TEXT + ' Hello ' + '\u4e16\u754c' + ' 123'


class TestOTFFallback(unittest.TestCase):
    """OTF + TTF 混合 fallback 测试"""

    NON_CID_CFF = ['cmunss', 'eb-garamond', 'LibertinusSerif']

    def _path(self, name):
        p = os.path.join(FONT_DIR, name)
        if not os.path.exists(p):
            self.skipTest(f'Font not found: {p}')
        return p

    def test_all_otf_basic_render(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        for ftype, fname in ALL_FONTS:
            if ftype != 'CFF':
                continue
            path = self._path(fname)
            fn = 'OTF_' + os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                pdfmetrics.registerFont(font)
                c = canvas.Canvas(os.devnull)
                c.setFont(fn, 12)
                c.drawString(100, 700, ASCII_TEXT)
                c.save()
            except Exception as e:
                self.fail(f'{fname} basic render failed: {e}')

    def test_all_ttf_basic_render(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        for ftype, fname in ALL_FONTS:
            if ftype != 'TTF':
                continue
            path = self._path(fname)
            fn = 'TTF_' + os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                pdfmetrics.registerFont(font)
                c = canvas.Canvas(os.devnull)
                c.setFont(fn, 12)
                c.drawString(100, 700, ASCII_TEXT)
                c.save()
            except Exception as e:
                self.fail(f'{fname} basic render failed: {e}')

    def test_otf_cjk_render_all(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        for ftype, fname in ALL_FONTS:
            if ftype != 'CFF':
                continue
            path = self._path(fname)
            fn = 'CJK_' + os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                pdfmetrics.registerFont(font)
                c = canvas.Canvas(os.devnull)
                c.setFont(fn, 12)
                c.drawString(100, 700, CJK_TEXT)
                c.save()
            except Exception as e:
                self.fail(f'{fname} CJK render failed: {e}')

    def test_otf_mixed_text_all(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        for ftype, fname in ALL_FONTS:
            path = self._path(fname)
            fn = 'MIX_' + os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                pdfmetrics.registerFont(font)
                c = canvas.Canvas(os.devnull)
                c.setFont(fn, 12)
                c.drawString(100, 700, MIXED_TEXT)
                c.save()
            except Exception as e:
                self.fail(f'{fname} mixed render failed: {e}')

    def test_otf_ttf_mixed_page(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        cff_names = [(ft, fn) for ft, fn in ALL_FONTS if ft == 'CFF']
        ttf_names = [(ft, fn) for ft, fn in ALL_FONTS if ft == 'TTF']
        for cft, cf in cff_names:
            for tft, tf in ttf_names:
                cpath = self._path(cf)
                tpath = self._path(tf)
                cfn = 'CFF_' + os.path.splitext(cf)[0].replace('-', '_')
                tfn = 'TTF_' + os.path.splitext(tf)[0].replace('-', '_')
                try:
                    cfont = OpenTypeFont(cfn, cpath)
                    tfont = OpenTypeFont(tfn, tpath)
                    pdfmetrics.registerFont(cfont)
                    pdfmetrics.registerFont(tfont)
                    c = canvas.Canvas(os.devnull)
                    c.setFont(cfn, 12)
                    c.drawString(100, 700, ASCII_TEXT)
                    c.setFont(tfn, 12)
                    c.drawString(100, 680, ASCII_TEXT)
                    c.save()
                except Exception as e:
                    self.fail(f'{cf} + {tf} mixed page failed: {e}')

    def test_substitution_fallback(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        for ftype, fname in ALL_FONTS[:3]:
            path = self._path(fname)
            fn = 'SUB_' + os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                font.substitutionFonts = []
                pdfmetrics.registerFont(font)
                w = font.stringWidth('Test', 12)
                self.assertGreater(w, 0)
            except Exception as e:
                self.fail(f'{fname} substitution fallback failed: {e}')

    def test_width_consistency(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        for ftype, fname in ALL_FONTS:
            path = self._path(fname)
            fn = 'W_' + os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                w1 = font.stringWidth('Hello', 12)
                self.assertGreater(w1, 0, f'{fname} zero width')
                w2 = font.stringWidth('Hello World', 12)
                self.assertGreater(w2, w1, f'{fname} world not wider')
            except Exception as e:
                self.fail(f'{fname} width failed: {e}')

    def test_is_cff_detection(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        for ftype, fname in ALL_FONTS:
            path = self._path(fname)
            font = OpenTypeFont('DET_' + fname.replace('.', '_'), path)
            expected = ftype == 'CFF'
            actual = getattr(font.face, 'isCFF', False)
            self.assertEqual(actual, expected, f'{fname} isCFF={actual} expected={expected}')

    def test_is_cid_detection(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        for ftype, fname in ALL_FONTS:
            if ftype != 'CFF':
                continue
            path = self._path(fname)
            font = OpenTypeFont('CID_' + fname.replace('.', '_'), path)
            detected = getattr(font.face, 'isCID', False)
            is_non_cid = any(n in fname for n in self.NON_CID_CFF)
            if is_non_cid:
                self.assertFalse(detected, f'{fname} non-CID detected as CID')
            else:
                self.assertTrue(detected, f'{fname} CID not detected')

    def test_has_ros_info(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        for ftype, fname in ALL_FONTS:
            if ftype != 'CFF':
                continue
            path = self._path(fname)
            font = OpenTypeFont('ROS_' + fname.replace('.', '_'), path)
            cid_info = getattr(font.face, 'cidInfo', None)
            is_non_cid = any(n in fname for n in self.NON_CID_CFF)
            if is_non_cid:
                self.assertIsNone(cid_info, f'{fname} non-CID should have no cidInfo')
            else:
                self.assertIsNotNone(cid_info, f'{fname} missing cidInfo')
                self.assertIn('Registry', cid_info, f'{fname} missing Registry')
                self.assertIn('Ordering', cid_info, f'{fname} missing Ordering')

    def test_otf_fallback(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        path = self._path('SourceHanSansK-Light.otf')
        font = OpenTypeFont('TestOTFFallback', path)
        font.substitutionFonts = []
        self.assertEqual(font.substitutionFonts, [])

    def test_mixed_fonts_type(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        path_otf = self._path('SourceHanSansK-Light.otf')
        path_ttf = self._path('NotoSansKR-Bold.ttf')
        otf = OpenTypeFont('TestOTF', path_otf)
        ttf = OpenTypeFont('TestTTF', path_ttf)
        self.assertTrue(getattr(otf.face, 'isCFF', False))
        self.assertFalse(getattr(ttf.face, 'isCFF', False))

    def test_pdf_output_all_fonts(self):
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        out = os.path.join(os.path.dirname(__file__), 'pdf-out', 'test_otf_fallback_allfonts.pdf')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        c = canvas.Canvas(out)
        y = 780
        for ftype, fname in ALL_FONTS:
            path = self._path(fname)
            fn = os.path.splitext(fname)[0].replace('-', '_')
            try:
                font = OpenTypeFont(fn, path)
                pdfmetrics.registerFont(font)
                c.setFont('Helvetica', 8)
                c.drawString(50, y, f'[{ftype:3s}] {fn}')
                c.setFont(fn, 10)
                c.drawString(50, y - 14, ASCII_TEXT + ' ' + CJK_TEXT)
                y -= 36
                if y < 50:
                    c.showPage()
                    y = 780
            except Exception as e:
                c.setFont('Helvetica', 8)
                c.drawString(50, y, f'[{ftype:3s}] {fn} SKIP: {e}')
                y -= 36
        c.save()

    def test_otf_ttf_mixed_page_pdf(self):
        """OTF + TTF 混合渲染 PDF，输出到 pdf-out 供目测"""
        from reportlab.pdfbase.openfonts import OpenTypeFont
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
        out = os.path.join(os.path.dirname(__file__), 'pdf-out', 'test_otf_ttf_mixed.pdf')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        c = canvas.Canvas(out)
        y = 780
        otfs = [(ft, fn) for ft, fn in ALL_FONTS if ft == 'CFF'][:4]
        ttfs = [(ft, fn) for ft, fn in ALL_FONTS if ft == 'TTF'][:2]
        for cft, cf in otfs:
            cpath = self._path(cf)
            cfn = os.path.splitext(cf)[0].replace('-', '_') + '_CFF'
            try:
                cfont = OpenTypeFont(cfn, cpath)
                pdfmetrics.registerFont(cfont)
            except Exception:
                continue
            for tft, tf in ttfs:
                tpath = self._path(tf)
                tfn = os.path.splitext(tf)[0].replace('-', '_') + '_TTF'
                try:
                    tfont = OpenTypeFont(tfn, tpath)
                    pdfmetrics.registerFont(tfont)
                except Exception:
                    continue
                c.setFont('Helvetica', 8)
                c.drawString(50, y, f'OTF: {cfn}  TTF: {tfn}')
                c.setFont(cfn, 10)
                c.drawString(50, y - 14, CJK_TEXT + ' ' + ASCII_TEXT)
                c.setFont(tfn, 10)
                c.drawString(50, y - 28, CJK_TEXT + ' ' + ASCII_TEXT)
                c.setFont('Helvetica', 8)
                c.drawString(50, y - 42, '-' * 60)
                y -= 60
                if y < 80:
                    c.showPage()
                    y = 780
        c.save()


def makeSuite():
    from reportlab.lib.testutils import makeSuiteForClasses
    return makeSuiteForClasses(TestOTFFallback)


if __name__ == '__main__':
    unittest.TextTestRunner().run(makeSuite())

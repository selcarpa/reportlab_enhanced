# Text shaping support for OpenType fonts
# Extracted from ttfonts.py for the openfonts package.

from collections import namedtuple
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.rl_accel import fp_str
from reportlab.lib.abag import ABag


class ShapedFragWord(list):
    '''list class to distinguish frag words that have been shaped'''
    pass


def makeShapedFragWord(w, K=[], V=[]):
    klass = w.__class__
    if klass in K:
        return V[K.index(klass)]
    v = ShapedFragWord if klass in (list, ShapedFragWord) else type('ShapedFragWord', (klass, ShapedFragWord), {})
    V.append(v)
    K.append(klass)
    if len(K) >= 127:
        K[:] = K[-127:]
        V[:] = V[-127:]
    return v


ShapeData = namedtuple('ShapeData', 'cluster x_advance y_advance x_offset y_offset width')

class ShapeData(ShapeData):
    def __repr__(self):
        return repr(tuple((map(fp_str, self))))

_sdGuardL = [ShapeData(-1, 0, 0, 0, 0, 0)]           # for the end of ShapeData list
_sdSimple = ShapeData(0x7fffffff, 0, 0, 0, 0, 0)     # for added simple chars


class ShapedStr(str):
    def __new__(cls, s, shapeData=None):
        self = super().__new__(cls, s)
        self.__shapeData__ = shapeData
        return self

    def __add__(self, other):
        return ShapedStr(super().__add__(other),
                          shapeData=(self.__shapeData__ + other.__shapeData__ if isinstance(other, ShapedStr)
                              else self.__shapeData__ + len(other) * [_sdSimple]))

    def __radd__(self, other):
        return ShapedStr(str(other) + str(self),
                          shapeData=(other.__shapeData__ + self.__shapeData__ if isinstance(other, ShapedStr)
                              else len(other) * [_sdSimple] + self.__shapeData__))

    def __getitem__(self, i):
        s = super().__getitem__(i)
        if not s: return s  # a simple str
        d = self.__shapeData__[i]
        return ShapedStr(s, d if isinstance(i, slice) else [d])


try:
    import uharfbuzz
except ImportError:
    uharfbuzz = None


if not uharfbuzz:
    def shapeFragWord(w, features=None):
        return w
else:
    def shapeFragWord(w, features=dict(kern=True, liga=True, dlig=True), force=False):
        '''take a frag word and return a shaped fragword if uharfbuzz makes any changes
        if no changes are made return the original word
        '''
        if isinstance(w, ShapedFragWord): return w
        F = []
        text = ''
        specials = {}
        for f, s in w[1:]:
            if hasattr(f, 'cbDefn'):
                specials.setdefault(len(text), []).append(f)
                continue
            F.extend(len(s) * [f])
            text += s
        ntext = len(text)
        if not F: return w
        ttfn = F[0].fontName
        ttfs = F[0].fontSize
        ttf = pdfmetrics.getFont(ttfn)
        try:
            hbf = ttf.hbFont(ttfs)
        except AttributeError:
            return w
        ttfs /= 1000
        buf = uharfbuzz.Buffer()
        buf.cluster_level = uharfbuzz.BufferClusterLevel.MONOTONE_CHARACTERS
        buf.add_str(text)
        buf.guess_segment_properties()
        infos = buf.glyph_infos
        uharfbuzz.shape(hbf, buf, features)

        infos = buf.glyph_infos
        positions = buf.glyph_positions

        changed = False
        shaped = False
        new = makeShapedFragWord(w)([])
        new0 = 0
        nf = None
        xpos = 0
        ypos = 0
        shapeDataAppend = [].append
        for i, (info, pos) in enumerate(zip(infos, positions)):
            gid = info.codepoint
            name = hbf.glyph_to_string(gid)
            cluster = info.cluster
            x_advance = pos.x_advance
            x_offset = pos.x_offset
            y_advance = pos.y_advance
            y_offset = pos.y_offset
            f = F[cluster]
            if nf is not f:
                if nf:
                    new.append((nf, ShapedStr(ns, shapeData=shapeDataAppend.__self__)))
                    new0 += newlen
                nf = f
                ns = ''
                newlen = 0
                shapeDataAppend = [].append
                _ = nf.fontName
                if _ != ttfn:
                    ttfn = _
                    ttf = pdfmetrics.getFont(ttfn)
                ttfs = nf.fontSize / 1000
            try:
                uchar = ttf.face.glyphToChar[gid][0]
            except KeyError:
                uchar = ttf.hbAddPrivate(name, gid, x_advance)
            ucharWidth = ttf.face.charWidths[uchar]
            uchar = chr(uchar)
            ns += uchar
            x_advance = ttf.pdfScale(x_advance)
            x_offset = ttf.pdfScale(x_offset)
            y_advance = ttf.pdfScale(y_advance)
            y_offset = ttf.pdfScale(y_offset)
            if x_advance: newlen += x_advance * ttfs
            shaped = shaped or (x_offset != 0 or y_offset != 0 
                                or i >= ntext 
                                or (text[i] == uchar and x_advance != ucharWidth))
            changed = changed or shaped or i >= ntext or text[i] != uchar or force
            shapeDataAppend(ShapeData(cluster, x_advance, y_advance, x_offset, y_offset, ucharWidth))
        if nf:  # we have at least one frag
            new.append((nf, ShapedStr(ns, shapeData=shapeDataAppend.__self__)))
            new0 += newlen
        if not changed: return w
        if not shaped:
            if changed:
                new = new.__class__([new[0]] + [tuple(_) for _ in new[1:]])
            else:
                return w
        if specials:
            S = []
            for k, v in specials.items():
                S.append(((k, k), v))
            for _ in new:
                S.append(((_[1].__shapeData__[0].cluster, _[1].__shapeData__[-1].cluster), _))
            new[:] = [_[1] for _ in sorted(S)]
        new.insert(0, new0)
        return new


def shapeStr(s, fontName, fontSize, force=False):
    return shapeFragWord([pdfmetrics.stringWidth(s, fontName, fontSize),
                          (ABag(fontName=fontName, fontSize=fontSize), s)], force=force)[1][1]

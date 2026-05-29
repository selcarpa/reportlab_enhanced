# Main user-facing font class for OpenType fonts
# Extracted from ttfonts.py for the openfonts package.

import os
from fnmatch import fnmatch
from weakref import WeakKeyDictionary

from reportlab.lib.utils import isUnicode
from reportlab.pdfbase import pdfmetrics, pdfdoc
from reportlab import rl_config
from reportlab.rl_config import unShapedFontGlob
from reportlab.lib.rl_accel import instanceStringWidthTTF

from ._common import TTFError, SUBSETN, makeToUnicodeCMap
from ._face import FontFace
from ._encoding import FontEncoding


class OpenTypeFont:
    """Represents an OpenType font (TTF or OTF).

    Its encoding is always UTF-8.

    Note: you cannot use the same OpenTypeFont object for different documents
    at the same time.

    Example of usage:

        font = OpenTypeFont('PostScriptFontName', '/path/to/font.ttf')
        pdfmetrics.registerFont(font)

        canvas.setFont('PostScriptFontName', size)
        canvas.drawString(x, y, "Some text encoded in UTF-8")
    """
    class State:
        namePrefix = 'F'
        def __init__(self, asciiReadable=None, ttf=None):
            A = self.assignments = {}   # maps unicode to subset and index
            self.nextCode = 0
            self.internalName = None
            self.frozen = 0
            face = getattr(ttf, 'face', None)
            if getattr(face, '_full_font', None):
                C = set(face.charToGlyph.keys())
                if 0xa0 in C: C.remove(0xa0)
                for n in range(256):
                    if n in C:
                        A[n] = n
                        C.remove(n)
                for n in C:
                    A[n] = n
                self.subsets = [[n for n in A]]
                self.frozen = True
                return

            if asciiReadable is None:
                asciiReadable = rl_config.ttfAsciiReadable

            if asciiReadable:
                subset0 = list(range(32, 128))
                charToGlyph = getattr(face, 'charToGlyph', None)
                if charToGlyph:
                    for n in subset0:
                        if n in charToGlyph:
                            A[n] = n
                else:
                    for n in subset0:
                        A[n] = n
                A[0] = 0
                self.subsets = [32 * [0] + subset0]
                self.nextCode = 1
            else:
                self.subsets = [[0] + [32] * 32]
                A[0] = 0
                self.nextCode = 1
                A[32] = 32

    _multiByte = 1      # We want our own stringwidth
    _dynamicFont = 1    # We want dynamic subsetting

    def __init__(self, name, filename, validate=0, subfontIndex=0, asciiReadable=None, shapable=True):
        """Loads an OpenType font from filename.

        If validate is set to a false values, skips checksum validation.  This
        can save time, especially if the font is large.
        """
        self.fontName = name
        self.face = FontFace(filename, validate=validate, subfontIndex=subfontIndex)
        self.encoding = FontEncoding()
        self.state = WeakKeyDictionary()
        if asciiReadable is None:
            asciiReadable = rl_config.ttfAsciiReadable
        self._asciiReadable = asciiReadable
        self.shapable = shapable and not any((fnmatch(name, _) for _ in unShapedFontGlob))
        self._substitutionFonts = []

    @property
    def substitutionFonts(self):
        if os.environ.get('REPORTLAB_FONT_FALLBACK', '0') != '1':
            return []
        return self._substitutionFonts

    @substitutionFonts.setter
    def substitutionFonts(self, value):
        self._substitutionFonts = value

    def hasGlyph(self, char_or_code):
        if isinstance(char_or_code, str):
            code = ord(char_or_code)
        else:
            code = char_or_code
        if code == 0xa0:
            code = 0x20
        return code in self.face.charToGlyph

    def stringWidth(self, text, size, encoding='utf8'):
        return instanceStringWidthTTF(self, text, size, encoding)

    def _assignState(self, doc, asciiReadable=None, namePrefix=None):
        '''convenience function for those wishing to roll their own state properties'''
        if asciiReadable is None:
            asciiReadable = self._asciiReadable
        try:
            state = self.state[doc]
        except KeyError:
            state = self.state[doc] = OpenTypeFont.State(asciiReadable, self)
            if namePrefix is not None:
                state.namePrefix = namePrefix
        return state

    def splitString(self, text, doc, encoding='utf-8'):
        """Splits text into a number of chunks, each of which belongs to a
        single subset.  Returns a list of tuples (subset, string).  Use subset
        numbers with getSubsetInternalName.  Doc is needed for distinguishing
        subsets when building different documents at the same time."""
        asciiReadable = self._asciiReadable
        try:
            state = self.state[doc]
        except KeyError:
            state = self.state[doc] = OpenTypeFont.State(asciiReadable, self)
        _31skip = 31 if asciiReadable and state.nextCode < 32 else -256
        curSet = -1
        cur = []
        results = []
        if not isUnicode(text):
            text = text.decode('utf-8')
        charToGlyph = self.face.charToGlyph
        assignments = state.assignments
        subsets = state.subsets
        for code in map(ord, text):
            if code == 0xa0: code = 32
            if code in assignments:
                n = assignments[code]
            elif code not in charToGlyph:
                n = 0
            else:
                if state.frozen:
                    raise pdfdoc.PDFError("Font %s is already frozen, cannot add new character U+%04X" % (self.fontName, code))
                n = state.nextCode
                if n & 0xFF == 32:
                    if n != 32: subsets[n >> 8].append(32)
                    state.nextCode += 1
                    n = state.nextCode
                if n > 32:
                    if not (n & 0xFF):
                        subsets.append([0])
                        state.nextCode += 1
                        n = state.nextCode
                    subsets[n >> 8].append(code)
                else:
                    if n == _31skip:
                        state.nextCode = 127
                    subsets[0][n] = code
                state.nextCode += 1
                assignments[code] = n
            if (n >> 8) != curSet:
                if cur:
                    results.append((curSet, bytes(cur)))
                curSet = (n >> 8)
                cur = []
            cur.append(n & 0xFF)
        if cur:
            results.append((curSet, bytes(cur)))
        return results

    def getSubsetInternalName(self, subset, doc):
        """Returns the name of a PDF Font object corresponding to a given
        subset of this dynamic font.  Use this function instead of
        PDFDocument.getInternalFontName."""
        try:
            state = self.state[doc]
        except KeyError:
            state = self.state[doc] = OpenTypeFont.State(self._asciiReadable)
        if subset < 0 or subset >= len(state.subsets):
            raise IndexError('Subset %d does not exist in font %s' % (subset, self.fontName))
        if state.internalName is None:
            state.internalName = state.namePrefix + repr(len(doc.fontMapping) + 1)
            doc.fontMapping[self.fontName] = '/' + state.internalName
            doc.delayedFonts.append(self)
        return '/%s+%d' % (state.internalName, subset)

    def addObjects(self, doc):
        try:
            state = self.state[doc]
        except KeyError:
            state = self.state[doc] = OpenTypeFont.State(self._asciiReadable)
        state.frozen = 1
        for n, subset in enumerate(state.subsets):
            internalName = self.getSubsetInternalName(n, doc)[1:]
            baseFontName = (b''.join((SUBSETN(n), b'+', self.face.name, self.face.subfontNameX))).decode('pdfdoc')

            cmapStream = pdfdoc.PDFStream()
            cmapStream.content = makeToUnicodeCMap(baseFontName, subset)
            if doc.compression:
                cmapStream.filters = [pdfdoc.PDFZCompress]
            cmapRef = doc.Reference(cmapStream, 'toUnicodeCMap:' + baseFontName)

            isCFF = getattr(self.face, 'isCFF', False)
            isCID = isCFF and getattr(self.face, 'isCID', False)

            if isCID:
                pdfFont = self._makeCIDType0Font(doc, baseFontName, internalName,
                                                 subset, cmapRef)
            elif isCFF:
                pdfFont = pdfdoc.PDFType1CFont()
                pdfFont.__Comment__ = 'Font %s subset %d' % (self.fontName, n)
                pdfFont.Name = internalName
                pdfFont.BaseFont = baseFontName
                pdfFont.FirstChar = 0
                pdfFont.LastChar = len(subset) - 1
                widths = list(map(self.face.getCharWidth, subset))
                pdfFont.Widths = pdfdoc.PDFArray(widths)
                pdfFont.ToUnicode = cmapRef
                pdfFont.FontDescriptor = self.face.addSubsetObjects(doc, baseFontName, subset)
            else:
                pdfFont = pdfdoc.PDFTrueTypeFont()
                pdfFont.__Comment__ = 'Font %s subset %d' % (self.fontName, n)
                pdfFont.Name = internalName
                pdfFont.BaseFont = baseFontName
                pdfFont.FirstChar = 0
                pdfFont.LastChar = len(subset) - 1
                widths = list(map(self.face.getCharWidth, subset))
                pdfFont.Widths = pdfdoc.PDFArray(widths)
                pdfFont.ToUnicode = cmapRef
                pdfFont.FontDescriptor = self.face.addSubsetObjects(doc, baseFontName, subset)

            ref = doc.Reference(pdfFont, internalName)
            fontDict = doc.idToObject['BasicFonts'].dict
            fontDict[internalName] = pdfFont
        del self.state[doc]

    def _makeCIDType0Font(self, doc, baseFontName, internalName, subset, cmapRef):
        cidInfo = getattr(self.face, 'cidInfo', None) or {}
        defaultWidth = self.face.defaultWidth or 1000
        widths = list(map(self.face.getCharWidth, subset))

        fontDescriptorRef = self.face.addSubsetObjects(doc, baseFontName, subset)

        cidDict = {
            'Type': '/Font',
            'Subtype': '/CIDFontType0',
            'BaseFont': pdfdoc.PDFName(baseFontName),
            'CIDSystemInfo': pdfdoc.PDFDictionary({
                'Registry': pdfdoc.PDFString(cidInfo.get('Registry', 'Adobe')),
                'Ordering': pdfdoc.PDFString(cidInfo.get('Ordering', 'Identity')),
                'Supplement': cidInfo.get('Supplement', 0),
            }),
            'FontDescriptor': fontDescriptorRef,
            'DW': defaultWidth,
        }
        wArray = _buildWArray(widths, defaultWidth)
        if wArray:
            cidDict['W'] = pdfdoc.PDFArray(wArray)
        cidFontDict = pdfdoc.PDFDictionary(cidDict)
        cidFontRef = doc.Reference(cidFontDict, 'CIDFont:' + baseFontName)

        encData = _buildCMap(subset)
        encStream = pdfdoc.PDFStream()
        encStream.content = encData
        encStreamRef = doc.Reference(encStream, 'CMap:' + baseFontName)

        type0Font = pdfdoc.PDFDictionary({
            'Type': '/Font',
            'Subtype': '/Type0',
            'BaseFont': pdfdoc.PDFName(baseFontName),
            'Name': pdfdoc.PDFName(internalName),
            'Encoding': encStreamRef,
            'DescendantFonts': pdfdoc.PDFArray([cidFontRef]),
            'ToUnicode': cmapRef,
        })
        type0Font.__RefOnly__ = 1
        type0Font.__Comment__ = 'Font %s subset (CID Type0)' % self.fontName
        return type0Font

    @property
    def hbFace(self):
        '''return uharbuzz.Face'''
        face = getattr(self, '__hbFace__', None)
        if not face:
            try:
                import uharfbuzz
            except ImportError:
                raise ValueError('Cannot import uharfbuzz so shaping is not allowed\nplease pip install uharfbuzz')
            blob = uharfbuzz.Blob(self.face._ttf_data)
            face = self.__hbFace__ = uharfbuzz.Face(blob)
            del blob
            self.__hbUnis = {}
            self.__hbPrivate = 0xE000
        return face

    def hbFont(self, fontSize=10):
        '''return uharfbuzz Font'''
        try:
            import uharfbuzz
        except ImportError:
            raise ValueError('Cannot import uharfbuzz so shaping is not allowed')
        font = uharfbuzz.Font(self.hbFace)
        font.ptem = fontSize
        self.hbAddPrivate = self.__addPrivate
        return font

    def __addPrivate(self, name, gid, advance):
        uchar = self.__hbUnis.get(name, None)
        if not uchar:
            face = self.face
            uchar = self.__hbPrivate
            while uchar in face.charToGlyph:
                uchar += 1
            assert uchar <= 0xF800
            self.__hbPrivate = self.__hbUnis[name] = uchar
            face.charToGlyph[uchar] = gid
            face.glyphToChar.setdefault(gid, []).append(uchar)
            face.charWidths[uchar] = advance
        return uchar

    def pdfScale(self, v):
        return self.face._pdfScale(v)

    def unregister(self):
        if self.fontName in pdfmetrics._fonts:
            del pdfmetrics._fonts[self.fontName]
        if self.face.name in pdfmetrics._dynFaceNames:
            del pdfmetrics._dynFaceNames[self.face.name]

    @property
    def shapable(self):
        try:
            import uharfbuzz
            return bool(self._shapable and uharfbuzz)
        except ImportError:
            return False
    
    @shapable.setter
    def shapable(self, v):
        try:
            import uharfbuzz
            self._shapable = bool(v and uharfbuzz)
        except ImportError:
            self._shapable = False


def _buildWArray(widths, defaultWidth):
    result = []
    i = 0
    n = len(widths)
    while i < n:
        if widths[i] != defaultWidth:
            runStart = i
            runWidths = []
            while i < n and widths[i] != defaultWidth:
                runWidths.append(widths[i])
                i += 1
            result.append(runStart)
            result.append(pdfdoc.PDFArray(runWidths))
        else:
            i += 1
    return result


def _buildCMap(subset):
    lines = []
    lines.append('/CIDInit /ProcSet findresource begin')
    lines.append('12 dict begin')
    lines.append('begincmap')
    lines.append('/CIDSystemInfo')
    lines.append('<< /Registry (Adobe) /Ordering (Identity) /Supplement 0 >>')
    lines.append('def')
    lines.append('/CMapName /CustomCMap def')
    lines.append('/CMapType 1 def')
    lines.append('1 begincodespacerange')
    lines.append('<00> <%02X>' % (len(subset) - 1))
    lines.append('endcodespacerange')
    lines.append('1 begincidrange')
    lines.append('<00> <%02X> 0' % (len(subset) - 1))
    lines.append('endcidrange')
    lines.append('endcmap')
    lines.append('CMapName currentdict /CMap defineresource pop')
    lines.append('end')
    lines.append('end')
    return '\n'.join(lines) + '\n'

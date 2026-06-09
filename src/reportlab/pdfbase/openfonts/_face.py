# Font face handling for OpenType fonts
# Extracted from ttfonts.py for the openfonts package.

from struct import unpack
from reportlab.pdfbase import pdfmetrics, pdfdoc
from ._common import FF_FIXED, FF_SERIF, FF_SYMBOLIC, FF_SCRIPT, FF_NONSYMBOLIC, FF_ITALIC, FF_ALLCAP, FF_SMALLCAP, FF_FORCEBOLD
from ._ttf import FontFile


def _extractCFFFromSFNT(sfntData):
    """Extract the CFF table from an sfnt (OTF) container.
    
    PDF /Type1C FontFile3 streams require raw CFF data, not the full sfnt file.
    This parses the sfnt table directory and returns just the CFF table data.
    """
    numTables = unpack('>H', sfntData[4:6])[0]
    offset = 12
    for _ in range(numTables):
        tag = sfntData[offset:offset+4]
        tableOffset = unpack('>I', sfntData[offset+8:offset+12])[0]
        tableLength = unpack('>I', sfntData[offset+12:offset+16])[0]
        if tag == b'CFF ':
            return sfntData[tableOffset:tableOffset+tableLength]
        offset += 16
    raise ValueError('CFF table not found in sfnt data')


class FontFace(FontFile, pdfmetrics.TypeFace):
    """OpenType typeface.

    Conceptually similar to a single byte typeface, but the glyphs are
    identified by UCS character codes instead of glyph names."""

    def __init__(self, filename, validate=0, subfontIndex=0):
        "Loads an OpenType font from filename."
        pdfmetrics.TypeFace.__init__(self, None)
        FontFile.__init__(self, filename, validate=validate, subfontIndex=subfontIndex)

    def getCharWidth(self, code):
        "Returns the width of character U+<code>"
        return self.charWidths.get(code, self.defaultWidth)

    def addSubsetObjects(self, doc, fontname, subset):
        """Generate an OpenType font subset and add it to the PDF document.
        Returns a PDFReference to the new FontDescriptor object."""

        sfntData = self.makeSubset(subset)

        if self.isCFF:
            fontContent = _extractCFFFromSFNT(sfntData)
        else:
            fontContent = sfntData

        fontFile = pdfdoc.PDFStream()
        fontFile.content = fontContent
        fontFile.dictionary['Length1'] = len(fontContent)
        if self.isCFF:
            if getattr(self, 'isCID', False):
                fontFile.dictionary['Subtype'] = pdfdoc.PDFName('CIDFontType0C')
            else:
                fontFile.dictionary['Subtype'] = pdfdoc.PDFName('Type1C')
        if doc.compression:
            fontFile.filters = [pdfdoc.PDFZCompress]
        fontFileRef = doc.Reference(fontFile, 'fontFile:%s(%s)' % (self.filename, fontname))

        flags = self.flags & ~ FF_NONSYMBOLIC
        flags = flags | FF_SYMBOLIC

        if self.isCFF:
            fontFileKey = 'FontFile3'
        else:
            fontFileKey = 'FontFile2'

        fontDescriptor = pdfdoc.PDFDictionary({
            'Type': '/FontDescriptor',
            'Ascent': self.ascent,
            'CapHeight': self.capHeight,
            'Descent': self.descent,
            'Flags': flags,
            'FontBBox': pdfdoc.PDFArray(self.bbox),
            'FontName': pdfdoc.PDFName(fontname),
            'ItalicAngle': self.italicAngle,
            'StemV': self.stemV,
            fontFileKey: fontFileRef,
            'MissingWidth': self.defaultWidth,
            })
        return doc.Reference(fontDescriptor, 'fontDescriptor:' + fontname)

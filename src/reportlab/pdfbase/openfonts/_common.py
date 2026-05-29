# Common utilities for OpenType font support
# Extracted from ttfonts.py for the openfonts package.

from struct import pack
from reportlab.pdfbase import pdfdoc


class TTFError(pdfdoc.PDFError):
    "OpenType/TrueType font exception"
    pass


def SUBSETN(n, table=bytes.maketrans(b'0123456789', b'ABCDEFGIJK')):
    return bytes('%6.6d' % n, 'ASCII').translate(table)


def makeToUnicodeCMap(fontname, subset):
    """Creates a ToUnicode CMap for a given subset.  See Adobe
    _PDF_Reference (ISBN 0-201-75839-3) for more information."""
    cmap = [
        "/CIDInit /ProcSet findresource begin",
        "12 dict begin",
        "begincmap",
        "/CIDSystemInfo",
        "<< /Registry (%s)" % fontname,
        "/Ordering (%s)" % fontname,
        "/Supplement 0",
        ">> def",
        "/CMapName /%s def" % fontname,
        "/CMapType 2 def",
        "1 begincodespacerange",
        "<00> <%02X>" % (len(subset) - 1),
        "endcodespacerange",
    ]
    entries = list(enumerate(subset))
    chunk_size = 100
    for start in range(0, len(entries), chunk_size):
        chunk = entries[start:start + chunk_size]
        cmap.append("%d beginbfchar" % len(chunk))
        for i, v in chunk:
            cmap.append("<%02X> <%04X>" % (i, v))
        cmap.append("endbfchar")
    cmap += [
        "endcmap",
        "CMapName currentdict /CMap defineresource pop",
        "end",
        "end"
    ]
    return '\n'.join(cmap)


def splice(stream, offset, value):
    """Splices the given value into stream at the given offset and
    returns the resulting stream (the original is unchanged)"""
    return stream[:offset] + value + stream[offset + len(value):]


def _set_ushort(stream, offset, value):
    """Writes the given unsigned short value into stream at the given
    offset and returns the resulting stream (the original is unchanged)"""
    return splice(stream, offset, pack(">H", value))


# PDF font flags (see PDF Reference Guide table 5.19)
FF_FIXED        = 1 <<  1-1
FF_SERIF        = 1 <<  2-1
FF_SYMBOLIC     = 1 <<  3-1
FF_SCRIPT       = 1 <<  4-1
FF_NONSYMBOLIC  = 1 <<  6-1
FF_ITALIC       = 1 <<  7-1
FF_ALLCAP       = 1 << 17-1
FF_SMALLCAP     = 1 << 18-1
FF_FORCEBOLD    = 1 << 19-1

# TrueType glyph flags (only those used in composite glyph processing)
GF_ARG_1_AND_2_ARE_WORDS        = 1 << 0
GF_ARGS_ARE_XY_VALUES           = 1 << 1
GF_WE_HAVE_A_SCALE              = 1 << 3
GF_MORE_COMPONENTS              = 1 << 5
GF_WE_HAVE_AN_X_AND_Y_SCALE     = 1 << 6
GF_WE_HAVE_A_TWO_BY_TWO         = 1 << 7

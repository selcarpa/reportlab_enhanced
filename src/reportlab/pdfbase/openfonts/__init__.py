# OpenType font support package
# Unified support for TrueType and CFF fonts.

from ._common import (
    TTFError, SUBSETN, makeToUnicodeCMap,
    FF_FIXED, FF_SERIF, FF_SYMBOLIC, FF_SCRIPT, FF_NONSYMBOLIC,
    FF_ITALIC, FF_ALLCAP, FF_SMALLCAP, FF_FORCEBOLD,
)
from ._sfnt import FontParser, TTFNameBytes, TTFOpenFile
from ._ttf import FontFile, FontMaker
from ._cff import CFFParser, CFFSubsetter
from ._face import FontFace
from ._encoding import FontEncoding
from ._font import OpenTypeFont
from ._shaping import (
    ShapedFragWord, ShapedStr, ShapeData, shapeFragWord, shapeStr,
    makeShapedFragWord, _sdGuardL, _sdSimple,
)

try:
    import uharfbuzz
except ImportError:
    uharfbuzz = None

def freshTTFont(ttfn, ttfpath, **kwds):
    '''return a new instance corresponding to a ttf path'''
    from reportlab.pdfbase import pdfmetrics
    try:
        ttf = pdfmetrics.getFont(ttfn)
        ttf.unregister()
    except:
        pass
    return OpenTypeFont(ttfn, ttfpath, **kwds)

# Backward compatibility aliases
TTFont = OpenTypeFont
TTFontParser = FontParser
TTFontFile = FontFile
TTFontFace = FontFace
TTFontMaker = FontMaker
TTEncoding = FontEncoding

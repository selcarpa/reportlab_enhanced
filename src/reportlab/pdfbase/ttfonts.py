#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__ = '$Id$'
__doc__="""TrueType font support (DEPRECATED - use openfonts instead)

This module is a compatibility layer that imports from the openfonts package.
Please migrate to using:

    from reportlab.pdfbase.openfonts import OpenTypeFont

All classes and functions are re-exported here for backward compatibility.
"""

import warnings

# Issue deprecation warning on import
warnings.warn(
    "reportlab.pdfbase.ttfonts is deprecated. "
    "Use reportlab.pdfbase.openfonts instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from openfonts for backward compatibility
from reportlab.pdfbase.openfonts import (
    # Main classes
    OpenTypeFont,
    FontParser,
    FontFile,
    FontFace,
    FontMaker,
    FontEncoding,
    
    # CFF support
    CFFParser,
    CFFSubsetter,
    
    # Shaping
    ShapedFragWord,
    ShapedStr,
    ShapeData,
    shapeFragWord,
    shapeStr,
    makeShapedFragWord,
    _sdGuardL,
    _sdSimple,
    
    # Utilities
    TTFError,
    SUBSETN,
    makeToUnicodeCMap,
    TTFNameBytes,
    TTFOpenFile,
    
    # PDF font flags
    FF_FIXED, FF_SERIF, FF_SYMBOLIC, FF_SCRIPT, FF_NONSYMBOLIC,
    FF_ITALIC, FF_ALLCAP, FF_SMALLCAP, FF_FORCEBOLD,
    
    # uharfbuzz
    uharfbuzz,
    
    # freshTTFont
    freshTTFont,
)

# Re-export from rl_accel for backward compatibility
from reportlab.lib.rl_accel import calcChecksum, add32

# Backward compatibility aliases
TTFont = OpenTypeFont
TTFontParser = FontParser
TTFontFile = FontFile
TTFontFace = FontFace
TTFontMaker = FontMaker
TTEncoding = FontEncoding

# Preserve the initial values for reset
from reportlab.rl_config import register_reset
from reportlab.pdfbase.openfonts._sfnt import _cached_ttf_dirs

def _reset():
    _cached_ttf_dirs.clear()

register_reset(_reset)
del register_reset

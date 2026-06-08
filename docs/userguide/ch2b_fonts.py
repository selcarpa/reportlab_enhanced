#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
from tools.docco.rl_doc_utils import *
import reportlab

heading1("Fonts")

disc("""
This chapter introduces the new unified font system introduced in this fork.
It provides a single API for both TrueType (.ttf) and OpenType/CFF (.otf) fonts,
with support for font fallback, text shaping, and automatic subsetting.
""")

disc("""
The old font modules ($reportlab.pdfbase.ttfonts$) have been refactored into a
new $reportlab.pdfbase.openfonts$ package. The legacy $TTFont$ name is preserved
as a backward-compatibility alias for $OpenTypeFont$. New code should import
from the new location.
""")

disc("""
Compared to the legacy system (Chapter 2a), the key changes are:
""")
bullet("""
Unified API: $OpenTypeFont$ handles both TrueType and OpenType/CFF fonts.
""")
bullet("""
CFF support: OpenType fonts using CFF outlines (PostScript-flavored OTF) are
now fully supported, including subsetting and PDF embedding.
""")
bullet("""
Font fallback: Automatically substitute glyphs from a fallback font when the
primary font lacks a character.
""")
bullet("""
Text shaping: Optional HarfBuzz-based text shaping (requires uharfbuzz) for
proper ligature, kerning, and complex script support.
""")
bullet("""
CID Type0 CIDFont support: For CFF fonts with CID keyed encoding, the system
generates proper CIDFontType0 + Type0 font dictionaries.
""")
bullet("""
Dynamic subsetting: Subsets are built on-the-fly based on actual characters used,
keeping PDF file sizes minimal.
""")

heading2("Basic usage: OpenTypeFont")

disc("""
The main class is $OpenTypeFont$ in the $reportlab.pdfbase.openfonts$ package.
It accepts both .ttf and .otf files:
""")

eg("""
from reportlab.pdfbase.openfonts import OpenTypeFont
from reportlab.pdfbase import pdfmetrics

# Load a TrueType font
font = OpenTypeFont('MyFont', 'path/to/font.ttf')
pdfmetrics.registerFont(font)

# Load an OpenType/CFF font
cffFont = OpenTypeFont('MyCFFFont', 'path/to/font.otf')
pdfmetrics.registerFont(cffFont)

# Use in canvas
from reportlab.pdfgen import canvas
c = canvas.Canvas('output.pdf')
c.setFont('MyFont', 12)
c.drawString(100, 700, 'Hello from OpenTypeFont!')
c.save()
""")

disc("""
The first argument is the internal name used to refer to the font in ReportLab.
The second argument is the path to the font file. If a relative path is given,
the file is searched for in the current directory and in directories specified
by $reportlab.rl_config.TTFSearchPath$.
""")

disc("""
$OpenTypeFont$ automatically detects whether the font is TrueType or CFF-based
by reading the sfnt header. No special handling is needed from user code.
""")

heading2("Backward compatibility")

disc("""
The old $reportlab.pdfbase.ttfonts$ module still works but emits a
DeprecationWarning. It is now a thin compatibility wrapper around the
$openfonts$ package. All existing code using $TTFont$ will continue to
function:
""")

eg("""
# Legacy import - still works but deprecated
from reportlab.pdfbase.ttfonts import TTFont

# TTFont is now an alias for OpenTypeFont
font = TTFont('Vera', 'Vera.ttf')  # same as OpenTypeFont('Vera', 'Vera.ttf')
pdfmetrics.registerFont(font)
""")

disc("""
The following backward-compatibility aliases are provided in $reportlab.pdfbase.ttfonts$:
""")
bullet("""
$TTFont$ = $OpenTypeFont$
""")
bullet("""
$TTFontParser$ = $FontParser$
""")
bullet("""
$TTFontFile$ = $FontFile$
""")
bullet("""
$TTFontFace$ = $FontFace$
""")
bullet("""
$TTFontMaker$ = $FontMaker$
""")
bullet("""
$TTEncoding$ = $FontEncoding$
""")

heading2("Font face properties")

disc("""
After loading a font, the $face$ attribute provides access to font metrics
and metadata:
""")

eg("""
font = OpenTypeFont('MyFont', 'font.ttf')
face = font.face

# Basic properties
print(face.name)           # PostScript font name
print(face.familyName)     # Font family name
print(face.styleName)      # Style name (Regular, Bold, etc.)
print(face.unitsPerEm)     # Font design units per em
print(face.bbox)           # Bounding box [xMin, yMin, xMax, yMax]
print(face.ascent)         # Typographic ascent
print(face.descent)        # Typographic descent
print(face.capHeight)      # Cap height
print(face.italicAngle)    # Italic angle
print(face.isCFF)          # True if CFF-based (OTF), False if TrueType
print(face.isCID)          # True if CFF font uses CID keyed encoding
print(face.defaultWidth)   # Default glyph width
""")

disc("""
Character widths and glyph mapping:
""")

eg("""
# Check if a character exists
print(0x4F60 in face.charToGlyph)  # CJK character
print('A' in face.charToGlyph)     # Can also use string

# Get character width
width = face.getCharWidth(0x4F60)  # width in 1000-units
width = face.getCharWidth(ord('A'))
""")

heading2("Font fallback")

disc("""
The font fallback feature allows automatic substitution of missing glyphs
from a fallback font. This is useful for mixed-script documents (e.g.,
Latin + CJK, or combining a symbol font with a text font).
""")

disc("""
The feature is controlled by the environment variable
$REPORTLAB_FONT_FALLBACK$. It is disabled by default:
""")

eg("""
REPORTLAB_FONT_FALLBACK=1 python your_script.py
""")

disc("""
Configure fallback fonts via the $substitutionFonts$ property:
""")

eg("""
from reportlab.pdfbase.openfonts import OpenTypeFont
from reportlab.pdfbase import pdfmetrics

primary = OpenTypeFont('NotoSans', 'NotoSans-Regular.ttf')
fallback = OpenTypeFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')

pdfmetrics.registerFont(primary)
pdfmetrics.registerFont(fallback)

primary.substitutionFonts = [fallback]

# Now text with CJK characters will automatically fall back
c.setFont('NotoSans', 12)
c.drawString(100, 700, 'Hello 你好 World')
""")

disc("""
A convenience function $registerFontWithFallback$ is provided in
$reportlab.pdfbase.pdfmetrics$:
""")

eg("""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.openfonts import OpenTypeFont

font = pdfmetrics.registerFontWithFallback(
    'NotoSans', 'NotoSans-Regular.ttf',
    fallbackFonts=[OpenTypeFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')]
)
# The fallback font is auto-registered and linked
""")

disc("""
The $fallbackFonts$ parameter accepts either font name strings (resolved via
$getFont$) or $OpenTypeFont$ instances.
""")

disc("""
You can check whether a font contains a specific glyph using $hasGlyph()$:
""")

eg("""
font = OpenTypeFont('MyFont', 'font.ttf')
font.hasGlyph('A')          # True
font.hasGlyph('你')          # False if font lacks CJK glyphs
font.hasGlyph(0x4F60)       # Same as above, using Unicode code point
""")

heading2("Font family registration for Platypus")

disc("""
To use OpenType fonts in Platypus paragraphs with $&lt;b&gt;$ and $&lt;i&gt;$ tags,
register a font family that maps style variants:
""")

eg("""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.openfonts import OpenTypeFont

pdfmetrics.registerFont(OpenTypeFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(OpenTypeFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(OpenTypeFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(OpenTypeFont('VeraBI', 'VeraBI.ttf'))

pdfmetrics.registerFontFamily(
    'Vera',
    normal='Vera',
    bold='VeraBd',
    italic='VeraIt',
    boldItalic='VeraBI'
)
""")

disc("""
If only a regular weight is available, map all variants to the same font:
""")

eg("""
pdfmetrics.registerFontFamily(
    'MyFont',
    normal='MyFont',
    bold='MyFont',
    italic='MyFont',
    boldItalic='MyFont'
)
""")

heading2("Text shaping (HarfBuzz)")

disc("""
When $uharfbuzz$ is installed, ReportLab can perform text shaping for proper
ligature, kerning, and complex script positioning. The shaping system is built
into the paragraph layout engine and is enabled automatically for fonts that
have their $shapable$ property set.
""")

disc("""
The shaping system provides the following APIs:
""")
bullet("""
$shapeFragWord(w)$: Shape a platypus frag word, returning a $ShapedFragWord$.
""")
bullet("""
$shapeStr(s, fontName, fontSize)$: Shape a plain string, returning a $ShapedStr$.
""")
bullet("""
$ShapedStr$: A string subclass carrying per-character positioning data.
""")

disc("""
You can check if a font is shapable:
""")

eg("""
font = OpenTypeFont('MyFont', 'font.ttf')
print(font.shapable)  # True if uharfbuzz is installed and font passed filters
""")

disc("""
To disable shaping for specific fonts, add a glob pattern to
$reportlab.rl_config.unShapedFontGlob$:
""")

eg("""
import reportlab.rl_config
reportlab.rl_config.unShapedFontGlob.append('*monospace*')
""")

heading2("Working with CFF (PostScript-flavored OTF) fonts")

disc("""
CFF fonts use PostScript-based outline data instead of TrueType glyph data.
The new $OpenTypeFont$ class handles both types transparently. The detection
is automatic:
""")

eg("""
font = OpenTypeFont('MyCFF', 'font.otf')
print(font.face.isCFF)    # True for CFF-based OTF
print(font.face.isCID)    # True if CID keyed (e.g., CJK OTF fonts)
""")

disc("""
CID-keyed CFF fonts (common for CJK fonts) are handled specially — they
generate PDF /CIDFontType0 + /Type0 font dictionaries instead of the
standard /Type1 + /FontFile3 encoding. This ensures proper rendering in
PDF viewers for large character sets.
""")

disc("""
For non-CID CFF fonts (e.g., Latin OTF fonts), the system generates standard
/Type1 font dictionaries with /FontFile3 containing the subsetted CFF data
with /Subtype /Type1C.
""")

heading2("Font file search path")

disc("""
When a relative font file path is provided, ReportLab searches for the file in:
""")
list1("The current working directory.")
list1("Directories listed in $reportlab.rl_config.TTFSearchPath$.")
restartList()

disc("""
You can configure the search path:
""")

eg("""
import reportlab.rl_config
reportlab.rl_config.TTFSearchPath = ['/usr/share/fonts', '/path/to/custom/fonts']
""")

heading2("TTC (TrueType Collection) support")

disc("""
Fonts packaged as .ttc files (TrueType Collections) are supported. Specify the
subfont index (0-based) to select which font from the collection to use:
""")

eg("""
font = OpenTypeFont('MyFont', 'collection.ttc', subfontIndex=0)  # first font
font2 = OpenTypeFont('MyFont2', 'collection.ttc', subfontIndex=1)  # second font
""")

heading2("Performance tips")

disc("""
For large fonts (especially CJK fonts with thousands of glyphs):
""")
bullet("""
Disable checksum validation for faster loading: pass $validate=0$ to the
$OpenTypeFont$ constructor.
""")
bullet("""
Font subsetting is automatic — only used characters are embedded in the PDF.
""")
bullet("""
Consider using OTF/CFF fonts with CID encoding for CJK text, as they
produce more compact PDF output.
""")

heading2("Migration guide")

disc("""
To migrate from the legacy font system to the new unified API:
""")
list1("Replace $from reportlab.pdfbase.ttfonts import TTFont$ with $from reportlab.pdfbase.openfonts import OpenTypeFont$.")
list1("Replace $TTFont(name, filename)$ with $OpenTypeFont(name, filename)$.")
list1("Replace $TTFont$ type checks with $OpenTypeFont$.")
list1("Import $registerFontWithFallback$ from $reportlab.pdfbase.pdfmetrics$ (same location as before).")
restartList()

disc("""
The old $TTFont$ name still works as a compatibility alias, but will emit
a $DeprecationWarning$. New code should use $OpenTypeFont$ directly.
""")

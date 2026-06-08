# TrueType font file handling
# Extracted from ttfonts.py for the openfonts package.

from struct import pack, unpack
from io import BytesIO
import os, time

from reportlab.lib.utils import bytestr, char2int, isStr, isBytes
from reportlab.lib.rl_accel import calcChecksum, add32
from reportlab import rl_config

from ._common import (
    TTFError, splice, _set_ushort,
    FF_FIXED, FF_SERIF, FF_SYMBOLIC, FF_SCRIPT, FF_NONSYMBOLIC,
    FF_ITALIC, FF_ALLCAP, FF_SMALLCAP, FF_FORCEBOLD,
    GF_ARG_1_AND_2_ARE_WORDS, GF_MORE_COMPONENTS,
    GF_WE_HAVE_A_SCALE, GF_WE_HAVE_AN_X_AND_Y_SCALE, GF_WE_HAVE_A_TWO_BY_TWO,
)
from ._sfnt import FontParser, TTFNameBytes
from ._cff import _readIndex


_CFF_STANDARD_SIDS = {
    0: '.notdef', 1: 'space', 2: 'exclam', 3: 'quotedbl', 4: 'numbersign',
    5: 'dollar', 6: 'percent', 7: 'ampersand', 8: 'quoteright',
    9: 'parenleft', 10: 'parenright', 11: 'asterisk', 12: 'plus', 13: 'comma',
    14: 'hyphen', 15: 'period', 16: 'slash', 17: 'zero', 18: 'one',
    19: 'two', 20: 'three', 21: 'four', 22: 'five', 23: 'six', 24: 'seven',
    25: 'eight', 26: 'nine', 27: 'colon', 28: 'semicolon', 29: 'less',
    30: 'equal', 31: 'greater', 32: 'question', 33: 'at', 34: 'A', 35: 'B',
    36: 'C', 37: 'D', 38: 'E', 39: 'F', 40: 'G', 41: 'H', 42: 'I', 43: 'J',
    44: 'K', 45: 'L', 46: 'M', 47: 'N', 48: 'O', 49: 'P', 50: 'Q', 51: 'R',
    52: 'S', 53: 'T', 54: 'U', 55: 'V', 56: 'W', 57: 'X', 58: 'Y', 59: 'Z',
    60: 'bracketleft', 61: 'backslash', 62: 'bracketright', 63: 'asciicircum',
    64: 'underscore', 65: 'quoteleft', 66: 'a', 67: 'b', 68: 'c', 69: 'd',
    70: 'e', 71: 'f', 72: 'g', 73: 'h', 74: 'i', 75: 'j', 76: 'k', 77: 'l',
    78: 'm', 79: 'n', 80: 'o', 81: 'p', 82: 'q', 83: 'r', 84: 's', 85: 't',
    86: 'u', 87: 'v', 88: 'w', 89: 'x', 90: 'y', 91: 'z', 92: 'braceleft',
    93: 'bar', 94: 'braceright', 95: 'asciitilde', 96: 'exclamdown',
    97: 'cent', 98: 'sterling', 99: 'fraction', 100: 'yen', 101: 'florin',
    102: 'section', 103: 'currency', 104: 'quotesingle', 105: 'quotedblleft',
    106: 'guillemotleft', 107: 'guilsinglleft', 108: 'guilsinglright',
    109: 'fi', 110: 'fl', 111: 'endash', 112: 'dagger', 113: 'daggerdbl',
    114: 'periodcentered', 115: 'paragraph', 116: 'bullet', 117: 'quotesinglbase',
    118: 'quotedblbase', 119: 'quotedblright', 120: 'guillemotright',
    121: 'ellipsis', 122: 'perthousand', 123: 'questiondown', 124: 'grave',
    125: 'acute', 126: 'circumflex', 127: 'tilde', 128: 'macron', 129: 'breve',
    130: 'dotaccent', 131: 'dieresis', 132: 'ring', 133: 'cedilla',
    134: 'hungarumlaut', 135: 'ogonek', 136: 'caron', 137: 'emdash',
    138: 'AE', 139: 'ordfeminine', 140: 'Lslash', 141: 'Oslash', 142: 'OE',
    143: 'ordmasculine', 144: 'ae', 145: 'dotlessi', 146: 'lslash',
    147: 'oslash', 148: 'oe', 149: 'germandbls', 150: 'onesuperior',
    151: 'logicalnot', 152: 'mu', 153: 'trademark', 154: 'Eth', 155: 'onehalf',
    156: 'plusminus', 157: 'Thorn', 158: 'onequarter', 159: 'divide',
    160: 'brokenbar', 161: 'degree', 162: 'thorn', 163: 'threequarters',
    164: 'twosuperior', 165: 'registered', 166: 'minus', 167: 'eth',
    168: 'multiply', 169: 'threesuperior', 170: 'copyright', 171: 'Aacute',
    172: 'Acircumflex', 173: 'Adieresis', 174: 'Agrave', 175: 'Aring',
    176: 'Atilde', 177: 'Ccedilla', 178: 'Eacute', 179: 'Ecircumflex',
    180: 'Edieresis', 181: 'Egrave', 182: 'Iacute', 183: 'Icircumflex',
    184: 'Idieresis', 185: 'Igrave', 186: 'Ntilde', 187: 'Oacute',
    188: 'Ocircumflex', 189: 'Odieresis', 190: 'Ograve', 191: 'Otilde',
    192: 'Scaron', 193: 'Uacute', 194: 'Ucircumflex', 195: 'Udieresis',
    196: 'Ugrave', 197: 'Yacute', 198: 'Ydieresis', 199: 'Zcaron',
    200: 'aacute', 201: 'acircumflex', 202: 'adieresis', 203: 'agrave',
    204: 'aring', 205: 'atilde', 206: 'ccedilla', 207: 'eacute',
    208: 'ecircumflex', 209: 'edieresis', 210: 'egrave', 211: 'iacute',
    212: 'icircumflex', 213: 'idieresis', 214: 'igrave', 215: 'ntilde',
    216: 'oacute', 217: 'ocircumflex', 218: 'odieresis', 219: 'ograve',
    220: 'otilde', 221: 'scaron', 222: 'uacute', 223: 'ucircumflex',
    224: 'udieresis', 225: 'ugrave', 226: 'yacute', 227: 'ydieresis',
    228: 'zcaron', 229: 'exclamsmall', 230: 'Hungarumlautsmall', 231: 'dollaroldstyle',
    232: 'dollarsuperior', 233: 'ampersandsmall', 234: 'Acutesmall',
    235: 'parenleftsuperior', 236: 'parenrightsuperior', 237: 'twodotenleader',
    238: 'onedotenleader', 239: 'zerooldstyle', 240: 'oneoldstyle',
    241: 'twooldstyle', 242: 'threeoldstyle', 243: 'fouroldstyle',
    244: 'fiveoldstyle', 245: 'sixoldstyle', 246: 'sevenoldstyle',
    247: 'eightoldstyle', 248: 'nineoldstyle', 249: 'commasuperior',
    250: 'threequartersemdash', 251: 'periodsuperior', 252: 'questionsmall',
    253: 'asuperior', 254: 'bsuperior', 255: 'centsuperior', 256: 'dsuperior',
    257: 'esuperior', 258: 'isuperior', 259: 'lsuperior', 260: 'msuperior',
    261: 'nsuperior', 262: 'osuperior', 263: 'rsuperior', 264: 'ssuperior',
    265: 'tsuperior', 266: 'ff', 267: 'ffi', 268: 'ffl', 269: 'parenleftinferior',
    270: 'parenrightinferior', 271: 'Circumflexsmall', 272: 'hyphensuperior',
    273: 'Gravesmall', 274: 'Asmall', 275: 'Bsmall', 276: 'Csmall',
    277: 'Dsmall', 278: 'Esmall', 279: 'Fsmall', 280: 'Gsmall', 281: 'Hsmall',
    282: 'Ismall', 283: 'Jsmall', 284: 'Ksmall', 285: 'Lsmall', 286: 'Msmall',
    287: 'Nsmall', 288: 'Osmall', 289: 'Psmall', 290: 'Qsmall', 291: 'Rsmall',
    292: 'Ssmall', 293: 'Tsmall', 294: 'Usmall', 295: 'Vsmall', 296: 'Wsmall',
    297: 'Xsmall', 298: 'Ysmall', 299: 'Zsmall', 300: 'colonmonetary',
    301: 'onefitted', 302: 'rupiah', 303: 'Tildesmall', 304: 'exclamdownsmall',
    305: 'centoldstyle', 306: 'Lslashsmall', 307: 'Scaronsmall',
    308: 'Zcaronsmall', 309: 'Dieresissmall', 310: 'Brevesmall',
    311: 'Caronsmall', 312: 'Dotaccentsmall', 313: 'Macronsmall',
    314: 'figuredash', 315: 'hypheninferior', 316: 'Ogoneksmall',
    317: 'Ringsmall', 318: 'Cedillasmall', 319: 'questiondownsmall',
    320: 'oneeighth', 321: 'threeeighths', 322: 'fiveeighths', 323: 'seveneighths',
    324: 'onethird', 325: 'twothirds', 326: 'zerosuperior', 327: 'foursuperior',
    328: 'fivesuperior', 329: 'sixsuperior', 330: 'sevensuperior',
    331: 'eightsuperior', 332: 'ninesuperior', 333: 'zeroinferior',
    334: 'oneinferior', 335: 'twoinferior', 336: 'threeinferior',
    337: 'fourinferior', 338: 'fiveinferior', 339: 'sixinferior',
    340: 'seveninferior', 341: 'eightinferior', 342: 'nineinferior',
    343: 'centinferior', 344: 'dollarinferior', 345: 'periodinferior',
    346: 'commainferior', 347: 'Agravesmall', 348: 'Aacutesmall',
    349: 'Acircumflexsmall', 350: 'Atildesmall', 351: 'Adieresissmall',
    352: 'Aringsmall', 353: 'AEsmall', 354: 'Ccedillasmall', 355: 'Egravesmall',
    356: 'Eacutesmall', 357: 'Ecircumflexsmall', 358: 'Edieresissmall',
    359: 'Igravesmall', 360: 'Iacutesmall', 361: 'Icircumflexsmall',
    362: 'Idieresissmall', 363: 'Ethsmall', 364: 'Ntildesmall',
    365: 'Ogravesmall', 366: 'Oacutesmall', 367: 'Ocircumflexsmall',
    368: 'Otildesmall', 369: 'Odieresissmall', 370: 'OEsmall',
    371: 'Oslashsmall', 372: 'Ugravesmall', 373: 'Uacutesmall',
    374: 'Ucircumflexsmall', 375: 'Udieresissmall', 376: 'Yacutesmall',
    377: 'Thornsmall', 378: 'Ydieresissmall', 379: '001.000',
    380: '001.001', 381: '001.002', 382: '001.003', 383: 'Black',
    384: 'Bold', 385: 'Book', 386: 'Light', 387: 'Medium', 388: 'Regular',
    389: 'Roman', 390: 'Semibold',
    391: 'Adobe', 392: 'Identity',
}

def _sidToString(strings, sid):
    if sid in strings:
        val = strings[sid]
        if isinstance(val, bytes):
            return val.decode('latin-1', errors='replace')
        return str(val)
    if sid in _CFF_STANDARD_SIDS:
        return _CFF_STANDARD_SIDS[sid]
    return ''

def _readStringsIdx(cff_data, strIdxOff):
    o, count, offs = _readIndex(cff_data, strIdxOff)
    strings = {}
    if count > 0 and len(offs) >= 2:
        for i in range(count):
            start = o + offs[i] - 1
            end = o + offs[i+1] - 1
            s = cff_data[start:end]
            sid = 391 + i
            strings[sid] = s
    return strings


class FontMaker:
    "Basic sfnt file generator"

    def __init__(self):
        "Initializes the generator."
        self.tables = {}

    def add(self, tag, data):
        "Adds a table to the sfnt file."
        if tag == 'head':
            data = splice(data, 8, b'\0\0\0\0')
        self.tables[tag] = data

    def makeStream(self):
        "Finishes the generation and returns the sfnt file as a string"
        stm = BytesIO()
        write = stm.write

        tables = self.tables
        numTables = len(tables)
        searchRange = 1
        entrySelector = 0
        while searchRange * 2 <= numTables:
            searchRange = searchRange * 2
            entrySelector = entrySelector + 1
        searchRange = searchRange * 16
        rangeShift = numTables * 16 - searchRange

        # Header
        # Use OTTO version for CFF (OTF) fonts, 0x00010000 for TrueType
        sfntVersion = 0x4F54544F if 'CFF ' in tables else 0x00010000
        write(pack(">lHHHH", sfntVersion, numTables, searchRange,
                                 entrySelector, rangeShift))

        # Table directory
        offset = 12 + numTables * 16
        wStr = lambda x: write(bytes(tag, 'latin1'))
        tables_items = list(sorted(tables.items()))
        for tag, data in tables_items:
            if tag == 'head':
                head_start = offset
            checksum = calcChecksum(data)
            wStr(tag)
            write(pack(">LLL", checksum, offset, len(data)))
            paddedLength = (len(data) + 3) & ~3
            offset = offset + paddedLength

        # Table data
        for tag, data in tables_items:
            data += b"\0\0\0"
            write(data[:len(data) & ~3])

        checksum = calcChecksum(stm.getvalue())
        checksum = add32(0xB1B0AFBA, -checksum)
        stm.seek(head_start + 8)
        write(pack('>L', checksum))

        return stm.getvalue()


class FontFile(FontParser):
    "TTF file parser and generator"
    _agfnc = 0
    _agfnm = {}

    def __init__(self, file, charInfo=1, validate=0, subfontIndex=0):
        """Loads and parses a TrueType font file.

        file can be a filename or a file object.  If validate is set to a false
        values, skips checksum validation.  This can save time, especially if
        the font is large.  See FontFile.extractInfo for more information.
        """
        if isStr(subfontIndex):  # bytes or unicode
            sfi = 0
            __dict__ = self.__dict__.copy()
            while True:
                FontParser.__init__(self, file, validate=validate, subfontIndex=sfi)
                numSubfonts = self.numSubfonts = self.read_ulong()
                self.extractInfo(charInfo)
                if (isBytes(subfontIndex) and subfontIndex == self.name
                    or subfontIndex == self.name.ustr):  # we found it
                    return
                if not sfi:
                    __dict__.update(dict(_ttf_data=self._ttf_data, filename=self.filename))
                sfi += 1
                if sfi >= numSubfonts:
                    raise ValueError('cannot find %r subfont %r' % (self.filename, subfontIndex))
                self.__dict__.clear()
                self.__dict__.update(__dict__)
        else:
            FontParser.__init__(self, file, validate=validate, subfontIndex=subfontIndex)
            self.extractInfo(charInfo)

    def extractInfo(self, charInfo=1):
        """
        Extract typographic information from the loaded font file.
        """
        # name - Naming table
        name_offset = self.seek_table("name")
        format = self.read_ushort()
        if format != 0:
            raise TTFError("Unknown name table format (%d)" % format)
        numRecords = self.read_ushort()
        string_data_offset = name_offset + self.read_ushort()
        names = {1: None, 2: None, 3: None, 4: None, 6: None}
        K = list(names.keys())
        nameCount = len(names)
        for i in range(numRecords):
            platformId = self.read_ushort()
            encodingId = self.read_ushort()
            languageId = self.read_ushort()
            nameId = self.read_ushort()
            length = self.read_ushort()
            offset = self.read_ushort()
            if nameId not in K:
                continue
            N = None
            if platformId == 3 and encodingId == 1 and languageId == 0x409:  # Microsoft, Unicode, US English, PS Name
                opos = self._pos
                try:
                    self.seek(string_data_offset + offset)
                    if length % 2 != 0:
                        raise TTFError("PostScript name is UTF-16BE string of odd length")
                    N = TTFNameBytes(self.get_chunk(string_data_offset + offset, length), 'utf_16_be')
                finally:
                    self._pos = opos
            elif platformId == 1 and encodingId == 0 and languageId == 0:  # Macintosh, Roman, English, PS Name
                N = TTFNameBytes(self.get_chunk(string_data_offset + offset, length), 'mac_roman')
            if N and names[nameId] == None:
                names[nameId] = N
                nameCount -= 1
                if nameCount == 0:
                    break
        if names[6] is not None:
            psName = names[6]
        elif names[4] is not None:
            psName = names[4]
        elif names[1] is not None:
            psName = names[1]
        else:
            psName = None

        if not psName:
            if rl_config.autoGenerateTTFMissingTTFName:
                fn = self.filename
                if fn:
                    bfn = os.path.splitext(os.path.basename(fn))[0]
                if not fn:
                    psName = bytestr('_RL_%s_%s_TTF' % (time.time(), self.__class__._agfnc))
                    self.__class__._agfnc += 1
                else:
                    psName = self._agfnm.get(fn, '')
                    if not psName:
                        if bfn:
                            psName = bytestr('_RL_%s_TTF' % bfn)
                        else:
                            psName = bytestr('_RL_%s_%s_TTF' % (time.time(), self.__class__._agfnc))
                            self.__class__._agfnc += 1
                        self._agfnm[fn] = psName
            else:
                raise TTFError("Could not find PostScript font name")

        psName = psName.__class__(psName.replace(b" ", b"-"))

        for c in psName:
            if char2int(c) > 126 or c in b' [](){}<>/%':
                raise TTFError("psName=%r contains invalid character %s" % (psName, ascii(c)))
        self.name = psName
        self.familyName = names[1] or psName
        self.styleName = names[2] or 'Regular'
        self.fullName = names[4] or psName
        self.uniqueFontID = names[3] or psName

        # head - Font header table
        try:
            self.seek_table("head")
        except:
            raise TTFError('head table not found ttf name=%s' % self.name)
        ver_maj, ver_min = self.read_ushort(), self.read_ushort()
        if ver_maj != 1:
            raise TTFError('Unknown head table version %d.%04x' % (ver_maj, ver_min))
        self.fontRevision = self.read_ushort(), self.read_ushort()

        self.skip(4)
        magic = self.read_ulong()
        if magic != 0x5F0F3CF5:
            raise TTFError('Invalid head table magic %04x' % magic)
        self.skip(2)
        self.unitsPerEm = unitsPerEm = self.read_ushort()
        if unitsPerEm == 1000:
            scale = lambda x: x
        else:
            _1000mult = 1000 / unitsPerEm
            scale = lambda x: x * _1000mult
        self._pdfScale = scale
        self.skip(16)
        xMin = self.read_short()
        yMin = self.read_short()
        xMax = self.read_short()
        yMax = self.read_short()
        self.bbox = list(map(scale, [xMin, yMin, xMax, yMax]))
        self.skip(3 * 2)
        indexToLocFormat = self.read_ushort()
        glyphDataFormat = self.read_ushort()

        # OS/2 - OS/2 and Windows metrics table
        subsettingAllowed = True
        if "OS/2" in self.table:
            self.seek_table("OS/2")
            version = self.read_ushort()
            self.skip(2)
            usWeightClass = self.read_ushort()
            self.skip(2)
            fsType = self.read_ushort()
            if fsType == 0x0002 or (fsType & 0x0300):
                subsettingAllowed = os.path.basename(self.filename) not in rl_config.allowTTFSubsetting
            self.skip(58)
            sTypoAscender = self.read_short()
            sTypoDescender = self.read_short()
            self.ascent = scale(sTypoAscender)
            self.descent = scale(sTypoDescender)

            if version > 1:
                self.skip(16)
                sCapHeight = self.read_short()
                self.capHeight = scale(sCapHeight)
            else:
                self.capHeight = self.ascent
        else:
            usWeightClass = 500
            self.ascent = scale(yMax)
            self.descent = scale(yMin)
            self.capHeight = self.ascent

        self.stemV = 50 + int((usWeightClass / 65.0) ** 2)

        # post - PostScript table
        self.seek_table("post")
        ver_maj, ver_min = self.read_ushort(), self.read_ushort()
        if ver_maj not in (1, 2, 3, 4):
            raise TTFError('Unknown post table version %d.%04x' % (ver_maj, ver_min))
        self.italicAngle = self.read_short() + self.read_ushort() / 65536.0
        self.underlinePosition = self.read_short()
        self.underlineThickness = self.read_short()
        isFixedPitch = self.read_ulong()

        self.flags = FF_SYMBOLIC
        if self.italicAngle != 0:
            self.flags = self.flags | FF_ITALIC
        if usWeightClass >= 600:
            self.flags = self.flags | FF_FORCEBOLD
        if isFixedPitch:
            self.flags = self.flags | FF_FIXED

        # hhea - Horizontal header table
        self.seek_table("hhea")
        ver_maj, ver_min = self.read_ushort(), self.read_ushort()
        if ver_maj != 1:
            raise TTFError('Unknown hhea table version %d.%04x' % (ver_maj, ver_min))
        self.skip(28)
        metricDataFormat = self.read_ushort()
        if metricDataFormat != 0:
            raise TTFError('Unknown horizontal metric data format (%d)' % metricDataFormat)
        numberOfHMetrics = self.read_ushort()
        if numberOfHMetrics == 0:
            raise TTFError('Number of horizontal metrics is 0')

        # maxp - Maximum profile table
        self.seek_table("maxp")
        ver_maj, ver_min = self.read_ushort(), self.read_ushort()
        if ver_maj == 1:
            # TrueType maxp (version 1.0) - 32 bytes
            self.numGlyphs = numGlyphs = self.read_ushort()
        elif ver_maj == 0:
            # CFF maxp (version 0.5) - 6 bytes
            self.numGlyphs = numGlyphs = self.read_ushort()
        else:
            raise TTFError('Unknown maxp table version %d.%04x' % (ver_maj, ver_min))
        if not subsettingAllowed:
            if self.numGlyphs > 0xFF:
                raise TTFError('Font does not allow subsetting/embedding (%04X)' % fsType)
            else:
                self._full_font = True
        else:
            self._full_font = False

        if not charInfo:
            self.charToGlyph = None
            self.defaultWidth = None
            self.charWidths = None
            return

        if glyphDataFormat != 0:
            raise TTFError('Unknown glyph data format (%d)' % glyphDataFormat)

        # cmap - Character to glyph index mapping table
        cmap_offset = self.seek_table("cmap")
        cmapVersion = self.read_ushort()
        cmapTableCount = self.read_ushort()
        if cmapTableCount == 0 and cmapVersion != 0:
            cmapTableCount, cmapVersion = cmapVersion, cmapTableCount
        encoffs = None
        enc = 0
        for n in range(cmapTableCount):
            platform = self.read_ushort()
            encoding = self.read_ushort()
            offset = self.read_ulong()
            if platform == 3:
                enc = 1
                encoffs = offset
            elif platform == 1 and encoding == 0 and enc != 1:
                enc = 2
                encoffs = offset
            elif platform == 1 and encoding == 1:
                enc = 1
                encoffs = offset
            elif platform == 0 and encoding != 5:
                enc = 1
                encoffs = offset
        if encoffs is None:
            raise TTFError('could not find a suitable cmap encoding')
        encoffs += cmap_offset
        self.seek(encoffs)
        fmt = self.read_ushort()
        self.charToGlyph = charToGlyph = {}
        self.glyphToChar = glyphToChar = {}
        if fmt in (13, 12, 10, 8):
            self.skip(2)
            length = self.read_ulong()
            lang = self.read_ulong()
        else:
            length = self.read_ushort()
            lang = self.read_ushort()
        if fmt == 0:
            T = [self.read_uint8() for i in range(length - 6)]
            for unichar in range(min(256, self.numGlyphs, len(T))):
                glyph = T[unichar]
                charToGlyph[unichar] = glyph
                glyphToChar.setdefault(glyph, []).append(unichar)
        elif fmt == 4:
            limit = encoffs + length
            segCount = int(self.read_ushort() / 2.0)
            self.skip(6)
            endCount = [self.read_ushort() for _ in range(segCount)]
            self.skip(2)
            startCount = [self.read_ushort() for _ in range(segCount)]
            idDelta = [self.read_short() for _ in range(segCount)]
            idRangeOffset_start = self._pos
            idRangeOffset = [self.read_ushort() for _ in range(segCount)]

            for n in range(segCount):
                for unichar in range(startCount[n], endCount[n] + 1):
                    if idRangeOffset[n] == 0:
                        glyph = (unichar + idDelta[n]) & 0xFFFF
                    else:
                        offset = (unichar - startCount[n]) * 2 + idRangeOffset[n]
                        offset = idRangeOffset_start + 2 * n + offset
                        if offset >= limit:
                            glyph = 0
                        else:
                            glyph = self.get_ushort(offset)
                            if glyph != 0:
                                glyph = (glyph + idDelta[n]) & 0xFFFF
                    charToGlyph[unichar] = glyph
                    glyphToChar.setdefault(glyph, []).append(unichar)
        elif fmt == 6:
            first = self.read_ushort()
            count = self.read_ushort()
            for glyph in range(first, first + count):
                unichar = self.read_ushort()
                charToGlyph[unichar] = glyph
                glyphToChar.setdefault(glyph, []).append(unichar)
        elif fmt == 10:
            first = self.read_ulong()
            count = self.read_ulong()
            for glyph in range(first, first + count):
                unichar = self.read_ushort()
                charToGlyph[unichar] = glyph
                glyphToChar.setdefault(glyph, []).append(unichar)
        elif fmt == 12:
            segCount = self.read_ulong()
            for n in range(segCount):
                start = self.read_ulong()
                end = self.read_ulong()
                inc = self.read_ulong() - start
                for unichar in range(start, end + 1):
                    glyph = unichar + inc
                    charToGlyph[unichar] = glyph
                    glyphToChar.setdefault(glyph, []).append(unichar)
        elif fmt == 13:
            segCount = self.read_ulong()
            for n in range(segCount):
                start = self.read_ulong()
                end = self.read_ulong()
                gid = self.read_ulong()
                for unichar in range(start, end + 1):
                    charToGlyph[unichar] = gid
                    glyphToChar.setdefault(gid, []).append(unichar)
        elif fmt == 2:
            T = [self.read_ushort() for i in range(256)]
            maxSHK = max(T)
            SH = []
            for i in range(maxSHK + 1):
                firstCode = self.read_ushort()
                entryCount = self.read_ushort()
                idDelta = self.read_ushort()
                idRangeOffset = (self.read_ushort() - (maxSHK - i) * 8 - 2) >> 1
                SH.append((firstCode, entryCount, idDelta, idRangeOffset))
            entryCount = (length - (self._pos - (cmap_offset + encoffs))) >> 1
            glyphs = [self.read_short() for i in range(entryCount)]
            last = -1
            for unichar in range(256):
                if T[unichar] == 0:
                    if last != -1:
                        glyph = 0
                    elif (unichar < SH[0][0] or unichar >= SH[0][0] + SH[0][1] or
                            SH[0][3] + (unichar - SH[0][0]) >= entryCount):
                        glyph = 0
                    else:
                        glyph = glyphs[SH[0][3] + (unichar - SH[0][0])]
                        if glyph != 0:
                            glyph += SH[0][2]
                    if glyph != 0 and glyph < self.numGlyphs:
                        charToGlyph[unichar] = glyph
                        glyphToChar.setdefault(glyph, []).append(unichar)
                else:
                    k = T[unichar]
                    for j in range(SH[k][1]):
                        if SH[k][3] + j >= entryCount:
                            glyph = 0
                        else:
                            glyph = glyphs[SH[k][3] + j]
                            if glyph != 0:
                                glyph += SH[k][2]
                        if glyph != 0 and glyph < self.numGlyphs:
                            enc = (unichar << 8) | (j + SH[k][0])
                            charToGlyph[enc] = glyph
                            glyphToChar.setdefault(glyph, []).append(enc)
                    if last == -1:
                        last = unichar
        else:
            raise ValueError('Unsupported cmap encoding format %d' % fmt)

        # hmtx - Horizontal metrics table
        self.seek_table("hmtx")
        aw = None
        self.charWidths = charWidths = {}
        self.hmetrics = []
        for glyph in range(numberOfHMetrics):
            aw, lsb = self.read_ushort(), self.read_ushort()
            self.hmetrics.append((aw, lsb))
            aw = scale(aw)
            if glyph == 0:
                self.defaultWidth = aw
            if glyph in glyphToChar:
                for char in glyphToChar[glyph]:
                    charWidths[char] = aw
        for glyph in range(numberOfHMetrics, numGlyphs):
            lsb = self.read_ushort()
            self.hmetrics.append((aw, lsb))
            if glyph in glyphToChar:
                for char in glyphToChar[glyph]:
                    charWidths[char] = aw

        # loca - Index to location (TrueType only, not CFF)
        if not self.isCFF:
            if 'loca' not in self.table:
                raise TTFError('missing location table')
            self.seek_table('loca')
            self.glyphPos = []
            if indexToLocFormat == 0:
                for n in range(numGlyphs + 1):
                    self.glyphPos.append(self.read_ushort() << 1)
            elif indexToLocFormat == 1:
                for n in range(numGlyphs + 1):
                    self.glyphPos.append(self.read_ulong())
            else:
                raise TTFError('Unknown location table format (%d)' % indexToLocFormat)
        else:
            # CFF fonts use CharStrings INDEX instead of loca
            self.glyphPos = None
        if 0x20 in charToGlyph:
            charToGlyph[0xa0] = charToGlyph[0x20]
            charWidths[0xa0] = charWidths[0x20]
        elif 0xa0 in charToGlyph:
            charToGlyph[0x20] = charToGlyph[0xa0]
            charWidths[0x20] = charWidths[0xa0]

        if self.isCFF:
            self._detectCID()

    def _detectCID(self):
        cff_data = self.get_table('CFF ')
        hdrSize = cff_data[2]
        o = hdrSize
        o, nc, no = _readIndex(cff_data, o)
        if nc > 0 and len(no) >= 2:
            o += (no[-1] - no[0])
        o, tc, to = _readIndex(cff_data, o)
        if tc > 0 and len(to) >= 2:
            td = cff_data[o + to[0] - 1 : o + to[1] - 1]
            ros = td.find(b'\x0c\x1e')
            if ros >= 0:
                self.isCID = True
                self.cidInfo = self._readROS(cff_data, o, td, ros)
            else:
                self.isCID = False
                self.cidInfo = None
        else:
            self.isCID = False
            self.cidInfo = None

    def _readROS(self, cff_data, strIdxOff, td, rosPos):
        strings = _readStringsIdx(cff_data, strIdxOff)
        stack = []
        pos = 0
        while pos < rosPos:
            b = td[pos]; pos += 1
            if b == 28:
                stack.append(unpack('>h', td[pos:pos+2])[0]); pos += 2
            elif b == 29:
                stack.append(unpack('>l', td[pos:pos+4])[0]); pos += 4
            elif b == 30:
                while pos < len(td):
                    b2 = td[pos]; pos += 1
                    if (b2 & 0x0f) == 0x0f or (b2 >> 4) == 0x0f:
                        break
            elif b == 31:
                pos += 4
            elif 32 <= b <= 246:
                stack.append(b - 139)
            elif 247 <= b <= 254:
                stack.append((b - 247) * 256 + td[pos] + 108); pos += 1
            elif b == 12:
                stack = []; pos += 1
            else:
                stack = []
        if len(stack) >= 3:
            return {'Registry': _sidToString(strings, stack[-3]),
                    'Ordering': _sidToString(strings, stack[-2]),
                    'Supplement': stack[-1]}
        return None

    def makeSubset(self, subset):
        """Create a subset of a TrueType or CFF font"""
        output = FontMaker()

        # Build a mapping of glyphs in the subset to glyph numbers in
        # the original font.  Also build a mapping of UCS codes to
        # glyph values in the new font.

        # Start with 0 -> 0: "missing character"
        glyphMap = [0]
        glyphSet = {0: 0}
        codeToGlyph = {}
        for code in subset:
            if code in self.charToGlyph:
                originalGlyphIdx = self.charToGlyph[code]
            else:
                originalGlyphIdx = 0
            if originalGlyphIdx not in glyphSet:
                glyphSet[originalGlyphIdx] = len(glyphMap)
                glyphMap.append(originalGlyphIdx)
            codeToGlyph[code] = glyphSet[originalGlyphIdx]

        # For TrueType fonts, include composite glyph components
        if not self.isCFF:
            start = self.get_table_pos('glyf')[0]
            n = 0
            while n < len(glyphMap):
                originalGlyphIdx = glyphMap[n]
                glyphPos = self.glyphPos[originalGlyphIdx]
                glyphLen = self.glyphPos[originalGlyphIdx + 1] - glyphPos
                n += 1
                if not glyphLen:
                    continue
                self.seek(start + glyphPos)
                numberOfContours = self.read_short()
                if numberOfContours < 0:
                    # composite glyph
                    self.skip(8)
                    flags = GF_MORE_COMPONENTS
                    while flags & GF_MORE_COMPONENTS:
                        flags = self.read_ushort()
                        glyphIdx = self.read_ushort()
                        if glyphIdx not in glyphSet:
                            glyphSet[glyphIdx] = len(glyphMap)
                            glyphMap.append(glyphIdx)
                        if flags & GF_ARG_1_AND_2_ARE_WORDS:
                            self.skip(4)
                        else:
                            self.skip(2)
                        if flags & GF_WE_HAVE_A_SCALE:
                            self.skip(2)
                        elif flags & GF_WE_HAVE_AN_X_AND_Y_SCALE:
                            self.skip(4)
                        elif flags & GF_WE_HAVE_A_TWO_BY_TWO:
                            self.skip(8)

        # The following tables are simply copied from the original
        for tag in ('name', 'OS/2', 'cvt ', 'fpgm', 'prep'):
            try:
                output.add(tag, self.get_table(tag))
            except KeyError:
                pass

        # post - PostScript
        post = b"\x00\x03\x00\x00" + self.get_table('post')[4:16] + b"\x00" * 16
        output.add('post', post)

        numGlyphs = len(glyphMap)

        # hmtx - Horizontal Metrics
        hmtx = []
        for n in range(numGlyphs):
            aw, lsb = self.hmetrics[glyphMap[n]]
            hmtx.append(int(aw))
            hmtx.append(int(lsb))

        n = len(hmtx) - 2
        while n and hmtx[n] == hmtx[n - 2]:
            n -= 2
        n += 2
        numberOfHMetrics = n >> 1
        hmtx = hmtx[:n] + hmtx[n+1::2]

        hmtx = pack(*([">%dH" % len(hmtx)] + hmtx))
        output.add('hmtx', hmtx)

        # hhea - Horizontal Header
        hhea = self.get_table('hhea')
        hhea = _set_ushort(hhea, 34, numberOfHMetrics)
        output.add('hhea', hhea)

        # maxp - Maximum Profile
        if self.isCFF:
            # CFF maxp is only 6 bytes (version 0.5)
            # Format: version (4 bytes) + numGlyphs (2 bytes)
            maxp = pack(">IH", 0x00005000, numGlyphs)
        else:
            maxp = self.get_table('maxp')
            maxp = _set_ushort(maxp, 4, numGlyphs)
        output.add('maxp', maxp)

        # cmap - Character to glyph mapping
        entryCount = len(subset)
        length = 10 + entryCount * 2
        cmap = [0, 1,
                1, 0, 0, 12,
                6, length, 0,
                0,
                entryCount] + \
               list(map(codeToGlyph.get, subset))
        cmap = pack(*([">%dH" % len(cmap)] + cmap))
        output.add('cmap', cmap)

        if self.isCFF:
            # CFF fonts: use CFF parser for subsetting
            from ._cff import CFFParser, CFFSubsetter
            cff = CFFParser(self)
            cff.parse()
            
            # Build glyph map for CFF subsetter
            cffGlyphMap = [0] * numGlyphs
            for newIdx, origIdx in enumerate(glyphMap):
                cffGlyphMap[newIdx] = origIdx
            
            subsetter = CFFSubsetter(cff, cffGlyphMap)
            cffData = subsetter.generate()
            output.add('CFF ', cffData)
            
            # head - Font header (no indexToLocFormat for CFF)
            head = self.get_table('head')
            output.add('head', head)
        else:
            # TrueType fonts: copy glyf and loca tables
            glyphData = self.get_table('glyf')
            offsets = []
            glyf = []
            pos = 0
            for n in range(numGlyphs):
                offsets.append(pos)
                originalGlyphIdx = glyphMap[n]
                glyphPos = self.glyphPos[originalGlyphIdx]
                glyphLen = self.glyphPos[originalGlyphIdx + 1] - glyphPos
                data = glyphData[glyphPos:glyphPos+glyphLen]
                # Fix references in composite glyphs
                if glyphLen > 2 and unpack(">h", data[:2])[0] < 0:
                    pos_in_glyph = 10
                    flags = GF_MORE_COMPONENTS
                    while flags & GF_MORE_COMPONENTS:
                        flags = unpack(">H", data[pos_in_glyph:pos_in_glyph+2])[0]
                        glyphIdx = unpack(">H", data[pos_in_glyph+2:pos_in_glyph+4])[0]
                        data = _set_ushort(data, pos_in_glyph + 2, glyphSet[glyphIdx])
                        pos_in_glyph = pos_in_glyph + 4
                        if flags & GF_ARG_1_AND_2_ARE_WORDS:
                            pos_in_glyph = pos_in_glyph + 4
                        else:
                            pos_in_glyph = pos_in_glyph + 2
                        if flags & GF_WE_HAVE_A_SCALE:
                            pos_in_glyph = pos_in_glyph + 2
                        elif flags & GF_WE_HAVE_AN_X_AND_Y_SCALE:
                            pos_in_glyph = pos_in_glyph + 4
                        elif flags & GF_WE_HAVE_A_TWO_BY_TWO:
                            pos_in_glyph = pos_in_glyph + 8
                glyf.append(data)
                pos = pos + glyphLen
                if pos % 4 != 0:
                    padding = 4 - pos % 4
                    glyf.append(b'\0' * padding)
                    pos = pos + padding
            offsets.append(pos)
            output.add('glyf', b''.join(glyf))

            # loca - Index to location
            loca = []
            if (pos + 1) >> 1 > 0xFFFF:
                indexToLocFormat = 1
                for offset in offsets:
                    loca.append(offset)
                loca = pack(*([">%dL" % len(loca)] + loca))
            else:
                indexToLocFormat = 0
                for offset in offsets:
                    loca.append(offset >> 1)
                loca = pack(*([">%dH" % len(loca)] + loca))
            output.add('loca', loca)

            # head - Font header
            head = self.get_table('head')
            head = _set_ushort(head, 50, indexToLocFormat)
            output.add('head', head)

        return output.makeStream()

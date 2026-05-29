# sfnt binary format parser for OpenType fonts
# Extracted from ttfonts.py for the openfonts package.

from struct import unpack, error as structError
from reportlab.lib.utils import bytestr
from reportlab.lib.rl_accel import hex32, add32, calcChecksum
from reportlab import rl_config
from ._common import TTFError


_cached_ttf_dirs = {}

def _ttf_dirs(*roots):
    R = _cached_ttf_dirs.get(roots, None)
    if R is None:
        import os
        join = os.path.join
        realpath = os.path.realpath
        R = []
        aR = R.append
        for root in roots:
            for r, d, f in os.walk(root, followlinks=True):
                s = realpath(r)
                if s not in R: aR(s)
                for s in d:
                    s = realpath(join(r, s))
                    if s not in R: aR(s)
        _cached_ttf_dirs[roots] = R
    return R


def TTFOpenFile(fn):
    '''Opens a TTF file possibly after searching TTFSearchPath
    returns (filename, file)
    '''
    from reportlab.lib.utils import rl_isfile, open_for_read
    try:
        f = open_for_read(fn, 'rb')
        return fn, f
    except IOError:
        import os
        if not os.path.isabs(fn):
            for D in _ttf_dirs(*rl_config.TTFSearchPath):
                tfn = os.path.join(D, fn)
                if rl_isfile(tfn):
                    f = open_for_read(tfn, 'rb')
                    return tfn, f
        raise TTFError('Can\'t open file "%s"' % fn)


class FontParser:
    "Basic sfnt file parser (shared by TrueType and CFF)"
    ttfVersions = (0x00010000, 0x74727565, 0x74746366)
    otfVersion = 0x4F54544F  # 'OTTO'
    ttcVersions = (0x00010000, 0x00020000)
    fileKind = 'TTF'
    isCFF = False

    def __init__(self, file, validate=0, subfontIndex=0):
        """Loads and parses an OpenType font file.  file can be a filename or a
        file object.  If validate is set to a false values, skips checksum
        validation.  This can save time, especially if the font is large.
        """
        self.validate = validate
        self.readFile(file)
        isCollection = self.readHeader()
        if isCollection:
            self.readTTCHeader()
            self.getSubfont(subfontIndex)
        else:
            if self.validate:
                self.checksumFile()
            self.readTableDirectory()
            self.subfontNameX = b''

    def readTTCHeader(self):
        self.ttcVersion = self.read_ulong()
        self.fileKind = 'TTC'
        self.ttfVersions = self.ttfVersions[:-1]
        if self.ttcVersion not in self.ttcVersions:
            raise TTFError('"%s" is not a %s file: can\'t read version 0x%8.8x' % (self.filename, self.fileKind, self.ttcVersion))
        self.numSubfonts = self.read_ulong()
        self.subfontOffsets = []
        a = self.subfontOffsets.append
        for i in range(self.numSubfonts):
            a(self.read_ulong())

    def getSubfont(self, subfontIndex):
        if self.fileKind != 'TTC':
            raise TTFError('"%s" is not a TTC file: use this method' % (self.filename, self.fileKind))
        try:
            pos = self.subfontOffsets[subfontIndex]
        except IndexError:
            raise TTFError('TTC file "%s": bad subfontIndex %s not in [0,%d]' % (self.filename, subfontIndex, self.numSubfonts - 1))
        self.seek(pos)
        self.readHeader()
        self.readTableDirectory()
        self.subfontNameX = bytestr('-' + str(subfontIndex))

    def readTableDirectory(self):
        try:
            self.numTables = self.read_ushort()
            self.searchRange = self.read_ushort()
            self.entrySelector = self.read_ushort()
            self.rangeShift = self.read_ushort()

            # Read table directory
            self.table = {}
            self.tables = []
            for n in range(self.numTables):
                record = {}
                record['tag'] = self.read_tag()
                record['checksum'] = self.read_ulong()
                record['offset'] = self.read_ulong()
                record['length'] = self.read_ulong()
                self.tables.append(record)
                self.table[record['tag']] = record
        except:
            raise TTFError('Corrupt %s file "%s" cannot read Table Directory' % (self.fileKind, self.filename))
        if self.validate:
            self.checksumTables()

    def readHeader(self):
        '''read the sfnt header at the current position'''
        try:
            self.version = version = self.read_ulong()
        except:
            raise TTFError('"%s" is not a %s file: can\'t read version' % (self.filename, self.fileKind))

        if version == self.otfVersion:
            # OpenType CFF font
            self.isCFF = True
            self.fileKind = 'OTF'
            return False
        elif version in self.ttfVersions:
            self.isCFF = False
            return version == self.ttfVersions[-1]
        else:
            raise TTFError('Not a recognized OpenType font: version=0x%8.8X' % version)

    def readFile(self, f):
        if not hasattr(self, '_ttf_data'):
            if hasattr(f, 'read'):
                self.filename = getattr(f, 'name', '(font)')
                self._ttf_data = f.read()
            else:
                self.filename, f = TTFOpenFile(f)
                self._ttf_data = f.read()
                f.close()
        self._pos = 0

    def checksumTables(self):
        for t in self.tables:
            table = self.get_chunk(t['offset'], t['length'])
            checksum = calcChecksum(table)
            if t['tag'] == 'head':
                adjustment = unpack('>l', table[8:8+4])[0]
                checksum = add32(checksum, -adjustment)
            xchecksum = t['checksum']
            if xchecksum != checksum:
                raise TTFError('%s file "%s": invalid checksum %s table: %s (expected %s)' % (self.fileKind, self.filename, hex32(checksum), t['tag'], hex32(xchecksum)))

    def checksumFile(self):
        checksum = calcChecksum(self._ttf_data)
        if 0xB1B0AFBA != checksum:
            raise TTFError('%s file "%s": invalid checksum %s (expected 0xB1B0AFBA) len: %d &3: %d' % (self.fileKind, self.filename, hex32(checksum), len(self._ttf_data), (len(self._ttf_data) & 3)))

    def get_table_pos(self, tag):
        "Returns the offset and size of a given table."
        offset = self.table[tag]['offset']
        length = self.table[tag]['length']
        return (offset, length)

    def seek(self, pos):
        "Moves read pointer to a given offset in file."
        self._pos = pos

    def skip(self, delta):
        "Skip the given number of bytes."
        self._pos = self._pos + delta

    def seek_table(self, tag, offset_in_table=0):
        """Moves read pointer to the given offset within a given table and
        returns absolute offset of that position in the file."""
        self._pos = self.get_table_pos(tag)[0] + offset_in_table
        return self._pos

    def read_tag(self):
        "Read a 4-character tag"
        self._pos += 4
        return str(self._ttf_data[self._pos - 4:self._pos], 'utf8')

    def get_chunk(self, pos, length):
        "Return a chunk of raw data at given position"
        return bytes(self._ttf_data[pos:pos+length])

    def read_uint8(self):
        self._pos += 1
        return int(self._ttf_data[self._pos-1])

    def read_ushort(self):
        "Reads an unsigned short"
        self._pos += 2
        return unpack('>H', self._ttf_data[self._pos-2:self._pos])[0]

    def read_ulong(self):
        "Reads an unsigned long"
        self._pos += 4
        return unpack('>L', self._ttf_data[self._pos - 4:self._pos])[0]

    def read_short(self):
        "Reads a signed short"
        self._pos += 2
        try:
            return unpack('>h', self._ttf_data[self._pos-2:self._pos])[0]
        except structError as error:
            raise TTFError(error)

    def get_ushort(self, pos):
        "Return an unsigned short at given position"
        return unpack('>H', self._ttf_data[pos:pos+2])[0]

    def get_ulong(self, pos):
        "Return an unsigned long at given position"
        return unpack('>L', self._ttf_data[pos:pos+4])[0]

    def get_table(self, tag):
        "Return the given table"
        pos, length = self.get_table_pos(tag)
        return self._ttf_data[pos:pos+length]


class TTFNameBytes(bytes):
    '''class used to return named strings'''
    def __new__(cls, b, enc='utf8'):
        try:
            ustr = b.decode(enc)
        except:
            ustr = b.decode('latin1')
        self = bytes.__new__(cls, ustr.encode('utf8'))
        self.ustr = ustr
        return self

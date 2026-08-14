# CFF (Compact Font Format) support for OpenType fonts
# Handles CFF table parsing and subsetting.

from struct import pack, unpack
from io import BytesIO
from ._common import TTFError


def _readIndex(data, offset):
    """Read a CFF INDEX structure. Returns (offset_after, count, offsets_list).
    
    The returned offsets are relative to the start of the INDEX (i.e., the
    byte at 'offset' before calling this function).
    """
    if offset + 2 > len(data):
        return offset, 0, []
    
    count = unpack('>H', data[offset:offset+2])[0]
    offset += 2
    
    if count == 0:
        return offset, 0, []
    
    offSize = data[offset]
    offset += 1
    
    offsets = []
    for i in range(count + 1):
        if offSize == 1:
            offsets.append(data[offset])
            offset += 1
        elif offSize == 2:
            offsets.append(unpack('>H', data[offset:offset+2])[0])
            offset += 2
        elif offSize == 3:
            offsets.append((data[offset] << 16) | (data[offset+1] << 8) | data[offset+2])
            offset += 3
        elif offSize == 4:
            offsets.append(unpack('>L', data[offset:offset+4])[0])
            offset += 4
    
    return offset, count, offsets


def _readDict(data, offset, end):
    """Read a CFF DICT structure. Returns dict of operator->operand."""
    result = {}
    stack = []
    
    while offset < end:
        b = data[offset]
        offset += 1
        
        if b == 28:
            if offset + 2 <= end:
                val = unpack('>h', data[offset:offset+2])[0]
                stack.append(val)
                offset += 2
        elif b == 29:
            if offset + 4 <= end:
                val = unpack('>l', data[offset:offset+4])[0]
                stack.append(val)
                offset += 4
        elif b == 30:
            while offset < end:
                b2 = data[offset]
                offset += 1
                if (b2 & 0x0f) == 0x0f or (b2 >> 4) == 0x0f:
                    break
        elif b == 31:
            offset += 4
        elif 32 <= b <= 246:
            stack.append(b - 139)
        elif 247 <= b <= 250:
            if offset + 1 <= end:
                val = ((b - 247) << 8) + data[offset] + 108
                stack.append(val)
                offset += 1
        elif 251 <= b <= 254:
            if offset + 1 <= end:
                val = -((b - 251) << 8) - data[offset] - 108
                stack.append(val)
                offset += 1
        elif b == 12:
            if offset < end:
                op = 0x100 + data[offset]
                offset += 1
                if stack:
                    result[op] = stack[:]
                    stack = []
        else:
            if stack:
                result[b] = stack[:]
                stack = []
    
    return result


def _encodeInt(val):
    """Encode an integer as CFF DICT bytes."""
    if -107 <= val <= 107:
        return bytes([val + 139])
    elif -1131 <= val <= 1131:
        if val >= 0:
            val2 = val - 108
            return bytes([247 + (val2 >> 8), val2 & 0xFF])
        else:
            val2 = -val - 108
            return bytes([251 + (val2 >> 8), val2 & 0xFF])
    elif -32768 <= val <= 32767:
        return bytes([28]) + pack('>h', val)
    else:
        return bytes([29]) + pack('>l', val)


def _encodeDict(topDict):
    """Encode a CFF Top DICT from {opcode: operands} dict."""
    out = b''
    for opcode in sorted(topDict.keys()):
        operands = topDict[opcode]
        for op in operands:
            out += _encodeInt(op)
        if opcode < 256:
            out += bytes([opcode])
        else:
            out += bytes([12, opcode - 256])
    return out


class CFFParser:
    """Parser for CFF tables in OpenType CFF fonts."""
    
    def __init__(self, font):
        self.font = font
        self.isCID = False
        self.numGlyphs = 0
        self.charStringsOffset = 0
        self.charStringsDataOffset = 0
        self.charStringsOffsets = []
        self.cffData = None
        self.topDict = {}
        
    def parse(self):
        """Parse the CFF table structure."""
        if 'CFF ' not in self.font.table:
            raise TTFError('No CFF table found in font')
        
        self.cffData = self.font.get_table('CFF ')
        data = self.cffData
        
        headerSize = data[2]
        offset = headerSize
        
        # Parse Name INDEX
        offset, nameCount, nameOffsets = _readIndex(data, offset)
        
        # Skip past Name INDEX data
        if nameCount > 0 and len(nameOffsets) >= 2:
            offset += (nameOffsets[-1] - nameOffsets[0])
        
        # Parse Top DICT INDEX
        offset, topDictCount, topDictOffsets = _readIndex(data, offset)
        
        # Parse Top DICT data
        if len(topDictOffsets) >= 2:
            # Top DICT data is at data[offset + topDictOffsets[0] - 1 : offset + topDictOffsets[-1] - 1]
            # But offsets[0] is always 1, so data starts at 'offset'
            topDictStart = offset
            topDictEnd = offset + (topDictOffsets[-1] - topDictOffsets[0])
            self.topDict = _readDict(data, topDictStart, topDictEnd)
            
            if 17 in self.topDict:
                operands = self.topDict[17]
                if len(operands) >= 1:
                    self.charStringsOffset = operands[0]
            
            if 286 in self.topDict:
                self.isCID = True
        
        # Skip past Top DICT INDEX data
        if len(topDictOffsets) >= 2:
            offset += (topDictOffsets[-1] - topDictOffsets[0])
        
        # Skip String INDEX
        offset, stringCount, stringOffsets = _readIndex(data, offset)
        if stringCount > 0 and len(stringOffsets) >= 2:
            offset += (stringOffsets[-1] - stringOffsets[0])
        
        # Skip Global Subr INDEX
        offset, subrCount, subrOffsets = _readIndex(data, offset)
        if subrCount > 0 and len(subrOffsets) >= 2:
            offset += (subrOffsets[-1] - subrOffsets[0])
        
        # Parse CharStrings INDEX
        if self.charStringsOffset > 0:
            offset = self.charStringsOffset
            offset, self.numGlyphs, self.charStringsOffsets = _readIndex(data, offset)
            self.charStringsDataOffset = offset
        
        return self
    
    def getCharString(self, glyphIndex):
        """Get raw CharString data for a glyph."""
        if glyphIndex >= len(self.charStringsOffsets) - 1:
            return b''
        base = self.charStringsDataOffset - 1
        start = base + self.charStringsOffsets[glyphIndex]
        end = base + self.charStringsOffsets[glyphIndex + 1]
        return self.cffData[start:end]


class CFFSubsetter:
    """Generates CFF font subsets by rebuilding the CharStrings INDEX.
    
    For CID-keyed fonts, preserves FDArray, Private DICTs, Local Subrs,
    rebuilds FDSelect for the new glyph order, and correctly updates
    all Top DICT offset operands.
    """
    
    def __init__(self, cffParser, glyphMap):
        self.cff = cffParser
        self.glyphMap = glyphMap
        
    def _findOldCharStringsEnd(self, data, csOffset):
        """Find the byte offset where the old CharStrings INDEX ends."""
        count = unpack('>H', data[csOffset:csOffset+2])[0]
        offSize = data[csOffset + 2]
        offsetsEnd = csOffset + 3 + (count + 1) * offSize
        
        if offSize == 1:
            totalDataSize = data[offsetsEnd - 1]
        elif offSize == 2:
            totalDataSize = unpack('>H', data[offsetsEnd-2:offsetsEnd])[0]
        elif offSize == 3:
            o = data[offsetsEnd-3:offsetsEnd]
            totalDataSize = (o[0] << 16) | (o[1] << 8) | o[2]
        elif offSize == 4:
            totalDataSize = unpack('>I', data[offsetsEnd-4:offsetsEnd])[0]
        else:
            totalDataSize = 0
        
        return offsetsEnd + totalDataSize
    
    def _buildNewCharStringsIndex(self, charstrings):
        """Build a new CharStrings INDEX."""
        numGlyphs = len(charstrings)
        offsets = [1]
        pos = 0
        for cs in charstrings:
            pos += len(cs)
            offsets.append(1 + pos)
        
        totalSize = pos
        if totalSize < 256:
            offSize = 1
        elif totalSize < 65536:
            offSize = 2
        elif totalSize < 16777216:
            offSize = 3
        else:
            offSize = 4
        
        out = BytesIO()
        out.write(pack('>H', numGlyphs))
        out.write(pack('>B', offSize))
        for off in offsets:
            if offSize == 1:
                out.write(pack('>B', off))
            elif offSize == 2:
                out.write(pack('>H', off))
            elif offSize == 3:
                out.write(pack('>BBB', (off >> 16) & 0xFF, (off >> 8) & 0xFF, off & 0xFF))
            elif offSize == 4:
                out.write(pack('>I', off))
        for cs in charstrings:
            out.write(cs)
        
        return out.getvalue()
    
    def _parseFdSelect(self, data, fdSelectOffset, numGlyphs):
        """Parse the original FDSelect and return a dict mapping
        old glyph index -> FD index."""
        fdMap = {}
        if fdSelectOffset is None:
            return fdMap
        
        fmt = data[fdSelectOffset]
        if fmt == 0:
            for gid in range(numGlyphs):
                fdMap[gid] = data[fdSelectOffset + 1 + gid]
        elif fmt == 3:
            nRanges = unpack('>H', data[fdSelectOffset + 1:fdSelectOffset + 3])[0]
            pos = fdSelectOffset + 3
            ranges = []
            for _ in range(nRanges):
                first = unpack('>H', data[pos:pos + 2])[0]
                fd = data[pos + 2]
                ranges.append((first, fd))
                pos += 3

            # Single-pass iteration through ranges: O(n + m) instead of O(n log m)
            range_idx = 0
            for gid in range(numGlyphs):
                while range_idx < len(ranges) - 1 and ranges[range_idx + 1][0] <= gid:
                    range_idx += 1
                fdMap[gid] = ranges[range_idx][1]
        return fdMap
    
    def _buildFdSelect(self, oldFdMap, numGlyphs):
        """Build a new FDSelect (format 0) for the subset glyphs.
        
        oldFdMap: dict old_glyph_idx -> fd_index
        self.glyphMap: list where glyphMap[new_idx] = old_idx
        """
        data = bytearray()
        data.append(0)  # format 0
        for newIdx in range(numGlyphs):
            oldIdx = self.glyphMap[newIdx]
            fd = oldFdMap.get(oldIdx, 0)
            data.append(fd)
        return bytes(data)
    
    def _buildCharset(self, numGlyphs):
        data = bytearray()
        data.append(0)  # format 0: 1-byte format tag, then 2-byte CIDs
        for i in range(1, numGlyphs):
            data.extend(pack('>H', i))  # CID = glyph index
        return bytes(data)
    
    def _patchTailOffsets(self, result, tdDelta, tailDelta):
        """Patch absolute CFF offsets inside FDArray Font DICTs and
        Private DICTs to account for section size changes.
        
        tdDelta: shift for data in head section (after Top DICT)
        tailDelta: shift for data in tail section (after CharStrings)
        """
        cff = self.cff
        if not cff.isCID:
            return
        
        topDict = cff.topDict
        fdArrayOrigOff = topDict.get(292, [None])[0]
        if fdArrayOrigOff is None:
            return
        
        fdArrayNewOff = fdArrayOrigOff + tailDelta
        if fdArrayNewOff < 0 or fdArrayNewOff >= len(result):
            return
        
        data = bytes(result)
        
        # Parse FDArray INDEX
        fdOff, fdCount, fdOffsets = _readIndex(data, fdArrayNewOff)
        if fdCount == 0 or len(fdOffsets) < 2:
            return
        
        fdDataStart = fdOff
        
        csOffset = cff.charStringsOffset
        
        for fdIdx in range(fdCount):
            fdDictStart = fdDataStart + fdOffsets[fdIdx] - 1
            fdDictEnd = fdDataStart + fdOffsets[fdIdx + 1] - 1
            fdDict = _readDict(data, fdDictStart, fdDictEnd)
            
            if 18 not in fdDict:
                continue
            
            privSize, privOff = fdDict[18]
            
            # Compute the delta for the Private DICT position
            if privOff >= csOffset:
                newPrivOff = privOff + tailDelta
            else:
                newPrivOff = privOff + tdDelta
            
            # Find and update Private offset in the raw bytes
            self._patchDictOperand(result, fdDictStart, fdDictEnd, 18, 1, privOff, newPrivOff)
            
            # Subrs offsets inside Private DICTs are RELATIVE to the
            # Private DICT data start (CFF spec).  Since the entire tail
            # section shifts by the same amount, relative offsets within
            # it stay unchanged -- no patching needed.
    
    def _patchDictOperand(self, data, start, end, opcode, operandIdx, oldValue, newValue):
        """Patch a specific operand in a DICT byte sequence.
        
        Finds operator `opcode` in the byte range [start, end) and
        replaces the operand[operandIdx] value from oldValue to newValue.
        The encoding size may change, so we adjust the DICT size.
        """
        # Find the operator in the byte sequence
        opBytes = bytes([opcode]) if opcode < 256 else bytes([12, opcode - 256])
        
        # We need to find the operand position.  Since dict encoding is
        # variable-length, we parse operand by operand until we find our
        # operator, counting which operand index we're at.
        pos = start
        stack = []
        while pos < end:
            b = data[pos]
            pos += 1
            
            if b == 28:
                stack.append(pos - 1)  # position of opcode byte
                pos += 2
            elif b == 29:
                stack.append(pos - 1)  # position of opcode byte
                pos += 4
            elif b == 30:
                while pos < end:
                    b2 = data[pos]; pos += 1
                    if (b2 & 0x0f) == 0x0f or (b2 >> 4) == 0x0f:
                        break
            elif b == 31:
                pos += 4
            elif 32 <= b <= 246:
                stack.append(pos - 1)  # position of the value byte
            elif 247 <= b <= 254:
                stack.append(pos - 1)  # position of first value byte
                pos += 1
            elif b == 12:
                checkB = 0x100 + data[pos]; pos += 1
                if checkB == opcode and len(stack) > operandIdx:
                    opPos = stack[operandIdx]
                    self._replaceDictValue(data, opPos, oldValue, newValue)
                    return
                stack = []
            else:
                if b == opcode and len(stack) > operandIdx:
                    opPos = stack[operandIdx]
                    self._replaceDictValue(data, opPos, oldValue, newValue)
                    return
                stack = []
    
    def _replaceDictValue(self, data, pos, oldValue, newValue):
        """Replace an encoded integer value in a DICT byte sequence.
        
        Ensures the new value uses the same encoding size as the old value
        to allow in-place replacement.
        """
        oldEnc = _encodeInt(oldValue)
        oldLen = len(oldEnc)
        newEnc = _encodeInt(newValue)
        
        if len(newEnc) == oldLen:
            data[pos:pos + oldLen] = newEnc
        elif len(newEnc) < oldLen:
            # Pad to same size using the old encoding format
            if oldLen == 3:  # was 16-bit (opcode 28)
                newEnc = bytes([28]) + pack('>h', newValue)
            elif oldLen == 5:  # was 32-bit (opcode 29)
                newEnc = bytes([29]) + pack('>l', newValue)
            data[pos:pos + oldLen] = newEnc
        else:
            # New encoding is larger than old: use the next larger fixed-size
            # format.  This handles the common case where a 16-bit offset
            # (3 bytes) grows to need 32-bit (5 bytes) after subsetting.
            if oldLen == 1:
                # Was single-byte (-107..107), promote to 16-bit (opcode 28)
                newEnc = bytes([28]) + pack('>h', newValue)
            else:
                # Was 16-bit or smaller, promote to 32-bit (opcode 29)
                newEnc = bytes([29]) + pack('>l', newValue)
            if len(newEnc) <= oldLen:
                # Should not happen, but guard against infinite recursion
                data[pos:pos + oldLen] = newEnc
            else:
                raise ValueError(
                    'CFF dict operand at offset %d grew from %d to %d bytes '
                    '(old=%d new=%d); in-place patching is not possible'
                    % (pos, oldLen, len(newEnc), oldValue, newValue))
    
    def generate(self):
        """Generate the CFF subset.
        
        Rebuilds the CFF with corrected section sizes and positions,
        rebuilds CharStrings and FDSelect, and patches all
        Top DICT offset operands.
        """
        cff = self.cff
        data = cff.cffData
        csOffset = cff.charStringsOffset
        numGlyphs = len(self.glyphMap)
        
        oldCSEnd = self._findOldCharStringsEnd(data, csOffset)
        oldCSSize = oldCSEnd - csOffset
        
        charstrings = []
        for oldIdx in self.glyphMap:
            charstrings.append(cff.getCharString(oldIdx))
        
        newIndexData = self._buildNewCharStringsIndex(charstrings)
        newCSSize = len(newIndexData)
        csDelta = newCSSize - oldCSSize
        
        headerSize = data[2]
        
        # Find Top DICT boundaries in the original CFF
        tdOff = headerSize
        tdOff, nc, noffs = _readIndex(data, tdOff)
        if nc > 0 and len(noffs) >= 2:
            tdOff += (noffs[-1] - noffs[0])
        
        tdIdxStart = tdOff
        tdOff, tc, tdoffsets = _readIndex(data, tdOff)
        
        tdDataStart = tdOff
        oldTdEnd = tdOff + (tdoffsets[-1] - tdoffsets[0])
        oldTdSize = oldTdEnd - tdDataStart
        
        topDict = _readDict(data, tdDataStart, oldTdEnd)
        
        # Parse original FDSelect for CID fonts
        oldFdMap = {}
        oldFdArrayPos = None
        if cff.isCID:
            oldFdSelectOffset = cff.topDict.get(293, [None])[0]
            oldFdMap = self._parseFdSelect(data, oldFdSelectOffset, cff.numGlyphs)
            oldFdArrayPos = cff.topDict.get(292, [None])[0]
        
        # For CID fonts, the tail may start before oldCSEnd (FDArray INDEX
        # header overlaps with the last CharString byte).  Use the FDArray
        # position as the true start of the tail section.
        tailSrcStart = oldCSEnd
        if oldFdArrayPos is not None and oldFdArrayPos < oldCSEnd:
            tailSrcStart = oldFdArrayPos
            csDelta += (oldCSEnd - tailSrcStart)
        
        # Step 1: compute csDelta shifts (only for tail structures)
        for op in [15, 16, 18, 292]:
            if op in topDict:
                operands = topDict[op]
                for i in range(len(operands)):
                    val = operands[i]
                    if op == 18 and i == 0:
                        continue
                    if op == 17:
                        continue
                    if val >= tailSrcStart:
                        operands[i] = val + csDelta
        
        # Update CIDCount to match new glyph count
        if cff.isCID and 290 in topDict:
            topDict[290] = [numGlyphs]
        
        # For CID fonts, rebuild a minimal charset matching the new
        # glyph count.  The charset is appended at the end of the CFF
        # along with the FDSelect.
        newCharset = b''
        if cff.isCID:
            newCharset = self._buildCharset(numGlyphs)
        
        # Step 2: Compute Top DICT size delta
        curDictData = _encodeDict(topDict)
        tdDelta = len(curDictData) - oldTdSize
        
        # Step 3: apply tdDelta to all offsets after oldTdEnd
        for op in [15, 16, 17, 18, 292]:
            if op in topDict:
                operands = topDict[op]
                for i in range(len(operands)):
                    val = operands[i]
                    if op == 18 and i == 0:
                        continue
                    if val > oldTdEnd:
                        operands[i] = val + tdDelta
        
        # Step 4: compute fdSelectPos for CID fonts
        if cff.isCID:
            csNewOff = topDict[17][0]
            middleSize = csOffset - oldTdEnd
            
            tailSize = max(0, len(data) - tailSrcStart)
            charsetOffset = (tdDataStart + len(curDictData)
                             + middleSize
                             + newCSSize
                             + tailSize)
            fdSelectPos = charsetOffset + len(newCharset)
            topDict[15] = [charsetOffset]
            topDict[293] = [fdSelectPos]
        
        # Step 5: re-encode with final values, iterate if fdselect changed the size
        for _ in range(2):
            newDictData = _encodeDict(topDict)
            newTdSize = len(newDictData)
            newTdDelta = newTdSize - oldTdSize
            
            if newTdDelta == tdDelta:
                break
            
            diff = newTdDelta - tdDelta
            for op in [15, 16, 17, 18, 292]:
                if op in topDict:
                    operands = topDict[op]
                    for i in range(len(operands)):
                        val = operands[i]
                        if op == 18 and i == 0:
                            continue
                        if val > oldTdEnd:
                            operands[i] = val + diff
            
            tdDelta = newTdDelta
            
            if cff.isCID:
                csNewOff = topDict[17][0]
                middleSize = csOffset - oldTdEnd
                tailSize = max(0, len(data) - tailSrcStart)
                charsetOffset = (tdDataStart + newTdSize
                                 + middleSize
                                 + newCSSize
                                 + tailSize)
                fdSelectPos = charsetOffset + len(newCharset)
                topDict[15] = [charsetOffset]
                topDict[293] = [fdSelectPos]
        
        newDictData = _encodeDict(topDict)
        newTdSize = len(newDictData)
        
        # Build the final CFF
        result = bytearray()
        
        tdOffSize = data[tdIdxStart + 2]
        result.extend(data[:tdDataStart])
        result.extend(newDictData)
        
        newTdOffset1 = newTdSize + 1
        offs0Start = tdIdxStart + 3
        offs1Start = offs0Start + tdOffSize
        if tdOffSize == 1:
            result[offs1Start] = newTdOffset1 & 0xFF
        elif tdOffSize == 2:
            result[offs1Start] = (newTdOffset1 >> 8) & 0xFF
            result[offs1Start + 1] = newTdOffset1 & 0xFF
        elif tdOffSize == 3:
            result[offs1Start] = (newTdOffset1 >> 16) & 0xFF
            result[offs1Start + 1] = (newTdOffset1 >> 8) & 0xFF
            result[offs1Start + 2] = newTdOffset1 & 0xFF
        elif tdOffSize == 4:
            result[offs1Start] = (newTdOffset1 >> 24) & 0xFF
            result[offs1Start + 1] = (newTdOffset1 >> 16) & 0xFF
            result[offs1Start + 2] = (newTdOffset1 >> 8) & 0xFF
            result[offs1Start + 3] = newTdOffset1 & 0xFF
        
        result.extend(data[oldTdEnd:csOffset])
        result.extend(newIndexData)
        if tailSrcStart < len(data):
            result.extend(data[tailSrcStart:])

        # Zero out local Subrs for unreferenced FDs (CID fonts).
        # This does not change any CFF offsets, but makes the zeroed
        # regions compress extremely well with zlib in the PDF stream.
        if cff.isCID and oldFdMap and oldFdArrayPos is not None:
            usedFDs = set(oldFdMap.get(self.glyphMap[n], 0)
                          for n in range(numGlyphs))
            _, fdArrayCount, _ = _readIndex(data, oldFdArrayPos)
            if len(usedFDs) < fdArrayCount:
                resultDelta = len(result) - len(data)
                fdArrInResult = oldFdArrayPos + resultDelta
                fdOff2, _, fdOffs2 = _readIndex(bytes(result), fdArrInResult)
                for fdIdx in range(len(fdOffs2) - 1):
                    if fdIdx in usedFDs:
                        continue
                    fdStart = fdOff2 + fdOffs2[fdIdx] - 1
                    fdEnd = fdOff2 + fdOffs2[fdIdx + 1] - 1
                    fdDict = _readDict(bytes(result), fdStart, fdEnd)
                    if 18 not in fdDict:
                        continue
                    privSize, privOff = fdDict[18]
                    privInResult = privOff + resultDelta
                    privDict = _readDict(bytes(result), privInResult,
                                         privInResult + privSize)
                    if 19 not in privDict:
                        continue
                    subrsOff = privDict[19][0]
                    subrsInResult = (privOff + subrsOff) + resultDelta
                    if 0 <= subrsInResult < len(result):
                        sOff, sCount, sOffs = _readIndex(
                            bytes(result), subrsInResult)
                        if sCount > 0 and len(sOffs) >= 2:
                            subrsEnd = sOff + (sOffs[-1] - sOffs[0])
                            if subrsEnd <= len(result):
                                result[subrsInResult:subrsEnd] = \
                                    b'\x00' * (subrsEnd - subrsInResult)

        if cff.isCID:
            newFdSelectData = self._buildFdSelect(oldFdMap, numGlyphs)
            if newCharset:
                result.extend(newCharset)
            result.extend(newFdSelectData)
        
        # Patch absolute offsets inside FDArray (Private DICTs, Subrs)
        self._patchTailOffsets(result, tdDelta, csDelta + tdDelta)
        
        return bytes(result)

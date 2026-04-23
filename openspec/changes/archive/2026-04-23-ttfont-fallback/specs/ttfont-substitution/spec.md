## ADDED Requirements

### Requirement: unicode2TT splits text by glyph availability
`unicode2TT(utext, fonts)` SHALL accept a Unicode string and a list of TTFont instances, and return `list[tuple[TTFont, str]]` where each tuple represents a font and the contiguous characters it can render.

#### Scenario: Pure ASCII text in main font
- **WHEN** `unicode2TT("Hello", [mainFont])` is called and mainFont contains all glyphs
- **THEN** returns `[(mainFont, "Hello")]`

#### Scenario: Mixed script text
- **WHEN** `unicode2TT("Hello你好", [mainFont, cjkFont])` is called and mainFont lacks CJK glyphs but cjkFont contains them
- **THEN** returns `[(mainFont, "Hello"), (cjkFont, "你好")]`

#### Scenario: All fonts missing a glyph
- **WHEN** a character is not in any font
- **THEN** that character is assigned to the main font (producing `.notdef`)

#### Scenario: Empty text
- **WHEN** `unicode2TT("", [font])` is called
- **THEN** returns `[]`

#### Scenario: Consecutive same-font characters merged
- **WHEN** multiple consecutive characters are all in the same font
- **THEN** they are merged into a single `(font, str)` tuple

### Requirement: unicode2TT maps nbsp to space
U+00A0 (non-breaking space) SHALL be treated as U+0020 (regular space) in `unicode2TT`, consistent with `splitString` behavior.

#### Scenario: Text containing nbsp
- **WHEN** `unicode2TT("A B", [font])` is called and font has glyph for space
- **THEN** nbsp is treated as space and the result is `[(font, "A B")]`

### Requirement: instanceStringWidthTTF uses fallback for width calculation
`_py_instanceStringWidthTTF` SHALL use `unicode2TT` to calculate widths across fallback fonts when `font.substitutionFonts` is non-empty.

#### Scenario: Width with fallback fonts
- **WHEN** text contains characters in both main and fallback fonts, and `substitutionFonts` is non-empty and fallback is enabled
- **THEN** returned width equals sum of each fragment's width in its respective font

#### Scenario: Width without fallback fonts
- **WHEN** `substitutionFonts` is empty or fallback is disabled
- **THEN** width calculation uses original single-font logic with no change

### Requirement: _formatText renders TTFont with font switching
`_formatText` in `textobject.py` SHALL use `unicode2TT` to split text and emit PDF `Tf` operators to switch fonts when rendering TTFont text with fallback.

#### Scenario: Mixed script rendering
- **WHEN** TTFont text contains characters requiring fallback, and `substitutionFonts` is non-empty and fallback is enabled
- **THEN** PDF content stream contains `Tf` operators to switch between main and fallback fonts

#### Scenario: All characters in main font
- **WHEN** all characters are in the main font
- **THEN** behavior is identical to no-fallback path (single `splitString` call)

#### Scenario: Font state restoration after fallback
- **WHEN** fallback rendering completes for a text segment
- **THEN** the current font is restored to the main font

### Requirement: HarfBuzz text degrades gracefully
When `substitutionFonts` is non-empty and the text is a `ShapedStr`, the system SHALL print a warning and fall back to the non-shaped TTFont rendering path.

#### Scenario: Shaped text with fallback fonts configured
- **WHEN** a ShapedStr is encountered and `font.substitutionFonts` is non-empty
- **THEN** a warning is printed and text is rendered via the non-shaped fallback path

### Requirement: text2PathDescription supports TTFont fallback
Both freetype and _renderPM backends of `text2PathDescription` SHALL split text via `unicode2TT` and render each fragment with its respective font.

#### Scenario: freetype backend with fallback
- **WHEN** `text2PathDescription` uses freetype backend and font has `substitutionFonts`
- **THEN** each fragment is rendered via `gs._text2Path()` with correct font and accumulated x offset

#### Scenario: _renderPM backend with fallback
- **WHEN** `text2PathDescription` uses _renderPM backend and font has `substitutionFonts`
- **THEN** each fragment is rendered via `gs._stringPath()` with correct font and accumulated x offset

### Requirement: renderPM drawString supports TTFont fallback
`drawString` in `renderPM.py` SHALL use `unicode2TT` to split text and render each fragment with font switching for TTFont with fallback.

#### Scenario: drawString with fallback
- **WHEN** TTFont has `substitutionFonts` and text contains characters requiring fallback
- **THEN** each fragment is rendered with `_setFont(gs, fbFont.fontName, fontSize)` and x offset accumulation

### Requirement: renderPS supports TTFont fallback
The PostScript renderer SHALL split TTFont text via `unicode2TT` and emit font switches for fallback fragments.

#### Scenario: PS output with fallback
- **WHEN** TTFont has `substitutionFonts` and text contains mixed scripts
- **THEN** PS output contains font switch commands and text output for each fragment

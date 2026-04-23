## ADDED Requirements

### Requirement: Unit tests for unicode2TT
Tests SHALL cover basic split, fallback split, all-missing, empty text, nbsp mapping, consecutive merging, and alternating characters.

#### Scenario: All unicode2TT test cases pass
- **WHEN** test suite runs `test_unicode2TT_*` tests
- **THEN** T01-T07 tests all pass (basic, fallback, all-missing, empty, nbsp, consecutive, alternating)

### Requirement: Unit tests for hasGlyph
Tests SHALL verify `hasGlyph` returns correct boolean for existing and missing characters, and handles both str and int inputs.

#### Scenario: hasGlyph test cases pass
- **WHEN** test suite runs `test_hasGlyph`
- **THEN** verifies True for existing chars, False for missing, nbsp→space, str/int equivalence

### Requirement: Environment variable control tests
Tests SHALL verify that the property getter respects the environment variable in real-time, including runtime toggle without module reload.

#### Scenario: Fallback disabled by default
- **WHEN** `REPORTLAB_FONT_FALLBACK` is not set
- **THEN** `font.substitutionFonts` returns `[]` after setting internal value

#### Scenario: Runtime toggle
- **WHEN** env var is set to `'1'` then cleared
- **THEN** property returns actual list then `[]` without reloading

### Requirement: String width consistency tests
Tests SHALL verify that `stringWidth` results are consistent with actual rendering when fallback is active.

#### Scenario: Width matches rendering
- **WHEN** text has mixed scripts and fallback is enabled
- **THEN** `stringWidth` result equals sum of fragment widths in respective fonts

### Requirement: PDF generation tests
Tests SHALL generate PDFs with mixed scripts and verify they are valid and contain correct font resources.

#### Scenario: Mixed script PDF
- **WHEN** PDF is generated with CJK+Latin text and fallback fonts
- **THEN** PDF file is valid and contains both font subsets

#### Scenario: All-in-main font PDF
- **WHEN** all characters are in the main font
- **THEN** PDF output is identical to no-fallback path

### Requirement: Graphics path tests
Tests SHALL verify `text2PathDescription` works with fallback fonts in both freetype and _renderPM backends.

#### Scenario: text2Path with fallback
- **WHEN** `text2PathDescription` is called with fallback fonts configured
- **THEN** path generation completes without error

### Requirement: renderPM/renderPS tests
Tests SHALL verify `drawString` works with fallback in both renderers.

#### Scenario: renderPM drawString with fallback
- **WHEN** `drawString` is called with mixed script text and fallback fonts
- **THEN** rendering completes without error and text position is correct

### Requirement: API tests for registerFontWithFallback
Tests SHALL verify the convenience function with both name-based and instance-based fallback specification.

#### Scenario: Registration by name and by instance
- **WHEN** `registerFontWithFallback` is called with name and instance variants
- **THEN** returned TTFont has correct `substitutionFonts` set

### Requirement: Regression tests
All existing TTFont and font embedding tests SHALL pass without modification.

#### Scenario: Existing test suite passes
- **WHEN** `test_pdfbase_ttfonts.py` and `test_pdfbase_fontembed.py` are run
- **THEN** all tests pass with no regressions

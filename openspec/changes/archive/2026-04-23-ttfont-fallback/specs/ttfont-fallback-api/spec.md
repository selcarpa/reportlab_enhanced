## ADDED Requirements

### Requirement: TTFont.substitutionFonts property with env var control
`TTFont.substitutionFonts` SHALL be a property whose getter reads `os.environ.get('REPORTLAB_FONT_FALLBACK', '0')` on every call. When the value is not `'1'`, the getter SHALL return `[]`. When the value is `'1'`, the getter SHALL return `self._substitutionFonts`.

#### Scenario: Fallback disabled by default
- **WHEN** `REPORTLAB_FONT_FALLBACK` is not set or is `'0'`
- **THEN** `font.substitutionFonts` returns `[]` even if `_substitutionFonts` has been set

#### Scenario: Fallback enabled via environment variable
- **WHEN** `REPORTLAB_FONT_FALLBACK` is set to `'1'`
- **THEN** `font.substitutionFonts` returns the actual fallback list

#### Scenario: Runtime toggle
- **WHEN** environment variable is changed at runtime
- **THEN** subsequent calls to `font.substitutionFonts` reflect the new state immediately

#### Scenario: Setter always stores value
- **WHEN** `font.substitutionFonts = [fallback]` is called regardless of env var
- **THEN** the value is stored in `self._substitutionFonts`

### Requirement: TTFont.hasGlyph method
`TTFont.hasGlyph(char_or_code)` SHALL accept a single character string or an integer Unicode code point and return `True` if the font contains a glyph for that character, `False` otherwise.

#### Scenario: Existing character
- **WHEN** `font.hasGlyph('A')` is called and font has glyph for 'A'
- **THEN** returns `True`

#### Scenario: Missing character
- **WHEN** `font.hasGlyph(0x4F60)` is called and font lacks CJK glyphs
- **THEN** returns `False`

#### Scenario: Nbsp treated as space
- **WHEN** `font.hasGlyph(' ')` is called and font has space glyph
- **THEN** returns `True` (nbsp mapped to space)

#### Scenario: Integer code point
- **WHEN** `font.hasGlyph(ord('A'))` is called
- **THEN** returns same result as `font.hasGlyph('A')`

### Requirement: pdfmetrics.registerFontWithFallback convenience function
`registerFontWithFallback(name, filename, fallbackFonts=None, **kwargs)` SHALL create and register a TTFont, then set its `substitutionFonts` from the provided list. Elements of `fallbackFonts` can be font name strings (looked up via `getFont`) or TTFont instances (auto-registered).

#### Scenario: Register with fallback by name
- **WHEN** `registerFontWithFallback('Main', 'main.ttf', fallbackFonts=['Fallback'])` is called and 'Fallback' is already registered
- **THEN** returns TTFont instance with `substitutionFonts` containing the fallback font

#### Scenario: Register with fallback by instance
- **WHEN** `registerFontWithFallback('Main', 'main.ttf', fallbackFonts=[TTFont('FB', 'fb.ttf')])` is called
- **THEN** the fallback TTFont is auto-registered and set as substitutionFont

#### Scenario: No fallback fonts
- **WHEN** `registerFontWithFallback('Main', 'main.ttf')` is called with no `fallbackFonts`
- **THEN** returns registered TTFont with `substitutionFonts` as `[]`

### Requirement: defaultTTFFallbackFonts configuration
`rl_settings.py` SHALL define `defaultTTFFallbackFonts = []` as a global default fallback font name list. The `_setOpt` mechanism in `rl_config.py` SHALL auto-import this setting.

#### Scenario: Default value
- **WHEN** no user configuration overrides `defaultTTFFallbackFonts`
- **THEN** `rl_config.defaultTTFFallbackFonts` is `[]`

#### Scenario: User override via reportlab_settings
- **WHEN** user sets `defaultTTFFallbackFonts = ['NotoSansCJK']` in `~/.reportlab_settings`
- **THEN** `rl_config.defaultTTFFallbackFonts` reflects the user value

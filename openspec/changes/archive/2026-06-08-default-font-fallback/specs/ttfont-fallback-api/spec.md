## MODIFIED Requirements

### Requirement: TTFont.substitutionFonts property always enabled
`TTFont.substitutionFonts` SHALL be a property whose getter returns `self._substitutionFonts` directly, without checking any environment variable. The font fallback feature is always enabled.

#### Scenario: Fallback always enabled
- **WHEN** `font.substitutionFonts` is accessed
- **THEN** returns `self._substitutionFonts` regardless of any environment variable

#### Scenario: Setter stores value
- **WHEN** `font.substitutionFonts = [fallback]` is called
- **THEN** the value is stored in `self._substitutionFonts` and returned by the getter

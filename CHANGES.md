# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **OpenType/CFF font support** — New `reportlab.pdfbase.openfonts` package for
  reading, subsetting, and embedding CFF-flavored OpenType fonts (.otf) in PDFs
  - Functionality: Supports both CID-Keyed (e.g. Source Han Sans, Noto CJK) and
    non-CID CFF fonts. Auto-detects font flavor via `isCFF`/`isCID` flags and
    emits the correct PDF font dictionary structure (`/Type0` + `/CIDFontType0`
    for CID fonts, `/Type1` + `FontFile3` for non-CID fonts)
  - Pure-Python CFF subsetter with complete offset patching (FDSelect, charset,
    Private DICT). HarfBuzz text shaping works with both CFF and TrueType faces
  - Compatibility: Entirely new package; no impact on existing `TTFont`, Type1,
    or any legacy APIs. All existing code continues to work unchanged
  - Known limitations: CFF2 fonts (OpenType 1.8+) and variable fonts
    (`fvar`/`gvar`) not yet supported. Unreferenced subroutines not pruned
    during subsetting
- OpenCode configuration and Chinese-localized development environment

### Changed (compatibility)
- **`reportlab.pdfbase.ttfonts` deprecated** — The module is now a thin
  compatibility shim that re-exports from `reportlab.pdfbase.openfonts` and
  emits a `DeprecationWarning` on import. All existing class and function names
  are preserved, so imports continue to work, but users should migrate to the
  new `openfonts` package. Scheduled for removal in a future release
- **`TTFont` unified with `OpenTypeFont`** — `TTFont` now inherits from
  `OpenTypeFont`. The public API is fully preserved; no code changes required
- PDF test outputs relocated from `tests/` root to `tests/pdf-out/` directory

### Fixed
- **PDFType1CFont.Subtype** — Corrected font dictionary Subtype from `Type1C`
  to `Type1` per PDF specification (ISO 32000, Table 111). `Type1C` is only
  valid for `FontFile3` streams (already correct in `_face.py`). PDFs with
  the incorrect `Type1C` Subtype may be rejected by strict PDF consumers;
  fix ensures spec compliance with no functional change for tolerant readers

## [0.0.1] - 2026-02-12

### Added
- **TrueType font fallback system** — Automatic glyph-level fallback when the
  primary font lacks certain characters
  - `TTFont.substitutionFonts`: list of fallback fonts consulted in order
  - `unicode2TT()`: splits text into fragments by glyph availability across the
    font chain for accurate mixed-script rendering
  - `stringWidth()`: per-fragment width measurement for correct line layout
  - `hasGlyph()`: glyph presence check (string or int codepoint)
  - `registerFontWithFallback()`: convenience API for one-step registration
  - `REPORTLAB_FONT_FALLBACK=1` environment variable to enable/disable at runtime
  - Compatibility: disabled by default — zero behaviour change for existing code.
    All existing `TTFont` APIs fully preserved; fallback is opt-in
- **User documentation i18n** — MkDocs-based HTML documentation with Chinese and
  English language switching for user guides
- **CI/CD automation** — GitHub Actions workflow for tests, GitHub Pages deployment,
  and PyPI publishing
- **OPSX experimental workflow** — Structured change proposal and review process

### Changed
- **Project renamed** — Package name changed from `reportlab` to
  `reportlab-enhanced` (Python import name `reportlab_enhanced`). The original
  `reportlab` namespace is preserved via a compatibility re-export layer for
  existing imports. See `src/reportlab/pdfbase/ttfonts.py` for the pattern
- **Version management** — Single source of truth moved to `pyproject.toml`;
  `__init__.py` now resolves version via `importlib.metadata`
- `setup.py` simplified to retain only dynamic build logic

## [0.0.0] - 2025-02-12

### Added
- Initial fork from ReportLab
- Based on ReportLab version 3.6.13

This version represents the starting point of the reportlab-enhanced fork,
containing all the features and fixes from the upstream ReportLab 3.6.13 release.

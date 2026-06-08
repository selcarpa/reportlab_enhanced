# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.0] - 2026-06-08

### Changed
- **BREAKING**: TTFont fallback is now enabled by default — the `REPORTLAB_FONT_FALLBACK`
  environment variable has been removed. `TTFont.substitutionFonts` now always returns
  the configured fallback list without requiring any environment variable.

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

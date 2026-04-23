# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Enhanced fork of ReportLab — a Python library for generating PDF documents, charts, and vector graphics. Pure Python since v4.0 (no C extensions). Requires Python >=3.9. BSD licensed.

## Version

Canonical version is `Version` in `src/reportlab/__init__.py` (~line 4). `VERSION.txt` is deliberately empty; `setup.py` reads `__init__.py` at build time.

## Commands

```bash
# Editable install
pip install -e .

# Run all tests
python setup.py tests-preinstall
# Or from tests directory:
cd tests && python runAll.py

# Run a single test
cd tests && python test_hello.py

# runAll.py flags
cd tests && python runAll.py --failfast --verbosity=2
cd tests && python runAll.py --exclude=test_graphics_speed,test_docs_build

# Generate docs
cd docs && python genAll.py
```

No linter, typechecker, or formatter is configured.

## Architecture

Source lives under `src/reportlab/` (setuptools `package_dir = {'': 'src'}`):

- **`pdfgen/`** — Low-level Canvas API. Direct PDF drawing operations, page management, coordinate transforms. Entry point: `from reportlab.pdfgen import canvas`
- **`platypus/`** — High-level document layout engine. Flowables (Paragraph, Table, Image), Frames, PageTemplates, and the BaseDocTemplate/BuildDocTemplate flow system. Paragraph handles XML-style markup parsing internally
- **`graphics/`** — Charts, barcodes, widgets, and renderers (SVG, PS, renderPM). Has subpackages for `charts/`, `barcode/`, `widgets/`
- **`pdfbase/`** — PDF primitives, font metrics, encryption. `pdfmetrics` manages font registration; `ttfonts` handles TrueType; `pdfpattern` builds PDF objects. Type1 fonts have a fallback mechanism via `unicode2T1()` and `Font.substitutionFonts`; TrueType fonts currently lack equivalent fallback
- **`lib/`** — Colors, validators, units, styles, and test utilities (`testutils`)

Key data flow: User code creates a Platypus document → story of Flowables → BaseDocTemplate.build() → Flowables are flowed into Frames on PageTemplates → each Flowable eventually calls into pdfgen Canvas for PDF operations.

## Test conventions

Tests use `unittest`, live in `tests/` as `test_*.py`. Each module exposes `makeSuite()` returning `makeSuiteForClasses(...)`. Test output files go through `outputfile('name.pdf')` from `reportlab.lib.testutils`. `runAll.py` cleans output before each run.

## Dependencies

Required: `pillow>=9.0.0`, `charset-normalizer`

Optional extras (in setup.py): `accel` (rl_accel), `renderpm` (rl_renderPM), `pycairo` (rlPyCairo + freetype-py), `bidi` (rlbidi), `shaping` (uharfbuzz). Some tests gracefully skip when optional packages are absent.

## Repository notes

- Upstream uses Mercurial; this fork retains `.hgeol`, `.hgignore`, `.hgtags` artifacts
- No CI workflow files in this fork
- `setup.py` downloads T1 font curves and a glyph list on first build (skip with `--no-download-t1-files`)
- Active development area: TTFont fallback support (see `project-doc/plan/`)

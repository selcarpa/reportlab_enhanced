# reportlab-enhanced

[中文](README.zh-CN.md)

An enhanced fork of [ReportLab](https://www.reportlab.com/) — the open-source Python library for generating PDF documents, charts, and vector graphics.

## Features

- Generate rich PDF documents with text, images, tables, and charts
- High-level layout engine (Platypus) with flowables, frames, and page templates
- Low-level Canvas API for direct PDF drawing operations
- Charts and graphics with SVG/PS/bitmap rendering support
- TrueType and Type1 font handling
- **Enhanced**: TrueType font fallback support for missing glyphs
- Pure Python (no C extensions required since v4.0)
- Python >= 3.9

## Enhancements over upstream

This fork builds on ReportLab 4.x with additional features:

- **TTFont Fallback**: Automatic font fallback for missing glyphs in TrueType fonts, controlled via environment variable `REPORTLAB_FONT_FALLBACK=1`
- Active development with improvements to font handling and CJK support

See [CHANGES.md](CHANGES.md) for the full changelog.

## Installation

```bash
pip install reportlab-enhanced
```

For development:

```bash
git clone https://github.com/selcarpa/reportlab_enhanced.git
cd reportlab-enhanced
pip install -e .
```

### Optional dependencies

```bash
pip install reportlab-enhanced[accel]      # rl_accel acceleration
pip install reportlab-enhanced[renderpm]   # rl_renderPM bitmap rendering
pip install reportlab-enhanced[pycairo]    # Cairo-based rendering
pip install reportlab-enhanced[bidi]       # Bidirectional text support
pip install reportlab-enhanced[shaping]    # HarfBuzz text shaping
```

## Quick Start

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=A4)
c.drawString(100, 750, "Hello, reportlab-enhanced!")
c.save()
```

For the high-level Platypus API:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("doc.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = [Paragraph("Hello, reportlab-enhanced!", styles["Title"])]
doc.build(story)
```

## Documentation

The original ReportLab documentation is available at [docs.reportlab.com](https://docs.reportlab.com/).

To build the included PDF manuals:

```bash
cd docs && python genAll.py
```

This generates three PDF references in the `docs/` directory.

## Development

This project extensively uses **vibe coding** with [Claude Code](https://claude.ai/code) (Anthropic Claude) as a development partner for code generation, refactoring, and documentation.

### Running tests

```bash
python setup.py tests-preinstall
# or
cd tests && python runAll.py
```

### Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/selcarpa/reportlab_enhanced).

## Acknowledgements

This project is a fork of [ReportLab](https://www.reportlab.com/) by ReportLab Inc., originally created by Andy Robinson, Robin Becker, and the ReportLab team. The upstream project has been developed since 2000 and provides the foundation for this enhanced version.

## License

BSD License. See [LICENSE](LICENSE) for details.

- Copyright (c) 2025-2026, selcarpa
- Copyright (c) 2000-2024, ReportLab Inc.

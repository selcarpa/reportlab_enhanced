# ReportLab User Guide Web

MkDocs site with i18n support for ReportLab User Guide.

## Build

```bash
# Install dependencies
cd docs/userguide_web
uv sync

# Convert Python DSL chapters to Markdown
uv run python py2md.py         # English
uv run python py2md.py --zh-CN  # Chinese

# Build MkDocs site
uv run python build.py
```

Output is in `site/`.

## Dependencies

- mkdocs
- mkdocs-material
- mkdocs-static-i18n

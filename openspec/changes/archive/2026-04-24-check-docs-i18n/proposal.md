## Why

The `docs/userguide/zh-CN/` directory contains i18n translations of all 14 User Guide chapters, but several files exceed 500 lines (ch2_graphics at 1105 lines, ch6_tables at 750, ch3_pdffeatures at 666, ch2a_fonts at 546). Long files are difficult for LLM-based tools to process reliably, and the previous session already demonstrated this problem with `graph_charts.py` (1459 lines → split into 3 files). Additionally, two chapters (ch5_paragraphs, ch6_tables) fail at PDF generation time due to missing image resources — a pre-existing defect affecting both English and Chinese versions. A systematic audit is needed to verify translation completeness, correctness, and file-size health.

## What Changes

- **Audit all 16 zh-CN translation files** for Python syntax correctness and structural fidelity to originals
- **Split long files** (over ~500 lines) into numbered sub-files using the `chapterName_N.py` pattern already established for `graph_charts`
- **Update `genuserguide.py`** to support split files for all chapters (it currently only handles this for `graph_charts` via a fallback loop)
- **Fix pre-existing image path issues** in ch5_paragraphs and ch6_tables so PDF generation succeeds
- **Verify end-to-end PDF generation** with `--lang=zh-CN`

## Capabilities

### New Capabilities
- `i18n-audit`: Systematic verification of zh-CN translations against English originals — syntax, coverage, and structural correctness
- `chapter-splitting`: Generic mechanism to split any long chapter file into numbered sub-files, with genuserguide.py auto-discovery

### Modified Capabilities

## Impact

- `docs/userguide/genuserguide.py` — chapter loading logic
- `docs/userguide/zh-CN/` — file restructuring (splits)
- `docs/userguide/zh-CN/ch5_paragraphs.py` — image path fix
- `docs/userguide/zh-CN/ch6_tables.py` — image path fix

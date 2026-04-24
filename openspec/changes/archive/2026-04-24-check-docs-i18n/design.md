## Context

The `docs/userguide/zh-CN/` directory holds Chinese translations of all 14 ReportLab User Guide chapters. The translation infrastructure consists of:

1. **`docs/i18n/`** — language string catalogs (`en.py`, `zh_CN.py`) for UI strings like "Chapter", "Figure", etc.
2. **`docs/userguide/zh-CN/`** — per-chapter Python files using `tools.docco.rl_doc_utils` helpers (`heading2()`, `disc()`, `eg()`, `draw()`, `Table`, etc.)
3. **`docs/userguide/genuserguide.py`** — orchestrator that `exec()`s each chapter file with a shared globals dict

Current state: all 16 zh-CN files load without syntax errors. Two files (ch5, ch6) fail at runtime due to missing image resources (`../images/testimg.gif`, `../images/replogo.gif`) — same failure occurs in English originals. The `graph_charts` chapter was already split into 3 sub-files. Four other files exceed 500 lines.

## Goals / Non-Goals

**Goals:**
- Split files over 500 lines into numbered sub-files (~400-500 lines each)
- Make `genuserguide.py` handle split files generically for all chapters
- Fix image path issues in ch5 and ch6 zh-CN translations
- Verify complete end-to-end PDF generation for zh-CN

**Non-Goals:**
- Translating new content (all chapters are already translated)
- Fixing the image path issue in English originals
- Changing the Sphinx-based docs (`docs/source/`) i18n
- Optimizing or refactoring the `rl_doc_utils` infrastructure

## Decisions

### 1. Split threshold: 500 lines

Files over 500 lines will be split. This keeps each file within a single LLM context window comfortably. The split boundary should fall at a `heading2()` or `heading3()` call to maintain logical coherence.

**Alternative considered**: 300-line limit — too aggressive, would create too many tiny files with fragmented headings.

### 2. Split file naming: `chapterName_N.py`

Follows the existing `graph_charts_1.py` / `graph_charts_2.py` / `graph_charts_3.py` pattern. Each sub-file begins with `from tools.docco.rl_doc_utils import *` and any necessary imports.

### 3. Generic split-file discovery in genuserguide.py

The current code already has a fallback loop that checks for `_N.py` files when the main file doesn't exist. This works for all chapters — no special-casing needed. The code is already correct; no changes needed to genuserguide.py for the splitting mechanism.

### 4. Image path fix approach

The image references use relative paths like `../images/testimg.gif`. The working directory when running genuserguide.py is `docs/userguide/`. The fix is to adjust paths in the zh-CN files to use absolute paths from the project root, or to use `os.path.join` to compute the correct relative path. The simplest fix: change `../images/` to an absolute path computed from `docsDir`.

## Risks / Trade-offs

- **Split boundaries may break logical flow** → Mitigate by splitting at `heading2()` boundaries only
- **Image path fix may not match English behavior** → The same fix should be applied to English originals in a separate change
- **Translation quality is not audited** → This change focuses on structural correctness; translation quality review is a separate task

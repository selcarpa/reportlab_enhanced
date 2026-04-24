## 1. Audit existing zh-CN translations

- [x] 1.1 Verify all 14 original chapters have corresponding zh-CN files (coverage check)
- [x] 1.2 Run `compile()` syntax check on all 16 zh-CN `.py` files
- [x] 1.3 Load each zh-CN file via exec() and verify flowable generation (record failures)
- [x] 1.4 Identify all files exceeding 500 lines

## 2. Split long files

- [x] 2.1 Split `ch2_graphics.py` (1105 lines) into 2-3 sub-files at heading2() boundaries
- [x] 2.2 Split `ch6_tables.py` (750 lines) into 2 sub-files at heading2() boundaries
- [x] 2.3 Split `ch3_pdffeatures.py` (666 lines) into 2 sub-files at heading2() boundaries
- [x] 2.4 Evaluate `ch2a_fonts.py` (546 lines) — split if natural heading2() boundary exists near 400-500 lines
- [x] 2.5 Remove original unsplit files after creating sub-files
- [x] 2.6 Verify each sub-file starts with required imports (`from tools.docco.rl_doc_utils import *`)

## 3. Fix pre-existing image path issues

- [x] 3.1 Fix `../images/testimg.gif` references in `ch5_paragraphs.py` zh-CN
- [x] 3.2 Fix `../images/replogo.gif` references in `ch6_tables.py` zh-CN sub-files
- [x] 3.3 Verify fixed files load without image errors

## 4. Verify genuserguide.py split-file discovery

- [x] 4.1 Confirm genuserguide.py fallback loop handles `_N.py` files for all chapter names
- [x] 4.2 Test that split chapters load in correct order with shared globals

## 5. End-to-end verification

- [x] 5.1 Run `uv run python docs/userguide/genuserguide.py --lang=zh-CN` and verify PDF output
- [x] 5.2 Run English version to confirm no regressions: `uv run python docs/userguide/genuserguide.py`

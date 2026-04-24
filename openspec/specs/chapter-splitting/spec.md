## ADDED Requirements

### Requirement: Files exceeding 500 lines SHALL be split into numbered sub-files
Any zh-CN chapter file with more than 500 lines MUST be split into `chapterName_1.py`, `chapterName_2.py`, etc., each under 500 lines. The main `chapterName.py` file SHALL be removed.

#### Scenario: Split produces files under threshold
- **WHEN** a zh-CN file exceeds 500 lines
- **THEN** it is replaced by numbered sub-files, each under 500 lines

### Requirement: Split boundaries SHALL occur at heading2() calls
Sub-files MUST begin at a `heading2()` or higher-level heading boundary to maintain logical coherence within each sub-file.

#### Scenario: Each sub-file starts with a heading
- **WHEN** a split file is created
- **THEN** the first substantive call (after imports) is `heading2()` or equivalent

### Requirement: Each sub-file SHALL include required imports
Every numbered sub-file MUST begin with `from tools.docco.rl_doc_utils import *` and any other imports needed by code in that file.

#### Scenario: Sub-files are independently loadable
- **WHEN** a sub-file is exec'd with only its own imports
- **THEN** all symbols used in the file are available

### Requirement: genuserguide.py SHALL auto-discover split files
When `chapterName.py` does not exist in the language directory, `genuserguide.py` MUST look for `chapterName_1.py`, `chapterName_2.py`, etc. and exec them in order.

#### Scenario: Split chapter loads correctly
- **WHEN** genuserguide.py processes a chapter whose main file is absent
- **THEN** it discovers and execs all numbered sub-files in sequence

### Requirement: End-to-end PDF generation SHALL succeed for zh-CN
Running `genuserguide.py --lang=zh-CN` MUST produce a valid PDF file without errors.

#### Scenario: zh-CN PDF is generated
- **WHEN** `uv run python docs/userguide/genuserguide.py --lang=zh-CN` is executed
- **THEN** a PDF file is created at `docs/reportlab-userguide-zh-CN.pdf`

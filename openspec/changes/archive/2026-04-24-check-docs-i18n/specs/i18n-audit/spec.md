## ADDED Requirements

### Requirement: All zh-CN files SHALL pass Python syntax validation
Every `.py` file in `docs/userguide/zh-CN/` MUST be valid Python that can be parsed by `compile()` without errors.

#### Scenario: Syntax check passes for all files
- **WHEN** each `.py` file in `docs/userguide/zh-CN/` is compiled with `compile(open(path).read(), path, 'exec')`
- **THEN** no SyntaxError is raised

### Requirement: Each original chapter SHALL have a corresponding zh-CN translation
For every chapter file in `docs/userguide/` (excluding `genuserguide.py`), there SHALL exist either a same-named file in `docs/userguide/zh-CN/` or a set of numbered sub-files (`chapterName_1.py`, `chapterName_2.py`, ...).

#### Scenario: All original chapters are covered
- **WHEN** the list of original chapter names is compared against zh-CN directory contents
- **THEN** every original chapter has at least one corresponding zh-CN file

### Requirement: All zh-CN files SHALL load without runtime errors (excluding pre-existing image issues)
Each zh-CN file, when `exec()`d with the standard `rl_doc_utils` globals, MUST produce flowables without raising exceptions. Known pre-existing image path issues in ch5 and ch6 are exempt until fixed.

#### Scenario: Files load and produce flowables
- **WHEN** each zh-CN file is exec'd with `rl_doc_utils` globals
- **THEN** the story gains flowables and no exception is raised

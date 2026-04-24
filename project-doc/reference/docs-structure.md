# docs/ 目录结构说明

## 总览

`docs/` 目录包含 ReportLab 的全部文档源文件、构建脚本和生成产物。文档系统包含两套独立的构建管线：**Platypus PDF 管线**（自研）和 **Sphinx HTML 管线**（标准工具）。

```
docs/
├── 00readme.txt              # 目录说明
├── genAll.py                 # 一键构建所有文档（PDF）的总入口
├── Makefile                  # Sphinx 构建配置（make html / make latex）
├── make.bat                  # Windows 下的 Sphinx 构建脚本
├── gen_epydoc                # Epydoc API 文档生成配置（已弃用）
├── images/                   # 文档中引用的图片资源
├── i18n/                     # PDF 用户手册的国际化模块
├── source/                   # Sphinx 文档源文件（.rst）
├── userguide/                # PDF 用户手册源文件（.py）
├── reference/                # PDF API 参考手册构建脚本
├── build/                    # Sphinx 构建产物输出目录
├── reportlab-userguide.pdf          # 英文用户手册（构建产物）
└── reportlab-userguide-zh-CN.pdf    # 中文用户手册（构建产物）
```

## 各子目录详解

### `userguide/` — PDF 用户手册

用 Python 脚本编写章节内容，通过 Platypus 文档引擎直接生成 PDF。每个 `.py` 文件是一个章节，执行时向 Platypus Story 中追加 Flowable。

**章节文件（英文）：**

| 文件 | 内容 |
|---|---|
| `ch1_intro.py` | 项目介绍 |
| `ch2_graphics.py` | 图形基础 |
| `ch2a_fonts.py` | 字体系统 |
| `ch3_pdffeatures.py` | PDF 特性（书签、链接等） |
| `ch4_platypus_concepts.py` | Platypus 布局概念 |
| `ch5_paragraphs.py` | 段落排版 |
| `ch6_tables.py` | 表格 |
| `ch7_custom.py` | 自定义 Flowable |
| `graph_intro.py` | 图表简介 |
| `graph_concepts.py` | 图表概念 |
| `graph_charts.py` | 图表类型 |
| `graph_shapes.py` | 图形形状 |
| `graph_widgets.py` | 小部件 |
| `app_demos.py` | 示例附录 |

**`genuserguide.py`** 是构建入口，按顺序加载各章节 `.py` 并执行，最终 `multiBuild` 输出 PDF。

用法：
```bash
# 英文版（默认）
cd docs && uv run python userguide/genuserguide.py

# 中文版
cd docs && uv run python userguide/genuserguide.py --lang=zh-CN
```

### `userguide/zh-CN/` — 中文翻译

中文版用户手册的章节文件。由于中文内容较多，部分章节被拆分为多个文件（如 `ch2a_fonts_1.py`、`ch2a_fonts_2.py`）。构建时 `genuserguide.py` 会自动检测：若单文件不存在，则查找 `_1`、`_2` 等编号文件并依次加载。

### `i18n/` — 国际化模块

为 PDF 用户手册提供多语言字符串常量（章节标题、目录标题、页码格式等）。

| 文件 | 作用 |
|---|---|
| `__init__.py` | 核心逻辑：`set_language()`、`get_strings()`，合并默认语言与目标语言的键值 |
| `en.py` | 英文字符串（默认，用作 fallback） |
| `zh_CN.py` | 中文字符串，未定义的键自动回退到英文 |

构建中文版时，`genuserguide.py` 调用 `set_language('zh_CN')`，章节脚本通过 `get_strings()` 获取对应语言的字符串。

### `source/` — Sphinx 文档源文件

基于 Sphinx 的 API 参考文档，源文件为 `.rst` 格式。

```
source/
├── conf.py          # Sphinx 配置（版本、主题、扩展、locale）
├── index.rst        # 文档首页 / 目录树
├── pdfgen.rst       # pdfgen 模块 API 文档
├── platypus.rst     # platypus 模块 API 文档
├── graphics.rst     # graphics 模块 API 文档
├── lib.rst          # lib 模块 API 文档
├── _static/         # 自定义 CSS
├── _templates/      # 自定义 Jinja2 模板
└── _locale/         # Sphinx 国际化翻译文件（gettext .po）
```

Sphinx 配置启用了 `autodoc`、`doctest`、`todo`、`coverage` 扩展，并通过 `locale_dirs = ['_locale']` 支持多语言。

用法：
```bash
cd docs && make html    # 生成 HTML 到 build/html/
```

### `reference/` — PDF API 参考手册

通过 YAML 描述文件 + `yaml2pdf` 工具生成 PDF 格式的 API 参考手册。

| 文件 | 作用 |
|---|---|
| `genreference.py` | 构建脚本，调用 `yaml2pdf.run()` 生成 PDF |
| `reference.yml` | YAML 格式的 API 描述数据 |
| `build.bat` | Windows 构建脚本 |

用法：
```bash
cd docs/reference && uv run python genreference.py
```

### `images/` — 图片资源

文档中引用的静态图片文件（GIF、JPG、PNG、A85 格式），包括 Logo、截图、示例图片等。

### `build/` — Sphinx 构建产物

Sphinx 的输出目录，包含 `doctrees/`（中间文件）和 `html/`（最终 HTML 页面）。此目录由 Sphinx 自动生成，不应手动编辑。

## 两套文档管线对比

| 特性 | Platypus PDF 管线 | Sphinx HTML 管线 |
|---|---|---|
| 源文件格式 | `.py`（Python 脚本） | `.rst`（reStructuredText） |
| 输出格式 | PDF | HTML / LaTeX |
| 构建工具 | 自研（Platypus + rl_doc_utils） | Sphinx |
| 国际化 | `i18n/` 模块 + 独立翻译章节 | `_locale/`（gettext .po 文件） |
| 覆盖内容 | 用户手册（教程式） | API 参考（自动提取 docstring） |

## 构建命令汇总

```bash
# 构建全部 PDF 文档（用户手册）
cd docs && uv run python genAll.py

# 单独构建英文用户手册
cd docs/userguide && uv run python genuserguide.py

# 单独构建中文用户手册
cd docs/userguide && uv run python genuserguide.py --lang=zh-CN

# 构建 Sphinx HTML 文档
cd docs && make html

# 构建 PDF API 参考手册
cd docs/reference && uv run python genreference.py
```

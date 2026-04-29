# 文档构建指南

## 概览

本项目有三套文档构建系统：

| 管线 | 源文件格式 | 输出格式 | 工具 |
|---|---|---|---|
| PDF 用户手册 | `.py` DSL | PDF | Platypus + rl_doc_utils |
| HTML 用户手册 | `.py` → `.md` | HTML | MkDocs + mkdocs-static-i18n |
| HTML API 参考 | `.rst` | HTML | Sphinx |

---

## 一、PDF 用户手册

用户手册由 `docs/userguide/genuserguide.py` 生成。脚本通过 `exec()` 加载各章节 Python 文件，调用 `rl_doc_utils` 的辅助函数（`heading2()`、`disc()`、`eg()`、`draw()` 等）构建文档流，最终由 Platypus 输出 PDF。

### 构建命令

```bash
# 英文版
uv run python docs/userguide/genuserguide.py

# 中文版
uv run python docs/userguide/genuserguide.py --lang=zh-CN
```

**输出：** `docs/reportlab-userguide.pdf` 或 `docs/reportlab-userguide-zh-CN.pdf`

### 其他参数

| 参数 | 说明 |
|------|------|
| `--lang=<lang>` | 语言代码，默认 `en` |
| `--outdir=<dir>` | 指定输出目录，默认为 `docs/` |
| `-s` | 静默模式 |
| `-timing` | 输出构建耗时 |
| `-prof` | cProfile 性能分析 |

### 章节文件结构

英文章节位于 `docs/userguide/`，中文翻译位于 `docs/userguide/zh-CN/`。

部分章节过长时拆分为多个带编号的子文件（如 `ch2_graphics_1.py`）。`genuserguide.py` 自动检测：若 `chapterName.py` 不存在，则依次加载 `chapterName_1.py`、`chapterName_2.py` 等。

### i18n 机制

- `docs/i18n/en.py` — 英文字符串常量（"Chapter"、"Figure" 等）
- `docs/i18n/zh_CN.py` — 中文字符串常量
- `docs/i18n/__init__.py` — 语言切换与字符串合并逻辑

---

## 二、HTML 用户手册

MkDocs + Material 主题构建的用户手册，支持中英文切换。

### 目录结构

```
docs/userguide_web/
├── docs/
│   ├── en/           # 英文 Markdown 章节
│   └── zh/           # 中文 Markdown 章节
├── build.py          # 构建脚本
├── mkdocs.yml        # MkDocs 配置
├── py2md.py          # Python DSL → Markdown 转换脚本
└── pyproject.toml    # 项目依赖
```

### 构建命令

```bash
cd docs/userguide_web

# 安装依赖
uv sync

# 转换 Python DSL 章节为 Markdown
uv run python py2md.py         # 英文
uv run python py2md.py --zh-CN  # 中文

# 构建 MkDocs HTML 网站
uv run python build.py
```

**输出：** `docs/userguide_web/site/`

### 中英文切换

mkdocs-static-i18n 插件在每页 header 自动生成语言切换下拉菜单，实现页到页的对应切换。

### mkdocs.yml 配置说明

```yaml
plugins:
  - i18n:
      docs_structure: folder   # 按 en/ zh/ 文件夹区分语言
      fallback_to_default: true # 中文缺失时 fallback 到英文
      languages:
        - locale: en
          name: English
          default: true
          nav: {...}  # 英文导航
        - locale: zh
          name: 中文
          nav: {...}  # 中文导航
```

---

## 三、HTML API 参考文档

基于 Sphinx 构建，源文件位于 `docs/source/`。

### 构建命令

```bash
cd docs
make html
```

**输出：** `docs/build/html/`

### 其他格式

```bash
make latex     # LaTeX 源文件 → docs/build/latex/
make changes   # 变更概览
make linkcheck # 检查外部链接
```

---

## 四、PDF API 参考手册

通过 YAML 描述文件 + `yaml2pdf` 工具生成 PDF。

```bash
cd docs/reference && uv run python genreference.py
```

---

## 五、一键构建所有 PDF

```bash
uv run python docs/genAll.py
```

---

## 目录结构

```
docs/
├── 00readme.txt              # 目录说明
├── genAll.py                 # 一键构建所有 PDF 文档
├── Makefile                  # Sphinx 构建配置
├── make.bat                  # Windows 构建脚本
├── gen_epydoc                # Epydoc 配置（已弃用）
├── images/                   # 文档图片资源
├── i18n/                     # PDF 用户手册国际化模块
├── source/                   # Sphinx 文档源文件（.rst）
├── userguide/                # PDF 用户手册源文件（.py DSL）
│   └── zh-CN/               # 中文翻译章节
├── userguide_web/            # HTML 用户手册（MkDocs）
├── reference/                # PDF API 参考手册
├── build/                   # Sphinx 构建产物
├── reportlab-userguide.pdf          # 英文用户手册 PDF
└── reportlab-userguide-zh-CN.pdf    # 中文用户手册 PDF
```

### `userguide/` 章节文件

| 文件 | 内容 |
|---|---|
| `ch1_intro.py` | 项目介绍 |
| `ch2_graphics.py` | 图形基础 |
| `ch2a_fonts.py` | 字体系统 |
| `ch3_pdffeatures.py` | PDF 特性 |
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

---

## 已知问题

英文版的 `ch5_paragraphs.py` 和 `ch6_tables.py` 中存在硬编码的相对图片路径（`../images/testimg.gif`），从项目根目录运行时无法解析。中文版已修正为 `docs/images/...`。

# 构建文档

本项目有两套文档构建系统：Sphinx（API 参考，输出 HTML）和自定义 Python 脚本（用户手册，输出 PDF）。

## 前置依赖

```bash
uv sync          # 安装项目运行时依赖（reportlab, pillow 等）
uv pip install sphinx  # Sphinx 仅构建 API 文档时需要
```

## 一、用户手册（PDF）

用户手册由 `docs/userguide/genuserguide.py` 生成。该脚本通过 `exec()` 依次加载各章节 Python 文件，每个文件调用 `rl_doc_utils` 提供的辅助函数（`heading2()`、`disc()`、`eg()`、`draw()` 等）构建文档故事流，最终由 Platypus 排版引擎输出 PDF。

### 构建英文版

```bash
uv run python docs/userguide/genuserguide.py
```

输出文件：`docs/reportlab-userguide.pdf`

### 构建中文版

```bash
uv run python docs/userguide/genuserguide.py --lang=zh-CN
```

输出文件：`docs/reportlab-userguide-zh-CN.pdf`

### 其他参数

| 参数 | 说明 |
|------|------|
| `--lang=<lang>` | 语言代码，默认 `en`。对应 `docs/userguide/<lang>/` 下的翻译文件 |
| `--outdir=<dir>` | 指定输出目录，默认为 `docs/` |
| `-s` | 静默模式（不打印进度信息） |
| `-timing` | 输出构建耗时 |
| `-prof` | 生成 cProfile 性能分析文件 |
| `(width, height)` | 位置参数，指定页面尺寸，如 `(595, 842)` |

### 章节文件结构

英文章节位于 `docs/userguide/`，中文翻译位于 `docs/userguide/zh-CN/`。

当一个章节过长（超过约 500 行）时，会被拆分为多个带编号的子文件：

```
docs/userguide/zh-CN/
├── ch2_graphics_1.py      # 拆分后的第 1 部分
├── ch2_graphics_2.py      # 拆分后的第 2 部分
├── ch2_graphics_3.py      # 拆分后的第 3 部分
├── graph_charts_1.py
├── graph_charts_2.py
├── graph_charts_3.py
└── ...
```

`genuserguide.py` 会自动检测：如果 `chapterName.py` 不存在，则依次加载 `chapterName_1.py`、`chapterName_2.py`、...。

每个子文件需以 `from tools.docco.rl_doc_utils import *` 及其他必要 import 开头。

### i18n 机制

- `docs/i18n/en.py` — 英文字符串常量（"Chapter"、"Figure" 等页眉页脚文本）
- `docs/i18n/zh_CN.py` — 中文字符串常量
- `docs/i18n/__init__.py` — 语言切换与字符串合并逻辑

翻译规则：
- `heading()` 文本翻译为对应语言
- `disc()` 说明文本翻译
- `eg()` 代码块保持不变
- 表格中的属性名（Property 列）保持英文，含义列翻译

### 已知问题

英文版的 `ch5_paragraphs.py` 和 `ch6_tables.py` 中存在硬编码的相对图片路径（`../images/testimg.gif`），从项目根目录运行时无法解析。中文版已修正为 `docs/images/...`。

## 二、API 参考文档（HTML）

API 参考基于 Sphinx 构建，源文件位于 `docs/source/`。

### 构建 HTML

```bash
cd docs
make html
```

输出目录：`docs/build/html/`

也可以直接调用：

```bash
sphinx-build -b html -d docs/build/doctrees docs/source docs/build/html
```

### 构建其他格式

```bash
cd docs
make latex     # 生成 LaTeX 源文件 → docs/build/latex/
make changes   # 生成变更概览
make linkcheck # 检查外部链接
```

### 翻译

Sphinx 翻译目录位于 `docs/source/_locale/`，包含 `.pot` 模板和 `zh-CN/LC_MESSAGES/` 下的 `.po/.mo` 翻译文件。构建中文 HTML 时需配置 `conf.py` 中的 `language` 设置。

## 三、一键构建所有文档

```bash
uv run python docs/genAll.py
```

该脚本会依次调用 `genuserguide.py` 构建用户手册。默认仅启用 `docs/userguide/genuserguide.py`（其他生成器已注释掉）。

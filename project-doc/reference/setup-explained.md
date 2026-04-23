# setup.py 功能说明

## 概览

`setup.py` 是项目的构建和安装脚本，基于 setuptools。它负责包的构建、安装、测试以及一些构建时的资源下载。

## 入口与版本

- 脚本自身的 `__version__='4.4.5'` 仅用于构建过程内部
- 包的实际版本由 `get_version()` 从 `src/reportlab/__init__.py` 的 `Version` 变量读取
- `get_version()` 先尝试读源码，失败后尝试 import 已编译的 `.pyc/.pyo`

## 命令分发（main 函数）

`main()` 根据命令参数分为两个分支：

### 测试命令

- `test` / `tests` / `tests-postinstall` / `tests-preinstall`：运行 `tests/runAll.py`
  - `--failfast`：遇到失败立即停止
  - `--verbose-tests`：详细输出
  - `--exclude=test_xxx,test_yyy`：排除指定测试
  - `tests-preinstall` 会将 `src/` 加入 `PYTHONPATH`（开发模式测试）

### 构建/安装命令

其余所有参数交给 `setuptools.setup()` 处理（如 `install`、`bdist_wheel`、`sdist` 等）。

## 构建时资源下载

构建过程中会执行两个下载操作：

### 1. T1 字体曲线文件（get_fonts）

- 从 `https://www.reportlab.com/ftp/pfbfer-20180109.zip` 下载
- 解压到 `src/reportlab/fonts/` 目录
- 仅在字体文件不存在时下载
- 可通过 `--no-download-t1-files` 跳过

### 2. Glyph 列表模块（get_glyphlist_module）

- 从 Adobe 的 AGL (Adobe Glyph List) 下载 glyphlist.txt
- 生成 `src/reportlab/pdfbase/_glyphlist.py`
- 包含 glyph 名称到 Unicode 的映射字典
- 仅在文件不存在时生成

## setup() 元数据

| 参数 | 值 | 说明 |
|------|------|------|
| `name` | `reportlab-enhanced` | PyPI 包名 |
| `version` | `get_version()` | 从 `__init__.py` 读取 |
| `license` | BSD | 双版权：selcarpa + ReportLab Inc. |
| `description` | The ReportLab Toolkit (Enhanced Fork) | 短描述 |
| `author` | selcarpa, Andy Robinson, ... | 作者列表 |
| `url` | github.com/selcarpa/reportlab_enhanced | 项目主页 |
| `package_dir` | `{'': 'src', 'reportlab': 'src/reportlab'}` | 源码在 src/ 下 |
| `python_requires` | `>=3.9,<4` | Python 版本要求 |

## 包结构

`packages` 列表声明了所有子包：

```
reportlab/
├── graphics/
│   ├── charts/
│   ├── samples/
│   ├── widgets/
│   └── barcode/
├── lib/
├── pdfbase/
├── pdfgen/
└── platypus/
```

`package_data` 通过 `reportlab_files` 列表包含字体文件和 license 文件。

## 依赖

### 必需依赖

- `pillow>=9.0.0`：图片处理（除 JPG 外的图片嵌入）
- `charset-normalizer`：字符编码检测

### 可选依赖（extras_require）

| extra | 包 | 用途 |
|-------|------|------|
| `accel` | `rl_accel` | C 加速模块 |
| `renderpm` | `rl_renderPM` | 位图渲染 |
| `pycairo` | `rlPyCairo` + `freetype-py` | Cairo 渲染后端 |
| `bidi` | `rlbidi` | 双向文本支持 |
| `shaping` | `uharfbuzz` | HarfBuzz 文字整形 |

## 辅助函数

- `infoline(t)`：带格式的日志输出，收集到 `INFOLINES`，构建结束时汇总打印
- `specialOption(n)`：从 `sys.argv` 中提取并移除自定义参数（如 `--verbose`）
- `spCall(cmd)`：执行子进程命令，用于运行测试
- `findFile(root, wanted)`：安全地递归查找文件，通过 dev/inode 防止符号链接循环
- `listFiles(root)`：安全地列出目录下所有文件
- `url2data(url)`：下载 URL 内容，返回 BytesIO 或原始字节

# 运行单元测试

## 快速开始

```bash
python setup.py tests-preinstall
```

此命令会自动将 `src/` 加入 `PYTHONPATH`，然后运行 `tests/runAll.py`。

## 单独运行测试

```bash
cd tests
python runAll.py
```

运行单个测试文件：

```bash
cd tests
python test_ttfont_fallback_core.py
```

## runAll.py 参数

| 参数 | 说明 |
|------|------|
| `--failfast` | 遇到失败立即停止 |
| `--verbosity=2` | 详细输出 |
| `--exclude=test_a,test_b` | 排除指定测试文件（不含 `.py` 后缀） |
| `--outdir=<path>` | 指定测试输出目录 |
| `--clean` | 清理测试输出文件后运行 |

示例：

```bash
cd tests
python runAll.py --failfast --verbosity=2 --exclude=test_graphics_speed,test_docs_build
```

## 测试文件命名与发现

- 测试文件以 `test_*.py` 命名，放在 `tests/` 目录下
- `runAll.py` 通过 glob 匹配自动发现所有 `test_*.py` 文件
- 每个文件必须实现 `makeSuite()` 函数，返回测试套件
- 以 `_` 开头的文件（如 `_ttfont_fallback_helpers.py`）不会被当作测试文件

## 测试分类

### 1. TTFont Fallback 测试

| 文件 | 说明 | 依赖 |
|------|------|------|
| `test_ttfont_fallback_core.py` | unicode2TT、hasGlyph、环境变量、stringWidth | 仅内部 Vera 字体 |
| `test_ttfont_fallback_multiscript.py` | 多语种回退、宽度计算 | 外部字体（自动跳过） |
| `test_ttfont_fallback_pdf.py` | PDF 生成 | 内部 + 外部字体 |
| `test_ttfont_fallback_api.py` | API 与回归测试 | 仅内部 Vera 字体 |

共享辅助代码在 `_ttfont_fallback_helpers.py` 中。

### 2. OTF/OpenType 测试

| 文件 | 说明 |
|------|------|
| `test_otf_loading.py` | OTF/TTF 字体加载 |
| `test_otf_metrics.py` | 字体验证（glyph count、bbox等） |
| `test_otf_subsetting.py` | 子集化测试 |
| `test_otf_rendering.py` | PDF渲染（生成实际PDF文件） |
| `test_otf_asian.py` | 亚洲CJK文本渲染 |
| `test_otf_fallback.py` | OTF + TTF 混合回退 |
| `test_pdfbase_otf.py` | OTF PDF 渲染基础测试 |

### 3. 传统TTF测试

| 文件 | 说明 |
|------|------|
| `test_pdfbase_ttfonts.py` | TrueType 核心功能测试 |

### 共享辅助代码

- `_ttfont_fallback_helpers.py` — fallback 测试辅助函数

## 外部字体

OTF/OpenType 测试需要 `tests_resource/` 目录下的外部字体。从以下地址下载：

```
https://reportlab-enhanced.tain.one/test-resource.zip
```

详细信息见 `tests_resource/README.md`。

如果缺失字体，相关测试会自动 skip，不影响其他测试。

## 测试输出

测试生成的 PDF 文件存放在 `tests/pdf-out/` 目录下，其他输出文件存放在 `tests/` 目录下。

运行前可清理所有输出：

```bash
cd tests
python runAll.py --clean
```

这些输出文件已在 `.gitignore` 中被忽略。
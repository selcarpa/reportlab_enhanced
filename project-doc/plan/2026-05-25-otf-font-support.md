# ReportLab OTF (CFF) Font Support 设计方案

## 1. 概述

### 1.1 背景

ReportLab 当前的字体体系中，TTFont 仅支持 TrueType 轮廓字体（`.ttf`、`.ttc`），
在 `TTFontParser.readHeader()` 中明确拒绝了 OpenType CFF 字体（sfnt 版本 `0x4F54544F`，即 "OTTO"）：

```python
if version==0x4F54544F:
    raise TTFError('%s file "%s": postscript outlines are not supported'%(self.fileKind,self.filename))
```

OTF 字体（OpenType with CFF outlines）是当前最常用的字体格式之一，尤其是：
- Adobe 的 Source Han Sans / Source Han Serif（思源黑体/宋体）
- Google 的 Noto Sans / Noto Serif CJK
- 大量商业字体的 OpenType 版本

本项目中已存在测试用 OTF 文件：`SourceHanSansK-Light.otf`（CFF 表大小 15.5MB）。

### 1.2 目标

为 ReportLab 添加 OTF（CFF 轮廓）字体支持，使得：
- 字体类可以加载 `.otf` 文件（CFF 轮廓）
- 正确提取字体度量信息（名称、宽度、bbox 等）
- 正确生成 PDF 子集嵌入（FontFile3 + Type1C）
- 与现有 TrueType 字体使用方式完全一致（API 不变）
- 与现有 TTFont fallback 机制兼容
- 对类名进行重构，使命名反映实际支持的字体格式

### 1.3 不在范围内

- CFF2 字体（OpenType 1.8+ 的新格式，使用 CFF2 表）
- 可变字体（Variable Fonts，使用 `fvar`/`gvar` 表）
- 从 OTF 字体自动推断 fallback 关系
- Type1 字体的更新或修改

---

## 2. 架构设计

### 2.1 双包架构

本方案采用双包架构，将字体核心逻辑与向后兼容分离：

| 文件/包 | 角色 | 说明 |
|--------|------|------|
| `src/reportlab/pdfbase/openfonts/` | **主包（新）** | 包含所有字体逻辑的全新包，命名反映 OpenType 标准 |
| `src/reportlab/pdfbase/ttfonts.py` | **兼容层（已过期）** | 仅保留向后兼容别名，导入自 `openfonts`，标注 `@deprecated` |

**设计原则**：
- `openfonts/` 包是未来所有开发的起点，新类名、新功能全部在此
- `ttfonts.py` 完全不承载新逻辑，仅做兼容转发，避免代码重复
- 两模块共存期间，`import` 路径对用户透明（`from reportlab.pdfbase import ttfonts` 继续工作）

### 2.2 CFF 与 TrueType 差异

| 方面 | TrueType (.ttf) | OpenType CFF (.otf) |
|------|----------------|---------------------|
| sfnt 版本 | `0x00010000` 或 `0x74727565` | `0x4F54544F` ("OTTO") |
| 轮廓格式 | TrueType 二次 B 样条 | CFF 三次贝塞尔 |
| 字形数据表 | `glyf` + `loca` | `CFF `（CharStrings INDEX） |
| maxp 格式 | 32 字节，版本 1.0 | 6 字节，版本 0.5 |
| 子集化 | 复制 glyf 条目，重建 loca | 重建 CharStrings INDEX、SUBR、FDSelect |
| PDF 嵌入 | FontFile2 / TrueType | FontFile3 / Type1C |
| PDF 字体子类型 | `TrueType` | `Type1C` |
| 共享表 | name, head, OS/2, post, hhea, hmtx, cmap | 同左（完全一致） |

### 2.3 类名重构

#### 用户面向类

| 旧名称 | 新名称 | 向后兼容别名 | 说明 |
|--------|--------|-------------|------|
| `TTFont` | `OpenTypeFont` | `TTFont = OpenTypeFont` | 主用户类，支持 TTF + OTF |

**`OpenTypeFont` 名称选择理由**：
- OpenType 是 TTF 和 OTF 的统一标准（ISO 14496-22）
- 明确表示字体格式为 OpenType（而非仅 TrueType）
- 与 `pdfmetrics.Font`（Type1 字体）形成清晰的命名体系

#### 内部类

| 旧名称 | 新名称 | 说明 |
|--------|--------|------|
| `TTFontParser` | `FontParser` | sfnt 二进制格式解析器 |
| `TTFontFile` | `FontFile` | 字体文件解析 + 子集生成 |
| `TTFontFace` | `FontFace` | 字体面（TypeFace + 度量 + 子集对象） |
| `TTFontMaker` | `FontMaker` | PDF 子集流生成器 |
| `TTEncoding` | `FontEncoding` | UTF-8 编码适配器 |

### 2.4 向后兼容策略

`ttfonts.py` 完全由兼容别名组成，不含任何类实现。

**效果**：
- 现有用户代码 `from reportlab.pdfbase.ttfonts import TTFont` 继续工作（带 DeprecationWarning）
- `isinstance(font, TTFont)` 继续工作
- 新代码推荐 `from reportlab.pdfbase.openfonts import OpenTypeFont`
- 内部代码直接使用 `openfonts` 中的新名称

---

## 3. 模块设计

### 3.1 新模块文件结构

```
src/reportlab/pdfbase/openfonts/
├── __init__.py       # 包入口，导出主类 + 向后兼容别名
├── _common.py         # 公共定义：错误类、SUBSETN、辅助函数
├── _sfnt.py           # FontParser 基类（sfnt 二进制解析）
├── _ttf.py            # FontFile、FontMaker（TrueType 专用）
├── _cff.py            # CFFParser、CFFSubsetter（新增 CFF 专用）
├── _face.py           # FontFace（字体面度量）
├── _encoding.py       # FontEncoding（UTF-8 编码适配器）
├── _font.py           # OpenTypeFont（主用户类）
└── _shaping.py        # ShapedFragWord、ShapedStr（文本整形支持）
```

**文件拆分原则**：
- **独立性**：每个模块可独立理解，CFF 代码与 TrueType 代码完全隔离
- **可测试性**：每个模块可单独测试，减少全量回归风险
- **可维护性**：文件体积适中（300-600 行），便于导航

### 3.2 各类归属

| 类名 | 模块文件 | 说明 |
|------|----------|------|
| `FontParser` | `_sfnt.py` | sfnt 二进制格式解析器 |
| `FontFile` | `_ttf.py` | 字体文件解析 + 子集生成 |
| `FontMaker` | `_ttf.py` | PDF 子集流生成器 |
| `FontFace` | `_face.py` | 字体面（度量 + 子集对象） |
| `FontEncoding` | `_encoding.py` | UTF-8 编码适配器 |
| `OpenTypeFont` | `_font.py` | 主用户类，支持 TTF + OTF |
| `CFFParser` | `_cff.py` | CFF 表解析器（新增） |
| `CFFSubsetter` | `_cff.py` | CFF 子集生成器（新增） |
| `TTFError` | `_common.py` | 异常类 |
| `SUBSETN`, `makeToUnicodeCMap`, `splice` | `_common.py` | 辅助函数 |

### 3.3 文件大小估算

| 文件 | 行数（估） | 说明 |
|------|----------|------|
| `_common.py` | ~80 | 错误类 + 辅助函数 |
| `_sfnt.py` | ~200 | FontParser 基类 |
| `_ttf.py` | ~700 | FontFile + FontMaker（TrueType 部分） |
| `_cff.py` | ~500 | CFFParser + CFFSubsetter |
| `_face.py` | ~100 | FontFace |
| `_encoding.py` | ~20 | FontEncoding |
| `_font.py` | ~300 | OpenTypeFont |
| `_shaping.py` | ~50 | 文本整形 |
| `__init__.py` | ~50 | 导出 + 别名 |
| **总计** | **~2000** | 与原 `ttfonts.py` 约 1585 行相当 |

### 3.4 受影响文件清单

#### 新增文件

| 文件 | 说明 |
|------|------|
| `src/reportlab/pdfbase/openfonts/__init__.py` | 包入口，导出主类 + 兼容别名 |
| `src/reportlab/pdfbase/openfonts/_common.py` | 公共定义：错误类、SUBSETN、辅助函数 |
| `src/reportlab/pdfbase/openfonts/_sfnt.py` | FontParser 基类（sfnt 解析） |
| `src/reportlab/pdfbase/openfonts/_ttf.py` | FontFile、FontMaker（TrueType 专用） |
| `src/reportlab/pdfbase/openfonts/_cff.py` | CFFParser、CFFSubsetter（新增 CFF 逻辑） |
| `src/reportlab/pdfbase/openfonts/_face.py` | FontFace（字体面） |
| `src/reportlab/pdfbase/openfonts/_encoding.py` | FontEncoding（编码适配器） |
| `src/reportlab/pdfbase/openfonts/_font.py` | OpenTypeFont（主用户类） |
| `src/reportlab/pdfbase/openfonts/_shaping.py` | ShapedFragWord、ShapedStr（文本整形） |
| `tests/test_pdfbase_otf.py` | OTF 字体测试 |

#### 修改文件

| 文件 | 修改内容 |
|------|---------|
| `src/reportlab/pdfbase/ttfonts.py` | 改为纯兼容层，从 openfonts 导入重导出 |
| `src/reportlab/pdfbase/pdfdoc.py` | 新增 `PDFType1CFont` 类 |
| `tests/test_pdfbase_ttfonts.py` | 测试继续通过（别名生效） |

#### 引用更新（ttfonts → openfonts，渐进式）

| 文件 | 引用数 | 说明 |
|------|--------|------|
| `src/reportlab/pdfbase/pdfmetrics.py` | 5 | 内部引用，迁移到 openfonts |
| `src/reportlab/platypus/paragraph.py` | 3 | 懒导入 + 示例代码 |
| `src/reportlab/graphics/testshapes.py` | 6 | `ttfonts.TTFont(...)` |
| `tests/test_ttfont_fallback_api.py` | 8 | 导入 + isinstance 检查 |
| `tests/test_ttfont_fallback_core.py` | 4 | 导入 + 实例化 |
| `tests/_ttfont_fallback_helpers.py` | 8 | 导入 + 实例化 |
| `tests/test_rl_accel.py` | 2 | 懒导入 + 实例化 |
| `tests/test_platypus_paragraphs.py` | 6 | 导入 + 实例化 |
| `tests/test_issues.py` | 2 | 懒导入 + 实例化 |
| `tests/test_paragraphs.py` | 1 | `ttfonts.TTFont(...)` |
| `tests/test_multibyte_jpn.py` | 5 | 导入 + 实例化 |
| `tests/test_pdfbase_encodings.py` | 3 | 导入 + 实例化 |
| `tests/test_arabic.py` | 2 | 导入 + 实例化 |
| `tests/test_charts_textlabels.py` | 2 | 懒导入 + 实例化 |
| `docs/userguide/genuserguide.py` | 4 | 示例代码 |
| `docs/userguide/ch2a_fonts.py` | 1 | 字符串引用 |
| `docs/userguide/zh-CN/ch2a_fonts_1.py` | 10 | 字符串引用 + 代码示例 |

#### 不受影响的文件

- `src/reportlab/pdfgen/textobject.py` — 仅注释引用
- `src/reportlab/pdfgen/canvas.py` — 导入 `ShapedStr` 等，不涉及字体类名
- `src/reportlab/graphics/renderPM.py` — 导入 `ShapedStr` 等
- `src/reportlab/graphics/utils.py` — 导入 `ShapedStr`
- `src/reportlab/rl_settings.py` — 无类引用

---

## 4. 公开 API

### 4.1 API 兼容性

**核心原则**：用户无需改变任何使用方式。现有代码：

```python
# 旧写法（继续支持）
font = TTFont('MyFont', 'MyFont.otf')  # 之前会报错，现在正常工作
pdfmetrics.registerFont(font)

# 新写法（推荐）
font = OpenTypeFont('MyFont', 'MyFont.otf')
pdfmetrics.registerFont(font)

c = canvas.Canvas('output.pdf')
c.setFont('MyFont', 12)
c.drawString(100, 700, 'Hello 你好')
c.save()
```

自动识别 OTF 文件，无需额外参数或配置。

### 4.2 新增内部属性

| 属性 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `FontParser.isCFF` | `FontParser` | `bool` | 标识是否为 CFF 字体，在 `readHeader()` 中设置 |
| `FontFace.cffData` | `FontFace` | `bytes` 或 `None` | CFF 表原始数据（仅 CFF 字体） |
| `FontFace.cffCharStrings` | `FontFace` | `list[tuple[int,int]]` 或 `None` | CharStrings INDEX 中每个字形的 (offset, length) |
| `FontFace.cffFDSelect` | `FontFace` | `bytes` 或 `None` | FDSelect 数据（CID 字体） |
| `FontFace.cffFDArray` | `FontFace` | `list[dict]` 或 `None` | Font DICT 数组（CID 字体） |
| `FontFace.cffCharset` | `FontFace` | `list` 或 `None` | 字符集数据（SID/CID 映射） |
| `FontFace.cffEncoding` | `FontFace` | `list` 或 `None` | CFF 编码数据 |

### 4.3 新增内部类

| 类 | 位置 | 说明 |
|----|------|------|
| `CFFParser` | `openfonts/_cff.py` | CFF 表解析器，提取 CharStrings、FDSelect、FDArray 等 |
| `CFFSubsetter` | `openfonts/_cff.py` | CFF 子集生成器，从完整 CFF 中提取子集 |
| `PDFType1CFont` | `pdfdoc.py` | PDF Type1C 字体字典（Subtype = /Type1C） |

---

## 5. 实现细节

### 5.1 整体数据流

```
OTF 文件 (.otf)
  │
  ├── FontParser.readHeader()
  │     └── 检测 OTTO 版本 → self.isCFF = True
  │
  ├── FontFile.extractInfo()
  │     ├── 共享表解析（name, head, OS/2, post, hhea, hmtx, cmap）→ 直接复用
  │     ├── maxp → 分支处理（CFF 版本 0.5，仅读 numGlyphs）
  │     ├── loca → 跳过（CFF 无此表）
  │     └── CFF 表 → CFFParser 解析 CharStrings INDEX
  │
  ├── FontFile.makeSubset()
  │     ├── 共享表（name, OS/2, post, hhea, hmtx, cmap）→ 直接复用
  │     ├── maxp → 生成 6 字节 CFF maxp
  │     └── CFF 子集 → CFFSubsetter 生成
  │
  └── FontFace.addObjects() / addSubsetObjects()
        └── PDFType1CFont + FontFile3 (Type1C)
```

### 5.2 受影响的代码路径

| 位置 | 当前行为（TrueType） | 需要的变更（CFF） |
|------|---------------------|-------------------|
| `FontParser.readHeader()` | 拒绝 OTTO 版本 | 接受 OTTO，设置 `self.isCFF = True` |
| `FontFile.extractInfo()` maxp | 读取 32 字节 maxp，检查版本 1.0 | 分支处理：CFF maxp 仅 6 字节，版本 0.5 |
| `FontFile.extractInfo()` loca | 读取 loca 表 | CFF 无 loca 表，跳过；存储 CFF 偏移信息 |
| `FontFile.makeSubset()` | 复制 glyf，重建 loca，生成 TTF sfnt 流 | 生成 CFF 子集流 |
| `FontFace.addSubsetObjects()` | 使用 FontFile2 | 使用 FontFile3 + Subtype /Type1C |
| `OpenTypeFont.addObjects()` | 创建 PDFTrueTypeFont | 创建 PDFType1CFont |
| `FontMaker.makeStream()` | 生成 TTF sfnt 流 | CFF 字体输出 CFF 表数据（不需要 sfnt 包装） |

### 5.3 可复用的代码

以下代码对 TTF 和 OTF 字体完全通用，无需修改：

- `FontParser` 的所有二进制读取方法（`read_ushort`、`read_tag` 等）
- `cmap` 表解析
- `hmtx` 表解析
- `name` 表解析
- `head` 表解析
- `OS/2` 表解析
- `post` 表解析
- `hhea` 表解析
- `OpenTypeFont.State` 子集管理
- `OpenTypeFont.splitString()` Unicode 到子集的拆分
- `makeToUnicodeCMap()` PDF ToUnicode CMap 生成

### 5.4 各模块结构设计

#### `_common.py` — 公共定义

| 内容 | 说明 |
|------|------|
| `TTFError` | 异常类，继承 `pdfdoc.PDFError` |
| `SUBSETN()` | 子集命名辅助函数 |
| `makeToUnicodeCMap()` | ToUnicode CMap 生成 |
| `splice()` / `_set_ushort()` | 二进制操作辅助函数 |
| `GF_*` 常量 | glyf 复合字形标志 |

#### `_sfnt.py` — sfnt 二进制格式解析器

| 类/函数 | 说明 |
|--------|------|
| `FontParser` | sfnt 解析基类，所有二进制读取方法 |
| `_ttf_dirs()` | TTF 搜索路径辅助 |
| `TTFOpenFile()` | TTF 文件打开辅助 |

**关键修改**：`readHeader()` 检测 OTTO 版本时设置 `self.isCFF = True`

#### `_ttf.py` — TrueType 专用逻辑

| 类 | 说明 |
|----|------|
| `FontFile(FontParser)` | 字体文件解析 + 子集生成 |
| `FontMaker` | PDF 子集流生成器 |

**关键修改**：
- `extractInfo()` 中 maxp 分支处理 CFF 格式
- `extractInfo()` 中 loca 表跳过（CFF 无此表）
- `makeSubset()` 分派到 `_makeCFFSubset()` 或 `_makeTTFSubset()`

#### `_cff.py` — CFF 表解析与子集生成（新增）

| 类 | 说明 |
|----|------|
| `CFFParser` | 解析 CFF 表：Header、NAME INDEX、STRING INDEX、DICT INDEX、CharStrings INDEX、Charset、FDSelect、FDArray |
| `CFFSubsetter` | CFF 子集生成器 |

**CFFParser 核心属性**：
- `name` — PostScript 字体名
- `numGlyphs` — 字形数量
- `charStrings` — CharStrings 偏移列表
- `charset` — SIDs/CIDs 列表
- `isCID` — 是否 CID-keyed 字体

**CFFSubsetter 子集化步骤**：
1. 重建 CharStrings INDEX（仅所需字形）
2. 重建 Charset（子集映射）
3. 重建 FDSelect（CID 字体）
4. 过滤 Global/Local SUBR INDEX

#### `_face.py` — 字体面

| 类 | 说明 |
|----|------|
| `FontFace(FontFile, pdfmetrics.TypeFace)` | 字体面度量 + 子集对象 |

**关键修改**：`addSubsetObjects()` 根据 `isCFF` 选择 FontFile2（TTF）或 FontFile3/Type1C（CFF）

#### `_encoding.py` — 编码适配器

| 类 | 说明 |
|----|------|
| `FontEncoding` | UTF-8 编码适配器（简单封装） |

#### `_font.py` — 主用户类

| 类/属性 | 说明 |
|--------|------|
| `OpenTypeFont` | 主用户类，支持 TTF + OTF |
| `OpenTypeFont.State` | 子集状态管理 |
| `substitutionFonts` | Fallback 字体列表 |

**关键修改**：`addObjects()` 根据 `self.face.isCFF` 创建 `PDFType1CFont` 或 `PDFTrueTypeFont`

#### `_shaping.py` — 文本整形支持

| 类 | 说明 |
|----|------|
| `ShapeData` | 文本整形状态持有 |
| `ShapedFragWord(list)` | 词粒度整形片段列表 |
| `ShapedStr(str)` | 带整形信息的字符串 |

#### `pdfdoc.py` — 新增 `PDFType1CFont`

```python
class PDFType1CFont(PDFType1Font):
    Subtype = "Type1C"
```

### 5.5 包导出设计

#### `openfonts/__init__.py`

```python
"""OpenType font support (TTF + OTF/CFF).

This module provides the canonical font classes for OpenType fonts.
For backward compatibility, the old ttfonts module still works but is deprecated.

Example::
    from reportlab.pdfbase.openfonts import OpenTypeFont
    font = OpenTypeFont('MyFont', 'MyFont.otf')
    pdfmetrics.registerFont(font)
"""

from ._common import TTFError, SUBSETN, makeToUnicodeCMap, splice, _set_ushort
from ._sfnt import FontParser
from ._ttf import FontFile, FontMaker
from ._cff import CFFParser, CFFSubsetter
from ._face import FontFace
from ._encoding import FontEncoding
from ._font import OpenTypeFont

# 向后兼容别名（deprecated）
TTFont = OpenTypeFont
TTFontParser = FontParser
TTFontFile = FontFile
TTFontFace = FontFace
TTFontMaker = FontMaker
TTEncoding = FontEncoding

__all__ = [
    'OpenTypeFont', 'FontParser', 'FontFile', 'FontFace',
    'FontMaker', 'FontEncoding', 'CFFParser', 'CFFSubsetter',
    # 别名
    'TTFont', 'TTFontParser', 'TTFontFile', 'TTFontFace',
    'TTFontMaker', 'TTEncoding',
]
```

#### `ttfonts.py`（兼容层）

```python
"""Deprecated compatibility module.

.. deprecated::
    所有字体逻辑已迁移至 :mod:`reportlab.pdfbase.openfonts`。
    请使用::

        from reportlab.pdfbase.openfonts import OpenTypeFont

    本模块将在未来版本中移除。
"""
import warnings
warnings.warn(
    "ttfonts is deprecated; use openfonts instead",
    DeprecationWarning,
    stacklevel=2,
)

from reportlab.pdfbase.openfonts import (
    OpenTypeFont,
    FontParser,
    FontFile,
    FontFace,
    FontMaker,
    FontEncoding,
    CFFParser,
    CFFSubsetter,
)

TTFont = OpenTypeFont
TTFontParser = FontParser
TTFontFile = FontFile
TTFontFace = FontFace
TTFontMaker = FontMaker
TTEncoding = FontEncoding
```

---

## 6. PDF 语义正确性

### 6.1 PDF Type1C 字体嵌入

在 PDF 中，CFF 字体使用以下结构：

```
<< /Type /Font
   /Subtype /Type1C
   /BaseFont /FontName
   /FontDescriptor << /Type /FontDescriptor
                      /FontName /FontName
                      /FontFile3 5 0 R
                      ... >>
   /Widths [...] >>
```

FontFile3 流包含完整的 CFF 数据（或子集化的 CFF 数据）。
PDF 查看器通过 FontFile3 的 Subtype (/Type1C) 识别 CFF 格式。

### 6.2 子集独立性

与 TrueType 子集相同，CFF 子集也是按文档独立管理的。
每个 `OpenTypeFont` 实例通过 `WeakKeyDictionary` 维护每个文档的子集状态。

### 6.3 ToUnicode CMap

CFF 字体的 ToUnicode CMap 生成与 TrueType 完全相同——它是 PDF 层面的，
与字体轮廓格式无关。`makeToUnicodeCMap()` 直接复用。

---

## 7. 约束与性能

### 7.1 边界情况

| 场景 | 行为 |
|------|------|
| 加载 OTF 文件 | `isCFF = True`，走 CFF 解析路径 |
| 加载 TTF 文件 | `isCFF = False`，走现有 TrueType 路径（零回归） |
| OTF + TTFont fallback | 与 TTF 相同，通过 `substitutionFonts` 属性控制 |
| OTF + HarfBuzz shaping | 初始版本：CFF 字体不参与 HarfBuzz shaping（降级到无 shaping 路径） |
| CFF2 字体 | 拒绝（sfnt 版本不同），后续版本支持 |
| 可变字体 | 拒绝（需要 `fvar`/`gvar` 表解析），后续版本支持 |
| CID-keyed OTF | 支持（通过 FDArray/FDSelect 解析） |
| 非标准 CFF 表 | 尽量容错，解析失败时抛出明确的 TTFError |
| 空字体（0 字形） | 拒绝 |
| CFF subroutinization | 子集化时保留被引用的 subroutines |

### 7.2 性能分析

#### 解析开销

CFF 表通常比 TrueType 的 glyf+loca 表大（因为包含完整的 CharStrings + hints）。
例如 `SourceHanSansK-Light.otf` 的 CFF 表为 15.5MB。

初始版本采用全量解析策略（读取整个 CFF 表到内存），后续可优化为惰性解析。

#### 子集化开销

CFF 子集化比 TrueType 更复杂（需要重建 CharStrings INDEX、SUBR 等），
但对于典型文档（几十到几百个字符），开销是可接受的。

#### PDF 文件大小

CFF 字体嵌入通常比 TrueType 更小（CFF 压缩效率更高），
但初始版本不实现 CFF 子集压缩（直接嵌入子集化的 CFF 数据）。

---

## 8. 测试计划

### 8.1 测试文件结构

```
tests/
├── test_otf_loading.py           # OTF/TTF 字体加载
├── test_otf_metrics.py           # 字体验证（glyph count、bbox 等）
├── test_otf_subsetting.py        # 子集化测试
├── test_otf_rendering.py         # PDF 渲染（生成实际 PDF 文件）
├── test_otf_asian.py             # 亚洲 CJK 文本渲染
├── test_otf_fallback.py          # OTF + TTF 混合 fallback
└── pdf-out/                      # PDF 输出目录
    ├── test_otf_rendering.pdf
    ├── test_otf_asian.pdf
    └── test_otf_fallback.pdf
```

**说明**：
- 外部字体存放在 `tests_resource/` 目录（详见 `tests_resource/README.md`）
- 字体缺失时，相关测试自动跳过（SKIP），不影响其他测试
- 测试使用 `makeSuite()` 模式，遵循 `tests/runAll.py` 发现机制

### 8.2 测试用例概要

| 文件 | 测试数 | 主要内容 |
|------|--------|---------|
| `test_otf_loading.py` | 4 | 加载验证、度量、宽度、cmap |
| `test_otf_metrics.py` | 2 | 字形数量、PostScript 名称 |
| `test_otf_subsetting.py` | 3 | glyph 映射、CharStrings、子集大小 |
| `test_otf_rendering.py` | 3 | PDF 生成、FontFile3、Type1C 子类型 |
| `test_otf_asian.py` | 2 | CJK 渲染、Unicode 范围 |
| `test_otf_fallback.py` | 4 | OTF fallback、宽度计算、混合字体 |

### 8.3 回归测试

在现有测试文件末尾追加（不新建文件）：

```python
# tests/test_pdfbase_ttfonts.py 末尾追加
def test_ttf_still_works(self):
    """确保 TrueType 字体不受影响"""
    font = TTFont('Test', 'some.ttf')
    assert font.face.isCFF == False

# tests/test_ttfont_fallback_api.py 末尾追加
def test_otf_alias_works(self):
    """确保 TTFont 别名仍可用"""
    from reportlab.pdfbase.openfonts import TTFont as OTFont
    font = OTFont('Test', 'test.otf')
    assert isinstance(font, OTFont)
```

### 8.4 测试数据

字体文件存放在 `tests_resource/` 目录，从 https://reportlab-enhanced.tain.one/test-resource.zip 下载。

| 字体 | 用途 |
|------|------|
| `SourceHanSansK-Light.otf` | OTF 测试主字体 |
| `NotoSansCJKsc-Regular.otf` | CJK fallback 测试 |
| `DejaVuSans.ttf` | TTF fallback 测试 |

---

## 9. 实施顺序

1. **创建 `openfonts/` 包目录**
2. **创建 `_common.py`**：迁移 `TTFError`、`SUBSETN`、辅助函数、常量
3. **创建 `_sfnt.py`**：迁移 `FontParser`，修改 `readHeader()` 接受 OTTO
4. **创建 `_ttf.py`**：迁移 `FontFile`、`FontMaker`，修改 `extractInfo()` 的 maxp/loca 分支
5. **创建 `_cff.py`**：新增 `CFFParser`、`CFFSubsetter` 类
6. **创建 `_face.py`**：迁移 `FontFace`，修改 `addSubsetObjects()` 支持 CFF
7. **创建 `_encoding.py`**：迁移 `FontEncoding`
8. **创建 `_font.py`**：迁移 `OpenTypeFont`，修改 `addObjects()` 支持 CFF
9. **创建 `_shaping.py`**：迁移 `ShapedFragWord`、`ShapedStr`
10. **创建 `__init__.py`**：包入口，导出主类 + 向后兼容别名
11. **改造 `ttfonts.py`** 为纯兼容层（导入重导出 + DeprecationWarning）
12. **新增 `pdfdoc.PDFType1CFont`** 类
13. **更新内部引用** 为 `openfonts`（`pdfmetrics.py` 等核心文件）
14. **渐进式更新** 测试文件和文档中的引用（别名保证兼容）

别名机制确保任何未更新的代码继续正常运行，DeprecationWarning 引导用户迁移。

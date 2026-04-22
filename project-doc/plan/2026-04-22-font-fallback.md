# ReportLab TrueType Font Fallback 设计方案

## 1. 概述

### 1.1 背景

ReportLab 当前的字体体系中，Type1（单字节）字体已具备基本的 fallback 机制：
通过 `unicode2T1()` 函数和 `Font.substitutionFonts` 属性，在主字体无法编码某字符时，
自动尝试替换字体列表中的其他字体。

然而，TrueType（TTFont）字体——当前最常用的字体类型——**尚无任何 fallback 支持**。
当 TTFont 遇到不包含的字形时，`splitString()` 方法直接将其映射到 glyph 0（`.notdef`），
导致 PDF 中出现方框或空白。

### 1.2 目标

为 TTFont 增加自动字体 fallback 支持，使得：
- 当主字体缺少某字形时，自动从 `substitutionFonts` 列表中查找包含该字形的字体
- 文本渲染、宽度计算、图形路径生成等场景均一致处理 fallback
- 与现有 Type1 fallback 机制保持 API 一致性
- 对无 fallback 配置的场景零开销

### 1.3 实验性功能声明

TTFont fallback 是一项**实验性功能**。为确保向后兼容并便于性能对比：

- **默认关闭**：即使设置了 `substitutionFonts`，在未显式启用的情况下，fallback 逻辑不会被触发
- 所有 TTFont 渲染路径保持与旧版完全一致的行为
- 启用后可进行 A/B 性能对比测试
- 功能稳定后将移除此开关，变为默认启用

### 1.4 不在范围内

- CID/CJK 字体的 fallback（CID 字体使用完全不同的编码模型）
- HarfBuzz 排版文本的跨字体 shaping（需 HarfBuzz 本身支持 font callback）
- 从字体文件自动推断 fallback 关系

---

## 2. 功能开关设计

### 2.1 环境变量控制

TTFont fallback 功能通过环境变量 `REPORTLAB_FONT_FALLBACK` 控制：

| 环境变量 | 值 | 行为 |
|----------|-----|------|
| `REPORTLAB_FONT_FALLBACK` | 未设置 / `0` | **默认**。所有 TTFont fallback 逻辑被跳过，行为与旧版完全一致 |
| `REPORTLAB_FONT_FALLBACK` | `1` | 启用 TTFont fallback。设置 `substitutionFonts` 的字体会执行 fallback 查找 |

**启用方式**：

```bash
# 运行时启用
REPORTLAB_FONT_FALLBACK=1 python your_script.py

# 或在代码中设置（任意时刻均可生效，getter 每次实时读取环境变量）
import os
os.environ['REPORTLAB_FONT_FALLBACK'] = '1'
```

### 2.2 单一根部控制点：`TTFont.substitutionFonts` property

**核心思路**：将 `TTFont.substitutionFonts` 从普通实例属性改为 property。
环境变量的判断集中在 property getter 中（每次调用时实时读取 `os.environ`），**下游所有代码无需感知开关的存在**。

```python
# ttfonts.py 中 TTFont 类
import os

class TTFont:
    ...
    @property
    def substitutionFonts(self):
        if os.environ.get('REPORTLAB_FONT_FALLBACK', '0') != '1':
            return []             # 开关关闭 → 返回空列表 → 下游走原有快速路径
        return self._substitutionFonts

    @substitutionFonts.setter
    def substitutionFonts(self, value):
        self._substitutionFonts = value
    ...
```

**效果**：
- 环境变量未设置或为 `0` 时，`font.substitutionFonts` 姯终返回 `[]`
- 下游代码（`_formatText`、`instanceStringWidthTTF`、`text2PathDescription`）中的 `if font.substitutionFonts:` 判断自然为 `False`，走原有快速路径
- 开关关闭时**零开销**：一次 `os.environ.get` + 一次字符串比较 + 返回空列表
- 开关开启时，`_substitutionFonts` 中存储的值正常返回
- **下游代码不需要任何额外的环境变量检查**，保持原来的 `getattr(font, 'substitutionFonts', None)` 写法即可
- **环境变量可在运行时任意时刻设置**：每次 property getter 调用时实时读取 `os.environ`，无需在 import 之前设置

### 2.3 性能对比方案

开关机制支持以下性能对比场景：

```bash
# 基准：关闭 fallback（旧版行为）
time python benchmark.py  # REPORTLAB_FONT_FALLBACK 未设置

# 实验：开启 fallback
REPORTLAB_FONT_FALLBACK=1 time python benchmark.py
```

建议的基准测试维度：
- 纯 ASCII 文本渲染（验证无回归）
- 混合脚本文本渲染（测量 fallback 开销）
- 大文档 PDF 生成（段落密集场景）
- PDF 文件体积对比（fallback 字体子集嵌入的增量）

---

## 3. 现有架构分析

### 3.1 字体类型与 fallback 现状

| 字体类型 | 类 | `_dynamicFont` | `_multiByte` | 当前 fallback |
|----------|-----|----------------|-------------|--------------|
| 标准14种 Type1 | `pdfmetrics.Font` | 0 | 0 | 通过 `unicode2T1` + `substitutionFonts` |
| 嵌入 Type1 | `pdfmetrics.Font` | 0 | 0 | 同上 |
| TrueType | `ttfonts.TTFont` | 1 | 1 | **无**（缺失字形映射为 glyph 0） |
| CID/CJK | `cidfonts.CIDFont` | 0 | 1 | `substitutionFonts = []`（空） |

### 3.2 Type1 fallback 工作原理

Type1 的 fallback 由两部分协作完成：

1. **`unicode2T1(utext, fonts)`**（`rl_accel.py`）：将文本按字体编码能力拆分为 `(font, bytes)` 对。
   尝试将文本编码到目标字体的编码，编码失败时截取失败片段递归尝试下一个字体。

2. **`_formatText`**（`textobject.py`）：遍历 `unicode2T1` 返回的 `(font, text)` 对，
   在 PDF 内容流中通过 `Tf` 操作符切换字体并输出文本。

### 3.3 TTFont 缺失字形处理

`splitString()`（`ttfonts.py:1253`）在 `charToGlyph` 字典中找不到码点时，
将其映射为 glyph 0（`.notdef`），无任何 fallback 尝试。

`instanceStringWidthTTF`（`rl_accel.py`）对缺失字形使用 `defaultWidth`，
不考虑 fallback 字体的宽度。

### 3.4 图形路径中的字体使用

`graphics/utils.py` 中 `text2PathDescription` 对动态字体（TTFont）直接调用
`gs._text2Path(text, ...)`，无 fallback；对 Type1 字体使用 `unicode2T1` 并逐字体绘制。

`graphics/renderPM.py` 和 `graphics/renderPS.py` 同样只在 Type1 路径中使用 `unicode2T1`。

---

## 4. 公开 API 设计

### 4.1 新增属性：`TTFont.substitutionFonts`

与 Type1 字体的 `Font.substitutionFonts` 保持一致。
实现为 property，内含环境变量开关判断作为**唯一的根部控制点**：

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `TTFont.substitutionFonts` | `list[TTFont]` | `[]` | Fallback 字体列表。主字体无法渲染的字符将按列表顺序查找第一个包含该字形的字体 |

**开关行为**（由 property getter 内部控制，下游无感知）：

| `REPORTLAB_FONT_FALLBACK` | `font.substitutionFonts` 返回值 | 下游行为 |
|---------------------------|----------------------------------|---------|
| 未设置 / `0` | `[]`（即使内部已设置值） | 走原有快速路径，与旧版完全一致 |
| `1` | 实际设置的 fallback 列表 | 执行 fallback 查找 |

**设置方式**：直接赋值，无需额外注册步骤。赋值始终成功（写入内部存储），是否生效取决于环境变量。

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font = TTFont('NotoSans', 'NotoSans-Regular.ttf')
fallback = TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')
pdfmetrics.registerFont(font)
pdfmetrics.registerFont(fallback)

font.substitutionFonts = [fallback]
```

**行为规则**：
- 列表中可以包含多个字体，按顺序查找第一个包含目标字形的字体
- 环境变量 `REPORTLAB_FONT_FALLBACK=1` 未设置时，getter 返回 `[]`，fallback 不生效
- 环境变量开启时，getter 返回实际列表，fallback 正常工作
- 初始版本仅支持 TTFont → TTFont 的 fallback；Type1 字体在 `unicode2TT` 中无 `charToGlyph`，不会被选中
- 下游代码只需 `if font.substitutionFonts:` 即可，无需感知环境变量

### 4.2 新增方法：`TTFont.hasGlyph(char_or_code)`

| 签名 | 返回值 | 说明 |
|------|--------|------|
| `hasGlyph(char_or_code)` | `bool` | 检查字体是否包含指定字符的字形 |

**参数**：
- `char_or_code`：单字符字符串（如 `'A'`）或 Unicode 码点整数（如 `0x4F60`）

**行为**：
- `U+00A0`（nbsp）被视为 `U+0020`（space），与 `splitString` 一致
- 通过检查 `face.charToGlyph` 字典判断字形存在性

```python
font = TTFont('Vera', 'Vera.ttf')
font.hasGlyph('A')        # True
font.hasGlyph(ord('A'))   # True
font.hasGlyph(0x4F60)     # False（CJK 字符不在 Vera 中）
```

### 4.3 新增便利函数：`pdfmetrics.registerFontWithFallback()`

| 签名 | 返回值 | 说明 |
|------|--------|------|
| `registerFontWithFallback(name, filename, fallbackFonts=None, **kwargs)` | `TTFont` | 注册 TTFont 并同时设置 fallback 字体 |

**参数**：
- `name`：字体名称（同 `TTFont` 构造函数）
- `filename`：字体文件路径（同 `TTFont` 构造函数）
- `fallbackFonts`：fallback 字体列表。元素可以是：
  - 字体名称字符串（需已通过 `registerFont` 注册）
  - `TTFont` 实例（将自动注册）
- `**kwargs`：传递给 `TTFont` 构造函数的额外参数（如 `subfontIndex`、`shapable` 等）

```python
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf'))

font = pdfmetrics.registerFontWithFallback(
    'NotoSans', 'NotoSans-Regular.ttf',
    fallbackFonts=['NotoSansCJK']
)
```

或直接传入 TTFont 实例：

```python
font = pdfmetrics.registerFontWithFallback(
    'NotoSans', 'NotoSans-Regular.ttf',
    fallbackFonts=[TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')]
)
```

### 4.4 新增配置项：`defaultTTFFallbackFonts`

| 配置项 | 位置 | 默认值 | 说明 |
|--------|------|--------|------|
| `defaultTTFFallbackFonts` | `rl_settings.py` | `[]` | 全局默认 TTF fallback 字体名称列表 |

- 列表中的字体名称需预先通过 `pdfmetrics.registerFont` 注册
- 可通过 `reportlab_settings.py` 或 `~/.reportlab_settings` 覆盖
- 示例配置：`defaultTTFFallbackFonts = ['NotoSansCJK', 'Symbol']`

**注意**：此配置项定义在 `rl_settings.py` 中，`rl_config.py` 的 `_setOpt` 机制会自动处理，
无需修改 `rl_config.py`。

**与 property 的关系**：`defaultTTFFallbackFonts` 定义了全局默认值。在 TTFont 注册后
（例如在 `registerFontWithFallback` 内部），自动将其赋值给 `font.substitutionFonts`。
赋值走 property setter，写入 `_substitutionFonts`；是否生效仍取决于环境变量控制的 getter。

### 4.5 新增内部函数：`unicode2TT(utext, fonts)`

| 签名 | 返回值 | 说明 |
|------|--------|------|
| `unicode2TT(utext, fonts)` | `list[tuple[TTFont, str]]` | 将 Unicode 文本按字形可用性拆分到多个 TTFont |

**参数**：
- `utext`：Unicode 字符串
- `fonts`：TTFont 列表，第一个为主字体，其余为 fallback 字体

**返回值**：`(TTFont, str)` 元组列表，每个元组表示该字体可以渲染的连续字符片段。
连续命中同一字体的字符会被合并为一个片段，以最小化 PDF 中字体切换次数。

**算法**：对每个字符，按 `fonts` 列表顺序查找第一个包含该字形的字体（通过 `charToGlyph` 检查）。
若所有字体均不包含该字符，回退到主字体（将产生 `.notdef`）。

**与 `splitString` 的关系**：`unicode2TT` 返回的 `str` 片段需要再传入对应字体的 `splitString` 方法
才能获得 PDF 可用的 `(subset, bytes)` 对。这是一个两步流程：
1. `unicode2TT` 按**字形可用性**拆分文本（返回 `(TTFont, str)` 对）
2. 每个 `str` 片段传入对应 `TTFont.splitString` 按**子集编码**拆分（返回 `(subset, bytes)` 对）

> 此函数为内部使用，导出自 `reportlab.lib.rl_accel`。
> 用户通常不需要直接调用，而是通过设置 `substitutionFonts` 属性间接触发。

### 4.6 API 与现有 Type1 fallback 的一致性

| 方面 | Type1 (现有) | TTFont (新增) |
|------|-------------|---------------|
| Fallback 属性 | `Font.substitutionFonts` | `TTFont.substitutionFonts`（property，getter 内实时检查环境变量） |
| 拆分函数 | `unicode2T1(text, fonts)` | `unicode2TT(text, fonts)` |
| 返回类型 | `list[tuple[Font, bytes]]` | `list[tuple[TTFont, str]]` |
| 宽度计算 | `instanceStringWidthT1` 使用 `unicode2T1` | `instanceStringWidthTTF` 使用 `unicode2TT` |
| 渲染路径 | `_formatText` 遍历 `(font, bytes)` 对 | `_formatText` 遍历 `(font, str)` 对 |
| 图形路径 | `text2PathDescription` 使用 `unicode2T1` | `text2PathDescription` 使用 `unicode2TT`（freetype 和 _renderPM 两个后端均需修改） |
| 渲染器 | `renderPM`/`renderPS` 使用 `unicode2T1` | `renderPM`/`renderPS` 使用 `unicode2TT` |
| 默认 fallback | `[Symbol, ZapfDingbats]`（内置字体） | `[]`（需用户手动配置） |

---

## 5. 详细设计

### 5.1 整体架构

新增 `unicode2TT()` 函数作为 TTFont fallback 的核心分发器，
与 `unicode2T1()` 平行存在，负责将文本拆分为 `(font, substring)` 对。

**数据流**：

```
文本输入
  │
  ├── TTFont（_dynamicFont=True）
  │     │
  │     ├── font.substitutionFonts 为空？（property getter 已处理环境变量）
  │     │     ├── 是 → 走原有 splitString 路径（零开销）
  │     │     └── 否 → unicode2TT(text, [font] + substitutionFonts)
  │     │                 逐字符检查 charToGlyph，分组为 (font, text) 对
  │     │                 每个 (font, text) 对各自走 splitString 渲染
  │     │
  │     ├── stringWidth 同理使用 unicode2TT 计算宽度
  │     │
  │     └── 图形路径（text2PathDescription / renderPM / renderPS）
  │           同样使用 unicode2TT 拆分，逐段调用各渲染后端
  │
  ├── Type1（现有逻辑不变）
  │     └── unicode2T1(text, [font] + substitutionFonts)
  │
  └── CID（不在本次范围）
```

### 5.2 受影响模块清单

| 文件 | 修改类型 | 修改内容摘要 |
|------|---------|-------------|
| `src/reportlab/lib/rl_accel.py` | 修改 + 新增 | `__all__` 添加 `unicode2TT`；新增 `_py_unicode2TT` 函数；修改 `_py_instanceStringWidthTTF` 支持 fallback |
| `src/reportlab/pdfbase/ttfonts.py` | 修改 | `TTFont.__init__` 添加 `self._substitutionFonts = []`；将 `substitutionFonts` 改为 property（含环境变量判断，为唯一根部控制点）；新增 `hasGlyph` 方法 |
| `src/reportlab/pdfgen/textobject.py` | 修改 | `_formatText` TTFont 分支添加 fallback 拆分与字体切换逻辑 |
| `src/reportlab/pdfbase/pdfmetrics.py` | 新增 | `registerFontWithFallback` 便利函数 |
| `src/reportlab/graphics/utils.py` | 修改 | `text2PathDescription` 的 freetype 路径和 `_renderPM` 路径均添加 fallback 逻辑 |
| `src/reportlab/graphics/renderPM.py` | 修改 | `drawString` 的 TTFont 分支添加 fallback 拆分与字体切换逻辑 |
| `src/reportlab/graphics/renderPS.py` | 修改 | PostScript 渲染器的 TTFont 分支添加 fallback 拆分逻辑 |
| `src/reportlab/rl_settings.py` | 修改 | `__all__` 添加 `'defaultTTFFallbackFonts'`；新增 `defaultTTFFallbackFonts = []` |
| `src/reportlab/rl_config.py` | 无需修改 | `_setOpt` 机制自动处理新配置项 |

### 5.3 源码修改说明

以下仅说明各模块的修改要点，不列出完整源码。具体实现时参照此说明进行修改。

#### 5.3.1 `rl_accel.py` 修改要点

1. **`__all__`** 中添加 `'unicode2TT'`
2. **新增 `_py_unicode2TT(utext, fonts)`**：按 `_py_funcs` 模式定义（`if 'unicode2TT' in _py_funcs:`），遵循 rl_accel 的纯 Python 实现约定。算法：预构建 `(font, charToGlyph)` 列表，逐字符扫描，按字体分组，nbsp → space
3. **修改 `_py_instanceStringWidthTTF`**：在原有快速路径前插入 `getattr(self, 'substitutionFonts', None)` 检查。有 fallback 时调用 `_py_unicode2TT` 按字体分段累加宽度。无需额外判断环境变量——`TTFont.substitutionFonts` property 已在根部处理
4. **纯 Python 环境**：本项目自 v4.0 起无 C 扩展，`_rl_accel` C 模块不可用时自动使用 Python 实现，无需额外兼容处理

#### 5.3.2 `ttfonts.py` 修改要点

1. **`TTFont.__init__`** 末尾添加 `self._substitutionFonts = []`（注意是带下划线的内部存储）
2. **将 `substitutionFonts` 改为 property**：getter 中每次调用时实时检查 `os.environ.get('REPORTLAB_FONT_FALLBACK', '0') != '1'`，关闭时返回 `[]`，开启时返回 `self._substitutionFonts`；setter 写入 `self._substitutionFonts`。此为**唯一的开关控制点**，下游所有代码无需感知环境变量。每次 getter 调用读取 `os.environ` 而非使用类级常量，确保运行时修改环境变量立即生效
3. **新增 `hasGlyph(char_or_code)` 方法**：接受 str 或 int，nbsp → space，返回 `code in self.face.charToGlyph`

#### 5.3.3 `textobject.py` 修改要点

`_formatText` 中 TTFont（`font._dynamicFont`）路径包含三层分支：
1. HarfBuzz 路径（`font.shapable and isinstance(text, ShapedStr)`）：调用 `splitString` 处理 shaped 文本（第 582-630 行）
2. 普通 TTFont 路径（第 632 行的 `else`）：调用 `splitString` 处理普通文本
3. 非 dynamicFont 路径：`_multiByte` 和 Type1（不在本次范围）

**修改位置**：在**普通 TTFont 路径**（第 632 行）前插入 fallback 逻辑。

1. **`_formatText` 普通 TTFont 路径**：在现有 `for subset, t in font.splitString(...)`（第 632 行）前增加 `getattr(font, 'substitutionFonts', None)` 判断。无需额外判断环境变量——`TTFont.substitutionFonts` property 已在根部处理。有 fallback 时：
   - 调用 `unicode2TT(text, [font] + font.substitutionFonts)` 将文本拆分为 `(TTFont, str)` 对
   - 遍历每个 `(fbFont, fbText)` 对：调用 `fbFont.splitString(fbText, canv._doc)` 获取 `(subset, bytes)` 对
   - 当 `fbFont` 与当前字体不同时，发出 `Tf` 操作符切换字体（与 Type1 fallback 第 658-664 行的模式一致，使用局部变量跟踪当前字体，无需新增实例变量）
   - 在所有 fallback 片段处理完毕后，恢复为主字体
2. **HarfBuzz 路径**：若检测到 `substitutionFonts` 非空且文本为 `ShapedStr`，打印 warning 并按无 shaping 处理（降级到普通 TTFont 路径，详见 §5.4）
3. **导入 `unicode2TT`**：采用惰性导入（在 `_formatText` 内部 import），避免循环依赖
4. **无需新增 `_curFontObj` 实例变量**：与 Type1 fallback 一致，使用局部变量跟踪当前渲染字体即可

#### 5.3.4 `graphics/utils.py` 修改要点

`text2PathDescription` 函数根据 `rl_config.textPaths` 配置选择后端，
两个后端分别由 `__makeTextPathsCode__()` 中不同的条件分支生成：
- **freetype 后端**（第 62-194 行）：`font._dynamicFont` 时直接调用 `gs._text2Path(text, ...)`
- **_renderPM 后端**（第 195-272 行）：`font._dynamicFont` 时调用 `gs._stringPath(text, x, y)` 逐字形处理

两个后端的 `font._dynamicFont` 分支均需添加 fallback 逻辑：
1. 检查 `getattr(font, 'substitutionFonts', None)` 是否非空
2. 有 fallback 时调用 `unicode2TT` 按字体拆分文本
3. 对每个 `(fbFont, fbText)` 片段：
   - freetype 后端：逐段调用 `gs._text2Path(fbText, ...)` 并累加 x 偏移
   - _renderPM 后端：逐段调用 `gs._stringPath(fbText, x, y)` 并累加 x 偏移
4. Fallback 字体为 TTFont（`_dynamicFont=1`），同样满足 `not (font._multiByte and not font._dynamicFont)` 条件，不会触发 ValueError

#### 5.3.5 `graphics/renderPM.py` 修改要点

`drawString` 方法（第 572-594 行）对 TTFont 直接调用 `gs.drawString(x, y, text)`，
对 Type1 使用 `unicode2T1` 做 fallback。需为 TTFont 分支添加类似的 fallback 逻辑：
1. 检查 `getattr(font, 'substitutionFonts', None)` 是否非空
2. 有 fallback 时调用 `unicode2TT` 拆分文本
3. 遍历每个 `(fbFont, fbText)` 片段，使用 `gs.drawString` 渲染并累加 x 偏移
4. 字体切换时需通过 `_setFont(gs, fbFont.fontName, fontSize)` 切换渲染状态

#### 5.3.6 `graphics/renderPS.py` 修改要点

PostScript 渲染器中 `_dynamicFont` 分支（第 321-324 行）直接调用 `self._textOut(x, y, s)`，
无 fallback。需添加与 renderPM 类似的 fallback 逻辑：
1. 检查 `getattr(font, 'substitutionFonts', None)` 是否非空
2. 有 fallback 时调用 `unicode2TT` 拆分文本
3. 遍历每个 `(fbFont, fbText)` 片段，切换 PS 字体并渲染，累加 x 偏移

#### 5.3.7 `pdfmetrics.py` 新增要点

在 `registerFont` 函数之后添加 `registerFontWithFallback` 函数。
接受 `fallbackFonts` 参数（str 或 TTFont 实例的列表），自动处理注册和赋值。

#### 5.3.8 `rl_settings.py` 修改要点

在 `__all__` 元组中添加 `'defaultTTFFallbackFonts'`，在设置区域添加 `defaultTTFFallbackFonts = []`。

### 5.4 HarfBuzz 排版文本处理

对于 HarfBuzz 排版文本（`_shapedTextOut` 分支），初始版本暂不支持跨字体 fallback。
若检测到 `substitutionFonts` 非空且文本为 `ShapedStr`，打印 warning 并按无 shaping 处理。
此部分作为后续增强。

---

## 6. PDF 语义正确性分析

### 6.1 字体切换在 PDF 中的表示

在 PDF 内容流中，字体切换通过 `Tf` 操作符实现：

```
/F1+0 12 Tf          % 设置字体为 F1 子集 0，字号 12
(Hello) Tj           % 输出 "Hello"
/F2+0 12 Tf          % 切换到 F2 子集 0
(你好) Tj            % 输出 "你好"
```

这与现有 Type1 fallback 的行为一致，PDF 规范完全支持。

### 6.2 子集独立性

每个 TTFont 实例独立维护自己的子集状态（通过 `WeakKeyDictionary` 以文档为 key）。
Fallback 到另一个 TTFont 时，该字体同样独立管理子集。不存在子集编号冲突问题。

**注意**：在 `_formatText` 中调用 `fbFont.getSubsetInternalName(subset, canv._doc)` 时，
需确保 fallback 字体已通过 `pdfmetrics.registerFont` 注册。`getSubsetInternalName` 内部
会调用 `doc.getInternalFontName`，该函数依赖字体已注册到文档的字体资源字典中。
`registerFont` 在注册时已将字体添加到 `_fonts` 字典，后续在 `addObjects` 阶段
会自动处理子集嵌入，无需额外操作。

### 6.3 ToUnicode CMap

每个 TTFont 子集在 `addObjects` 时独立生成 `ToUnicode` CMap，用于 PDF 查看器
将子集编码映射回 Unicode。Fallback 字体的 CMap 与主字体互不干扰。

### 6.4 字体描述符

每个 TTFont 子集生成独立的 `FontDescriptor` 和 `FontFile2`（嵌入的 TTF 子集）。
Fallback 字体将增加额外的 `FontDescriptor` 对象，PDF 文件会相应增大。

---

## 7. 边界情况与约束

| 场景 | 行为 |
|------|------|
| 字形不存在于任何字体 | 使用主字体渲染（产生 `.notdef`），与当前行为一致 |
| nbsp (U+00A0) | 映射为 U+0020（空格），与 `splitString` 一致 |
| 空文本 | `unicode2TT("")` 返回 `[]`，不产生任何输出 |
| 全部字符在主字体中 | `unicode2TT` 返回单个 `(font, text)` 对，行为与无 fallback 一致 |
| substitutionFonts 为空 | 走原有快速路径，零额外开销（property getter 一次 `os.environ.get` + 一次字符串比较） |
| substitutionFonts 含非 TTFont | Type1 字体无 `face.charToGlyph`，不会被 `unicode2TT` 选中。初始版本建议仅用 TTFont |
| 多文档并行使用 | `TTFont.state` 使用 `WeakKeyDictionary`，同一实例可在不同文档间安全使用 |
| 字体冻结（frozen） | 冻结发生在 `addObjects`（文档保存时），在 `_formatText`（渲染时）之后，无时序问题 |
| 段落布局 | 修改后的 `instanceStringWidthTTF` 在有 fallback 时考虑 fallback 字体宽度，段落布局正确处理混合脚本 |

---

## 8. 性能分析

### 8.1 无 fallback 场景

通过 `TTFont.substitutionFonts` property getter 的环境变量判断，
关闭时返回 `[]`，下游 `if font.substitutionFonts:` 为 `False`，走原有快速路径。
额外开销：property getter 中一次 `os.environ.get` + 一次字符串比较。可忽略。

### 8.2 有 fallback 场景

`unicode2TT` 对每个字符执行：
- 一次 `ord()` 调用
- 最多 N 次 `in dict` 操作（N = 字体数量）

对于典型的 2-3 个 fallback 字体，字符处理开销约为原始 `splitString` 的 2-3 倍。
考虑到文本渲染不是 PDF 生成的瓶颈（段落布局才是），这个开销是可接受的。

### 8.3 优化空间（后续）

- 缓存字形查找结果：`{code: font}` 字典，避免重复查找
- 批量预检查：对常用字符范围（如 ASCII）直接判定在主字体中
- 缓存 `os.environ.get` 结果：若环境变量在运行时不变，可缓存以避免重复字典查找（权衡：丧失运行时切换能力）

---

## 9. 测试计划

### 9.1 新增测试文件

**文件**：`tests/test_pdfbase_ttfont_fallback.py`

### 9.2 测试用例

#### 9.2.1 单元测试

**环境变量测试说明**：由于 `TTFont.substitutionFonts` property getter 每次调用时实时读取
`os.environ`（而非使用类级常量），测试可直接在用例中 `os.environ[...] = ...` 修改环境变量，
无需重新加载模块。每个测试用例应在 `setUp`/`tearDown` 中保存和恢复原始环境变量值。

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T01 | `test_unicode2TT_basic` | 基本文本拆分 | 纯 ASCII 文本返回 `[(font, text)]` |
| T02 | `test_unicode2TT_fallback` | 混合脚本文本 | 拆分为多个 `(font, text)` 对 |
| T03 | `test_unicode2TT_all_missing` | 所有字体均无字形 | 回退到主字体 |
| T04 | `test_unicode2TT_empty_text` | 空文本 | 返回 `[]` |
| T05 | `test_unicode2TT_nbsp` | 包含 nbsp 的文本 | nbsp 被映射为空格 |
| T06 | `test_unicode2TT_consecutive` | 连续同字体字符 | 合并为单个片段 |
| T07 | `test_unicode2TT_alternating` | 交替字体字符 | 每个字符独立片段 |
| T08 | `test_hasGlyph` | TTFont.hasGlyph 方法 | 对存在/不存在的字符返回正确 bool |
| T09 | `test_fallback_disabled_by_default` | 环境变量未设置 | 设置 substitutionFonts 后 getter 仍返回 `[]`，fallback 不生效 |
| T10 | `test_fallback_enabled_by_env` | 环境变量设置为 1 | 在运行时设置 `os.environ['REPORTLAB_FONT_FALLBACK'] = '1'` 后 getter 返回实际列表；清除环境变量后 getter 又返回 `[]` |
| T11 | `test_fallback_runtime_toggle` | 运行时切换环境变量 | 同一 TTFont 实例在环境变量切换后行为随之改变，无需重新加载模块 |

#### 9.2.2 宽度计算测试

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T12 | `test_stringWidth_no_fallback` | 无 fallback 的宽度 | 与原始实现结果一致 |
| T13 | `test_stringWidth_with_fallback` | 有 fallback 的宽度 | 宽度 = 主字体宽度 + fallback 字体宽度之和 |
| T14 | `test_stringWidth_consistency` | 宽度与渲染一致性 | `stringWidth` 结果 = 实际渲染宽度 |

#### 9.2.3 PDF 生成测试

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T20 | `test_fallback_pdf_basic` | 基础 fallback PDF | PDF 文件可正常生成和打开 |
| T21 | `test_fallback_pdf_mixed` | 混合脚本 PDF | 中英文混排正确渲染 |
| T22 | `test_fallback_pdf_all_in_main` | 所有字符在主字体中 | 行为与无 fallback 一致 |
| T23 | `test_fallback_pdf_all_in_fallback` | 所有字符在 fallback 中 | fallback 字体正确使用 |
| T24 | `test_fallback_no_substitution` | substitutionFonts 为空 | 走原有路径，无回归 |

#### 9.2.4 图形路径测试

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T30 | `test_text2Path_fallback` | 带 fallback 的文本路径 | 路径生成无异常 |
| T31 | `test_text2Path_no_fallback` | 无 fallback 的文本路径 | 与原始结果一致 |

#### 9.2.5 renderPM/renderPS 测试

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T35 | `test_renderPM_drawString_fallback` | renderPM 带 fallback 的 drawString | 渲染无异常，文本位置正确 |
| T36 | `test_renderPS_drawString_fallback` | renderPS 带 fallback 的文本输出 | PS 输出中包含正确的字体切换 |

#### 9.2.6 API 测试

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T32 | `test_registerFontWithFallback` | 便利函数注册 | 返回 TTFont 实例且 substitutionFonts 已设置 |
| T33 | `test_registerFontWithFallback_by_name` | 通过名称指定 fallback | 查找已注册字体 |
| T34 | `test_registerFontWithFallback_by_instance` | 通过实例指定 fallback | 自动注册并设置 |

#### 9.2.7 回归测试

| 编号 | 测试名称 | 描述 | 验证内容 |
|------|---------|------|---------|
| T40 | `test_existing_ttfont_tests_pass` | 现有 TTFont 测试全部通过 | `test_pdfbase_ttfonts.py` 无回归 |
| T41 | `test_existing_fontembed_tests_pass` | 现有字体嵌入测试通过 | `test_pdfbase_fontembed.py` 无回归 |

### 9.3 现有测试文件的修改

**无需修改**。现有测试中 TTFont 不设置 `substitutionFonts`，走原有快速路径。
实现后运行完整测试套件确认无回归。

---

## 10. 实施步骤

### 阶段 1：核心基础设施（预计 1-2 天）

1. `rl_accel.py`：添加 `_py_unicode2TT` 函数
2. `ttfonts.py`：为 `TTFont` 添加 `_substitutionFonts` 内部属性、`substitutionFonts` property（含环境变量开关）和 `hasGlyph` 方法
3. 编写并运行 `test_unicode2TT_*` 和 `test_hasGlyph` 单元测试

### 阶段 2：宽度计算集成（预计 0.5 天）

4. `rl_accel.py`：修改 `_py_instanceStringWidthTTF` 支持 fallback
5. 编写并运行 `test_stringWidth_*` 测试
6. 验证纯 Python 环境下宽度计算正确

### 阶段 3：文本渲染集成（预计 1-2 天）

7. `textobject.py`：修改 `_formatText` TTFont 分支
8. 编写并运行 `test_fallback_pdf_*` 测试
9. 人工检查生成的 PDF 文件

### 阶段 4：图形路径与渲染器集成（预计 1 天）

10. `graphics/utils.py`：修改 `text2PathDescription` 的 freetype 和 _renderPM 两个后端
11. `graphics/renderPM.py`：修改 `drawString` 的 TTFont 分支
12. `graphics/renderPS.py`：修改 PostScript 渲染器的 TTFont 分支
13. 编写并运行图形路径和渲染器测试

### 阶段 5：配置与便利 API（预计 0.5 天）

12. `rl_settings.py`：添加 `defaultTTFFallbackFonts`
13. `pdfmetrics.py`：添加 `registerFontWithFallback`
14. 编写 API 测试

### 阶段 6：回归测试与文档更新（预计 1 天）

15. 运行完整测试套件
16. 性能基准测试
17. 边界情况验证
18. 文档更新（见第 11 节）

---

## 11. 项目文档影响分析

本次功能变更涉及以下项目文档的更新：

### 11.1 需要更新的文档

#### 11.1.1 用户手册：`docs/userguide/ch2a_fonts.py`

**主要更新区域**：

1. **"Automatic output font substitution" 小节（第 88-105 行）**

   当前内容仅描述 Type1 字体的自动 fallback（通过 Symbol/ZapfDingbats）。
   需扩展此节，增加 TTFont fallback 的说明：
   - TTFont 现在也支持 `substitutionFonts` 属性
   - 说明 TTFont fallback 与 Type1 fallback 的异同（自动编码 vs 字形查找）
   - 给出基本使用示例

2. **"TrueType Font Support" 小节（第 294-365 行）**

   在 TTFont 注册和使用说明之后，增加：
   - `TTFont.substitutionFonts` 属性的说明和用法示例
   - `TTFont.hasGlyph()` 方法的说明
   - `pdfmetrics.registerFontWithFallback()` 便利函数的说明
   - 中英文混排的使用示例（最常见的 fallback 场景）

3. **"To Do" 小节（第 486-499 行）**

   功能实现后，移除或更新与 TTFont fallback 相关的待办事项（如有）。

**建议新增内容位置**：在 "TrueType Font Support" 小节的 `registerFontFamily` 说明之后（约第 365 行），
新增一个 `heading3("TrueType Font Fallback")` 小节，集中说明 TTFont fallback 的完整用法。

**建议新增内容要点**：

```
heading3("TrueType Font Fallback (Experimental)")

disc("""
This feature is experimental and disabled by default.
To enable it, set the environment variable REPORTLAB_FONT_FALLBACK=1
before importing reportlab.
""")

# 说明启用方式
eg("""
REPORTLAB_FONT_FALLBACK=1 python your_script.py
""")

# 示例：直接设置 substitutionFonts
eg("""
font = TTFont('NotoSans', 'NotoSans-Regular.ttf')
fallback = TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')
pdfmetrics.registerFont(font)
pdfmetrics.registerFont(fallback)
font.substitutionFonts = [fallback]
# Now text with mixed scripts will automatically use the fallback
c.setFont('NotoSans', 12)
c.drawString(100, 700, 'Hello 你好 World')
""")

# 示例：使用便利函数
eg("""
pdfmetrics.registerFontWithFallback(
    'NotoSans', 'NotoSans-Regular.ttf',
    fallbackFonts=[TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')]
)
""")

# 说明 hasGlyph
disc("""
You can check if a font contains a specific glyph with hasGlyph()...
""")
```

#### 11.1.2 变更日志：`CHANGES.md`

在当前版本的变更条目中添加：

```
CHANGES  4.5.0   ??/02/2026
----------------------------
    * ...
    * added experimental TTFont fallback support via substitutionFonts property
      (requires REPORTLAB_FONT_FALLBACK=1 environment variable to enable)
    * added TTFont.hasGlyph() method
    * added pdfmetrics.registerFontWithFallback() convenience function
    * added rl_settings.defaultTTFFallbackFonts configuration option
```

#### 11.1.3 API 参考文档

- **`docs/reference/reference.yml`**：如果 API 参考中列出了 `pdfmetrics` 模块的公开函数，
  需要添加 `registerFontWithFallback` 的条目。
- **`docs/source/`**（Sphinx 源）：如果 Sphinx 文档仍然维护，需要添加相关 API 的 autodoc 条目。

#### 11.1.4 README

无需修改。`README.txt` 不涉及具体 API 细节。

### 11.2 无需更新的文档

| 文档 | 原因 |
|------|------|
| `docs/userguide/ch2_graphics.py` | 图形章节不涉及字体 fallback 细节 |
| `demos/stdfonts/` | 仅演示标准 14 字体，不涉及 TTFont |
| `INSTALL.txt` | 无安装相关变更 |
| `LICENSE` | 无许可变更 |
| `tools/docco/` | 文档工具链，与字体功能无关 |

### 11.3 文档更新时序

文档更新应在**阶段 6（回归测试与文档更新）**中进行，与功能实现同步完成。
具体顺序：

1. 功能实现完成并通过全部测试
2. 更新 `docs/userguide/ch2a_fonts.py`
3. 运行 `docs/genAll.py` 重新生成用户手册 PDF
4. 检查生成的 PDF 中新增章节的排版和示例
5. 更新 `CHANGES.md`
6. 提交所有文档变更

---

## 12. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 段落布局宽度计算偏差 | 低 | 高 | 严格测试 `stringWidth` 一致性 |
| PDF 查看器兼容性问题 | 低 | 高 | 使用标准 PDF 字体切换操作，测试主流查看器 |
| 性能退化 | 低 | 中 | 无 fallback 时零开销（property getter 一次 `os.environ.get` + 一次字符串比较）；有 fallback 时优化路径 |
| 子集编号冲突 | 极低 | 高 | 每个字体独立子集空间，不存在冲突 |
| HarfBuzz 排版兼容性 | 中 | 中 | 初始版本对 shaped 文本禁用 fallback |
| 用户手册生成失败 | 低 | 中 | 新增示例使用项目自带 Vera 字体，确保可重复构建 |
| 环境变量未设置导致 fallback 不生效 | 低 | 中 | 文档中明确说明 `REPORTLAB_FONT_FALLBACK=1` 的必要性；后续版本稳定后移除开关 |
| property 替换实例属性引入兼容问题 | 极低 | 中 | property 行为与普通属性几乎一致；`hasGlyph` 等新增方法不覆盖任何现有接口 |
| renderPM/renderPS fallback 字体切换 | 低 | 中 | 这两个渲染器中 TTFont 直接使用 `gs.drawString`，切换字体需确保 gstate 同步更新 |

---

## 13. 未来增强方向

1. **CID 字体 fallback**：为 `CIDFont` / `UnicodeCIDFont` 添加类似的 `substitutionFonts` 支持
2. **HarfBuzz 跨字体 shaping**：利用 HarfBuzz 的 font callback 机制实现排版级别的 fallback
3. **缓存 `os.environ.get` 结果**：若运行时环境变量切换需求消失，可缓存环境变量判断结果以进一步降低 property getter 开销
4. **字形查找缓存**：添加 LRU 缓存加速重复字符的字体查找
5. **自动 fallback 配置**：根据 Unicode 脚本范围自动推荐 fallback 字体
6. **FontCollection 支持**：从 TTC 文件自动提取 fallback 字体
7. **TTFont → Type1 fallback**：在 `unicode2TT` 中支持 Type1 字体的编码判断

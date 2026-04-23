# TTFont 字体 Fallback — 实施记录

## 概述

为 TTFont 实现 Unicode 字形缺失时的自动 fallback，行为与 Type1 的 `unicode2T1` + `substitutionFonts` 机制对齐。功能通过环境变量 `REPORTLAB_FONT_FALLBACK=1` 启用，默认关闭。

## 变更范围

### 新增

| 变更 | 说明 |
|------|------|
| `unicode2TT()` | 按字形可用性将文本拆分为 `(TTFont, str)` 对，与 `unicode2T1` 平行 |
| `TTFont.hasGlyph(char_or_code)` | 检查字体是否包含指定字形，支持 str/int 参数 |
| `TTFont.substitutionFonts` property | 环境变量控制的 fallback 字体列表，getter 实时读取 `os.environ` |
| `pdfmetrics.registerFontWithFallback()` | 便利函数，注册 TTFont 并同时设置 fallback |
| `rl_settings.defaultTTFFallbackFonts` | 全局默认 fallback 字体名称列表（默认 `[]`） |
| `tests/test_pdfbase_ttfont_fallback.py` | 36 个测试用例，覆盖核心逻辑、宽度计算、PDF 生成、API |
| `tests_resource/` | 外部测试字体目录（gitignore），附 README 说明初始化方式 |

### 修改

| 文件 | 变更 |
|------|------|
| `rl_accel.py` | `__all__` 新增 `unicode2TT`；新增 `_py_unicode2TT` 实现；`instanceStringWidthTTF` 支持 fallback 分段宽度计算；所有 12 个函数添加模块级名称绑定以支持 IDE 静态分析 |
| `ttfonts.py` | `__init__` 新增 `_substitutionFonts`；`substitutionFonts` 改为 property（含环境变量开关）；新增 `hasGlyph` 方法 |
| `textobject.py` | `_formatText` 普通 TTFont 路径增加 fallback 拆分与字体切换；HarfBuzz 路径增加降级处理 |
| `graphics/utils.py` | freetype 和 `_renderPM` 两个后端均增加 fallback 拆分逻辑 |
| `graphics/renderPM.py` | `drawString` 的 TTFont 分支增加 fallback 拆分与字体切换 |
| `graphics/renderPS.py` | `_dynamicFont` 分支增加 fallback 拆分与 PS 字体切换 |
| `docs/userguide/ch2a_fonts.py` | 新增 "TrueType Font Fallback (Experimental)" 文档小节 |
| `CHANGES.md` | 添加版本变更条目 |
| `.gitignore` | 添加 `tests_resource/*.ttf` |

## 架构决策

1. **property + 环境变量为唯一控制点** — 下游代码只需 `if font.substitutionFonts:` 即可，无需感知开关
2. **新增 `unicode2TT` 而非修改 `unicode2T1`** — 两类字体的字形检测机制不同（编码尝试 vs `charToGlyph` 查找），独立实现避免回归
3. **两步渲染流程** — `unicode2TT` 按字形拆分 → 各片段独立走 `splitString` 子集编码，职责分离
4. **HarfBuzz 降级** — shaped 文本遇到 fallback 时打印 warning 并走普通路径，跨字体 shaping 留作后续增强
5. **rl_accel 静态可见性** — 为所有 12 个动态导出函数添加模块级名称绑定，修复 IDE 静态分析误报

## 测试

- 基础测试（25 个）：使用项目自带的 Vera 字体，无需额外配置
- 多脚本测试（11 个）：需要 `tests_resource/` 中的外部 TTF 字体，缺失时自动 SKIP
- 回归验证：现有 `test_pdfbase_ttfonts.py` 25 个测试全部通过

## 受影响模块一览

```
src/reportlab/lib/rl_accel.py          # 核心：unicode2TT、宽度计算
src/reportlab/pdfbase/ttfonts.py       # 核心：property、hasGlyph
src/reportlab/pdfgen/textobject.py     # 渲染：PDF 内容流字体切换
src/reportlab/graphics/utils.py        # 图形：text2PathDescription 两个后端
src/reportlab/graphics/renderPM.py     # 渲染：drawString 位图输出
src/reportlab/graphics/renderPS.py     # 渲染：PostScript 输出
src/reportlab/pdfbase/pdfmetrics.py    # API：registerFontWithFallback
src/reportlab/rl_settings.py           # 配置：defaultTTFFallbackFonts
```

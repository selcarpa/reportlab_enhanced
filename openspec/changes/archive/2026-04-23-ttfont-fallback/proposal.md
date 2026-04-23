## Why

ReportLab 的 TrueType 字体（TTFont）在遇到不包含的字形时直接映射为 glyph 0（`.notdef`），导致 PDF 中出现方框或空白。Type1 字体已通过 `unicode2T1()` 和 `substitutionFonts` 具备自动 fallback 机制，但 TTFont——当前最常用的字体类型——尚无等效支持。这使得中英文混排、多脚本文档等场景需要用户手动切换字体，增加使用复杂度。

## What Changes

- 为 `TTFont` 新增 `substitutionFonts` property（含环境变量 `REPORTLAB_FONT_FALLBACK` 开关控制）
- 为 `TTFont` 新增 `hasGlyph(char_or_code)` 方法
- 新增 `unicode2TT(utext, fonts)` 函数，按字形可用性将文本拆分到多个 TTFont
- 修改 `_py_instanceStringWidthTTF` 支持 fallback 字体的宽度计算
- 修改 `_formatText` 的 TTFont 渲染路径，支持跨字体渲染
- 修改 `text2PathDescription`（freetype 和 _renderPM 两个后端）支持 fallback
- 修改 `renderPM.py` 和 `renderPS.py` 的 TTFont 渲染路径支持 fallback
- 新增 `pdfmetrics.registerFontWithFallback()` 便利函数
- 新增 `rl_settings.defaultTTFFallbackFonts` 全局配置项
- 默认关闭（需 `REPORTLAB_FONT_FALLBACK=1` 环境变量启用），对无 fallback 配置的场景零开销

## Capabilities

### New Capabilities
- `ttfont-substitution`: TTFont 自动字体 fallback——字形查找、文本拆分、宽度计算、渲染路径的完整支持
- `ttfont-fallback-api`: 公开 API 层——`substitutionFonts` property、`hasGlyph()` 方法、`registerFontWithFallback()` 便利函数、`defaultTTFFallbackFonts` 配置项
- `ttfont-fallback-testing`: 测试覆盖——单元测试、宽度一致性测试、PDF 生成测试、图形路径测试、回归测试

### Modified Capabilities

（无已有 capability 需要修改——这是新增功能）

## Impact

- **源码文件**：`rl_accel.py`、`ttfonts.py`、`textobject.py`、`pdfmetrics.py`、`graphics/utils.py`、`graphics/renderPM.py`、`graphics/renderPS.py`、`rl_settings.py`
- **新增测试**：`tests/test_pdfbase_ttfont_fallback.py`
- **API 兼容性**：完全向后兼容。`substitutionFonts` property 在环境变量未设置时返回 `[]`，下游代码走原有快速路径；`hasGlyph` 和 `registerFontWithFallback` 为新增接口，不覆盖任何现有方法
- **依赖**：无新增外部依赖
- **PDF 语义**：使用标准 `Tf` 操作符切换字体，完全符合 PDF 规范；每个 TTFont 独立管理子集状态，无编号冲突

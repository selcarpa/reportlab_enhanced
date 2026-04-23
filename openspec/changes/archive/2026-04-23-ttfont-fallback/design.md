## Context

ReportLab 的字体体系中，Type1 字体已通过 `unicode2T1()` + `Font.substitutionFonts` 具备自动 fallback。但 TTFont（TrueType）——当前最常用的字体类型——在 `splitString()` 中将缺失字形直接映射为 glyph 0，无任何 fallback 尝试。

本项目的纯 Python 架构（v4.0 起无 C 扩展）简化了实现：`rl_accel.py` 中的 `_py_funcs` 模式使新增函数可按同样模式加入，无需考虑 C 扩展兼容性。

关键约束：
- `splitString()` 负责子集编码，返回 `(subset, bytes)` 对——这是 PDF 渲染的最终步骤
- TTFont 渲染路径有三层：HarfBuzz shaped → 普通 TTFont → 非 dynamicFont
- `text2PathDescription` 有两个条件编译的后端（freetype / _renderPM）
- 每个字体实例独立维护子集状态（`WeakKeyDictionary`），天然支持多文档并行

## Goals / Non-Goals

**Goals:**
- TTFont 遇到缺失字形时自动从 `substitutionFonts` 列表查找可用字体
- 文本渲染、宽度计算、图形路径、renderPM、renderPS 全部场景一致处理 fallback
- 与 Type1 fallback 保持 API 一致性（`substitutionFonts` 属性、拆分函数模式）
- 环境变量控制的开关确保无 fallback 场景零开销
- 向后兼容：默认关闭，现有代码行为不变

**Non-Goals:**
- CID/CJK 字体的 fallback（不同编码模型）
- HarfBuzz 排版文本的跨字体 shaping（需 HarfBuzz 本身支持 font callback）
- 从字体文件自动推断 fallback 关系
- TTFont → Type1 的 fallback（Type1 无 `charToGlyph`，初始版本不支持）

## Decisions

### D1: property + 环境变量作为单一根部控制点

将 `TTFont.substitutionFonts` 实现为 property，getter 每次调用时实时读取 `os.environ.get('REPORTLAB_FONT_FALLBACK')`。关闭时返回 `[]`，开启时返回 `self._substitutionFonts`。

**替代方案**：类级常量（import 时读取一次）→ 放弃，因为会冻结环境变量，无法运行时切换。

**理由**：所有下游代码只需 `if font.substitutionFonts:` 即可，无需感知开关。环境变量判断集中在 property getter 一处。

### D2: 新增 `unicode2TT()` 而非修改 `unicode2T1()`

新增独立的 `unicode2TT(utext, fonts)` 函数，与 `unicode2T1` 平行存在。

**替代方案**：统一为一个 `unicode2Font()` 函数 → 放弃，因为 Type1 和 TTFont 的字形检测机制完全不同（编码尝试 vs `charToGlyph` 查找），强行统一增加复杂度。

**理由**：保持 `unicode2T1` 不变，避免回归风险；`unicode2TT` 可针对 TTFont 特性优化。

### D3: 两步渲染流程

文本先经 `unicode2TT` 按字形可用性拆分为 `(TTFont, str)` 对，再各自经 `splitString` 进行子集编码。

**理由**：`splitString` 的职责是子集编码（CID 映射），不应同时承担字形查找。两步分离使每步职责清晰，且 fallback 字体各自独立走 `splitString`，子集状态互不干扰。

### D4: HarfBuzz 文本降级处理

当 `substitutionFonts` 非空且文本为 `ShapedStr` 时，打印 warning 并降级到普通 TTFont 路径（无 shaping）。

**理由**：HarfBuzz 的跨字体 shaping 需要 font callback 支持，实现复杂度高。降级保证功能可用，shaping 作为后续增强。

### D5: `hasGlyph()` 的 nbsp 处理

`U+00A0`（nbsp）映射为 `U+0020`（space），与 `splitString` 行为一致。

**理由**：确保 `hasGlyph` 与实际渲染行为一致，避免宽度计算和渲染不匹配。

## Risks / Trade-offs

- **段落布局宽度偏差** → `instanceStringWidthTTF` 修改后严格使用与渲染相同的 `unicode2TT` 拆分逻辑，确保宽度一致性
- **renderPM/renderPS 字体切换同步** → `_setFont(gs, fbFont.fontName, fontSize)` 确保 gstate 与渲染字体一致
- **PDF 文件体积增大** → fallback 字体将嵌入额外子集，属预期行为；用户可通过精简 fallback 列表控制
- **性能** → 无 fallback 时仅增加一次 `os.environ.get` + 字符串比较；有 fallback 时 `unicode2TT` 逐字符扫描，对 2-3 个 fallback 字体开销约 2-3 倍，可接受
- **property 替换实例属性** → 行为差异极小（赋值走 setter 无变化），测试覆盖验证兼容性

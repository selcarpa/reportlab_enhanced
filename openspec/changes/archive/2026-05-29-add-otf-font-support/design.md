## Context

ReportLab 的字体系统当前基于 `ttfonts.py` 模块，仅支持 TrueType 轮廓字体。该模块包含约 1585 行代码，混合了 sfnt 二进制解析、TrueType 专用逻辑、PDF 生成和用户接口等多个关注点。

OpenType CFF 字体（.otf）是当今最常用的字体格式之一，但 ReportLab 在 `TTFontParser.readHeader()` 中明确拒绝了 sfnt 版本 `0x4F54544F`（"OTTO"）的字体文件。

本设计基于项目中已有的详细设计方案（`project-doc/plan/2026-05-25-otf-font-support.md`）。

## Goals / Non-Goals

**Goals:**

- 支持加载 OpenType CFF 字体（.otf），自动识别文件类型
- 正确提取字体度量信息（名称、宽度、bbox 等）
- 正确生成 PDF 子集嵌入（FontFile3 + Type1C）
- 与现有 TrueType 字体使用方式完全一致（API 不变）
- 与现有 TTFont fallback 机制兼容
- 对类名进行重构，使命名反映实际支持的字体格式
- 保持完全向后兼容

**Non-Goals:**

- CFF2 字体支持（OpenType 1.8+ 新格式）
- 可变字体支持（Variable Fonts）
- 从 OTF 字体自动推断 fallback 关系
- Type1 字体的更新或修改
- CFF 子集压缩（初始版本直接嵌入子集化的 CFF 数据）

## Decisions

### 双包架构

采用双包架构，将字体核心逻辑与向后兼容分离：

| 文件/包 | 角色 | 说明 |
|--------|------|------|
| `src/reportlab/pdfbase/openfonts/` | **主包（新）** | 包含所有字体逻辑的全新包 |
| `src/reportlab/pdfbase/ttfonts.py` | **兼容层（已过期）** | 仅保留向后兼容别名 |

**理由**：`openfonts/` 包是未来所有开发的起点，新类名、新功能全部在此。`ttfonts.py` 完全不承载新逻辑，仅做兼容转发，避免代码重复。

### 类名重构

| 旧名称 | 新名称 | 向后兼容别名 |
|--------|--------|-------------|
| `TTFont` | `OpenTypeFont` | `TTFont = OpenTypeFont` |
| `TTFontParser` | `FontParser` | `TTFontParser = FontParser` |
| `TTFontFile` | `FontFile` | `TTFontFile = FontFile` |
| `TTFontFace` | `FontFace` | `TTFontFace = FontFace` |
| `TTFontMaker` | `FontMaker` | `TTFontMaker = FontMaker` |
| `TTEncoding` | `FontEncoding` | `TTEncoding = FontEncoding` |

**理由**：OpenType 是 TTF 和 OTF 的统一标准（ISO 14496-22），新命名更准确地反映字体格式。

### 模块拆分

将 `openfonts/` 包拆分为 9 个模块，每个模块职责清晰：

| 模块 | 行数（估） | 职责 |
|------|----------|------|
| `_common.py` | ~80 | 错误类、辅助函数 |
| `_sfnt.py` | ~200 | sfnt 二进制格式解析 |
| `_ttf.py` | ~700 | TrueType 专用逻辑 |
| `_cff.py` | ~500 | CFF 表解析与子集生成 |
| `_face.py` | ~100 | 字体面度量 |
| `_encoding.py` | ~20 | UTF-8 编码适配器 |
| `_font.py` | ~300 | 主用户类 |
| `_shaping.py` | ~50 | 文本整形支持 |
| `__init__.py` | ~50 | 包入口、导出、别名 |

**理由**：每个模块可独立理解，CFF 代码与 TrueType 代码完全隔离，便于维护和测试。

### CFF 处理策略

在 `FontParser.readHeader()` 中检测 OTTO 版本并设置 `self.isCFF = True`，后续代码路径根据此标志分支处理：

- **共享表解析**：name, head, OS/2, post, hhea, hmtx, cmap（TTF 和 OTF 完全一致）
- **maxp 分支**：CFF 版本 0.5，仅 6 字节；TrueType 版本 1.0，32 字节
- **CFF 表**：使用 `CFFParser` 解析 CharStrings INDEX
- **子集化**：使用 `CFFSubsetter` 生成 CFF 子集流

## Risks / Trade-offs

- **CFF 表内存占用**：CFF 表通常比 TrueType 的 glyf+loca 表大（如 SourceHanSansK-Light.otf 的 CFF 表为 15.5MB）。初始版本采用全量解析策略，后续可优化为惰性解析。
- **HarfBuzz 兼容性**：初始版本中 CFF 字体不参与 HarfBuzz shaping（降级到无 shaping 路径）。后续版本可扩展。
- **向后兼容警告**：`ttfonts.py` 的 DeprecationWarning 会影响现有代码的静默运行。这是有意设计，引导用户迁移。

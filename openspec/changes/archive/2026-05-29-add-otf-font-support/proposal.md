## Why

ReportLab 当前仅支持 TrueType 轮廓字体（TTF/TTC），不支持 OpenType CFF 字体（OTF）。
OTF 字体是当今最常用的字体格式之一，包括 Adobe Source Han 系列、Google Noto 系列等大量流行字体。
用户无法在 ReportLab 中使用这些字体生成 PDF，限制了文档的排版质量和国际化能力。

## What Changes

- 新增 `openfonts/` 包，支持 TTF 和 OTF 字体的统一加载、度量提取和子集化
- 新增 `CFFParser` 和 `CFFSubsetter` 类，处理 CFF 轮廓字体的解析和子集生成
- 新增 `PDFType1CFont` 类，用于 PDF 中嵌入 CFF 字体（FontFile3 + /Type1C）
- 将原有 `TTFont` 类重命名为 `OpenTypeFont`，保留向后兼容别名
- 将原有 `ttfonts.py` 改造为纯兼容层（导入重导出 + DeprecationWarning）
- API 完全兼容：`TTFont('name', 'font.otf')` 之前报错，现在正常工作

## Capabilities

### New Capabilities

- `otf-font-support`: 支持加载和使用 OpenType CFF 字体（.otf），包括字体解析、度量提取、PDF 子集嵌入
- `font-class-refactoring`: 将字体相关类重命名为反映 OpenType 标准的名称，保留向后兼容别名
- `cff-subsetting`: CFF 字体的子集化生成（CharStrings INDEX 重建、FDSelect 处理等）

### Modified Capabilities

（无现有规范需要修改）

## Impact

- 新增文件：`src/reportlab/pdfbase/openfonts/` 包（9 个模块）
- 修改文件：`src/reportlab/pdfbase/ttfonts.py`（改为兼容层）
- 修改文件：`src/reportlab/pdfbase/pdfdoc.py`（新增 `PDFType1CFont`）
- 测试文件：新增 `tests/test_pdfbase_otf.py` 及多个 OTF 测试文件
- 向后兼容：所有现有使用 `TTFont` 的代码无需修改即可继续工作

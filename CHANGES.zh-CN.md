# 变更记录

## [Unreleased]

### 新增
- **OpenType/CFF 字体支持** — 新增 `reportlab.pdfbase.openfonts` 包，支持 CFF 格式
  OpenType 字体（.otf）的读取、子集化与 PDF 嵌入
  - 功能：同时支持 CID-Keyed（如 Source Han Sans、Noto CJK）和 non-CID 两类
    CFF 字体，通过 `isCFF`/`isCID` 标志自动检测并生成正确的 PDF 字体字典结构
    （CID 字体使用 `/Type0` + `/CIDFontType0`，非 CID 字体使用 `/Type1` + `FontFile3`）
  - 纯 Python 实现的 CFF 子集化器，完整处理 FDSelect、charset、Private DICT 偏移修补
  - HarfBuzz 文本塑形同时支持 CFF 和 TrueType 字体
  - 兼容性：全新包，对现有 `TTFont`、Type1 及所有遗留 API 无影响，已有代码无需修改
  - 已知限制：暂不支持 CFF2 字体（OpenType 1.8+）和可变字体（`fvar`/`gvar`），
    子集化时未裁剪未引用的子程序
- 新增 OpenCode 配置与中文本地化开发环境

### 变更（兼容性）
- **`reportlab.pdfbase.ttfonts` 标记为已弃用** — 该模块现为兼容性薄层，
  从 `reportlab.pdfbase.openfonts` 重导出所有内容，并在导入时发出
  `DeprecationWarning`。所有已有类和函数名保留，导入继续可用，
  但用户应迁移至新的 `openfonts` 包，计划在未来版本中移除
- **`TTFont` 统一为 `OpenTypeFont` 的子类** — `TTFont` 现在继承自
  `OpenTypeFont`，公共 API 完全保留，无需修改现有代码
- PDF 测试输出从 `tests/` 根目录移至 `tests/pdf-out/` 目录

### 修复
- **PDFType1CFont.Subtype** — 字体字典 Subtype 从 `Type1C` 更正为 `Type1`，
  符合 PDF 规范（ISO 32000, Table 111）。`Type1C` 仅用于 `FontFile3` 流
  （已在 `_face.py` 中正确设置）。使用错误 `Type1C` Subtype 生成的 PDF 可能被
  严格 PDF 阅读器拒绝；此修复确保规范兼容，对宽容阅读器无功能变化

## [0.0.1] - 2026-02-12

### 新增
- **TrueType 字体回退系统** — 主字体缺失字形时自动按优先级回退到备选字体
  - `TTFont.substitutionFonts`：备选字体列表，按顺序依次查找
  - `unicode2TT()`：按字形可用性将文本拆分为片段，实现准确的混合脚本渲染
  - `stringWidth()`：按片段分别计算宽度，确保正确换行布局
  - `hasGlyph()`：字形存在性检查，支持字符串和整数码点两种参数
  - `registerFontWithFallback()`：一步注册字体与回退的便捷接口
  - `REPORTLAB_FONT_FALLBACK=1` 环境变量控制启用/禁用
  - 兼容性：默认关闭，对现有代码零行为变化。所有已有 `TTFont` API 完全保留，
    回退为可选加入
- **用户文档国际化** — 基于 MkDocs 的中英文 HTML 文档，支持用户手册语言切换
- **CI/CD 自动化** — GitHub Actions 工作流，支持测试、GitHub Pages 部署和 PyPI 发布
- **OPSX 实验性工作流** — 结构化的变更提议与评审流程

### 变更
- **项目更名** — 包名从 `reportlab` 变更为 `reportlab-enhanced`
  （Python 导入名为 `reportlab_enhanced`）。通过兼容性重导出层保留原始
  `reportlab` 命名空间供已有导入使用（参见 `src/reportlab/pdfbase/ttfonts.py`）
- **版本管理** — 以 `pyproject.toml` 作为唯一事实来源；`__init__.py` 通过
  `importlib.metadata` 解析版本
- `setup.py` 精简为仅保留动态构建逻辑

## [0.0.0] - 2025-02-12

### 新增
- 从 ReportLab 初始 fork
- 基于 ReportLab 3.6.13 版本

此版本代表 reportlab-enhanced fork 的起点，
包含上游 ReportLab 3.6.13 版本的全部功能与修复。

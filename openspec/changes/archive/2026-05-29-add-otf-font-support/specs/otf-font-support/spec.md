## ADDED Requirements

### Requirement: 加载 OTF 字体文件

系统 SHALL 支持加载 OpenType CFF 字体文件（.otf），自动识别文件类型并正确解析。

#### Scenario: 加载 OTF 文件成功
- **WHEN** 用户调用 `TTFont('MyFont', 'font.otf')` 或 `OpenTypeFont('MyFont', 'font.otf')`
- **THEN** 系统成功加载字体，`font.face.isCFF` 属性为 `True`

#### Scenario: 加载 TTF 文件仍然有效
- **WHEN** 用户调用 `TTFont('MyFont', 'font.ttf')`
- **THEN** 系统成功加载字体，`font.face.isCFF` 属性为 `False`

#### Scenario: 拒绝 CFF2 字体
- **WHEN** 用户尝试加载使用 CFF2 表的字体文件
- **THEN** 系统抛出 `TTFError` 异常

### Requirement: 提取字体度量信息

系统 SHALL 正确提取 OTF 字体的度量信息，包括名称、宽度、bbox 等。

#### Scenario: 提取字体名称
- **WHEN** 成功加载 OTF 字体
- **THEN** `font.face.name` 属性包含正确的 PostScript 字体名

#### Scenario: 提取字符宽度
- **WHEN** 成功加载 OTF 字体
- **THEN** `font.face.charWidths` 字典包含所有字形的宽度信息

#### Scenario: 提取字体 bbox
- **WHEN** 成功加载 OTF 字体
- **THEN** `font.face.bbox` 元组包含正确的字体边界框

### Requirement: PDF 子集嵌入

系统 SHALL 正确生成 OTF 字体的 PDF 子集嵌入，使用 FontFile3 和 Type1C 子类型。

#### Scenario: 生成 PDF 子集
- **WHEN** 用户在文档中使用 OTF 字体并保存 PDF
- **THEN** 生成的 PDF 包含 FontFile3 流，Subtype 为 /Type1C

#### Scenario: ToUnicode CMap 生成
- **WHEN** 生成 OTF 字体的 PDF 子集
- **THEN** 系统生成正确的 ToUnicode CMap，支持文本搜索和复制

### Requirement: 向后兼容

系统 SHALL 保持与现有代码的完全向后兼容。

#### Scenario: 旧导入路径仍然有效
- **WHEN** 用户代码使用 `from reportlab.pdfbase.ttfonts import TTFont`
- **THEN** 导入成功（带 DeprecationWarning），`TTFont` 类可用

#### Scenario: isinstance 检查仍然有效
- **WHEN** 用户使用 `isinstance(font, TTFont)` 检查
- **THEN** 检查结果正确

### Requirement: 测试输出文件规范

所有新增测试用例输出 PDF 文件时 SHALL 遵循以下命名规范：

1. 输出目录统一为 `tests/pdf-out/`
2. 文件名 SHALL 包含测试方法名，格式为 `test_<方法名>.pdf`
3. 同一测试类中的不同测试方法 SHALL 生成不同的文件名

#### Scenario: 测试输出到指定目录
- **WHEN** 测试方法 `test_otf_rendering_basic` 执行并生成 PDF
- **THEN** 输出文件路径为 `tests/pdf-out/test_otf_rendering_basic.pdf`

#### Scenario: 文件名与测试方法关联
- **WHEN** 测试方法 `test_otf_cjk_rendering` 执行并生成 PDF
- **THEN** 输出文件名为 `test_otf_cjk_rendering.pdf`，可直接从文件名识别出对应的测试方法

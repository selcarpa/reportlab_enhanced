## ADDED Requirements

### Requirement: CFF 表解析

系统 SHALL 解析 CFF 表，提取 CharStrings INDEX、FDSelect、FDArray 等结构。

#### Scenario: 解析标准 CFF 字体
- **WHEN** 加载标准 CFF 字体（非 CID）
- **THEN** `CFFParser` 正确解析 CharStrings INDEX，`charStrings` 列表包含每个字形的偏移信息

#### Scenario: 解析 CID-keyed CFF 字体
- **WHEN** 加载 CID-keyed CFF 字体
- **THEN** `CFFParser` 正确解析 FDSelect 和 FDArray，`isCID` 属性为 `True`

### Requirement: CFF 子集生成

系统 SHALL 从完整 CFF 数据中生成子集，仅包含文档中实际使用的字形。

#### Scenario: 生成 CharStrings 子集
- **WHEN** 文档使用了 100 个字形
- **THEN** 生成的 CFF 子集仅包含这 100 个字形的 CharStrings

#### Scenario: 重建 Charset
- **WHEN** 生成 CFF 子集
- **THEN** 子集的 Charset 映射正确对应子集中的字形

#### Scenario: 处理 FDSelect（CID 字体）
- **WHEN** 生成 CID-keyed CFF 字体的子集
- **THEN** FDSelect 正确映射子集中的字形到 Font DICT

### Requirement: 测试输出文件规范

所有新增测试用例输出文件时 SHALL 遵循以下命名规范：

1. 输出目录统一为 `tests/pdf-out/`
2. 文件名 SHALL 包含测试方法名，格式为 `test_<方法名>.pdf` 或 `test_<方法名>.cff`
3. 同一测试类中的不同测试方法 SHALL 生成不同的文件名

#### Scenario: 测试输出到指定目录
- **WHEN** 测试方法 `test_cff_subset_basic` 执行并生成子集文件
- **THEN** 输出文件路径为 `tests/pdf-out/test_cff_subset_basic.cff`

#### Scenario: 文件名与测试方法关联
- **WHEN** 测试方法 `test_cff_subset_cid` 执行并生成 PDF
- **THEN** 输出文件名为 `test_cff_subset_cid.pdf`，可直接从文件名识别出对应的测试方法

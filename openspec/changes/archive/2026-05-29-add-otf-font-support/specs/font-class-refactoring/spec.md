## ADDED Requirements

### Requirement: 类名重命名

系统 SHALL 将字体相关类重命名为反映 OpenType 标准的名称，同时保留向后兼容别名。

#### Scenario: 新类名可用
- **WHEN** 用户代码使用 `from reportlab.pdfbase.openfonts import OpenTypeFont`
- **THEN** 导入成功，`OpenTypeFont` 类可用

#### Scenario: 旧类名作为别名可用
- **WHEN** 用户代码使用 `from reportlab.pdfbase.openfonts import TTFont`
- **THEN** 导入成功，`TTFont` 是 `OpenTypeFont` 的别名

#### Scenario: 别名在 isinstance 检查中工作
- **WHEN** 用户使用 `isinstance(font, TTFont)` 检查
- **THEN** 检查结果正确（因为 `TTFont = OpenTypeFont`）

### Requirement: 兼容层模块

系统 SHALL 将 `ttfonts.py` 改造为纯兼容层，从 `openfonts` 包导入并重导出。

#### Scenario: 导入兼容层产生警告
- **WHEN** 用户代码导入 `ttfonts` 模块
- **THEN** 系统发出 `DeprecationWarning`

#### Scenario: 兼容层中的类可用
- **WHEN** 用户代码使用 `from reportlab.pdfbase.ttfonts import TTFont`
- **THEN** 导入成功，`TTFont` 类可用

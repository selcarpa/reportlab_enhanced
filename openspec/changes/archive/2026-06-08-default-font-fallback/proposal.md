## Why

TTFont 字体回退功能目前通过 `REPORTLAB_FONT_FALLBACK=1` 环境变量控制开关，默认关闭。经过测试验证，该功能已稳定可靠，应作为默认行为启用，消除用户手动配置的步骤。

## What Changes

- **BREAKING**: 移除 `REPORTLAB_FONT_FALLBACK` 环境变量，TTFont 字体回退功能默认始终启用
- 移除 `substitutionFonts` property 中的环境变量检查逻辑
- 更新所有相关文档和 README，移除环境变量设置说明
- 更新测试用例，移除环境变量设置/清理代码
- 版本升级至 `0.1.0`

## Capabilities

### New Capabilities

_(无新增 capability)_

### Modified Capabilities

- `ttfont-fallback-api`: 移除环境变量控制，`substitutionFonts` property 直接返回 `self._substitutionFonts`（默认启用）

## Impact

- `src/reportlab/pdfbase/ttfonts.py`: `substitutionFonts` getter 移除环境变量检查
- `tests/test_ttfont_fallback_*.py`: 4 个测试文件需移除 `REPORTLAB_FONT_FALLBACK` 环境变量设置/清理代码
- `README.md`, `README.zh-CN.md`: 移除环境变量说明
- `docs/userguide/ch2a_fonts.py`, `docs/userguide/zh-CN/ch2a_fonts_1.py`: 移除环境变量启用说明
- `project-doc/plan/2026-04-22-font-fallback.md`: 移除环境变量相关描述
- `CHANGES.md`: 记录行为变更
- `src/reportlab/__init__.py`: 更新 `Version` 为 `0.1.0`

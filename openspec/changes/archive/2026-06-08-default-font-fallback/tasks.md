## 1. 核心实现

- [x] 1.1 `src/reportlab/pdfbase/ttfonts.py`：移除 `substitutionFonts` getter 中的环境变量检查，直接返回 `self._substitutionFonts`
- [x] 1.2 `src/reportlab/__init__.py`：将 `Version` 更新为 `0.1.0`

## 2. 测试更新

- [x] 2.1 `tests/test_ttfont_fallback_api.py`：移除所有 `REPORTLAB_FONT_FALLBACK` 环境变量设置/清理代码
- [x] 2.2 `tests/test_ttfont_fallback_core.py`：移除所有 `REPORTLAB_FONT_FALLBACK` 环境变量设置/清理代码
- [x] 2.3 `tests/test_ttfont_fallback_pdf.py`：移除所有 `REPORTLAB_FONT_FALLBACK` 环境变量设置/清理代码
- [x] 2.4 `tests/test_ttfont_fallback_multiscript.py`：移除所有 `REPORTLAB_FONT_FALLBACK` 环境变量设置/清理代码

## 3. 文档更新

- [x] 3.1 `README.md`：移除 `REPORTLAB_FONT_FALLBACK=1` 环境变量说明，更新 TTFont Fallback 描述
- [x] 3.2 `README.zh-CN.md`：移除 `REPORTLAB_FONT_FALLBACK=1` 环境变量说明，更新 TTFont 字体回退描述
- [x] 3.3 `docs/userguide/ch2a_fonts.py`：移除环境变量启用说明和示例
- [x] 3.4 `docs/userguide/zh-CN/ch2a_fonts_1.py`：移除环境变量启用说明和示例
- [x] 3.5 `project-doc/plan/2026-04-22-font-fallback.md`：移除环境变量相关描述
- [x] 3.6 `project-doc/reference/testing.md`：移除 `REPORTLAB_FONT_FALLBACK` 环境变量表格行
- [x] 3.7 `CHANGES.md`：记录字体回退功能默认启用的行为变更

## 4. 验证

- [ ] 4.1 运行所有 TTFont 回退相关测试确认通过
- [ ] 4.2 确认代码中不再有 `REPORTLAB_FONT_FALLBACK` 引用

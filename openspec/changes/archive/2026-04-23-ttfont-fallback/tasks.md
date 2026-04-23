## 1. 核心基础设施

- [x] 1.1 `rl_accel.py`：`__all__` 添加 `'unicode2TT'`，新增 `_py_unicode2TT(utext, fonts)` 纯 Python 实现
- [x] 1.2 `ttfonts.py`：`TTFont.__init__` 末尾添加 `self._substitutionFonts = []`
- [x] 1.3 `ttfonts.py`：将 `substitutionFonts` 改为 property（getter 实时读取 `os.environ.get('REPORTLAB_FONT_FALLBACK', '0')`，setter 写入 `_substitutionFonts`）
- [x] 1.4 `ttfonts.py`：新增 `hasGlyph(char_or_code)` 方法（接受 str/int，nbsp→space，检查 `face.charToGlyph`）

## 2. 宽度计算集成

- [x] 2.1 `rl_accel.py`：修改 `_py_instanceStringWidthTTF`，在快速路径前检查 `getattr(self, 'substitutionFonts', None)`，有 fallback 时用 `_py_unicode2TT` 分段计算宽度

## 3. 文本渲染集成

- [x] 3.1 `textobject.py`：在 `_formatText` 普通 TTFont 路径（第 632 行 `else` 分支）前插入 fallback 判断
- [x] 3.2 `textobject.py`：实现 fallback 渲染逻辑——调用 `unicode2TT` 拆分文本，遍历片段各自走 `splitString`，字体切换时发出 `Tf` 操作符，完成后恢复主字体
- [x] 3.3 `textobject.py`：HarfBuzz 路径添加降级处理——检测 `substitutionFonts` 非空且文本为 `ShapedStr` 时打印 warning 并走普通 TTFont 路径
- [x] 3.4 `textobject.py`：惰性导入 `unicode2TT` 避免循环依赖

## 4. 图形路径与渲染器集成

- [x] 4.1 `graphics/utils.py`：freetype 后端的 `_dynamicFont` 分支添加 fallback——检查 `substitutionFonts`，调用 `unicode2TT` 拆分，逐段 `_text2Path` 并累加 x 偏移
- [x] 4.2 `graphics/utils.py`：_renderPM 后端的 `_dynamicFont` 分支添加同样的 fallback 逻辑（逐段 `_stringPath` 并累加 x 偏移）
- [x] 4.3 `graphics/renderPM.py`：`drawString` 的 TTFont 分支添加 fallback——`unicode2TT` 拆分，逐段 `drawString`，通过 `_setFont` 切换字体并累加 x 偏移
- [x] 4.4 `graphics/renderPS.py`：`_dynamicFont` 分支添加 fallback——`unicode2TT` 拆分，逐段切换 PS 字体并渲染

## 5. 配置与便利 API

- [x] 5.1 `rl_settings.py`：`__all__` 添加 `'defaultTTFFallbackFonts'`，新增 `defaultTTFFallbackFonts = []`
- [x] 5.2 `pdfmetrics.py`：新增 `registerFontWithFallback(name, filename, fallbackFonts=None, **kwargs)` 函数

## 6. 测试

- [x] 6.1 创建 `tests/test_pdfbase_ttfont_fallback.py`，实现 unicode2TT 单元测试（T01-T07）
- [x] 6.2 实现 hasGlyph 测试（T08）
- [x] 6.3 实现环境变量控制测试（T09-T11）
- [x] 6.4 实现宽度计算测试（T12-T14）
- [x] 6.5 实现 PDF 生成测试（T20-T24）
- [x] 6.6 实现图形路径测试（T30-T31）
- [x] 6.7 实现 renderPM/renderPS 测试（T35-T36）
- [x] 6.8 实现 API 测试（T32-T34）
- [x] 6.9 运行现有测试套件确认无回归（T40-T41）

## 7. 文档更新

- [x] 7.1 更新 `docs/userguide/ch2a_fonts.py`——新增 TTFont Fallback 小节
- [x] 7.2 更新 `CHANGES.md`——添加版本变更条目

## 1. 包结构创建

- [x] 1.1 创建 `src/reportlab/pdfbase/openfonts/` 目录
- [x] 1.2 创建 `_common.py`：迁移 TTFError、SUBSETN、辅助函数
- [x] 1.3 创建 `_sfnt.py`：迁移 FontParser 基类

## 2. TrueType 逻辑迁移

- [x] 2.1 创建 `_ttf.py`：迁移 FontFile、FontMaker 类
- [x] 2.2 修改 `readHeader()` 接受 OTTO 版本，设置 `isCFF = True`

## 3. CFF 支持实现

- [x] 3.1 创建 `_cff.py`：实现 CFFParser 类（解析 CFF 表结构）
- [x] 3.2 实现 CFFSubsetter 类（生成 CFF 子集）
- [x] 3.3 修改 `extractInfo()` 处理 CFF maxp（6 字节，版本 0.5）
- [x] 3.4 修改 `makeSubset()` 分派到 CFF 子集生成

## 4. 接口层实现

- [x] 4.1 创建 `_face.py`：迁移 FontFace，修改 `addSubsetObjects()` 支持 CFF
- [x] 4.2 创建 `_encoding.py`：迁移 FontEncoding
- [x] 4.3 创建 `_font.py`：迁移 OpenTypeFont，修改 `addObjects()` 支持 CFF
- [x] 4.4 创建 `_shaping.py`：迁移 ShapedFragWord、ShapedStr

## 5. 包入口与兼容层

- [x] 5.1 创建 `__init__.py`：导出主类 + 向后兼容别名
- [x] 5.2 改造 `ttfonts.py` 为纯兼容层（导入重导出 + DeprecationWarning）

## 6. PDF 集成

- [x] 6.1 在 `pdfdoc.py` 新增 `PDFType1CFont` 类
- [x] 6.2 修改 `OpenTypeFont.addObjects()` 根据 `isCFF` 选择字体类型

## 7. 测试

- [x] 7.1 创建 `tests/test_pdfbase_otf.py`：OTF 字体加载测试
- [x] 7.2 创建 OTF 渲染测试（生成实际 PDF 文件）
- [x] 7.3 创建 OTF fallback 测试（混合字体）
- [x] 7.4 验证现有 TrueType 测试仍然通过

## 8. 引用更新

- [x] 8.1 更新 `src/reportlab/pdfbase/pdfmetrics.py` 内部引用
- [x] 8.2 更新 `src/reportlab/platypus/paragraph.py` 引用
- [x] 8.3 更新 `src/reportlab/graphics/testshapes.py` 引用
- [x] 8.4 更新测试文件中的引用（渐进式）

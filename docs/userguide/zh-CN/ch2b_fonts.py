#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
from tools.docco.rl_doc_utils import *

heading1("字体")

disc("""
本章介绍本分支引入的新统一字体系统。它通过单一 API 同时支持 TrueType (.ttf)
和 OpenType/CFF (.otf) 字体，并提供字体回退、文本 shaping 和自动子集化功能。
""")

disc("""
旧的字体模块（$reportlab.pdfbase.ttfonts$）已被重构为新的
$reportlab.pdfbase.openfonts$ 包。旧的 $TTFont$ 名称作为向后兼容别名
保留给 $OpenTypeFont$。新代码应从新位置导入。
""")

disc("""
与遗留系统（第 2a 章）相比，主要变化如下：
""")
bullet("""
统一 API：$OpenTypeFont$ 同时处理 TrueType 和 OpenType/CFF 字体。
""")
bullet("""
CFF 支持：使用 CFF 轮廓（PostScript 风格的 OTF）的 OpenType 字体现已完全支持，
包括子集化和 PDF 嵌入。
""")
bullet("""
字体回退：当主字体缺少某个字符时，自动从回退字体中替换字形。
""")
bullet("""
文本 shaping：基于 HarfBuzz 的可选文本 shaping（需要 uharfbuzz），
支持正确的连字、字距调整和复杂文字布局。
""")
bullet("""
CID Type0 CIDFont 支持：对于使用 CID keyed 编码的 CFF 字体，
系统生成正确的 CIDFontType0 + Type0 字体字典。
""")
bullet("""
动态子集化：根据实际使用的字符动态构建子集，保持 PDF 文件体积最小。
""")

heading2("基本用法：OpenTypeFont")

disc("""
主要类是 $reportlab.pdfbase.openfonts$ 包中的 $OpenTypeFont$。
它同时接受 .ttf 和 .otf 文件：
""")

eg("""
from reportlab.pdfbase.openfonts import OpenTypeFont
from reportlab.pdfbase import pdfmetrics

# 加载 TrueType 字体
font = OpenTypeFont('MyFont', 'path/to/font.ttf')
pdfmetrics.registerFont(font)

# 加载 OpenType/CFF 字体
cffFont = OpenTypeFont('MyCFFFont', 'path/to/font.otf')
pdfmetrics.registerFont(cffFont)

# 在 canvas 中使用
from reportlab.pdfgen import canvas
c = canvas.Canvas('output.pdf')
c.setFont('MyFont', 12)
c.drawString(100, 700, 'Hello from OpenTypeFont!')
c.save()
""")

disc("""
第一个参数是在 ReportLab 中引用字体的内部名称。第二个参数是字体文件的路径。
如果使用相对路径，将在当前目录和 $reportlab.rl_config.TTFSearchPath$ 指定的
目录中搜索文件。
""")

disc("""
$OpenTypeFont$ 通过读取 sfnt 头部自动检测字体是基于 TrueType 还是 CFF。
用户代码无需特殊处理。
""")

heading2("向后兼容性")

disc("""
旧的 $reportlab.pdfbase.ttfonts$ 模块仍然可用，但会发出 DeprecationWarning
警告。它现在是 $openfonts$ 包的薄兼容性包装。所有使用 $TTFont$ 的现有代码
将继续正常运行：
""")

eg("""
# 旧导入路径 - 仍然可用但已弃用
from reportlab.pdfbase.ttfonts import TTFont

# TTFont 现在是 OpenTypeFont 的别名
font = TTFont('Vera', 'Vera.ttf')  # 等同于 OpenTypeFont('Vera', 'Vera.ttf')
pdfmetrics.registerFont(font)
""")

disc("""
$reportlab.pdfbase.ttfonts$ 中提供了以下向后兼容别名：
""")
bullet("""
$TTFont$ = $OpenTypeFont$
""")
bullet("""
$TTFontParser$ = $FontParser$
""")
bullet("""
$TTFontFile$ = $FontFile$
""")
bullet("""
$TTFontFace$ = $FontFace$
""")
bullet("""
$TTFontMaker$ = $FontMaker$
""")
bullet("""
$TTEncoding$ = $FontEncoding$
""")

heading2("字体 face 属性")

disc("""
加载字体后，$face$ 属性提供了对字体度量和元数据的访问：
""")

eg("""
font = OpenTypeFont('MyFont', 'font.ttf')
face = font.face

# 基本属性
print(face.name)           # PostScript 字体名称
print(face.familyName)     # 字体家族名称
print(face.styleName)      # 样式名称（Regular, Bold 等）
print(face.unitsPerEm)     # 字体设计单位 per em
print(face.bbox)           # 边界框 [xMin, yMin, xMax, yMax]
print(face.ascent)         # 排版上升高度
print(face.descent)        # 排版下降高度
print(face.capHeight)      # 大写字母高度
print(face.italicAngle)    # 斜体角度
print(face.isCFF)          # 如果基于 CFF (OTF) 则为 True，TrueType 则为 False
print(face.isCID)          # 如果 CFF 字体使用 CID keyed 编码则为 True
print(face.defaultWidth)   # 默认字形宽度
""")

disc("""
字符宽度和字形映射：
""")

eg("""
# 检查字符是否存在
print(0x4F60 in face.charToGlyph)  # CJK 字符
print('A' in face.charToGlyph)     # 也可以使用字符串

# 获取字符宽度
width = face.getCharWidth(0x4F60)  # 宽度以 1000 单位表示
width = face.getCharWidth(ord('A'))
""")

heading2("字体回退")

disc("""
字体回退功能允许在主字体缺少某字符时自动从回退字体中替换字形。
这对于混合文本文档（例如拉丁文 + 中日韩文字，或组合符号字体与文本字体）
非常有用。
""")

disc("""
该功能由环境变量 $REPORTLAB_FONT_FALLBACK$ 控制。默认禁用：
""")

eg("""
REPORTLAB_FONT_FALLBACK=1 python your_script.py
""")

disc("""
通过 $substitutionFonts$ 属性配置回退字体：
""")

eg("""
from reportlab.pdfbase.openfonts import OpenTypeFont
from reportlab.pdfbase import pdfmetrics

primary = OpenTypeFont('NotoSans', 'NotoSans-Regular.ttf')
fallback = OpenTypeFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')

pdfmetrics.registerFont(primary)
pdfmetrics.registerFont(fallback)

primary.substitutionFonts = [fallback]

# 现在包含 CJK 字符的文本会自动回退
c.setFont('NotoSans', 12)
c.drawString(100, 700, 'Hello 你好 World')
""")

disc("""
$reportlab.pdfbase.pdfmetrics$ 中提供了便捷函数 $registerFontWithFallback$：
""")

eg("""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.openfonts import OpenTypeFont

font = pdfmetrics.registerFontWithFallback(
    'NotoSans', 'NotoSans-Regular.ttf',
    fallbackFonts=[OpenTypeFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')]
)
# 回退字体已自动注册并关联
""")

disc("""
$fallbackFonts$ 参数接受字体名字符串（通过 $getFont$ 解析）或
$OpenTypeFont$ 实例。
""")

disc("""
您可以使用 $hasGlyph()$ 检查字体是否包含特定字形：
""")

eg("""
font = OpenTypeFont('MyFont', 'font.ttf')
font.hasGlyph('A')          # True
font.hasGlyph('你')          # 如果字体缺少 CJK 字形则为 False
font.hasGlyph(0x4F60)       # 同上，使用 Unicode 码点
""")

heading2("为 Platypus 注册字体家族")

disc("""
要在 Platypus 段落中配合 $&lt;b&gt;$ 和 $&lt;i&gt;$ 标签使用 OpenType 字体，
请注册一个映射样式变体的字体家族：
""")

eg("""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.openfonts import OpenTypeFont

pdfmetrics.registerFont(OpenTypeFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(OpenTypeFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(OpenTypeFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(OpenTypeFont('VeraBI', 'VeraBI.ttf'))

pdfmetrics.registerFontFamily(
    'Vera',
    normal='Vera',
    bold='VeraBd',
    italic='VeraIt',
    boldItalic='VeraBI'
)
""")

disc("""
如果只有常规字重可用，将所有变体映射到同一个字体：
""")

eg("""
pdfmetrics.registerFontFamily(
    'MyFont',
    normal='MyFont',
    bold='MyFont',
    italic='MyFont',
    boldItalic='MyFont'
)
""")

heading2("文本 shaping（HarfBuzz）")

disc("""
当安装了 $uharfbuzz$ 时，ReportLab 可以执行文本 shaping 以实现正确的
连字、字距调整和复杂文字定位。shaping 系统内置于段落布局引擎中，
对于设置了 $shapable$ 属性的字体自动启用。
""")

disc("""
shaping 系统提供以下 API：
""")
bullet("""
$shapeFragWord(w)$：对 platypus frag word 进行 shaping，返回 $ShapedFragWord$。
""")
bullet("""
$shapeStr(s, fontName, fontSize)$：对纯字符串进行 shaping，返回 $ShapedStr$。
""")
bullet("""
$ShapedStr$：携带每个字符定位数据的字符串子类。
""")

disc("""
您可以检查字体是否可进行 shaping：
""")

eg("""
font = OpenTypeFont('MyFont', 'font.ttf')
print(font.shapable)  # 如果安装了 uharfbuzz 且字体通过过滤条件则为 True
""")

disc("""
要禁用特定字体的 shaping，请将 glob 模式添加到
$reportlab.rl_config.unShapedFontGlob$：
""")

eg("""
import reportlab.rl_config
reportlab.rl_config.unShapedFontGlob.append('*monospace*')
""")

heading2("使用 CFF（PostScript 风格 OTF）字体")

disc("""
CFF 字体使用基于 PostScript 的轮廓数据而不是 TrueType 字形数据。
新的 $OpenTypeFont$ 类透明地处理两种类型。自动检测：
""")

eg("""
font = OpenTypeFont('MyCFF', 'font.otf')
print(font.face.isCFF)    # CFF 风格 OTF 为 True
print(font.face.isCID)    # CID keyed 字体为 True（如 CJK OTF 字体）
""")

disc("""
CID-keyed CFF 字体（在 CJK 字体中常见）经过特殊处理——它们生成 PDF
/CIDFontType0 + /Type0 字体字典，而不是标准的 /Type1 + /FontFile3 编码。
这确保了在 PDF 查看器中大字符集的正确渲染。
""")

disc("""
对于非 CID CFF 字体（例如拉丁 OTF 字体），系统生成标准的 /Type1 字体字典，
其中 /FontFile3 包含子集化的 CFF 数据，/Subtype 为 /Type1C。
""")

heading2("字体文件搜索路径")

disc("""
当提供相对字体文件路径时，ReportLab 在以下位置搜索文件：
""")
list1("当前工作目录。")
list1("$reportlab.rl_config.TTFSearchPath$ 中列出的目录。")
restartList()

disc("""
您可以配置搜索路径：
""")

eg("""
import reportlab.rl_config
reportlab.rl_config.TTFSearchPath = ['/usr/share/fonts', '/path/to/custom/fonts']
""")

heading2("TTC（TrueType Collection）支持")

disc("""
支持以 .ttc 文件（TrueType 集合）打包的字体。指定子字体索引（从 0 开始）
以选择集合中的哪个字体：
""")

eg("""
font = OpenTypeFont('MyFont', 'collection.ttc', subfontIndex=0)  # 第一个字体
font2 = OpenTypeFont('MyFont2', 'collection.ttc', subfontIndex=1)  # 第二个字体
""")

heading2("性能建议")

disc("""
对于大型字体（尤其是包含数千个字符的 CJK 字体）：
""")
bullet("""
禁用校验和验证以加快加载速度：将 $validate=0$ 传递给 $OpenTypeFont$ 构造函数。
""")
bullet("""
字体子集化是自动的——只有实际使用的字符才会嵌入到 PDF 中。
""")
bullet("""
对于 CJK 文本，考虑使用带有 CID 编码的 OTF/CFF 字体，它们可以生成更紧凑的 PDF 输出。
""")

heading2("迁移指南")

disc("""
要从旧字体系统迁移到新的统一 API：
""")
list1("将 $from reportlab.pdfbase.ttfonts import TTFont$ 替换为 $from reportlab.pdfbase.openfonts import OpenTypeFont$。")
list1("将 $TTFont(name, filename)$ 替换为 $OpenTypeFont(name, filename)$。")
list1("将 $TTFont$ 类型检查替换为 $OpenTypeFont$。")
list1("从 $reportlab.pdfbase.pdfmetrics$ 导入 $registerFontWithFallback$（位置与之前相同）。")
restartList()

disc("""
旧的 $TTFont$ 名称仍然可以作为兼容性别名使用，但会发出 $DeprecationWarning$ 警告。
新代码应直接使用 $OpenTypeFont$。
""")

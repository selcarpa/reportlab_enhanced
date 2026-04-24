#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch2a_fonts.py
from tools.docco.rl_doc_utils import *
from reportlab.lib.codecharts import SingleByteEncodingChart
from reportlab.platypus import Image
import reportlab

heading1("字体与编码")

disc("""
本章介绍字体、编码以及亚洲语言支持功能。
如果您只需要为西欧语言生成 PDF，可以先阅读下面的"Unicode 是默认编码"一节，
然后在第一次阅读时跳过其余部分。
我们期望本节内容随着时间推移而大幅扩展。我们希望开源能让我们比其他工具
更好地支持世界上更多的语言，并欢迎在这一领域提供反馈和帮助。
""")

heading2("Unicode 和 UTF8 是默认的输入编码")

disc("""
从 ReportLab 2.0 版本（2006 年 5 月）开始，所有提供给我们的 API 的文本输入
都应该使用 UTF8 编码或 Python Unicode 对象。这适用于 canvas.drawString 及相关 API 的参数、
表格单元格内容、绘图对象参数以及段落源文本。
""")


disc("""
我们曾考虑让输入编码可配置甚至依赖于区域设置，
但最终决定"显式优于隐式"。""")

disc("""
这简化了我们以前在处理希腊字母、符号等方面所做的许多工作。
要显示任何字符，只需找到其 Unicode 码位，
并确保您使用的字体能够显示该字符。""")

disc("""
如果您正在适配 ReportLab 1.x 应用程序，或者从包含单字节数据
（例如 latin-1 或 WinAnsi）的其他来源读取数据，
您需要将其转换为 Unicode。Python codecs 包现在包含了
所有常见编码的转换器，包括亚洲语言编码。
""")



disc(u"""
如果您的数据没有使用 UTF8 编码，一旦输入非 ASCII 字符，
就会得到一个 UnicodeDecodeError。例如，下面的代码片段
尝试读取并打印一系列名字，包括一个带有法语重音的名字：
^Marc-André Lemburg^。标准错误信息非常有用，
会告诉您它不喜欢哪个字符：
""")

eg(u"""
>>> from reportlab.pdfgen.canvas import Canvas
>>> c = Canvas('temp.pdf')
>>> y = 700
>>> for line in file('latin_python_gurus.txt','r'):
...     c.drawString(100, y, line.strip())
...
Traceback (most recent call last):
...
UnicodeDecodeError: 'utf8' codec can't decode bytes in position 9-11: invalid data
-->é L<--emburg
>>>
""")


disc("""
最简单的修复方法是将您的数据转换为 Unicode，
指明其原始编码，如下所示：""")

eg("""
>>> for line in file('latin_input.txt','r'):
...     uniLine = unicode(line, 'latin-1')
...     c.drawString(100, y, uniLine.strip())
>>>
>>> c.save()
""")


heading2("自动输出字体替换")

disc("""
代码中仍有一些地方会引用编码，包括 rl_config 的
defaultEncoding 参数，以及传递给各种 Font 构造函数的参数。
在过去，当人们需要使用 PDF 查看设备支持的 Symbol 和 ZapfDingbats 字体中的字形时，
这些编码非常有用。

默认情况下，标准字体（Helvetica、Courier、Times Roman）
将提供 Latin-1 中可用的字形。但是，如果我们的引擎检测到
字体中没有的字符，它会尝试切换到 Symbol 或 ZapfDingbats 来显示这些字符。
例如，如果您在调用 ^drawString^ 时包含一把右向剪刀的 Unicode 字符
✂，您应该能看到它（在 ^test_pdfgen_general.py/pdf^ 中有一个示例）。
在您的代码中无需切换字体。

""")


heading2("使用非标准 Type 1 字体")

disc("""
如上一章所述，每份 Acrobat Reader 都内置了 14 种标准字体。
因此，ReportLab PDF 库只需通过名称引用这些字体。
如果您想使用其他字体，它们必须对您的代码可用，
并且将被嵌入到 PDF 文档中。""")

disc("""
您可以使用下面描述的机制在文档中包含任意字体。
我们有一个名为 <i>DarkGardenMK</i> 的开源字体，
可用于测试和/或文档编写目的（您也可以使用它）。
它随 ReportLab 发行版一起提供，位于 $reportlab/fonts$ 目录中。
""")

disc("""
目前字体嵌入依赖于 Adobe AFM（'Adobe Font Metrics'）和 PFB（'Printer Font Binary'）
格式的字体描述文件。前者是 ASCII 文件，包含字体中字符（'字形'）的信息，
如高度、宽度、边界框信息和其他'度量数据'，而后者是描述字体形状的二进制文件。
$reportlab/fonts$ 目录包含 $'DarkGardenMK.afm'$ 和 $'DarkGardenMK.pfb'$
文件，它们被用作示例字体。
""")

disc("""
在下面的示例中，找到包含测试字体的文件夹，
并将其注册到 $pdfmetrics$ 模块中以供将来使用，
之后我们就可以像使用任何其他标准字体一样使用它。
""")


eg("""
import os
import reportlab
from reportlab.pdfgen import canvas
folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
afmFile = os.path.join(folder, 'DarkGardenMK.afm')
pfbFile = os.path.join(folder, 'DarkGardenMK.pfb')

from reportlab.pdfbase import pdfmetrics
justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
faceName = 'DarkGardenMK' # pulled from AFM file
pdfmetrics.registerTypeFace(justFace)
justFont = pdfmetrics.Font('DarkGardenMK', faceName, 'WinAnsiEncoding')
pdfmetrics.registerFont(justFont)

# Create a canvas to draw on
output_file = "output.pdf"
c = canvas.Canvas(output_file)

# Use the font and write text
c.setFont('DarkGardenMK', 32)
c.drawString(10, 150, 'This should be in')
c.drawString(10, 100, 'DarkGardenMK')

# Save the canvas
c.save()
""")


disc("""
请注意，参数 "WinAnsiEncoding" 与输入无关；
它是指定字体文件中哪组字符将被激活和可用。
""")

illust(examples.customfont1, "使用一个非常规字体")

disc("""
字体的 face name 来自 AFM 文件的 $FontName$ 字段。
在上面的示例中，我们提前知道了名称，但通常字体描述文件的名称
相当晦涩，这时您可能希望从 AFM 文件中自动获取名称。
如果没有更复杂的方法，您可以使用如下简单代码：
""")

eg("""
class FontNameNotFoundError(Exception):
    pass


def findFontName(path):
    "Extract a font name from an AFM file."

    f = open(path)

    found = 0
    while not found:
        line = f.readline()[:-1]
        if not found and line[:16] == 'StartCharMetrics':
            raise FontNameNotFoundError, path
        if line[:8] == 'FontName':
            fontName = line[9:]
            found = 1

    return fontName
""")

disc("""
在 <i>DarkGardenMK</i> 示例中，我们显式指定了要加载的字体描述文件的位置。
通常，您更希望将字体存储在某个规范的位置，
并让嵌入机制知道这些位置。使用我们在本节开头已经看到的相同配置机制，
我们可以指定 Type-1 字体的默认搜索路径。
""")

disc("""
遗憾的是，目前还没有针对此类位置的可靠标准
（即使在同一平台上也没有），因此您可能需要编辑
$reportlab_settings.py$ 或 $~/.reportlab_settings$ 文件，
以修改 $T1SearchPath$ 标识符的值，
使其包含额外的目录。我们自己的建议是在开发中使用 ^reportlab/fonts^
文件夹；在任何类型的服务器部署中，将所需的字体作为应用程序的打包部分。
这可以避免其他软件或系统管理员安装和卸载字体对您造成影响。
""")

heading3("关于缺失字形的警告")
disc("""如果您指定了编码，通常假定字体设计者已经提供了所有需要的字形。
然而，事实并非总是如此。在我们的示例字体中，
字母表中的字母是存在的，但许多符号和重音符号缺失。
默认行为是当传入无法绘制的字符时，字体打印一个 'notdef' 字符——
通常是一个色块、点或空格。但是，您可以要求库改为发出警告；
下面的代码（在加载字体之前执行）将在注册字体时
为任何不在字体中的字形生成警告。""")

eg("""
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
""")



heading2("标准单字节字体编码")
disc("""
本节向您展示常见编码中可用的字形。
""")


disc("""下面的代码表显示了 $WinAnsiEncoding$ 中的字符。
这是 Windows 和美洲及西欧许多 Unix 系统上的标准编码。
它也被称为代码页 1252（Code Page 1252），并且实际上与 ISO-Latin-1
相同（它包含一两个额外字符）。这是 ReportLab PDF 库使用的默认编码。
它是从 $reportlab/lib$ 中的标准例程 $codecharts.py$ 生成的，
该例程可用于显示字体的内容。边缘的索引编号为十六进制。""")

cht1 = SingleByteEncodingChart(encodingName='WinAnsiEncoding',charsPerRow=32, boxSize=12)
illust(lambda canv: cht1.drawOn(canv, 0, 0), "WinAnsi 编码", cht1.width, cht1.height)

disc("""下面的代码表显示了 $MacRomanEncoding$ 中的字符。
顾名思义，这是美洲和西欧 Macintosh 计算机上的标准编码。
与非 Unicode 编码一样，前 128 个码位（在本例中为顶部 4 行）
是 ASCII 标准，与上面的 WinAnsi 代码表一致；但底部 4 行不同。""")
cht2 = SingleByteEncodingChart(encodingName='MacRomanEncoding',charsPerRow=32, boxSize=12)
illust(lambda canv: cht2.drawOn(canv, 0, 0), "MacRoman 编码", cht2.width, cht2.height)

disc("""这两种编码可用于标准字体（Helvetica、Times-Roman、Courier 及其变体），
并且可用于大多数商业字体，包括 Adobe 的字体。但是，某些字体包含非文本字形，
这个概念并不真正适用。例如，ZapfDingbats 和 Symbol 可以各自被视为
拥有自己的编码。""")

cht3 = SingleByteEncodingChart(faceName='ZapfDingbats',encodingName='ZapfDingbatsEncoding',charsPerRow=32, boxSize=12)
illust(lambda canv: cht3.drawOn(canv, 0, 0), "ZapfDingbats 及其唯一编码", cht3.width, cht3.height)

cht4 = SingleByteEncodingChart(faceName='Symbol',encodingName='SymbolEncoding',charsPerRow=32, boxSize=12)
illust(lambda canv: cht4.drawOn(canv, 0, 0), "Symbol 及其唯一编码", cht4.width, cht4.height)


CPage(5)
heading2("TrueType 字体支持")
disc("""
Marius Gedminas（$mgedmin@delfi.lt$）在 Viktorija Zaksiene（$vika@pov.lt$）
的帮助下贡献了对嵌入式 TrueType 字体的支持。TrueType 字体以 Unicode/UTF8 方式工作，
不受 256 个字符的限制。""")


CPage(3)
disc("""我们使用 <b>$reportlab.pdfbase.ttfonts.TTFont$</b> 创建 TrueType
字体对象，并使用 <b>$reportlab.pdfbase.pdfmetrics.registerFont$</b> 进行注册。
在 pdfgen 中直接绘制到画布时，我们可以这样做""")
eg("""
import os
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

# we know some glyphs are missing, suppress warnings
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

# Create a canvas to draw on
output_file = "output.pdf"
c = canvas.Canvas(output_file)

c.setFont('Vera', 32)
c.drawString(10, 150, "Some text encoded in UTF-8")
c.drawString(10, 100, "In the Vera TT Font!")

# Save the canvas
c.save()
""")
illust(examples.ttffont1, "使用 Vera TrueType 字体")
disc("""在上面的示例中，TrueType 字体对象是使用以下方式创建的""")
eg("""
    TTFont(name,filename)
""")
disc("""其中第一个参数指定 ReportLab 内部名称，第二个参数是表示字体 TTF 文件的
字符串（或类文件对象）。在 Marius 的原始补丁中，文件名应该完全正确，
但我们做了修改，使得如果文件名是相对路径，
则会在当前目录以及 $reportlab.rl_config.TTFSearchpath$ 指定的目录中
搜索对应的文件！""")

from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Vera',normal='Vera',bold='VeraBd',italic='VeraIt',boldItalic='VeraBI')

disc("""在 Platypus 中使用 TT 字体之前，我们应该添加从字体系列名称到
各个字体名称的映射，这些名称描述了在 $&lt;b&gt;$ 和 $&lt;i&gt;$ 属性下的行为。""")

eg("""
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Vera',normal='Vera',bold='VeraBd',italic='VeraIt',boldItalic='VeraBI')
""")

disc("""如果我们只有 Vera 常规字体，没有粗体或斜体，那么我们必须将所有字体
映射到相同的内部字体名称。^&lt;b&gt;^ 和 ^&lt;i&gt;^ 标签现在可以安全使用，
但没有效果。按照上述方式注册和映射 Vera 字体后，
我们可以使用如下段落文本""")
parabox2("""<font name="Times-Roman" size="14">This is in Times-Roman</font>
<font name="Vera" color="magenta" size="14">and this is in magenta <b>Vera!</b></font>""","在段落中使用 TTF 字体")

heading3("TrueType 字体回退（实验性功能）")
disc("""
这是一项实验性功能。当 TrueType 字体不包含某个字符的字形时，
ReportLab 可以自动回退到替代字体。
这对于混合文本文档（如拉丁文 + 中日韩文字）非常有用。
""")
disc("""
该功能默认禁用。设置环境变量 $REPORTLAB_FONT_FALLBACK=1$ 以启用它。
""")
eg("""
REPORTLAB_FONT_FALLBACK=1 python your_script.py
""")
disc("""
通过设置 TTFont 上的 $substitutionFonts$ 属性来配置回退字体：
""")
eg("""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font = TTFont('NotoSans', 'NotoSans-Regular.ttf')
fallback = TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')
pdfmetrics.registerFont(font)
pdfmetrics.registerFont(fallback)
font.substitutionFonts = [fallback]
# Now mixed-script text will automatically use the fallback font
c.setFont('NotoSans', 12)
c.drawString(100, 700, 'Hello 你好 World')
""")
disc("""
还提供了一个便捷函数 $registerFontWithFallback$：
""")
eg("""
font = pdfmetrics.registerFontWithFallback(
    'NotoSans', 'NotoSans-Regular.ttf',
    fallbackFonts=[TTFont('NotoSansCJK', 'NotoSansCJK-Regular.ttf')]
)
""")
disc("""您可以使用 $hasGlyph()$ 检查字体是否包含特定字形：
""")
eg("""
font.hasGlyph('A')        # True
font.hasGlyph(0x4F60)     # False if font lacks CJK glyphs
""")

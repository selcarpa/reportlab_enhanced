from tools.docco.rl_doc_utils import *
from reportlab.lib.codecharts import SingleByteEncodingChart
from reportlab.platypus import Image
import reportlab

heading2("亚洲字体支持")
disc("""ReportLab PDF 库旨在为亚洲字体提供完整支持。
PDF 是第一个真正可移植的亚洲文本处理解决方案。主要有两种方法：
Adobe 的亚洲语言包，或 TrueType 字体。
""")

heading3("亚洲语言包")
disc("""
这种方法提供最佳性能，因为不需要在 PDF 文件中嵌入任何内容；
与标准字体一样，一切都在阅读器端。
""")

disc("""
Adobe 为每种主要语言提供附加组件。在 Adobe Reader 6.0 和 7.0 中，
当您尝试打开使用这些字体的文档时，系统会提示您下载并安装它们。
在早期版本中，打开亚洲文档时会看到错误消息，
需要知道该怎么做。
""")

disc("""
日语、繁体中文（台湾/香港）、简体中文（中国大陆）
和韩语都受支持，我们的软件了解以下字体：
""")
bullet("""
$chs$ = 简体中文（大陆）：'$STSong-Light$'
""")
bullet("""
$cht$ = 繁体中文（台湾）：'$MSung-Light$'、'$MHei-Medium$'
""")
bullet("""
$kor$ = 韩语：'$HYSMyeongJoStd-Medium$'、'$HYGothic-Medium$'
""")
bullet("""
$jpn$ = 日语：'$HeiseiMin-W3$'、'$HeiseiKakuGo-W5$'
""")


disc("""由于许多用户没有安装字体包，我们包含了一张
日语字符的^位图^（分辨率较低）。我们将在下面讨论生成它们所需的内容。""")
# include a bitmap of some Asian text
I=os.path.join(os.path.dirname(reportlab.__file__),'docs','images','jpnchars.jpg')
try:
    getStory().append(Image(I))
except:
    disc("""此处应该显示一张图片。""")

disc("""在 2.0 版本之前，注册 CID 字体时必须指定众多本地编码之一。
在 2.0 版本中，您应该使用新的 UnicodeCIDFont 类。""")

eg("""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# Create a canvas to draw on
output_file = "output.pdf"
c = canvas.Canvas(output_file)

c.setFont('HeiseiMin-W3', 16)

# the two unicode characters below are "Tokyo"
msg = u'\\u6771\\u4EAC : Unicode font, unicode input'
c.drawString(100, 675, msg)
""")
#had to double-escape the slashes above to get escapes into the PDF

disc("""带有显式编码的旧编码风格仍然有效，但现在仅在需要构建
垂直文本时才相关。我们计划在未来为 UnicodeCIDFont 构造函数添加
更易读的水平和垂直文本选项。以下四个测试脚本生成相应语言的示例：""")
eg("""tests/test_multibyte_jpn.py
tests/test_multibyte_kor.py
tests/test_multibyte_chs.py
tests/test_multibyte_cht.py""")

## put back in when we have vertical text...
##disc("""The illustration below shows part of the first page
##of the Japanese output sample.  It shows both horizontal and vertical
##writing, and illustrates the ability to mix variable-width Latin
##characters in Asian sentences.  The choice of horizontal and vertical
##writing is determined by the encoding, which ends in 'H' or 'V'.
##Whether an encoding uses fixed-width or variable-width versions
##of Latin characters also depends on the encoding used; see the definitions
##below.""")
##
##Illustration(image("../images/jpn.gif", width=531*0.50,
##height=435*0.50), 'Output from test_multibyte_jpn.py')
##
##caption("""
##Output from test_multibyte_jpn.py
##""")




disc("""在早期版本的 ReportLab PDF 库中，我们必须使用 Adobe 的 CMap 文件
（位于 Acrobat Reader 附近，如果安装了亚洲语言包的话）。
现在我们只需要处理一种编码，字符宽度数据已嵌入到包中，
生成时不再需要 CMap 文件。^rl_config.py^ 中的 CMap 搜索路径
现在已弃用，如果您仅使用 UnicodeCIDFont，它不会产生任何效果。
""")


heading3("包含亚洲字符的 TrueType 字体")
disc("""
这是最简单的方法。使用亚洲 TrueType 字体完全不需要特殊处理。
例如，在"控制面板"中安装了日语选项的 Windows 用户，
将拥有一个 "msmincho.ttf" 字体可以使用。但请注意，
解析字体需要时间，而且可能需要在 PDF 中嵌入相当大的子集。
我们现在还可以解析以 .ttc 结尾的文件，它是 .ttf 的一个小变体。

""")


heading3("待办事项")
disc("""我们预计将在一段时间内持续开发此包的这一领域。
以下是主要优先事项的概要。我们欢迎您的帮助！""")

bullet("""
确保我们在水平和垂直书写中拥有所有编码的准确字符度量数据。""")

bullet("""
为 ^UnicodeCIDFont^ 添加选项，以允许在字体支持的情况下使用垂直和比例变体。""")


bullet("""
改进段落中的自动换行代码，并允许垂直书写。""")



CPage(5)
heading2("RenderPM 测试")

disc("""这里也许是提及 $reportlab/graphics/renderPM.py$ 测试函数的最佳位置，
它可以被认为是测试 renderPM（即"像素映射渲染器"，
与 renderPDF、renderPS 或 renderSVG 相对）的规范位置。""")

disc("""如果您从命令行运行它，应该会看到大量如下输出。""")

eg("""C:\\code\\reportlab\\graphics>renderPM.py
wrote pmout\\renderPM0.gif
wrote pmout\\renderPM0.tif
wrote pmout\\renderPM0.png
wrote pmout\\renderPM0.jpg
wrote pmout\\renderPM0.pct
...
wrote pmout\\renderPM12.gif
wrote pmout\\renderPM12.tif
wrote pmout\\renderPM12.png
wrote pmout\\renderPM12.jpg
wrote pmout\\renderPM12.pct
wrote pmout\\index.html""")

disc("""它运行一系列测试，从"Hello World"测试开始，
依次测试各种线条；不同大小、字体、颜色和对齐方式的文本字符串；
基本形状；平移和旋转的组；缩放坐标；旋转字符串；嵌套组；
锚定和非标准字体。""")

disc("""它创建一个名为 $pmout$ 的子目录，将图像文件写入其中，
并写入一个 $index.html$ 页面，方便查看所有结果。""")

disc("""您可能想查看的字体相关测试是测试 #11（'非标准字体中的文本字符串'）
和测试 #12（'测试各种字体'）。""")




##### FILL THEM IN

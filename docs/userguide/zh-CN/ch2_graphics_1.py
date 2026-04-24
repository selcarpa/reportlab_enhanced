#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch2_graphics.py
from tools.docco.rl_doc_utils import *
from reportlab.lib.codecharts import SingleByteEncodingChart

heading1("使用 $pdfgen$ 进行图形和文本处理")

heading2("基本概念")
disc("""
$pdfgen$ 包是生成 PDF 文档的最低层接口。一个 $pdfgen$ 程序本质上
是一系列指令，用于将文档"绘制"到一系列页面上。提供绘制操作的
接口对象就是 $pdfgen canvas$。
""")

disc("""
画布可以被想象成一张白纸，纸上的点使用笛卡尔 ^(X,Y)^ 坐标系来标识，
默认情况下 ^(0,0)^ 原点位于页面的左下角。此外，第一个坐标 ^x^ 向右延伸，
第二个坐标 ^y^ 向上延伸。
""")

disc("""
下面是一个使用画布的简单示例程序。
""")

eg("""
    from reportlab.pdfgen import canvas
    def hello(c):
        c.drawString(100,100,"Hello World")
    c = canvas.Canvas("hello.pdf")
    hello(c)
    c.showPage()
    c.save()
""")

disc("""
上面的代码创建了一个 $canvas$ 对象，它将在当前工作目录中生成
一个名为 $hello.pdf$ 的 PDF 文件。然后它调用 $hello$ 函数，
将 $canvas$ 作为参数传入。最后，$showPage$ 方法保存画布的当前页面，
$save$ 方法存储文件并关闭画布。
""")

disc("""
$showPage$ 方法使 $canvas$ 停止在当前页面上绘制，
后续的任何操作将在后续页面上绘制（如果有的话——如果没有后续操作，
则不会创建新页面）。$save$ 方法必须在文档构建完成后调用——
它生成 PDF 文档，这也是 $canvas$ 对象的全部目的。
""")

heading2("关于画布的更多信息")
disc("""
在描述绘制操作之前，我们先岔开话题，介绍一下可以用来配置画布的一些操作。
有许多不同的设置可供使用。如果您是 Python 新手，或者迫不及待地想要生成一些输出，
您可以先跳过这一部分，但稍后请回来阅读！""")

disc("""首先，我们来看看画布的构造函数参数：""")

eg("""    def __init__(self,filename,
                 pagesize=(595.27,841.89),
                 bottomup = 1,
                 pageCompression=0,
                 encoding=rl_config.defaultEncoding,
                 verbosity=0
                 encrypt=None):
                 """)

disc("""$filename$ 参数控制最终 PDF 文件的名称。
您也可以传入任何打开的二进制流（例如 $sys.stdout$，即带有二进制编码的 Python 进程标准输出），
PDF 文档将写入该流。由于 PDF 是二进制格式，在它之前或之后写入其他内容时需要小心；
您不能在 HTML 页面中间内联传递 PDF 文档！""")

disc("""$pagesize$ 参数是一个由两个数字组成的元组，单位为磅（1/72 英寸）。
画布默认为 $A4$（一种国际标准页面尺寸，与美国标准的 $letter$ 页面尺寸不同），
但最好明确指定。大多数常见的页面尺寸可以在库模块 $reportlab.lib.pagesizes$ 中找到，
因此您可以使用如下表达式""")

eg("""from reportlab.lib.pagesizes import letter, A4
myCanvas = Canvas('myfile.pdf', pagesize=letter)
width, height = letter  #keep for later
""")

pencilnote()

disc("""如果您的文档打印出现问题，请确保您使用了正确的页面尺寸（通常是 $A4$ 或 $letter$）。
有些打印机在页面过大或过小时无法正常工作。""")

disc("""很多时候，您需要根据页面尺寸进行计算。在上面的示例中，我们提取了宽度和高度。
在程序的后面部分，我们可以使用 $width$ 变量来定义右边距为 $width - inch$，
而不是使用常量。使用变量后，即使页面尺寸发生变化，边距仍然合理。""")

disc("""$bottomup$ 参数用于切换坐标系。某些图形系统（如 PDF 和 PostScript）
将 (0,0) 放在页面左下角，而其他系统（如许多图形用户界面 [GUI]）
将原点放在左上角。$bottomup$ 参数已被弃用，未来可能会被移除""")

todo("""需要验证它是否在所有任务中都能正常工作，如果不能，则将其移除""")

disc("""$pageCompression$ 选项决定每页的 PDF 操作流是否被压缩。
默认情况下页面流不被压缩，因为压缩会减慢文件生成过程。
如果输出大小很重要，请设置 $pageCompression=1$，但请记住，
压缩后的文档会更小，但生成速度会更慢。请注意，图像<i>总是</i>被压缩的，
此选项仅在每页有大量文本和矢量图形时才能节省空间。""")

disc("""$encoding$ 参数在 2.0 版本中已基本过时，99% 的用户可以忽略它。
其默认值即可满足需求，除非您特别需要使用 MacRoman 中存在而 Winansi 中不存在的
约 25 个字符。相关参考请参见：
<font color="blue"><u><a href="http://www.alanwood.net/demos/charsetdiffs.html">http://www.alanwood.net/demos/charsetdiffs.html</a></u></font>。

该参数决定标准 Type 1 字体使用的字体编码；这应该与您系统上的编码相对应。
请注意，这是<i>字体内部</i>使用的编码；您传递给 ReportLab 工具包进行渲染的文本
应始终是 Python unicode 字符串对象或 UTF-8 编码的字节字符串（参见下一章）！
字体编码目前有两个值：$'WinAnsiEncoding'$ 或 $'MacRomanEncoding'$。
上面的变量 $rl_config.defaultEncoding$ 指向前者，这是 Windows、Mac OS X
和许多 Unix 系统（包括 Linux）上的标准。如果您是 Mac 用户且没有 OS X，
可能需要进行全局更改：修改 <i>reportlab/pdfbase/pdfdoc.py</i> 顶部的行来切换。
否则，您可能完全可以忽略此参数，永远不需要传递它。
对于所有 TTF 字体和常用的 CID 字体，此处传入的编码会被忽略，
因为 ReportLab 库本身知道这些字体的正确编码。""")

disc("""演示脚本 $reportlab/demos/stdfonts.py$ 会打印两份测试文档，
显示所有字体中的所有码点，以便您查找字符。特殊字符可以使用通常的 Python
转义序列插入到字符串命令中；例如 \\101 = 'A'。""")

disc("""$verbosity$ 参数决定打印多少日志信息。默认为零，
以帮助需要从标准输出捕获 PDF 的应用程序。当值为 1 时，
每次生成文档时您都会收到一条确认消息。更高的数字将来可能会提供更多输出。""")

disc("""$encrypt$ 参数决定文档是否加密以及如何加密。
默认情况下，文档不加密。如果 $encrypt$ 是一个字符串对象，
它将用作 PDF 的用户密码。如果 $encrypt$ 是 $reportlab.lib.pdfencrypt.StandardEncryption$
的一个实例，则使用该对象来加密 PDF。这允许对加密设置进行更细粒度的控制。
加密将在第 4 章中更详细地介绍。""")

todo("待完成 - 所有信息函数和其他非绘制内容")
todo("""涵盖所有构造函数参数，以及 setAuthor 等。""")

heading2("绘制操作")
disc("""
假设上面引用的 $hello$ 函数实现如下（我们暂不详细解释每个操作）。
""")

eg(examples.testhello)

disc("""
查看这段代码，可以注意到使用画布执行的操作本质上分为两种类型。
第一种类型在页面上绘制内容，例如文本字符串、矩形或线条。
第二种类型更改画布的状态，例如更改当前填充或描边颜色，
或更改当前字体的类型和大小。
""")

disc("""
如果我们将程序想象成一位在画布上工作的画家，"绘制"操作使用当前的
工具集（颜色、线条样式、字体等）在画布上涂色，
而"状态更改"操作则更改当前工具之一（例如将填充颜色从之前的颜色更改为蓝色，
或将当前字体更改为 15 磅的 $Times-Roman$）。
""")

disc("""
上面列出的"Hello World"程序生成的文档将包含以下图形。
""")

illust(examples.hello, '$pdfgen$ 中的 "Hello World"')

heading3("关于本文档中的演示")

disc("""
本文档包含所讨论代码的演示，如上面矩形中所示的示例。
这些演示绘制在嵌入在本指南实际页面中的"迷你页面"上。
迷你页面宽 %s 英寸，高 %s 英寸。演示显示的是演示代码的实际输出。
为方便起见，输出的大小略有缩小。
""" % (examplefunctionxinches, examplefunctionyinches))

heading2('工具：绘图操作')

disc("""
本节简要列出了程序可用于通过画布接口在页面上绘制信息的可用工具。
这些工具将在后面的章节中详细讨论。此处列出是为了方便参考和总结。
""")

heading3("线条方法")

eg("""canvas.line(x1,y1,x2,y2)""")
eg("""canvas.lines(linelist)""")

disc("""
线条方法在画布上绘制直线段。
""")

heading3("形状方法")

eg("""canvas.grid(xlist, ylist) """)
eg("""canvas.bezier(x1, y1, x2, y2, x3, y3, x4, y4)""")
eg("""canvas.arc(x1,y1,x2,y2) """)
eg("""canvas.rect(x, y, width, height, stroke=1, fill=0) """)
eg("""canvas.ellipse(x1,y1, x2,y2, stroke=1, fill=0)""")
eg("""canvas.wedge(x1,y1, x2,y2, startAng, extent, stroke=1, fill=0) """)
eg("""canvas.circle(x_cen, y_cen, r, stroke=1, fill=0)""")
eg("""canvas.roundRect(x, y, width, height, radius, stroke=1, fill=0) """)

disc("""
形状方法在画布上绘制常见的复杂形状。
""")

heading3("字符串绘制方法")

eg("""canvas.drawString(x, y, text):""")
eg("""canvas.drawRightString(x, y, text) """)
eg("""canvas.drawCentredString(x, y, text)""")

disc("""
字符串绘制方法在画布上绘制单行文本。
""")

heading3("文本对象方法")
eg("""textobject = canvas.beginText(x, y) """)
eg("""canvas.drawText(textobject) """)

disc("""
文本对象用于以 $canvas$ 接口不直接支持的方式格式化文本。
程序使用 $beginText$ 从 $canvas$ 创建文本对象，
然后通过调用 $textobject$ 的方法来格式化文本。
最后使用 $drawText$ 将 $textobject$ 绘制到画布上。
""")

heading3("路径对象方法")

eg("""path = canvas.beginPath() """)
eg("""canvas.drawPath(path, stroke=1, fill=0, fillMode=None) """)
eg("""canvas.clipPath(path, stroke=1, fill=0, fillMode=None) """)

disc("""
路径对象类似于文本对象：它们为执行画布接口不直接提供的复杂图形绘制
提供了专门的控制。程序使用 $beginPath$ 创建路径对象，
使用路径对象的方法用图形填充路径，
然后使用 $drawPath$ 在画布上绘制路径。""")

disc("""也可以使用 $clipPath$ 方法将路径用作"裁剪区域"——
例如，可以使用圆形路径裁剪掉矩形图像的外部部分，
使页面上只显示图像的圆形部分。
""")

disc("""如果指定了 $fill=1$，则可以使用 $fillMode$ 参数设置 0=$even-odd$ 或 1=$non-zero$ 填充模式。
这将改变复杂路径的填充方式。如果使用默认值 $None$，
则使用画布的 $_fillMode$ 属性值（通常为 $0$，即 $even-odd$）。""")

heading3("图像方法")
pencilnote()
disc("""
您需要 Python Imaging Library (PIL) 才能在 ReportLab 包中使用图像。
运行 $tests$ 子目录中的脚本 $test_pdfgen_general.py$ 并查看输出的第 7 页，
可以找到下面技术的示例。
""")

disc("""
有两种听起来相似的图像绘制方法。首选方法是 $drawImage$。
它实现了缓存系统，因此您可以定义一次图像并多次绘制；
它在 PDF 文件中只会存储一次。$drawImage$ 还公开了一个高级参数——
透明蒙版，未来还会公开更多参数。较旧的技术 $drawInlineImage$ 将位图存储在页面流中，
因此如果您在文档中多次使用同一图像会非常低效；但如果图像非常小且不重复，
则可以生成渲染更快的 PDF。我们先讨论最旧的方法：
""")

eg("""canvas.drawInlineImage(self, image, x,y, width=None,height=None) """)

disc("""
$drawInlineImage$ 方法将图像放置在画布上。$image$ 参数可以是 PIL Image 对象
或图像文件名。支持许多常见的文件格式，包括 GIF 和 JPEG。
它返回实际图像的像素大小，以 (width, height) 元组形式表示。
""")

eg("""canvas.drawImage(self, image, x,y, width=None,height=None,mask=None) """)
disc("""
参数和返回值与 $drawInlineImage$ 相同。但是，我们使用了缓存系统；
给定的图像仅在第一次使用时存储，后续使用时只进行引用。
如果您提供文件名，它假定相同的文件名意味着相同的图像。
如果您提供 PIL 图像，它会测试内容是否实际发生了更改，然后再重新嵌入。""")

disc("""
$mask$ 参数让您可以创建透明图像。它接受 6 个数字，
定义将被遮罩或视为透明的 RGB 值范围。例如，使用 [0,2,40,42,136,139]，
它将遮盖红色值为 0 或 1、绿色值为 40 或 41、蓝色值为 136、137 或 138
的任何像素（在 0-255 的范围内）。目前您需要自己知道哪种颜色是"透明的"
或背景色。""")

disc("""PDF 支持许多图像功能，我们将随着时间的推移公开更多功能，
可能会通过向 $drawImage$ 添加额外的关键字参数来实现。""")

heading3("结束页面")

eg("""canvas.showPage()""")

disc("""$showPage$ 方法结束当前页面。所有后续绘制将在另一页上进行。""")

pencilnote()

disc("""警告！在 $pdfgen$ 中前进到新页面时，所有状态更改（字体更改、颜色设置、几何变换等）
都会被遗忘。任何您希望保留的状态设置都必须在程序继续绘制之前重新设置！""")

heading2('工具箱：状态更改操作')

disc("""
本节简要列出了切换程序通过 $canvas$ 接口在页面上绘制信息所用工具的方法。
这些方法也将在后面的章节中详细讨论。
""")

heading3("更改颜色")
eg("""canvas.setFillColorCMYK(c, m, y, k) """)
eg("""canvas.setStrikeColorCMYK(c, m, y, k) """)
eg("""canvas.setFillColorRGB(r, g, b) """)
eg("""canvas.setStrokeColorRGB(r, g, b) """)
eg("""canvas.setFillColor(acolor) """)
eg("""canvas.setStrokeColor(acolor) """)
eg("""canvas.setFillGray(gray) """)
eg("""canvas.setStrokeGray(gray) """)

disc("""
PDF 支持三种不同的颜色模型：灰度、加色（红/绿/蓝即 RGB）
和带明暗参数的减色（青/品红/黄/黑即 CMYK）。
ReportLab 包还提供了诸如 $lawngreen$ 等命名颜色。
图形状态中有两个基本颜色参数：用于图形内部填充的 $Fill$ 颜色
和用于图形边界描边的 $Stroke$ 颜色。上述方法支持使用四种颜色规格中的任何一种
来设置填充或描边颜色。
""")

heading3("更改字体")
eg("""canvas.setFont(psfontname, size, leading = None) """)

disc("""
$setFont$ 方法将当前文本字体更改为给定的类型和大小。
$leading$ 参数指定从一行文本前进到下一行时向下移动的距离。
""")

heading3("更改图形线条样式")

eg("""canvas.setLineWidth(width) """)
eg("""canvas.setLineCap(mode) """)
eg("""canvas.setLineJoin(mode) """)
eg("""canvas.setMiterLimit(limit) """)
eg("""canvas.setDash(self, array=[], phase=0) """)

disc("""
PDF 中绘制的线条可以呈现多种图形样式。
线条可以有不同的宽度，可以以不同的端点样式结束，
可以以不同的连接样式相交，可以是连续的，也可以是点线或虚线。
上述方法调整这些不同的参数。""")

heading3("更改几何变换")

eg("""canvas.setPageSize(pair) """)
eg("""canvas.transform(a,b,c,d,e,f): """)
eg("""canvas.translate(dx, dy) """)
eg("""canvas.scale(x, y) """)
eg("""canvas.rotate(theta) """)
eg("""canvas.skew(alpha, beta) """)

disc("""
所有 PDF 绘制都适应指定的页面大小。在指定页面大小之外绘制的元素不可见。
此外，所有绘制的元素都经过仿射变换，该变换可能会调整它们的位置
和/或扭曲它们的外观。$setPageSize$ 方法调整当前页面大小。
$transform$、$translate$、$scale$、$rotate$ 和 $skew$ 方法
向当前变换添加额外的变换。重要的是要记住，这些变换是<i>增量</i>的——
新变换修改当前变换（但不会替换它）。
""")

heading3("状态控制")

eg("""canvas.saveState() """)
eg("""canvas.restoreState() """)

disc("""
通常，保存当前字体、图形变换、线条样式和其他图形状态以便稍后恢复是很重要的。
$saveState$ 方法标记当前图形状态，以便稍后通过匹配的 $restoreState$ 进行恢复。
请注意，保存和恢复方法的调用必须匹配——restore 调用将状态恢复到
最近保存但尚未恢复的状态。但是，您不能在一个页面上保存状态
然后在下一个页面上恢复——页面之间不保留任何状态。""")

heading2("其他 $canvas$ 方法")

disc("""
并非所有 $canvas$ 对象的方法都属于"工具"或"工具箱"类别。
以下是一些不太容易归类的杂项方法，列在此处是为了完整性。
""")

eg("""
 canvas.setAuthor()
 canvas.addOutlineEntry(title, key, level=0, closed=None)
 canvas.setTitle(title)
 canvas.setSubject(subj)
 canvas.pageHasData()
 canvas.showOutline()
 canvas.bookmarkPage(name)
 canvas.bookmarkHorizontalAbsolute(name, yhorizontal)
 canvas.doForm()
 canvas.beginForm(name, lowerx=0, lowery=0, upperx=None, uppery=None)
 canvas.endForm()
 canvas.linkAbsolute(contents, destinationname, Rect=None, addtopage=1, name=None, **kw)
 canvas.linkRect(contents, destinationname, Rect=None, addtopage=1, relative=1, name=None, **kw)
 canvas.getPageNumber()
 canvas.addLiteral()
 canvas.getAvailableFonts()
 canvas.stringWidth(self, text, fontName, fontSize, encoding=None)
 canvas.setPageCompression(onoff=1)
 canvas.setPageTransition(self, effectname=None, duration=1,
                        direction=0,dimension='H',motion='I')
""")

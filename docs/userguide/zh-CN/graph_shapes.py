#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__='3.3.0'
from tools.docco.rl_doc_utils import *
from reportlab.graphics.shapes import *

heading2("图形形状")

disc("""
本节介绍图形形状的概念及其作为图形库所有输出构建块的重要性。
我们将介绍现有形状的一些属性及其与图表之间的关系，
并简要介绍针对不同输出格式使用不同渲染器的概念。
""")

heading3("可用的图形形状")

disc("""
绘图由图形形状组成。通过组合同一组基本形状，几乎可以构建出任何内容。
模块 $shapes.py$ 提供了许多基本形状和构造，可以将其添加到绘图中。
它们包括：
""")

bullet("Rect（矩形）")
bullet("Circle（圆形）")
bullet("Ellipse（椭圆）")
bullet("Wedge（楔形，即饼图切片）")
bullet("Polygon（多边形）")
bullet("Line（直线）")
bullet("PolyLine（折线）")
bullet("String（字符串）")
bullet("Group（组）")
bullet("Path（路径，<i>尚未实现，但将在未来添加</i>）")

disc("""
下面的绘图取自我们的测试套件，展示了大部分基本形状（组除外）。
具有填充绿色表面的形状也被称为<i>实心形状</i>
（包括 $Rect$、$Circle$、$Ellipse$、$Wedge$ 和 $Polygon$）。
""")

from reportlab.graphics import testshapes

t = testshapes.getDrawing06()
draw(t, "基本图形形状")


heading3("形状属性")

disc("""
形状有两种属性——一种用于定义其几何形状，另一种用于定义其样式。
让我们创建一个带有 3 磅粗绿色边框的红色矩形：
""")

eg("""
>>> from reportlab.graphics.shapes import Rect
>>> from reportlab.lib.colors import red, green
>>> r = Rect(5, 5, 200, 100)
>>> r.fillColor = red
>>> r.strokeColor = green
>>> r.strokeWidth = 3
>>>
""")

from reportlab.graphics.shapes import Rect
from reportlab.lib.colors import red, green
d = Drawing(220, 120)
r = Rect(5, 5, 200, 100)
r.fillColor = red
r.strokeColor = green
r.strokeWidth = 3
d.add(r)
draw(d, "带有绿色边框的红色矩形")

disc("""
<i>注意：在后续示例中，我们将省略导入语句。</i>
""")

disc("""
所有形状都有许多可以设置的属性。在交互式提示符下，
我们可以使用它们的 <i>dumpProperties()</i> 方法来列出这些属性。
以下是可用于配置 Rect 的属性：
""")

eg("""
>>> r.dumpProperties()
fillColor = Color(1.00,0.00,0.00)
height = 100
rx = 0
ry = 0
strokeColor = Color(0.00,0.50,0.00)
strokeDashArray = None
strokeLineCap = 0
strokeLineJoin = 0
strokeMiterLimit = 0
strokeWidth = 3
width = 200
x = 5
y = 5
>>>
""")

disc("""
形状通常具有<i>样式属性</i>和<i>几何属性</i>。
$x$、$y$、$width$ 和 $height$ 是几何属性的一部分，
在创建矩形时必须提供，因为缺少这些属性就毫无意义。
其他属性是可选的，并具有合理的默认值。
""")

disc("""
您可以在后续行中设置其他属性，或者将它们作为可选参数传递给构造函数。
我们也可以这样创建矩形：
""")

eg("""
>>> r = Rect(5, 5, 200, 100,
             fillColor=red,
             strokeColor=green,
             strokeWidth=3)
""")

disc("""
让我们逐一介绍样式属性。$fillColor$ 很直观。
$stroke$ 是出版术语中指形状边缘的描边；描边具有颜色、宽度、可能的虚线模式，
以及一些（很少使用的）处理线条拐角的功能。
$rx$ 和 $ry$ 是可选的几何属性，用于定义圆角矩形的圆角半径。
""")

disc("所有其他实心形状共享相同的样式属性。")


heading3("线条")

disc("""
我们提供了单条直线、折线和曲线。线条具有所有 $stroke*$ 属性，但没有 $fillColor$。
以下是一些 Line 和 PolyLine 示例及相应的图形输出：
""")

eg("""
    Line(50,50, 300,100,
         strokeColor=colors.blue, strokeWidth=5)
    Line(50,100, 300,50,
         strokeColor=colors.red,
         strokeWidth=10,
         strokeDashArray=[10, 20])
    PolyLine([120,110, 130,150, 140,110, 150,150, 160,110,
              170,150, 180,110, 190,150, 200,110],
             strokeWidth=2,
             strokeColor=colors.purple)
""")

d = Drawing(400, 200)
d.add(Line(50,50, 300,100,strokeColor=colors.blue, strokeWidth=5))
d.add(Line(50,100, 300,50,
           strokeColor=colors.red,
           strokeWidth=10,
           strokeDashArray=[10, 20]))
d.add(PolyLine([120,110, 130,150, 140,110, 150,150, 160,110,
          170,150, 180,110, 190,150, 200,110],
         strokeWidth=2,
         strokeColor=colors.purple))
draw(d, "Line 和 PolyLine 示例")


heading3("字符串")

disc("""
ReportLab Graphics 包并非为复杂的文本排版而设计，
但它可以在所需位置放置字符串，并支持左/右/居中对齐。
让我们创建一个 $String$ 对象并查看其属性：
""")

eg("""
>>> s = String(10, 50, 'Hello World')
>>> s.dumpProperties()
fillColor = Color(0.00,0.00,0.00)
fontName = Times-Roman
fontSize = 10
text = Hello World
textAnchor = start
x = 10
y = 50
>>>
""")

disc("""
字符串有一个 textAnchor 属性，其值可以是 'start'、'middle' 或 'end'。
如果设置为 'start'，则 x 和 y 对应字符串的起始位置，依此类推。
这提供了一种简单的文本对齐方式。
""")

disc("""
字符串使用通用字体标准：Acrobat Reader 中的 Type 1 Postscript 字体。
因此，我们可以在 ReportLab 中使用基本的 14 种字体，并获得准确的字体度量信息。
我们最近还添加了对额外 Type 1 字体的支持，所有渲染器都知道如何渲染 Type 1 字体。
""")

##Until now we have worked with bitmap renderers which have to use
##TrueType fonts and which make some substitutions; this could lead
##to differences in text wrapping or even the number of labels on
##a chart between renderers.

disc("""
下面是一个更花哨的示例，使用下面的代码片段。
请参阅 ReportLab 用户指南，了解如何注册像 'DarkGardenMK' 这样的非标准字体！
""")

eg("""
    d = Drawing(400, 200)
    for size in range(12, 36, 4):
        d.add(String(10+size*2, 10+size*2, 'Hello World',
                     fontName='Times-Roman',
                     fontSize=size))

    d.add(String(130, 120, 'Hello World',
                 fontName='Courier',
                 fontSize=36))

    d.add(String(150, 160, 'Hello World',
                 fontName='DarkGardenMK',
                 fontSize=36))
""")

from reportlab.pdfbase import pdfmetrics
from reportlab import rl_config
rl_config.warnOnMissingFontGlyphs = 0
afmFile, pfbFile = getJustFontPaths()
T1face = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
T1faceName = 'DarkGardenMK'
pdfmetrics.registerTypeFace(T1face)
T1font = pdfmetrics.Font(T1faceName, T1faceName, 'WinAnsiEncoding')
pdfmetrics.registerFont(T1font)

d = Drawing(400, 200)
for size in range(12, 36, 4):
    d.add(String(10+size*2, 10+size*2, 'Hello World',
                 fontName='Times-Roman',
                 fontSize=size))

d.add(String(130, 120, 'Hello World',
             fontName='Courier',
             fontSize=36))

d.add(String(150, 160, 'Hello World',
             fontName='DarkGardenMK',
             fontSize=36))

draw(d, '花哨字体示例')


heading3("""路径""")

disc("""
Postscript 路径是图形中一个被广泛理解的概念。
它们目前尚未在 $reportlab/graphics$ 中实现，但很快就会实现。
""")

# NB This commented out section is for 'future compatibility' - paths haven't
#    been implemented yet, but when they are we can uncomment this back in.

    ##disc("""Postscript paths are a widely understood concept in graphics. A Path
    ##       is a way of defining a region in space. You put an imaginary pen down,
    ##       draw straight and curved segments, and even pick the pen up and move
    ##       it. At the end of this you have described a region, which may consist
    ##       of several distinct close shapes or unclosed lines. At the end, this
    ##       'path' is 'stroked and filled' according to its properties. A Path has
    ##       the same style properties as a solid shape. It can be used to create
    ##       any irregular shape.""")

    ##disc("""In Postscript-based imaging models such as PDF, Postscript and SVG,
    ##       everything is done with paths. All the specific shapes covered above
    ##       are instances of paths; even text strings (which are shapes in which
    ##       each character is an outline to be filled). Here we begin creating a
    ##       path with a straight line and a bezier curve:""")

    ##eg("""
    ##>>> P = Path(0,0, strokeWidth=3, strokeColor=red)
    ##>>> P.lineTo(0, 50)
    ##>>> P.curveTo(10,50,80,80,100,30)
    ##>>>
    ##""")

    ##disc("""As well as being the only way to draw complex shapes, paths offer some
    ##       performance advantages in renderers which support them. If you want to
    ##       create a scatter plot with 5000 blue circles of different sizes, you
    ##       can create 5000 circles, or one path object. With the latter, you only
    ##       need to set the color and line width once. PINGO just remembers the
    ##       drawing sequence, and writes it out into the file. In renderers which
    ##       do not support paths, the renderer will still have to decompose it
    ##       into 5000 circles so you won't save anything.""")

    ##disc("""<b>Note that our current path implementation is an approximation; it
    ##         should be finished off accurately for PDF and PS.</b>""")


heading3("组")

disc("""
最后，我们有 Group（组）对象。组有一个内容列表，其中包含其他节点。
它还可以应用变换——其内容可以被旋转、缩放或平移。
如果您了解数学原理，可以直接设置变换矩阵。
否则，它提供了旋转、缩放等方法。
这里我们创建一个被旋转和平移的组：
""")

eg("""
>>> g =Group(shape1, shape2, shape3)
>>> g.rotate(30)
>>> g.translate(50, 200)
""")

disc("""
组提供了一种重用的工具。您可以创建一组形状来表示某个组件——
比如坐标系——并将它们放在一个名为 "Axis" 的组中。
然后您可以将该组放入其他组中，每个组有不同的平移和旋转，
就能得到一组坐标轴。它仍然是同一个组，只是在不同的位置绘制。
""")

disc("""
让我们用稍微多一点代码来实现这一点：
""")

eg("""
    d = Drawing(400, 200)

    Axis = Group(
        Line(0,0,100,0),  # x axis
        Line(0,0,0,50),   # y axis
        Line(0,10,10,10), # ticks on y axis
        Line(0,20,10,20),
        Line(0,30,10,30),
        Line(0,40,10,40),
        Line(10,0,10,10), # ticks on x axis
        Line(20,0,20,10),
        Line(30,0,30,10),
        Line(40,0,40,10),
        Line(50,0,50,10),
        Line(60,0,60,10),
        Line(70,0,70,10),
        Line(80,0,80,10),
        Line(90,0,90,10),
        String(20, 35, 'Axes', fill=colors.black)
        )

    firstAxisGroup = Group(Axis)
    firstAxisGroup.translate(10,10)
    d.add(firstAxisGroup)

    secondAxisGroup = Group(Axis)
    secondAxisGroup.translate(150,10)
    secondAxisGroup.rotate(15)

    d.add(secondAxisGroup)

    thirdAxisGroup = Group(Axis,
                           transform=mmult(translate(300,10),
                                           rotate(30)))
    d.add(thirdAxisGroup)
""")

d = Drawing(400, 200)
Axis = Group(
    Line(0,0,100,0),  # x axis
    Line(0,0,0,50),   # y axis
    Line(0,10,10,10), # ticks on y axis
    Line(0,20,10,20),
    Line(0,30,10,30),
    Line(0,40,10,40),
    Line(10,0,10,10), # ticks on x axis
    Line(20,0,20,10),
    Line(30,0,30,10),
    Line(40,0,40,10),
    Line(50,0,50,10),
    Line(60,0,60,10),
    Line(70,0,70,10),
    Line(80,0,80,10),
    Line(90,0,90,10),
    String(20, 35, 'Axes', fill=colors.black)
    )
firstAxisGroup = Group(Axis)
firstAxisGroup.translate(10,10)
d.add(firstAxisGroup)
secondAxisGroup = Group(Axis)
secondAxisGroup.translate(150,10)
secondAxisGroup.rotate(15)
d.add(secondAxisGroup)
thirdAxisGroup = Group(Axis,
                       transform=mmult(translate(300,10),
                                       rotate(30)))
d.add(thirdAxisGroup)
draw(d, "组示例")

#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__='3.3.0'
from tools.docco.rl_doc_utils import *
from reportlab.graphics.shapes import *
from reportlab.graphics.widgets import signsandsymbols

heading2("小部件")

disc("""
现在我们将介绍小部件及其与图形形状的关系。
通过大量示例，我们将展示小部件如何实现可重用的图形组件。
""")


heading3("图形形状与小部件")

disc("""到目前为止，绘图一直是"纯数据"。其中没有实际执行任何操作的代码，
       只是协助程序员检查和检查绘图。事实上，这正是整个概念的基石，
       也是让我们实现可移植性的关键——渲染器只需要实现基本形状。""")

disc("""我们想要构建可重用的图形对象，包括一个强大的图表库。
       为此，我们需要比重用矩形和圆形更实在的东西。我们应该能够编写供他人
       重用的对象——箭头、齿轮、文本框、UML 图节点，甚至是完整的图表。""")

disc("""
Widget 标准是建立在 shapes 模块之上的标准。
任何人都可以编写新的小部件，我们可以构建小部件库。
小部件支持 $getProperties()$ 和 $setProperties()$ 方法，
因此您可以以统一的方式检查、修改以及为它们编写文档。
""")

bullet("小部件是一种可重用的形状")
bullet("""它可以在不传入参数的情况下初始化；
       当调用其 $draw()$ 方法时，它会创建一个基本形状或
       一个组来表示自身""")
bullet("""它可以有任意参数，这些参数可以驱动其绘制方式""")
bullet("""它有一个 $demo()$ 方法，应返回一个在 200x100 矩形中
       精美绘制的自身示例。这是自动文档工具的基石。
       $demo()$ 方法还应有一个编写良好的文档字符串，
       因为它也会被打印出来！""")

disc("""小部件似乎与"绘图只是一组形状"的理念相矛盾；
       它们难道不是有自己的代码吗？它们的工作方式是：小部件可以将自身
       转换为一组基本形状。如果其某些组件本身也是小部件，它们也会被转换。
       这在渲染过程中自动发生；渲染器不会看到您的图表小部件，
       而只是看到一组矩形、线条和字符串。您也可以显式地"展平"绘图，
       将所有小部件转换为基本形状。""")


heading3("使用小部件")

disc("""
让我们想象一个简单的新小部件。
我们将使用一个小部件来绘制一张脸，然后展示它是如何实现的。
""")

eg("""
>>> from reportlab.lib import colors
>>> from reportlab.graphics import shapes
>>> from reportlab.graphics import widgetbase
>>> from reportlab.graphics import renderPDF
>>> d = shapes.Drawing(200, 100)
>>> f = widgetbase.Face()
>>> f.skinColor = colors.yellow
>>> f.mood = "sad"
>>> d.add(f)
>>> renderPDF.drawToFile(d, 'face.pdf', 'A Face')
""")

from reportlab.graphics import widgetbase
d = Drawing(200, 120)
f = widgetbase.Face()
f.x = 50
f.y = 10
f.skinColor = colors.yellow
f.mood = "sad"
d.add(f)
draw(d, '小部件示例')

disc("""
让我们看看它有哪些可用的属性，使用我们之前见过的 $setProperties()$ 方法：
""")

eg("""
>>> f.dumpProperties()
eyeColor = Color(0.00,0.00,1.00)
mood = sad
size = 80
skinColor = Color(1.00,1.00,0.00)
x = 10
y = 10
>>>
""")

disc("""
上面的代码看起来有一个奇怪的地方：我们在创建脸时并没有设置大小或位置。
这是为了允许统一的接口来构造小部件和编写文档而做出的必要权衡——
它们的 $__init__()$ 方法不能要求参数。
相反，它们通常被设计为适合 200 x 100 的窗口，
您可以在创建后通过设置 x、y、width 等属性来移动或调整大小。
""")

disc("""
此外，小部件总是提供一个 $demo()$ 方法。
像这样简单的小部件在设置属性之前总是会做一些合理的事情，
但更复杂的小部件（如图表）可能没有任何数据可以绘制。
文档工具会调用 $demo()$，这样您精心设计的新图表类就可以创建一个
展示其功能的绘图。
""")

disc("""
以下是模块 <i>signsandsymbols.py</i> 中提供的一些简单小部件：
""")

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets import signsandsymbols

d = Drawing(230, 230)

ne = signsandsymbols.NoEntry()
ds = signsandsymbols.DangerSign()
fd = signsandsymbols.FloppyDisk()
ns = signsandsymbols.NoSmoking()

ne.x, ne.y = 10, 10
ds.x, ds.y = 120, 10
fd.x, fd.y = 10, 120
ns.x, ns.y = 120, 120

d.add(ne)
d.add(ds)
d.add(fd)
d.add(ns)

draw(d, 'signsandsymbols.py 中的几个示例')

disc("""
以下是生成上图中所示小部件所需的代码：
""")

eg("""
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets import signsandsymbols

d = Drawing(230, 230)

ne = signsandsymbols.NoEntry()
ds = signsandsymbols.DangerSign()
fd = signsandsymbols.FloppyDisk()
ns = signsandsymbols.NoSmoking()

ne.x, ne.y = 10, 10
ds.x, ds.y = 120, 10
fd.x, fd.y = 10, 120
ns.x, ns.y = 120, 120

d.add(ne)
d.add(ds)
d.add(fd)
d.add(ns)
""")


heading3("复合小部件")

disc("""让我们想象一个复合小部件，它并排绘制两张脸。
       当您有了 Face 小部件后，这很容易构建。""")

eg("""
>>> tf = widgetbase.TwoFaces()
>>> tf.faceOne.mood
'happy'
>>> tf.faceTwo.mood
'sad'
>>> tf.dumpProperties()
faceOne.eyeColor = Color(0.00,0.00,1.00)
faceOne.mood = happy
faceOne.size = 80
faceOne.skinColor = None
faceOne.x = 10
faceOne.y = 10
faceTwo.eyeColor = Color(0.00,0.00,1.00)
faceTwo.mood = sad
faceTwo.size = 80
faceTwo.skinColor = None
faceTwo.x = 100
faceTwo.y = 10
>>>
""")

disc("""属性 'faceOne' 和 'faceTwo' 是故意公开的，以便您可以直接访问它们。
       也可能有顶层属性，但在这种情况下没有。""")


heading3("验证小部件")

disc("""小部件设计者决定验证策略，但默认情况下它们的工作方式与形状相同——
       检查每次赋值——前提是设计者提供了检查信息。""")


heading3("实现小部件")

disc("""我们试图使实现小部件尽可能简单。以下是一个不进行类型检查的
       Face 小部件的代码：""")

eg("""
class Face(Widget):
    \"\"\"This draws a face with two eyes, mouth and nose.\"\"\"

    def __init__(self):
        self.x = 10
        self.y = 10
        self.size = 80
        self.skinColor = None
        self.eyeColor = colors.blue
        self.mood = 'happy'

    def draw(self):
        s = self.size  # abbreviate as we will use this a lot
        g = shapes.Group()
        g.transform = [1,0,0,1,self.x, self.y]
        # background
        g.add(shapes.Circle(s * 0.5, s * 0.5, s * 0.5,
                            fillColor=self.skinColor))
        # CODE OMITTED TO MAKE MORE SHAPES
        return g
""")

disc("""我们在本文档中省略了所有绘制形状的代码，但您可以在发行版的
       $widgetbase.py$ 中找到它。""")

disc("""默认情况下，任何没有前导下划线的属性都会被 setProperties 返回。
       这是一项深思熟虑的策略，旨在鼓励一致的编码约定。""")

disc("""一旦您的小部件可以工作了，您可能想要添加验证支持。
       这涉及向类添加一个名为 $_verifyMap$ 的字典，
       将属性名称映射到"检查函数"。
       $widgetbase.py$ 模块定义了一组检查函数，名称如
       $isNumber$、$isListOfShapes$ 等。您也可以简单地使用 $None$，
       这意味着该属性必须存在但可以是任何类型。
       您也应该编写自己的检查函数。我们希望将"mood"自定义属性
       限制为 "happy"、"sad" 或 "ok" 值。因此我们这样做：""")

eg("""
class Face(Widget):
    \"\"\"This draws a face with two eyes.  It exposes a
    couple of properties to configure itself and hides
    all other details\"\"\"
    def checkMood(moodName):
        return (moodName in ('happy','sad','ok'))
    _verifyMap = {
        'x': shapes.isNumber,
        'y': shapes.isNumber,
        'size': shapes.isNumber,
        'skinColor':shapes.isColorOrNone,
        'eyeColor': shapes.isColorOrNone,
        'mood': checkMood
        }
""")

disc("""这种检查将在每次属性赋值时执行；或者，如果 $config.shapeChecking$
       关闭，则在您调用 $myFace.verify()$ 时执行。""")


heading3("为小部件编写文档")

disc("""
我们正在开发一个通用工具来为任何 Python 包或模块编写文档；
该工具已检入 ReportLab，将用于生成 ReportLab 包的参考文档。
当遇到小部件时，它会在手册中添加额外的章节，包括：
""")

bullet("小部件类的文档字符串")
bullet("来自 <i>demo()</i> 方法的代码片段，以便人们可以看到如何使用它")
bullet("由 <i>demo()</i> 方法生成的绘图")
bullet("绘图中该小部件的属性转储。")

disc("""
这个工具将意味着我们可以保证小部件和图表的文档始终是最新的，
无论是在网站上还是在印刷品中；您也可以为自己的小部件做同样的事情！
""")


heading3("小部件设计策略")

disc("""我们无法为小部件设计提出一致的架构，因此将这个问题留给了作者！
       如果您不喜欢默认的验证策略，或者 $setProperties/getProperties$
       的工作方式，您可以自行覆盖它们。""")

disc("""对于简单的小部件，建议您按照我们上面的做法：
       选择不重叠的属性，在 $__init__$ 中初始化每个属性，
       在调用 $draw()$ 时构造所有内容。
       您也可以使用 $__setattr__$ 钩子，在某些属性被设置时更新内容。
       考虑一个饼图。如果您想要公开各个切片，您可能会编写如下代码：""")

eg("""
from reportlab.graphics.charts import piecharts
pc = piecharts.Pie()
pc.defaultColors = [navy, blue, skyblue] #used in rotation
pc.data = [10,30,50,25]
pc.slices[7].strokeWidth = 5
""")
#removed 'pc.backColor = yellow' from above code example

disc("""最后一行是有问题的，因为我们只创建了四个切片——
       事实上我们可能还没有创建它们。$pc.slices[7]$ 会引发错误吗？
       它是否是当定义第七个楔形时覆盖默认设置的预设？
       我们现在将这个问题直接留给小部件作者，并建议您在公开
       其存在依赖于其他属性值的"子对象"之前，先让简单的小部件正常工作 :-)""")

disc("""我们还讨论了父小部件将属性传递给其子部件的规则。
       似乎普遍需要一种全局方式来表达"所有切片从其父级获取 lineWidth"，
       而无需大量重复编码。我们还没有通用解决方案，因此再次将此留给小部件作者。
       我们希望人们能尝试推送、拉取和模式匹配方法，并想出好的方案。
       与此同时，我们当然可以编写整体式图表小部件，就像 Visual Basic
       和 Delphi 中的那样。""")

disc("""现在请看以下使用早期版本饼图小部件的示例代码及其生成的输出：""")

eg("""
from reportlab.lib.colors import *
from reportlab.graphics import shapes,renderPDF
from reportlab.graphics.charts.piecharts import Pie

d = Drawing(400,200)
d.add(String(100,175,"Without labels", textAnchor="middle"))
d.add(String(300,175,"With labels", textAnchor="middle"))

pc = Pie()
pc.x = 25
pc.y = 50
pc.data = [10,20,30,40,50,60]
pc.slices[0].popout = 5
d.add(pc, 'pie1')

pc2 = Pie()
pc2.x = 150
pc2.y = 50
pc2.data = [10,20,30,40,50,60]
pc2.labels = ['a','b','c','d','e','f']
d.add(pc2, 'pie2')

pc3 = Pie()
pc3.x = 275
pc3.y = 50
pc3.data = [10,20,30,40,50,60]
pc3.labels = ['a','b','c','d','e','f']
pc3.slices.labelRadius = 0.65
pc3.slices.fontName = "Helvetica-Bold"
pc3.slices.fontSize = 16
pc3.slices.fontColor = colors.yellow
d.add(pc3, 'pie3')
""")

# Hack to force a new paragraph before the todo() :-(
disc("")

from reportlab.lib.colors import *
from reportlab.graphics import shapes,renderPDF
from reportlab.graphics.charts.piecharts import Pie

d = Drawing(400,200)
d.add(String(100,175,"Without labels", textAnchor="middle"))
d.add(String(300,175,"With labels", textAnchor="middle"))

pc = Pie()
pc.x = 25
pc.y = 50
pc.data = [10,20,30,40,50,60]
pc.slices[0].popout = 5
d.add(pc, 'pie1')

pc2 = Pie()
pc2.x = 150
pc2.y = 50
pc2.data = [10,20,30,40,50,60]
pc2.labels = ['a','b','c','d','e','f']
d.add(pc2, 'pie2')

pc3 = Pie()
pc3.x = 275
pc3.y = 50
pc3.data = [10,20,30,40,50,60]
pc3.labels = ['a','b','c','d','e','f']
pc3.slices.labelRadius = 0.65
pc3.slices.fontName = "Helvetica-Bold"
pc3.slices.fontSize = 16
pc3.slices.fontColor = colors.yellow
d.add(pc3, 'pie3')

draw(d, '饼图示例')

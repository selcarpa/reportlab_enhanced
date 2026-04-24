#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__='3.3.0'
from tools.docco.rl_doc_utils import *

heading2("基本概念")

disc("""
在本节中，我们将介绍图形库的一些基本原则，这些概念将在后面的各个章节中出现。
""")


heading3("绘图与渲染器")

disc("""
<i>Drawing</i>（绘图）是一种与平台无关的图形描述方式，
用于描述一组形状的集合。
它与 PDF、PostScript 或任何其他输出格式没有直接关联。
幸运的是，大多数矢量图形系统都遵循 PostScript 模型，
因此可以无歧义地描述各种形状。
""")

disc("""
一个绘图包含若干基本 <i>Shape</i>（形状）。
常见的形状包括广为人知的矩形、圆形、线条等。
一种特殊（逻辑）形状是 <i>Group</i>（组），它可以容纳其他形状并对它们应用变换。
组代表形状的复合体，允许将复合体当作单个形状来处理。
几乎所有图形都可以由少量基本形状组合而成。
""")

disc("""
该包提供了多个 <i>Renderer</i>（渲染器），它们知道如何将绘图输出为不同的格式。
包括 PDF（renderPDF）、PostScript（renderPS）和位图输出（renderPM）。
位图渲染器使用 Raph Levien 的 <i>libart</i> 光栅化器
和 Fredrik Lundh 的 <i>Python Imaging Library</i>（PIL）。
SVG 渲染器使用 Python 标准库的 XML 模块，
因此您不需要安装 XML-SIG 的额外 PyXML 包。
如果您安装了正确的扩展，可以将绘图生成为用于 Web 的位图格式，
也可以生成为用于 PDF 文档的矢量格式，并获得"相同的输出"。
""")

disc("""
PDF 渲染器具有特殊的"特权"——Drawing 对象同时也是一个 <i>Flowable</i>，
因此可以直接放置在任何 Platypus 文档的故事流中，
或者用一行代码直接绘制到 <i>Canvas</i> 上。
此外，PDF 渲染器还提供了一个实用函数，可以快速生成单页 PDF 文档。
""")

disc("""
SVG 渲染器比较特殊，因为它仍处于实验阶段。
它生成的 SVG 代码并没有经过任何优化，
只将 ReportLab Graphics (RLG) 中可用的功能映射到 SVG。
这意味着不支持 SVG 动画、交互性、脚本，
也不支持更复杂的裁剪、遮罩或渐变形状。
所以请小心使用，如果发现任何错误，请向我们报告！
""")

heading3("坐标系")

disc("""
在我们的 X-Y 坐标系中，Y 轴方向从底部<i>向上</i>。
这与 PDF、PostScript 和数学记法一致。
对于人们来说，这似乎也更自然，尤其是在处理图表时。
请注意，在其他图形模型（如 SVG）中，Y 坐标方向是<i>向下</i>的。
对于 SVG 渲染器来说这实际上不是问题，
它会自动翻转绘图内容，使您的 SVG 输出看起来与预期一致。
""")

disc("""
X 坐标方向与惯例相同，从左到右。
目前似乎还没有任何模型主张相反的方向——
至少目前还没有（不过有一些有趣的例外，
比如阿拉伯人看时间序列图表时的情况……）。
""")


heading3("入门示例")

disc("""
让我们创建一个简单的绘图，包含字符串 "Hello World" 和一些特殊字符，
显示在一个彩色矩形之上。
创建完成后，我们将绘图保存为独立的 PDF 文件。
""")

eg("""
    from reportlab.lib import colors
    from reportlab.graphics.shapes import *

    d = Drawing(400, 200)
    d.add(Rect(50, 50, 300, 100, fillColor=colors.yellow))
    d.add(String(150,100, 'Hello World', fontSize=18, fillColor=colors.red))
    d.add(String(180,86, 'Special characters \\
                 \\xc2\\xa2\\xc2\\xa9\\xc2\\xae\\xc2\\xa3\\xce\\xb1\\xce\\xb2',
                 fillColor=colors.red))

    from reportlab.graphics import renderPDF
    renderPDF.drawToFile(d, 'example1.pdf', 'My First Drawing')
""")

disc("这将生成一个包含以下图形的 PDF 文件：")

from reportlab.graphics.shapes import *
from reportlab.graphics import testshapes
t = testshapes.getDrawing01()
draw(t, "'Hello World'")

disc("""
每个渲染器都可以根据其格式做适当的处理，
并可以拥有所需的任何 API。
如果涉及文件格式，通常会有一个 $drawToFile$ 函数，
这就是您需要了解的关于渲染器的全部内容。
让我们将同一个绘图保存为封装 PostScript 格式：
""")

##eg("""
##    from reportlab.graphics import renderPS
##    renderPS.drawToFile(D, 'example1.eps', 'My First Drawing')
##""")
eg("""
    from reportlab.graphics import renderPS
    renderPS.drawToFile(d, 'example1.eps')
""")

disc("""
这将生成一个包含相同绘图的 EPS 文件，
可以导入到 Quark Express 等排版工具中。
如果我们想将相同的绘图生成为用于网站的位图文件，
只需编写如下代码：
""")

eg("""
    from reportlab.graphics import renderPM
    renderPM.drawToFile(d, 'example1.png', 'PNG')
""")

disc("""
还支持许多其他位图格式，如 GIF、JPG、TIFF、BMP 和 PPN，
因此您不太可能需要添加额外的后处理步骤来转换为所需的最终格式。
""")

disc("""
要生成包含相同绘图的 SVG 文件，
可以导入到 Illustrator 等图形编辑工具中，
只需编写如下代码：
""")

eg("""
    from reportlab.graphics import renderSVG
    renderSVG.drawToFile(d, 'example1.svg')
""")


heading3("属性验证")

disc("""
Python 是一门非常动态的语言，允许我们在运行时执行语句，
这很容易导致意外行为。
一种微妙的"错误"是给框架不知道的属性赋值，
因为使用的属性名包含拼写错误。
Python 允许这样做（例如给对象添加新属性），
但图形框架在没有采取特殊对策的情况下无法检测到这种"拼写错误"。
""")

disc("""
有两种验证技术可以避免这种情况。
默认情况下，每个对象会在运行时检查每次赋值，
确保您只能给"合法"属性赋值。
这是默认行为。
由于这会带来少量的性能开销，因此在需要时可以关闭此行为。
""")

eg("""
>>> r = Rect(10,10,200,100, fillColor=colors.red)
>>>
>>> r.fullColor = colors.green # note the typo
>>> r.x = 'not a number'       # illegal argument type
>>> del r.width                # that should confuse it
""")

disc("""
在静态类型语言中，这些语句会被编译器捕获，
但 Python 允许您这样做。
第一个错误可能让您盯着图片困惑为什么颜色不对。
第二个错误可能要到后端尝试绘制矩形时才会显现。
第三个错误虽然不太可能发生，但会导致一个不知道如何绘制自身的无效对象。
""")

eg("""
>>> r = shapes.Rect(10,10,200,80)
>>> r.fullColor = colors.green
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
  File "C:\\code\\users\\andy\\graphics\\shapes.py", line 254, in __setattr__
    validateSetattr(self,attr,value)    #from reportlab.lib.attrmap
  File "C:\\code\\users\\andy\\lib\\attrmap.py", line 74, in validateSetattr
    raise AttributeError, "Illegal attribute '%s' in class %s" % (name, obj.__class__.__name__)
AttributeError: Illegal attribute 'fullColor' in class Rect
>>>
""")

disc("""
这会带来性能开销，因此在需要时可以关闭此行为。
要关闭验证，请在首次导入 reportlab.graphics.shapes 之前使用以下代码：
""")

eg("""
>>> import reportlab.rl_config
>>> reportlab.rl_config.shapeChecking = 0
>>> from reportlab.graphics import shapes
>>>
""")

disc("""
关闭 $shapeChecking$ 后，类将在构建时不包含验证钩子，代码应该会更快。
目前，在批量图表操作中，性能开销约为 25%，因此几乎不值得禁用。
然而，如果将来我们将渲染器用 C 语言重写（这是完全可能的），
剩余的 75% 将缩减到几乎为零，此时验证带来的节省将非常显著。
""")

disc("""
每个对象（包括绘图本身）都有一个 $verify()$ 方法。
该方法要么成功，要么抛出异常。
如果您关闭了自动验证，那么在开发代码进行测试时应显式调用 $verify()$，
或者在批处理过程中调用一次。
""")


heading3("属性编辑")

disc("""
ReportLab Graphics 的一个核心理念（将在下面详细介绍）是，
您可以自动为部件生成文档。
这意味着获取所有可编辑属性，包括其子组件的属性。
""")

disc("""
另一个目标是能够为绘图创建 GUI 界面和配置文件。
可以构建一个通用 GUI 来显示绘图的所有可编辑属性，
让您修改它们并查看结果。
Visual Basic 或 Delphi 开发环境就是此类工具的良好范例。
在批处理图表应用中，一个文件可以列出图表中所有组件的所有属性，
然后与数据库查询合并来批量生成图表。
""")

disc("""
为了支持这些应用，我们提供了两个接口：$getProperties$ 和 $setProperties$，
以及一个便捷方法 $dumpProperties$。
第一个返回对象可编辑属性的字典；第二个用于批量设置属性。
如果对象有公开的"子对象"，则可以递归地设置和获取它们的属性。
等我们在后面看到 <i>Widget</i>（部件）时，这会更加容易理解，
但我们需要在框架的基础层就提供这种支持。
""")

eg("""
>>> r = shapes.Rect(0,0,200,100)
>>> import pprint
>>> pprint.pprint(r.getProperties())
{'fillColor': Color(0.00,0.00,0.00),
 'height': 100,
 'rx': 0,
 'ry': 0,
 'strokeColor': Color(0.00,0.00,0.00),
 'strokeDashArray': None,
 'strokeLineCap': 0,
 'strokeLineJoin': 0,
 'strokeMiterLimit': 0,
 'strokeWidth': 1,
 'width': 200,
 'x': 0,
 'y': 0}
>>> r.setProperties({'x':20, 'y':30, 'strokeColor': colors.red})
>>> r.dumpProperties()
fillColor = Color(0.00,0.00,0.00)
height = 100
rx = 0
ry = 0
strokeColor = Color(1.00,0.00,0.00)
strokeDashArray = None
strokeLineCap = 0
strokeLineJoin = 0
strokeMiterLimit = 0
strokeWidth = 1
width = 200
x = 20
y = 30
>>>  """)

disc("""
<i>注意：$pprint$ 是 Python 标准库模块，允许您将输出"美观打印"为多行，
而不是一长行。</i>
""")

disc("""
这三种方法在这里看起来作用不大，
但正如我们将看到的，在处理非基本对象时，
它们使我们的部件框架变得更加强大。
""")


heading3("命名子对象")

disc("""
您可以将对象添加到 $Drawing$ 和 $Group$ 对象中。
这些对象通常会放入一个内容列表中。
但是，您也可以在添加对象时为其指定名称。
这允许您在构造绘图之后引用并可能修改其中的任何元素。
""")

eg("""
>>> d = shapes.Drawing(400, 200)
>>> s = shapes.String(10, 10, 'Hello World')
>>> d.add(s, 'caption')
>>> s.caption.text
'Hello World'
>>>
""")

disc("""
请注意，您可以在绘图中的多个上下文中使用同一个形状实例；
如果您选择在多个位置使用同一个 $Circle$ 对象（例如在散点图中），
并使用不同的名称来访问它，它仍然是一个共享对象，对它的修改将是全局的。
""")

disc("""
这提供了一种创建和修改交互式绘图的范式。
""")

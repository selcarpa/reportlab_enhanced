#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__='3.3.0'
from tools.docco.rl_doc_utils import *
from reportlab.graphics.shapes import *

heading2("图表")

disc("""
这其中的大部分动机是为了创建一个灵活的图表包。
本节介绍了我们图表模型背后的思想、设计目标以及图表包中已有的组件。
""")


heading3("设计目标")

disc("以下是一些设计目标：")

disc("<i>使简单的顶层使用变得非常简单</i>")
disc("""<para lindent="+36">应该能够以最少的代码行创建一个简单的图表，并通过合理的自动设置使其"做出正确的事情"。
上面的饼图代码片段就做到了这一点。如果一个真正的图表有许多子组件，除非您想自定义它们的行为，
否则您仍然不需要与它们交互。</para>""")

disc("<i>允许精确定位</i>")
disc("""<para lindent="+36">在出版和平面设计中，一个绝对的要求是控制每个元素的位置和样式。
我们将尽量提供以固定大小和绘图比例来指定事物的属性，而不是自动调整大小。
因此，当您将 y 轴标签的字体变大时，"内部绘图矩形"不会神奇地改变，
即使这意味着您的标签可能会溢出图表矩形的左边缘。预览图表并选择适合的大小和间距是您的工作。</para>""")

disc("""<para lindent="+36">有些事情确实需要自动化。例如，如果您想将 N 个柱子放入 200 点的空间中，
并且事先不知道 N 的值，我们将柱间距指定为柱宽的百分比而不是点数大小，
让图表自行计算。这仍然是确定性的和可控的。</para>""")

disc("<i>单独或成组控制子元素</i>")
disc("""<para lindent="+36">我们使用智能集合类，让您可以自定义一组事物，或者只自定义其中的一个。
例如，您可以在我们的实验性饼图中这样做：</para>""")

eg("""
d = Drawing(400,200)
pc = Pie()
pc.x = 150
pc.y = 50
pc.data = [10,20,30,40,50,60]
pc.labels = ['a','b','c','d','e','f']
pc.slices.strokeWidth=0.5
pc.slices[3].popout = 20
pc.slices[3].strokeWidth = 2
pc.slices[3].strokeDashArray = [2,2]
pc.slices[3].labelRadius = 1.75
pc.slices[3].fontColor = colors.red
d.add(pc, '')
""")

disc("""<para lindent="+36">$pc.slices[3]$ 实际上会惰性地创建一个小对象，用于保存有关该切片的信息；
如果在绘制时存在第四个切片，该对象将用于格式化它。</para>""")

disc("<i>只暴露您应该更改的内容</i>")
disc("""<para lindent="+36">从统计角度来看，在上面的示例中让您直接调整某个饼图切片的角度是错误的，
因为角度是由数据决定的。因此，并非所有内容都会通过公共属性暴露出来。
可能存在"后门"让您在真正需要时绕过这个限制，或者提供高级功能的方法，
但一般来说属性将是正交的。</para>""")

disc("<i>基于组合和组件</i>")
disc("""<para lindent="+36">图表由可重用的子组件构建而成。图例是一个容易理解的例子。
如果您需要一种特殊类型的图例（例如圆形色块），您应该继承标准图例组件。
然后您可以这样做……</para>""")

eg("""
c = MyChartWithLegend()
c.legend = MyNewLegendClass()    # just change it
c.legend.swatchRadius = 5    # set a property only relevant to the new one
c.data = [10,20,30]   #   and then configure as usual...
""")

disc("""<para lindent="+36">……或者创建/修改您自己的图表或绘图类，默认创建其中一个。
这对于时间序列图表也非常相关，因为 x 轴可以有多种样式。</para>""")

disc("""<para lindent="+36">顶层图表类将创建许多这样的组件，然后调用方法或设置私有属性来告诉它们
高度和位置——所有这些都应该自动为您完成并且您无法自定义的内容。
我们正在建模组件应该是什么样子，并将在达成共识后在这里发布它们的 API。</para>""")

disc("<i>多图表</i>")
disc("""<para lindent="+36">组件方法的一个推论是您可以创建包含多个图表或自定义数据图形的图。
我们最喜欢的一个目标示例是由用户贡献到我们画廊中的天气预报图；
我们希望使创建此类绘图变得容易，将构建块连接到它们的图例，
并以一致的方式输入数据。</para>""")
disc("""<para lindent="+36">（如果您想查看图像，可以在我们的网站上找到
<font color="blue"><a href="https://www.reportlab.com/media/imadj/data/RLIMG_e5e5cb85cc0a555f5433528ac38c5884.PDF">此处</a></font>）</para>""")


##heading3("Key Concepts and Components")
heading3("概述")

disc("""图表或绘图是放置在绘图上的一个对象；它本身不是绘图。
因此您可以控制它的位置，将多个图表放在同一个绘图上，或添加注释。""")

disc("""图表有两个轴；轴可以是值轴或类别轴。轴又有一个 Labels 属性，
让您可以配置所有文本标签或单独配置每一个。
大多数因图表而异的配置细节都与轴属性或轴标签相关。""")

disc("""对象通过上一节讨论的接口暴露属性；这些都是可选的，
目的是让最终用户配置外观。图表正常工作所必须设置的项以及图表与其组件之间的
必要通信，是通过方法来处理的。""")

disc("""您可以继承任何图表组件并用您的替代品替换原始组件，
前提是您实现了必要的方法和属性。""")


heading2("标签")

disc("""
标签是附加到某个图表元素的文本字符串。
它们用于轴上、标题或轴旁边，或附加到单个数据点上。
标签可以包含换行符，但只能使用一种字体。
""")

disc("""标签的文本和"原点"通常由其父对象设置。它们通过方法而不是属性来访问。
因此，X 轴决定每个刻度标签的"参考点"和每个标签的数字或日期文本。
但是，最终用户可以直接设置标签（或标签集合）的属性，
以影响其相对于此原点的位置和所有格式。""")

eg("""
from reportlab.graphics import shapes
from reportlab.graphics.charts.textlabels import Label

d = Drawing(200, 100)

# mark the origin of the label
d.add(Circle(100,90, 5, fillColor=colors.green))

lab = Label()
lab.setOrigin(100,90)
lab.boxAnchor = 'ne'
lab.angle = 45
lab.dx = 0
lab.dy = -20
lab.boxStrokeColor = colors.green
lab.setText('Some\nMulti-Line\nLabel')

d.add(lab)
""")


from reportlab.graphics import shapes
from reportlab.graphics.charts.textlabels import Label

d = Drawing(200, 100)

# mark the origin of the label
d.add(Circle(100,90, 5, fillColor=colors.green))

lab = Label()
lab.setOrigin(100,90)
lab.boxAnchor = 'ne'
lab.angle = 45
lab.dx = 0
lab.dy = -20
lab.boxStrokeColor = colors.green
lab.setText('Some\nMulti-Line\nLabel')

d.add(lab)

draw(d, '标签示例')



disc("""
在上面的绘图中，标签是相对于绿色圆点定义的。
文本框的东北角应该在原点下方十个点处，并围绕该角旋转 45 度。
""")

disc("""
目前标签具有以下属性，我们相信这些属性足以满足我们迄今为止见过的所有图表：
""")

disc("")

data=[["属性", "含义"],
      ["dx", """标签的 x 位移。"""],
      ["dy", """标签的 y 位移。"""],
      ["angle", """应用于标签的旋转角度（逆时针）。"""],
      ["boxAnchor", "标签的框锚点，取值为 'n'、'e'、'w'、's'、'ne'、'nw'、'se'、'sw' 之一。"],
      ["textAnchor", """标签文本的锚定位置，取值为 'start'、'middle'、'end' 之一。"""],
      ["boxFillColor", """标签框使用的填充颜色。"""],
      ["boxStrokeColor", "标签框使用的描边颜色。"],
      ["boxStrokeWidth", """标签框的线宽。"""],
      ["fontName", """标签的字体名称。"""],
      ["fontSize", """标签的字体大小。"""],
      ["leading", """标签文本行的行距值。"""],
      ["x", """参考点的 X 坐标。"""],
      ["y", """参考点的 Y 坐标。"""],
      ["width", """标签的宽度。"""],
      ["height", """标签的高度。"""]
      ]
t=Table(data, colWidths=(100,330))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('FONT',(0,1),(0,-1),'Courier',8,8),
            ('FONT',(1,1),(1,-1),'Times-Roman',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - 标签属性""")

disc("""
要查看更多具有不同属性组合的 $Label$ 对象示例，
请查看 $tests$ 文件夹中的 ReportLab 测试套件，
运行脚本 $test_charts_textlabels.py$ 并查看它生成的 PDF 文档！
""")



heading2("轴")

disc("""
我们识别两种基本的轴类型——<i>值轴</i>和<i>类别轴</i>。
两者都有水平和垂直两种变体。
两者都可以被子类化以创建非常特定类型的轴。
例如，如果您在时间序列应用中有复杂的规则来决定显示哪些日期，
或者需要不规则的缩放，您可以覆盖轴并创建一个新的。
""")

disc("""
轴负责确定从数据坐标到图像坐标的映射；根据图表的请求变换点；
绘制自身及其刻度线、网格线和轴标签。
""")

disc("""
此绘图显示了两个轴，每种类型一个，它们是直接创建的，没有引用任何图表：
""")


from reportlab.graphics import shapes
from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis

drawing = Drawing(400, 200)

data = [(10, 20, 30, 40), (15, 22, 37, 42)]

xAxis = XCategoryAxis()
xAxis.setPosition(75, 75, 300)
xAxis.configure(data)
xAxis.categoryNames = ['Beer', 'Wine', 'Meat', 'Cannelloni']
xAxis.labels.boxAnchor = 'n'
xAxis.labels[3].dy = -15
xAxis.labels[3].angle = 30
xAxis.labels[3].fontName = 'Times-Bold'

yAxis = YValueAxis()
yAxis.setPosition(50, 50, 125)
yAxis.configure(data)

drawing.add(xAxis)
drawing.add(yAxis)

draw(drawing, '两个独立的轴')


disc("以下是创建它们的代码：")

eg("""
from reportlab.graphics import shapes
from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis

drawing = Drawing(400, 200)

data = [(10, 20, 30, 40), (15, 22, 37, 42)]

xAxis = XCategoryAxis()
xAxis.setPosition(75, 75, 300)
xAxis.configure(data)
xAxis.categoryNames = ['Beer', 'Wine', 'Meat', 'Cannelloni']
xAxis.labels.boxAnchor = 'n'
xAxis.labels[3].dy = -15
xAxis.labels[3].angle = 30
xAxis.labels[3].fontName = 'Times-Bold'

yAxis = YValueAxis()
yAxis.setPosition(50, 50, 125)
yAxis.configure(data)

drawing.add(xAxis)
drawing.add(yAxis)
""")

disc("""
请记住，通常您不需要直接创建轴；
使用标准图表时，它会附带现成的轴。
方法是图表用来配置轴并处理几何关系的方式。
不过，我们将在下面详细讨论它们。
与我们描述的轴正交对应的轴基本上具有相同的属性，
除了那些涉及刻度的属性。
""")


heading3("XCategoryAxis 类")

disc("""
类别轴实际上没有缩放功能；它只是将自身划分为等大小的区间。
它比值轴更简单。
图表（或程序员）通过 $setPosition(x, y, length)$ 方法设置其位置。
下一阶段是向其展示数据以便它可以配置自身。
这对类别轴来说很简单——它只需计算其中一个数据系列中的数据点数量。
$reversed$ 属性（如果为 1）表示类别应该反转。
绘制绘图时，轴可以通过其 $scale()$ 方法为图表提供帮助，
告诉图表给定类别在页面上的起始和结束位置。
我们还没有看到让人们覆盖类别宽度或位置的需求。
""")

disc("XCategoryAxis 具有以下可编辑属性：")

disc("")

data=[["属性", "含义"],
      ["visible", """是否绘制轴？有时您不想显示一个或两个轴，
但它们仍然需要存在，因为它们管理点的缩放。"""],
      ["strokeColor", "轴的颜色"],
      ["strokeDashArray", """是否用虚线绘制轴，如果是，用什么类型。
默认值为 None"""],
      ["strokeWidth", "轴的宽度（以点为单位）"],
      ["tickUp", """刻度线应该从轴向上突出多远？
（注意，将此值设为图表高度即可得到网格线）"""],
      ["tickDown", """刻度线应该从轴向下突出多远？"""],
      ["categoryNames", """None 或字符串列表。这应该与每个数据系列
具有相同的长度。"""],
      ["labels", """刻度线的标签集合。默认情况下，每个文本标签的"北方"
（即顶部中心）定位在轴上每个类别中心下方 5 个点处。
您可以重新定义整个标签组或任何一个标签的任何属性。
如果 categoryNames=None，则不绘制标签。"""],
      ["title", """尚未实现。这需要类似于标签，但还允许您直接设置文本。
它将有一个默认位置在轴下方。"""]]
t=Table(data, colWidths=(100,330))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('FONT',(0,1),(0,-1),'Courier',8,8),
            ('FONT',(1,1),(1,-1),'Times-Roman',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - XCategoryAxis 属性""")


heading3("YValueAxis")

disc("""
图中的左轴是一个 YValueAxis。
值轴与类别轴的不同之处在于，沿其长度的每个点对应于图表空间中的一个 y 值。
轴的工作是配置自身，并根据请求将 Y 值从图表空间转换为点，
以协助父图表进行绘制。
""")

disc("""
$setPosition(x, y, length)$ 和 $configure(data)$ 的工作方式与类别轴完全相同。
如果您没有完全指定最大值、最小值和刻度间隔，那么 $configure()$ 会导致轴选择合适的值。
配置完成后，值轴可以使用 $scale()$ 方法将 y 数据值转换为绘图空间。
例如：
""")

eg("""
>>> yAxis = YValueAxis()
>>> yAxis.setPosition(50, 50, 125)
>>> data = [(10, 20, 30, 40),(15, 22, 37, 42)]
>>> yAxis.configure(data)
>>> yAxis.scale(10)  # should be bottom of chart
50.0
>>> yAxis.scale(40)  # should be near the top
167.1875
>>>
""")

disc("""默认情况下，最高数据点与轴的顶部对齐，最低数据点与轴的底部对齐，
轴为其刻度点选择"漂亮的整数"。您可以使用以下属性覆盖这些设置。""")

disc("")

data=[["属性", "含义"],
      ["visible", """是否绘制轴？有时您不想显示一个或两个轴，
但它们仍然需要存在，因为它们管理点的缩放。"""],
      ["strokeColor", "轴的颜色"],
      ["strokeDashArray", """是否用虚线绘制轴，如果是，用什么类型。
默认值为 None"""],
      ["strokeWidth", "轴的宽度（以点为单位）"],
      ["tickLeft", """刻度线应该从轴向左突出多远？
（注意，将此值设为图表高度即可得到网格线）"""],
      ["tickRight", """刻度线应该从轴向右突出多远？"""],

      ["valueMin", """轴底部应对应的 y 值。
默认值为 None，此时轴将其设置为最低的实际数据点（例如上面示例中的 10）。
通常将其设置为零以避免误导视觉。"""],
      ["valueMax", """轴顶部应对应的 y 值。
默认值为 None，此时轴将其设置为最高的实际数据点（例如上面示例中的 42）。
通常将其设置为一个"整数"，使数据柱不会完全到达顶部。"""],
      ["valueStep", """刻度间隔之间的 y 值变化量。默认情况下这是
None，图表会尝试选择比下面的 minimumTickSpacing 稍大的"漂亮整数"。"""],

      ["valueSteps", """放置刻度线的数字列表。"""],

      ["minimumTickSpacing", """当 valueStep 设置为 None 时使用此值，否则忽略。
设计者指定刻度线的间距不应小于 X 个点（大概基于标签字体大小和角度的考虑）。
图表尝试 1、2、5、10、20、50、100……类型的值（如有必要会降到 1 以下），
直到找到大于所需间距的间隔，并将其用作步长。"""],
      ["labelTextFormat", """这决定了标签中显示的内容。与接受固定字符串的类别轴不同，
值轴上的标签应该是数字。您可以提供一个"格式字符串"，如 '%0.2f'（显示两位小数），
或一个接受数字并返回字符串的任意函数。后者的一个用途是将时间戳转换为
可读的年-月-日格式。"""],
      ["title", """尚未实现。这需要类似于标签，但还允许您直接设置文本。
它将有一个默认位置在轴下方。"""]]
t=Table(data, colWidths=(100,330))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('FONT',(0,1),(0,-1),'Courier',8,8),
            ('FONT',(1,1),(1,-1),'Times-Roman',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - YValueAxis 属性""")

disc("""
$valueSteps$ 属性让您可以明确指定刻度线的位置，
因此您不必遵循规则间隔。因此，您可以借助几个辅助函数绘制月末和月末日期，
而不需要特殊的时间序列图表类。
以下代码展示了如何创建具有特殊刻度间隔的简单 $XValueAxis$。
请确保在调用 configure 方法之前设置 $valueSteps$ 属性！
""")

eg("""
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.axes import XValueAxis

drawing = Drawing(400, 100)

data = [(10, 20, 30, 40)]

xAxis = XValueAxis()
xAxis.setPosition(75, 50, 300)
xAxis.valueSteps = [10, 15, 20, 30, 35, 40]
xAxis.configure(data)
xAxis.labels.boxAnchor = 'n'

drawing.add(xAxis)
""")


from reportlab.graphics import shapes
from reportlab.graphics.charts.axes import XValueAxis

drawing = Drawing(400, 100)

data = [(10, 20, 30, 40)]

xAxis = XValueAxis()
xAxis.setPosition(75, 50, 300)
xAxis.valueSteps = [10, 15, 20, 30, 35, 40]
xAxis.configure(data)
xAxis.labels.boxAnchor = 'n'

drawing.add(xAxis)

draw(drawing, '具有非等距刻度线的轴')


disc("""
除了这些属性之外，所有轴类都有三个描述如何将两个轴相互连接的属性。
同样，这只有在您定义自己的图表或想要修改使用此类轴的现有图表的外观时才有意义。
这些属性在这里只是简要列出，但您可以在模块
$reportlab/graphics/axes.py$ 中找到大量示例函数供您研究……
""")

disc("""
一个轴通过在第一个轴上调用方法 $joinToAxis(otherAxis, mode, pos)$ 连接到另一个轴，
其中 $mode$ 和 $pos$ 分别是由 $joinAxisMode$ 和 $joinAxisPos$ 描述的属性。
$'points'$ 表示使用绝对值，$'value'$ 表示使用相对值
（两者都由 $joinAxisPos$ 属性指示）沿轴方向。
""")

disc("")

data=[["属性", "含义"],
      ["joinAxis", """如果为 true，则连接两个轴。"""],
      ["joinAxisMode", """用于连接轴的模式（'bottom'、'top'、'left'、'right'、'value'、'points'、None）。"""],
      ["joinAxisPos", """与另一个轴连接的位置。"""],
      ]
t=Table(data, colWidths=(100,330))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('FONT',(0,1),(0,-1),'Courier',8,8),
            ('FONT',(1,1),(1,-1),'Times-Roman',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - 轴连接属性""")

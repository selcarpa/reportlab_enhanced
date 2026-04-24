from tools.docco.rl_doc_utils import *

heading2("线图")

disc("""
下面我们展示一个更复杂的折线图示例，
该示例还使用了一些实验性功能，例如在每个数据点处放置线标记。
""")

eg("""
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker

drawing = Drawing(400, 200)

data = [
    ((1,1), (2,2), (2.5,1), (3,3), (4,5)),
    ((1,2), (2,3), (2.5,2), (3.5,5), (4,6))
]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = data
lp.joinedLines = 1
lp.lines[0].symbol = makeMarker('FilledCircle')
lp.lines[1].symbol = makeMarker('Circle')
lp.lineLabelFormat = '%2.0f'
lp.strokeColor = colors.black
lp.xValueAxis.valueMin = 0
lp.xValueAxis.valueMax = 5
lp.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5]
lp.xValueAxis.labelTextFormat = '%2.1f'
lp.yValueAxis.valueMin = 0
lp.yValueAxis.valueMax = 7
lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]

drawing.add(lp)
""")


from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker

drawing = Drawing(400, 200)

data = [
    ((1,1), (2,2), (2.5,1), (3,3), (4,5)),
    ((1,2), (2,3), (2.5,2), (3.5,5), (4,6))
]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = data
lp.joinedLines = 1
lp.lines[0].symbol = makeMarker('FilledCircle')
lp.lines[1].symbol = makeMarker('Circle')
lp.lineLabelFormat = '%2.0f'
lp.strokeColor = colors.black
lp.xValueAxis.valueMin = 0
lp.xValueAxis.valueMax = 5
lp.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5]
lp.xValueAxis.labelTextFormat = '%2.1f'
lp.yValueAxis.valueMin = 0
lp.yValueAxis.valueMax = 7
lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]

drawing.add(lp)

draw(drawing, 'LinePlot sample')



disc("")

data=[["属性","含义"],
      ["data", "要绘制的数据，由数字（列表的）列表组成。"],
      ["x, y, width, height", """折线图的边界框。
注意 x 和 y 指定的不是中心点，而是左下角"""],
      ["xValueAxis", """垂直值轴，可以按照前面描述的方式进行格式化。"""],
      ["yValueAxis", """水平值轴，可以按照前面描述的方式进行格式化。"""],
      ["strokeColor", """默认值为 None。这将在绘图矩形周围绘制边框，
在调试时可能很有用。坐标轴会覆盖此设置。"""],
      ["strokeWidth", """默认值为 None。绘图矩形周围边框的宽度。"""],
      ["fillColor", """默认值为 None。这将用纯色填充绘图矩形。"""],
      ["lines.strokeColor", """线条的颜色。"""],
      ["lines.strokeWidth", """线条的宽度。"""],
      ["lines.symbol", """每个数据点使用的标记。
你可以使用 makeMarker() 函数创建新标记。
例如，要使用圆形标记，函数调用为 makeMarker('Circle')"""],
      ["lineLabels", """用于格式化所有线条标签的标签集合。由于
这是一个二维数组，你可以使用以下语法显式格式化
第二条线的第三个标签：
  chart.lineLabels[(1,2)].fontSize = 12"""],
      ["lineLabelFormat", """默认值为 None。与 YValueAxis 类似，如果你提供
一个函数或格式字符串，则会在每条线旁边
显示数值标签。你也可以将其设置为 'values' 以显示
在 lineLabelArray 中显式定义的值。"""],
      ["lineLabelArray", """显式的线条标签值数组，如果存在则必须与数据大小匹配。
这些标签值仅在上面的 lineLabelFormat 属性
设置为 'values' 时才会显示。"""]]
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
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - LinePlot 属性""")




heading2("饼图")

disc("""
像往常一样，我们从一个示例开始：
""")

eg("""
from reportlab.graphics.charts.piecharts import Pie
d = Drawing(200, 100)

pc = Pie()
pc.x = 65
pc.y = 15
pc.width = 70
pc.height = 70
pc.data = [10,20,30,40,50,60]
pc.labels = ['a','b','c','d','e','f']

pc.slices.strokeWidth=0.5
pc.slices[3].popout = 10
pc.slices[3].strokeWidth = 2
pc.slices[3].strokeDashArray = [2,2]
pc.slices[3].labelRadius = 1.75
pc.slices[3].fontColor = colors.red
d.add(pc)
""")

from reportlab.graphics.charts.piecharts import Pie

d = Drawing(400, 200)

pc = Pie()
pc.x = 125
pc.y = 25
pc.width = 150
pc.height = 150
pc.data = [10,20,30,40,50,60]
pc.labels = ['a','b','c','d','e','f']

pc.slices.strokeWidth=0.5
pc.slices[3].popout = 10
pc.slices[3].strokeWidth = 2
pc.slices[3].strokeDashArray = [2,2]
pc.slices[3].labelRadius = 1.25
pc.slices[3].fontColor = colors.red

d.add(pc)

draw(d, 'A bare bones pie chart')

disc("""
属性在下面介绍。
饼图有一个 'slices' 集合，我们在同一个表格中记录楔形属性。
""")

disc("")

data=[["属性", "含义"],
      ["data", "数字列表或元组"],
      ["x, y, width, height", """饼图的边界框。
注意 x 和 y 指定的不是中心点，而是左下角，
并且 width 和 height 不必相等；
饼图可以是椭圆形的，切片将被正确绘制。"""],
      ["labels", """None，或字符串列表。
如果你不想要饼图边缘周围的标签，将其设为 None。
由于无法预知切片的大小，我们通常
不建议在饼图内部或周围放置标签；更好的做法是
将它们放在旁边的图例中。"""],
      ["startAngle", """第一个饼图切片的起始角度在哪里？
默认值为 '90'，即十二点钟方向。"""],
      ["direction", """切片按什么方向排列？
默认值为 'clockwise'（顺时针）。"""],
      ["sideLabels", """创建一个标签分两列排列的图表，
左右各一列。"""],
      ["sideLabelsOffset", """这是饼图宽度的一个分数，定义了饼图
与标签列之间的水平距离。"""],
      ["simpleLabels", """默认值为 1。设为 0 以启用可自定义标签
以及在 slices 集合中使用 label_ 前缀的属性。"""],
      ["slices", """切片集合。
这允许你自定义每个楔形或单个楔形。参见下文"""],
      ["slices.strokeWidth", "楔形的边框宽度"],
      ["slices.strokeColor", "边框颜色"],
      ["slices.strokeDashArray", "实线或虚线配置"],
      ["slices.popout", """切片应该从饼图中心突出多远？
默认值为零。"""],
      ["slices.fontName", "标签字体名称"],
      ["slices.fontSize", "标签字体大小"],
      ["slices.fontColor", "标签文字颜色"],
      ["slices.labelRadius", """控制文本标签的锚点。
它是半径的一个分数；0.7 会将文本放置在饼图内部，
1.2 会将其放置在稍外侧。（注意，如果我们添加标签，
我们将保留此属性来指定它们的锚点）"""]]
t=Table(data, colWidths=(130,300))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('FONT',(0,1),(0,-1),'Courier',8,8),
            ('FONT',(1,1),(1,-1),'Times-Roman',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - Pie 属性""")

heading3("自定义标签")

disc("""
每个切片标签可以通过修改 $slices$ 集合中
以 $label_$ 为前缀的属性来单独自定义。
例如，$pc.slices[2].label_angle = 10$ 会更改
第三个标签的角度。
""")

disc("""
在使用这些自定义属性之前，你需要
通过以下方式禁用简单标签：$pc.simplesLabels = 0$
""")

disc("")

data=[["属性", "含义"],
      ["label_dx", """标签的 X 偏移量"""],
      ["label_dy", """标签的 Y 偏移量"""],
      ["label_angle", """标签的角度，默认值 (0) 为水平方向，90 为垂直方向，
180 为倒置"""],
      ["label_boxAnchor", """标签的锚定点"""],
      ["label_boxStrokeColor", """标签框的边框颜色"""],
      ["label_boxStrokeWidth", """标签框的边框宽度"""],
      ["label_boxFillColor", """标签框的填充颜色"""],
      ["label_strokeColor", """标签文字的边框颜色"""],
      ["label_strokeWidth", """标签文字的边框宽度"""],
      ["label_text", """标签的文本"""],
      ["label_width", """标签的宽度"""],
      ["label_maxWidth", """标签可以增长到的最大宽度"""],
      ["label_height", """标签的高度"""],
      ["label_textAnchor", """标签可以增长到的最大高度"""],
      ["label_visible", """如果为 True 则绘制标签"""],
      ["label_topPadding", """框的顶部内边距"""],
      ["label_leftPadding", """框的左侧内边距"""],
      ["label_rightPadding", """框的右侧内边距"""],
      ["label_bottomPadding", """框的底部内边距"""],
      ["label_simple_pointer", """设为 1 以使用简单指针"""],
      ["label_pointer_strokeColor", """指示线的颜色"""],
      ["label_pointer_strokeWidth", """指示线的宽度"""]]
t=Table(data, colWidths=(130,300))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('FONT',(0,1),(0,-1),'Courier',8,8),
            ('FONT',(1,1),(1,-1),'Times-Roman',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - Pie.slices 标签自定义属性""")

heading3("侧边标签")

disc("""
如果将 sideLabels 属性设为 true，则切片的标签
将被放置在两列中，饼图左右各一列，饼图的起始角度将自动设置。
右列的锚点设置为 'start'，左列的锚点设置为 'end'。
饼图边缘到任一列边缘的距离由 sideLabelsOffset 属性决定，
该属性是饼图宽度的一个分数。
如果更改了 xradius，饼图可能会与标签重叠，因此
我们建议将 xradius 保持为 None。
下面是一个示例。
""")

from reportlab.graphics.charts.piecharts import sample5, sample7, sample8
drawing5 = sample5()
draw(drawing5, 'An example of a piechart with sideLabels =1')

disc("""
如果你将 sideLabels 设为 True，那么某些属性
将变得多余，例如 pointerLabelMode。
此外，sideLabelsOffset 只有在 sideLabels
设为 true 时才会影响饼图。
""")

heading4("一些问题")

disc("""
如果切片太多，指针可能会交叉。
""")

drawing7 = sample7()
draw(drawing7, 'An example of pointers crossing')

disc("""
此外，尽管设置了 checkLabelOverlap，如果标签
对应于不相邻的切片，标签仍然可能重叠。
""")

drawing8 = sample8()
draw(drawing8, 'An example of labels overlapping')

heading2("图例")

disc("""
目前可以找到各种初步的图例类，但需要进行清理
以与图表模型的其余部分保持一致。
图例是指定图表颜色和线条样式的天然位置；
我们提议每个图表创建时都带有一个不可见的 $legend$ 属性。
然后可以通过以下方式指定颜色：
""")

eg("""
myChart.legend.defaultColors = [red, green, blue]
""")

disc("""
也可以定义一组共享同一图例的图表：
""")

eg("""
myLegend = Legend()
myLegend.defaultColor = [red, green.....] #yuck!
myLegend.columns = 2
# etc.
chart1.legend = myLegend
chart2.legend = myLegend
chart3.legend = myLegend
""")

# Hack to force a new paragraph before the todo() :-(
disc("")

todo("""这可行吗？与直接指定图表颜色相比，这种复杂化是否可接受？""")



heading3("遗留问题")

disc("""
有几个问题<i>几乎</i>已经解决，但现在将它们
真正公开还为时过早。
不过，以下是正在进行的工作列表：
""")

bullet("""
颜色规范 - 目前图表有一个未公开的属性
$defaultColors$，它提供了一个颜色循环列表，
使得每个数据系列都有自己的颜色。
目前，如果你引入图例，你需要确保它共享
相同的颜色列表。
最有可能的是，这将被替换为一种方案，用于指定
一种包含每个数据系列不同属性值的图例。
这个图例然后也可以被多个图表共享，但本身不需要可见。
""")

bullet("""
其他图表类型 - 当当前设计变得更加稳定后，
我们预计会添加条形图的变体，以处理百分比条形图
以及此处展示的并排变体。
""")


heading3("展望")

disc("""
处理所有图表类型需要一些时间。
我们预计首先完成条形图和饼图，然后
试验实现更通用的图表。
""")


heading3("X-Y 图")

disc("""
大多数其他图表涉及两个值轴，并以某种形式直接绘制 x-y 数据。
数据系列可以绘制为线条、标记符号、两者兼有，
或自定义图形（如开-高-低-收图形）。
它们都共享缩放和轴/标题格式化的概念。
在某个阶段，一个例程将遍历数据系列，并
在给定的 x-y 位置对数据点"执行某些操作"。
给定一个基本的折线图，只需覆盖一个方法（例如
$drawSeries()$）就可以非常容易地派生出
自定义图表类型。
""")


heading3("标记自定义与自定义形状")

disc("""
知名的绘图软件包如 Excel、Mathematica 等提供
了各种标记类型以添加到图表中。
我们可以做得更好 - 你可以编写任何你想要的图表控件，
然后告诉图表将其作为标记使用。
""")


heading4("组合图表")

disc("""
组合多种图表类型非常容易。
你只需在同一个矩形中绘制多个图表（条形图、折线图等），
根据需要抑制坐标轴。
例如，一个图表可以在左侧轴上关联一条表示苏格兰
15 年伤寒病例数的折线，同时在右侧轴上显示一组
表示通货膨胀率的条形图。
如果有人能提醒我们这个示例的出处，我们将
注明来源，并乐意展示这个著名的图表作为示例。
""")


heading3("交互式编辑器")

disc("""
Graphics 包的一个原则是使其图形组件的所有"有趣"
属性都可以通过设置相应公共属性的值来访问和修改。
这使得构建一个类似 GUI 编辑器的工具变得非常有吸引力，
帮助你交互式地完成这些操作。
""")

disc("""
ReportLab 使用 Tkinter 工具包构建了这样一个工具，
它可以加载描述绘图的纯 Python 代码，并记录你的
属性编辑操作。
然后，这个"更改历史"被用来创建该图表子类的代码，
可以立即保存并像任何其他图表一样使用，或作为
另一个交互式编辑会话的新起点。
""")

disc("""
不过，这仍在开发中，发布的条件
还需要进一步明确。
""")


heading3("杂项")

disc("""
本文并未详尽地介绍所有图表类。
这些类正在不断开发中。
要查看当前发行版中的确切内容，请使用
$graphdocpy.py$ 工具。
默认情况下，它将在 reportlab/graphics 上运行，并生成一份
完整报告。
（如果你想在其他模块或包上运行它，
$graphdocpy.py -h$ 会打印帮助信息，告诉你
如何操作。）
""")

disc("""
这就是在"记录控件"一节中提到的工具。
""")

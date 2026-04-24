#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__='3.3.0'
from tools.docco.rl_doc_utils import *

heading2("柱状图")

disc("""
本节介绍当前的 $VerticalBarChart$ 类，它使用了前面介绍的坐标轴和标签。
我们认为这是朝着正确方向迈出的一步，但远非最终版本。
请注意，与我们交流的人大约各占一半，对于应该称其为"垂直"还是"水平"柱状图存在分歧。
我们选择了这个名称，因为"Vertical"出现在"Bar"旁边，
所以我们将其理解为柱条（而非类别轴）是垂直的。
""")

disc("""
像往常一样，我们从一个示例开始：
""")

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

drawing = Drawing(400, 200)

data = [
        (13, 5, 20, 22, 37, 45, 19, 4),
        (14, 6, 21, 23, 38, 46, 20, 5)
        ]

bc = VerticalBarChart()
bc.x = 50
bc.y = 50
bc.height = 125
bc.width = 300
bc.data = data
bc.strokeColor = colors.black

bc.valueAxis.valueMin = 0
bc.valueAxis.valueMax = 50
bc.valueAxis.valueStep = 10

bc.categoryAxis.labels.boxAnchor = 'ne'
bc.categoryAxis.labels.dx = 8
bc.categoryAxis.labels.dy = -2
bc.categoryAxis.labels.angle = 30
bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99',
       'Apr-99','May-99','Jun-99','Jul-99','Aug-99']

drawing.add(bc)

draw(drawing, 'Simple bar chart with two data series')


eg("""
    # code to produce the above chart

    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart

    drawing = Drawing(400, 200)

    data = [
            (13, 5, 20, 22, 37, 45, 19, 4),
            (14, 6, 21, 23, 38, 46, 20, 5)
            ]

    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.strokeColor = colors.black

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 50
    bc.valueAxis.valueStep = 10

    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99',
           'Apr-99','May-99','Jun-99','Jul-99','Aug-99']

    drawing.add(bc)
""")

disc("""
这段代码的大部分内容都是关于设置坐标轴和标签的，我们已经在前面介绍过了。
以下是 $VerticalBarChart$ 类的顶层属性：
""")

disc("")

data=[["Property", "Meaning"],
      ["data", """应为"数字列表的列表"或"数字元组的列表"。如果只有一个系列，
可以这样写：data = [(10,20,30,42),]"""],
      ["x, y, width, height", """定义内部的"绘图矩形"。我们上面用黄色边框高亮显示了它。
请注意，您需要自行将图表放置在绘图中，以便为所有坐标轴标签和刻度线留出空间。
我们指定这个"内部矩形"是因为这样可以非常方便地以一致的方式布局多个图表。"""],
      ["strokeColor", """默认值为 None。这将在绘图矩形周围绘制边框，在调试时可能有用。
坐标轴会覆盖此设置。"""],
      ["fillColor", """默认值为 None。这将用纯色填充绘图矩形。（请注意，我们可以像其他实心形状一样
实现 dashArray 等属性。）"""],
      ["useAbsolute", """默认值为 0。如果为 1，则以下三个属性是以点为单位的绝对值
（这意味着您可以创建柱条超出绘图矩形的图表）；如果为 0，
它们是相对量，表示各元素的比例宽度。"""],
      ["barWidth", """柱条的宽度。默认值为 10。"""],
      ["groupSpacing", """默认值为 5。这是每组柱条之间的间距。如果只有一个系列，
请使用 groupSpacing 而不是 barSpacing 来分隔柱条。
groupSpacing 的一半用于图表中第一个柱条之前，另一半用于最后一个柱条之后。"""],
      ["barSpacing", """默认值为 0。这是每组中各柱条之间的间距。如果您想在上面的示例中
让绿色和红色柱条之间有一点间隙，可以将此值设为非零。"""],
      ["barLabelFormat", """默认值为 None。与 YValueAxis 类似，如果您提供一个函数或格式字符串，
则会在每个柱条旁边绘制显示数值的标签。标签会自动定位在正值柱条的上方
和负值柱条的下方。"""],
      ["barLabels", """用于格式化所有柱条标签的标签集合。由于这是一个二维数组，
您可以使用以下语法显式格式化第二个系列的第三个标签：
  chart.barLabels[(1,2)].fontSize = 12"""],
      ["valueAxis", """值轴，可以按照前面的描述进行格式化。"""],
      ["categoryAxis", """类别轴，可以按照前面的描述进行格式化。"""],

      ["title", """尚未实现。这需要类似于标签的功能，但同时允许直接设置文本。
它应该有一个默认位置在坐标轴下方。"""]]
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
caption("""Table <seq template="%(Chapter)s-%(Table+)s"/> - VerticalBarChart properties""")


disc("""
从这个表格中我们可以推断，在上面的代码中添加以下行应该将柱条组之间的间距加倍
（$groupSpacing$ 属性的默认值为五个点），我们还应该看到同一组柱条之间有
一些微小的间距（$barSpacing$）。
""")

eg("""
    bc.groupSpacing = 10
    bc.barSpacing = 2.5
""")

disc("""
事实上，这正是我们在上面的代码中添加这些行后看到的结果。
请注意，单个柱条的宽度也发生了变化。
这是因为柱条之间增加的间距必须从某个地方"取出"，
因为图表的总宽度保持不变。
""")

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

drawing = Drawing(400, 200)

data = [
        (13, 5, 20, 22, 37, 45, 19, 4),
        (14, 6, 21, 23, 38, 46, 20, 5)
        ]

bc = VerticalBarChart()
bc.x = 50
bc.y = 50
bc.height = 125
bc.width = 300
bc.data = data
bc.strokeColor = colors.black

bc.groupSpacing = 10
bc.barSpacing = 2.5

bc.valueAxis.valueMin = 0
bc.valueAxis.valueMax = 50
bc.valueAxis.valueStep = 10

bc.categoryAxis.labels.boxAnchor = 'ne'
bc.categoryAxis.labels.dx = 8
bc.categoryAxis.labels.dy = -2
bc.categoryAxis.labels.angle = 30
bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99',
       'Apr-99','May-99','Jun-99','Jul-99','Aug-99']

drawing.add(bc)

draw(drawing, 'Like before, but with modified spacing')

disc("""
柱条标签会自动显示在负值柱条下端 <i>下方</i>，
以及正值柱条上端 <i>上方</i>。
""")


disc("""
垂直柱状图也支持堆叠柱条。
您可以通过将 $categoryAxis$ 上的 $style$ 属性设置为 $'stacked'$
来启用此布局。
""")

eg("""
    bc.categoryAxis.style = 'stacked'
""")

disc("""
以下是之前图表的数值以堆叠样式排列的示例。
""")


drawing = Drawing(400, 200)

data = [
        (13, 5, 20, 22, 37, 45, 19, 4),
        (14, 6, 21, 23, 38, 46, 20, 5)
        ]

bc = VerticalBarChart()
bc.x = 50
bc.y = 50
bc.height = 125
bc.width = 300
bc.data = data
bc.strokeColor = colors.black

bc.groupSpacing = 10
bc.barSpacing = 2.5

bc.valueAxis.valueMin = 0
bc.valueAxis.valueMax = 100
bc.valueAxis.valueStep = 20

bc.categoryAxis.labels.boxAnchor = 'ne'
bc.categoryAxis.labels.dx = 8
bc.categoryAxis.labels.dy = -2
bc.categoryAxis.labels.angle = 30
bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99',
       'Apr-99','May-99','Jun-99','Jul-99','Aug-99']
bc.categoryAxis.style = 'stacked'

drawing.add(bc)
draw(drawing, 'Stacking bars on top of each other.')


##Property Value
##data This should be a "list of lists of numbers" or "list of tuples of numbers". If you have just one series, write it as
##data = [(10,20,30,42),]
##
##x, y, width, height These define the inner 'plot rectangle'. We highlighted this with a yellow border above. Note that it is your job to place the chart on the drawing in a way which leaves room for all the axis labels and tickmarks. We specify this 'inner rectangle' because it makes it very easy to lay out multiple charts in a consistent manner.
##strokeColor Defaults to None. This will draw a border around the plot rectangle, which may be useful in debugging. Axes will overwrite this.
##fillColor Defaults to None. This will fill the plot rectangle with a solid color. (Note that we could implement dashArray etc. as for any other solid shape)
##barLabelFormat This is a format string or function used for displaying labels above each bar. We're working on ways to position these labels so that they work for positive and negative bars.
##useAbsolute Defaults to 0. If 1, the three properties below are absolute values in points (which means you can make a chart where the bars stick out from the plot rectangle); if 0, they are relative quantities and indicate the proportional widths of the elements involved.
##barWidth As it says. Defaults to 10.
##groupSpacing Defaults to 5. This is the space between each group of bars. If you have only one series, use groupSpacing and not barSpacing to split them up. Half of the groupSpacing is used before the first bar in the chart, and another half at the end.
##barSpacing Defaults to 0. This is the spacing between bars in each group. If you wanted a little gap between green and red bars in the example above, you would make this non-zero.
##barLabelFormat Defaults to None. As with the YValueAxis, if you supply a function or format string then labels will be drawn next to each bar showing the numeric value.
##barLabels A collection of labels used to format all bar labels. Since this is a two-dimensional array, you may explicitly format the third label of the second series using this syntax:
##    chart.barLabels[(1,2)].fontSize = 12
##
##valueAxis The value axis, which may be formatted as described previously
##categoryAxis The categoryAxis, which may be formatted as described previously
##title, subTitle Not implemented yet. These would be label-like objects whose text could be set directly and which would appear in sensible locations. For now, you can just place extra strings on the drawing.


heading2("折线图")

disc("""
我们将"折线图"（Line Charts）视为本质上与"柱状图"（Bar Charts）相同，
只是用线条代替了柱条。
两者共享相同的类别轴/值轴对。
这与"折线图"（Line Plots）不同，后者的两个轴都是 <i>值轴</i>。
""")

disc("""
以下代码及其输出将作为一个简单的示例。
后面会有更多解释。
目前，您也可以运行工具 $reportlab/lib/graphdocpy.py$（不带任何参数），
并在生成的 PDF 文档中搜索折线图的示例来学习。
""")

eg("""
from reportlab.graphics.charts.linecharts import HorizontalLineChart

drawing = Drawing(400, 200)

data = [
    (13, 5, 20, 22, 37, 45, 19, 4),
    (5, 20, 46, 38, 23, 21, 6, 14)
]

lc = HorizontalLineChart()
lc.x = 50
lc.y = 50
lc.height = 125
lc.width = 300
lc.data = data
lc.joinedLines = 1
catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
lc.categoryAxis.categoryNames = catNames
lc.categoryAxis.labels.boxAnchor = 'n'
lc.valueAxis.valueMin = 0
lc.valueAxis.valueMax = 60
lc.valueAxis.valueStep = 15
lc.lines[0].strokeWidth = 2
lc.lines[1].strokeWidth = 1.5
drawing.add(lc)
""")

from reportlab.graphics.charts.linecharts import HorizontalLineChart

drawing = Drawing(400, 200)

data = [
    (13, 5, 20, 22, 37, 45, 19, 4),
    (5, 20, 46, 38, 23, 21, 6, 14)
]

lc = HorizontalLineChart()
lc.x = 50
lc.y = 50
lc.height = 125
lc.width = 300
lc.data = data
lc.joinedLines = 1
catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
lc.categoryAxis.categoryNames = catNames
lc.categoryAxis.labels.boxAnchor = 'n'
lc.valueAxis.valueMin = 0
lc.valueAxis.valueMax = 60
lc.valueAxis.valueStep = 15
lc.lines[0].strokeWidth = 2
lc.lines[1].strokeWidth = 1.5
drawing.add(lc)

draw(drawing, 'HorizontalLineChart sample')


disc("")

data=[["Property","Meaning"],
      ["data", "要绘制的数据，为数字（列表的）列表。"],
      ["x, y, width, height", """折线图的边界框。
请注意，x 和 y 不是指定中心点，而是指定左下角。"""],
      ["valueAxis", """值轴，可以按照前面的描述进行格式化。"""],
      ["categoryAxis", """类别轴，可以按照前面的描述进行格式化。"""],
 ["strokeColor", """默认值为 None。这将在绘图矩形周围绘制边框，
在调试时可能有用。坐标轴会覆盖此设置。"""],
      ["fillColor", """默认值为 None。这将用纯色填充绘图矩形。"""],
      ["lines.strokeColor", """线条的颜色。"""],
      ["lines.strokeWidth", """线条的宽度。"""],
      ["lineLabels", """用于格式化所有线条标签的标签集合。由于这是一个二维数组，
您可以使用以下语法显式格式化第二条线的第三个标签：
  chart.lineLabels[(1,2)].fontSize = 12"""],
      ["lineLabelFormat", """默认值为 None。与 YValueAxis 类似，如果您提供一个函数或格式字符串，
则会在每条线旁边绘制显示数值的标签。您也可以将其设置为 'values'，
以显示在 lineLabelArray 中显式定义的值。"""],
      ["lineLabelArray", """线标签值的显式数组，如果存在，必须与数据大小匹配。
这些标签值仅在上述 lineLabelFormat 属性设置为 'values' 时才会显示。"""]]
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
caption("""Table <seq template="%(Chapter)s-%(Table+)s"/> - HorizontalLineChart properties""")

from tools.docco.rl_doc_utils import *

heading2('路径与线条')

disc("""正如文本对象专为文本的专门呈现而设计，
路径对象专为图形的专门构建而设计。当路径对象被绘制到 $canvas$ 上时，
它们作为一个整体图形（如矩形）被绘制，整个图形的绘制模式可以调整：
图形的线条可以被绘制（描边）或不绘制；图形的内部可以被填充或不填充；等等。""")

disc("""
例如，$star$ 函数使用路径对象来绘制一颗星
""")

eg(examples.teststar)

disc("""
$star$ 函数的设计旨在用于说明 $pdfgen$ 支持的各种线条样式参数。
""")

illust(examples.star, "线条样式参数")

heading3("线条连接设置")

disc("""
$setLineJoin$ 方法可以调整线段相交时是形成尖角、方角还是圆角。
""")

eg(examples.testjoins)

disc("""
线条连接设置对于粗线才真正有意义，因为对于细线来说效果不明显。
""")

illust(examples.joins, "不同的线条连接样式")

heading3("线条端点设置")

disc("""线条端点设置通过 $setLineCap$ 方法调整，决定终止线端的形状——
是在顶点处精确的方形、超出顶点的方形，还是超出顶点的半圆形。
""")

eg(examples.testcaps)

disc("""线条端点设置与线条连接设置一样，只有在线条较粗时才能清楚地看到。""")

illust(examples.caps, "线条端点设置")

heading3("虚线和断续线")

disc("""
$setDash$ 方法允许将线条断开为点或虚线。
""")

eg(examples.testdashes)

disc("""
虚线或点的模式可以是简单的开/关重复模式，也可以是复杂的重复模式。
""")

illust(examples.dashes, "一些虚线模式")

heading3("使用路径对象创建复杂图形")

disc("""
线段、曲线、弧线和其他图形的组合可以使用路径对象合并为单个图形。
例如，下面显示的函数使用线段和曲线构建了两个路径对象。
该函数稍后将用作铅笔图标构建的一部分。
""")

eg(examples.testpenciltip)

disc("""
请注意，铅笔尖的内部作为一个对象填充，即使它是由多条线段和曲线构成的。
铅笔芯然后使用新的路径对象绘制在其上方。
""")

illust(examples.penciltip, "铅笔尖")

heading2('矩形、圆形、椭圆')

disc("""
$pdfgen$ 模块支持许多常用的形状，如矩形、圆角矩形、椭圆和圆形。
这些图形中的每一种都可以在路径对象中使用，也可以直接绘制在 $canvas$ 上。
例如，下面的 $pencil$ 函数使用矩形和圆角矩形以及各种填充颜色
和一些其他标注来绘制铅笔图标。
""")

eg(examples.testpencil)

pencilnote()

disc("""
请注意，此函数用于创建左侧的"边栏铅笔"。
还要注意元素的绘制顺序很重要，因为例如白色矩形会"擦除"黑色矩形的某些部分，
而"笔尖"会覆盖黄色矩形的某些部分。
""")

illust(examples.pencil, "完整的铅笔")

heading2('贝塞尔曲线')

disc("""
希望构建曲线边界的程序通常使用贝塞尔曲线来形成边界。
""")

eg(examples.testbezier)

disc("""
贝塞尔曲线由四个控制点 $(x1,y1)$、$(x2,y2)$、$(x3,y3)$、$(x4,y4)$ 指定。
曲线从 $(x1,y1)$ 开始，在 $(x4,y4)$ 结束，
从 $(x1,y1)$ 到 $(x2,y2)$ 的线段和从 $(x3,y3)$ 到 $(x4,y4)$ 的线段
都构成曲线的切线。此外，曲线完全包含在以控制点为顶点的凸多边形中。
""")

illust(examples.bezier, "基本贝塞尔曲线")

disc("""
上面的绘制（$testbezier$ 的输出）展示了贝塞尔曲线、
由控制点定义的切线以及以控制点为顶点的凸多边形。
""")

heading3("平滑连接贝塞尔曲线序列")

disc("""
将多条贝塞尔曲线连接起来形成一条平滑曲线通常很有用。
要从多条贝塞尔曲线构建更大的平滑曲线，
请确保在控制点处相连的相邻贝塞尔曲线的切线位于同一条直线上。
""")

eg(examples.testbezier2)

disc("""
$testbezier2$ 创建的图形描述了一条平滑的复杂曲线，
因为相邻的切线"对齐"了，如下所示。
""")

illust(examples.bezier2, "贝塞尔曲线")

heading2("路径对象方法")

disc("""
路径对象通过在画布上的起始点放置"画笔"或"画刷"
并绘制线段或曲线到画布上的其他点来构建复杂图形。
大多数操作从上一次操作的终点开始在画布上绘制，
并将画刷留在新的终点。
""")

eg("""pathobject.moveTo(x,y)""")

disc("""
$moveTo$ 方法抬起画刷（结束当前正在进行的任何线段或曲线序列），
并将画刷放在画布上的新 ^(x,y)^ 位置，以开始新的路径序列。
""")

eg("""pathobject.lineTo(x,y)""")

disc("""
$lineTo$ 方法从当前画刷位置到新 ^(x,y)^ 位置绘制直线段。
""")

eg("""pathobject.curveTo(x1, y1, x2, y2, x3, y3) """)

disc("""
$curveTo$ 方法从当前画刷位置开始绘制贝塞尔曲线，
使用 ^(x1,y1)^、^(x2,y2)^ 和 ^(x3,y3)^ 作为其他三个控制点，
将画刷留在 ^(x3,y3)^。
""")

eg("""pathobject.arc(x1,y1, x2,y2, startAng=0, extent=90) """)

eg("""pathobject.arcTo(x1,y1, x2,y2, startAng=0, extent=90) """)

disc("""
$arc$ 和 $arcTo$ 方法绘制部分椭圆。$arc$ 方法首先"抬起画刷"
并开始新的形状序列。$arcTo$ 方法在绘制部分椭圆之前，
通过线段将部分椭圆的起点连接到当前形状序列。
点 ^(x1,y1)^ 和 ^(x2,y2)^ 定义包围椭圆的矩形的对角点。
$startAng$ 是一个角度（以度为单位），指定从哪里开始部分椭圆，
其中 0 角度是包围矩形右边的中点
（当 ^(x1,y1)^ 是左下角且 ^(x2,y2)^ 是右上角时）。
$extent$ 是在椭圆上遍历的角度（以度为单位）。
""")

eg(examples.testarcs)

disc("""上面的 $arcs$ 函数演示了两种部分椭圆方法。
它产生以下绘制。""")

illust(examples.arcs, "路径对象中的弧线")

eg("""pathobject.rect(x, y, width, height) """)

disc("""$rect$ 方法绘制一个矩形，左下角位于 ^(x,y)^，
具有指定的 ^width^ 和 ^height^。""")

eg("""pathobject.ellipse(x, y, width, height)""")

disc("""$ellipse$ 方法绘制一个椭圆，包含在左下角位于 ^(x,y)^、
具有指定 ^width^ 和 ^height^ 的矩形中。
""")

eg("""pathobject.circle(x_cen, y_cen, r) """)

disc("""$circle$ 方法绘制一个以 ^(x_cen, y_cen)^ 为圆心、
以 ^r^ 为半径的圆。
""")

eg(examples.testvariousshapes)

disc("""
上面的 $variousshapes$ 函数展示了放置在参考网格中的矩形、圆形和椭圆。
""")

illust(examples.variousshapes, "路径对象中的矩形、圆形、椭圆")

eg("""pathobject.close() """)

disc("""
$close$ 方法通过从图形的最后一个点到图形的起始点
（即画刷最近一次通过 $moveTo$ 或 $arc$ 或其他放置操作放置在纸上的点）
绘制线段来关闭当前图形。
""")

eg(examples.testclosingfigures)

disc("""
$closingfigures$ 函数演示了关闭或不关闭图形的效果，
包括线段和部分椭圆。
""")

illust(examples.closingfigures, "关闭和不关闭路径对象图形")

disc("""
关闭或不关闭图形只影响图形的描边轮廓，不影响图形的填充，如上所示。
""")


disc("""
有关使用路径对象进行更广泛绘制的示例，请查看 $hand$ 函数。
""")

eg(examples.testhand)

disc("""
在调试模式下（默认），$hand$ 函数显示了用于构建图形的贝塞尔曲线的切线段。
请注意，切线段对齐的地方曲线平滑连接，而切线段不对齐的地方曲线会出现"锐利边缘"。
""")

illust(examples.hand, "使用贝塞尔曲线绘制的手的轮廓")

disc("""
在非调试模式下使用时，$hand$ 函数只显示贝塞尔曲线。
设置 $fill$ 参数后，图形使用当前填充颜色进行填充。
""")

eg(examples.testhand2)

disc("""
请注意，边框的"描边"在重叠处会绘制在内部填充之上。
""")

illust(examples.hand2, "完成的手，已填充")



heading2("扩展阅读：ReportLab 图形库")

disc("""
到目前为止，我们看到的图形都是在相当低的层次上创建的。
但值得注意的是，还有另一种方式可以使用专用的
高级 <i>ReportLab 图形库</i> 创建更复杂的图形。
""")

disc("""
它可以用于生成高质量、跨平台、可复用的图形，
支持不同的输出格式（矢量和位图），如 PDF、EPS、SVG、JPG 和 PNG。
""")

disc("""
关于其理念和功能的更详细描述将在本文档的第 11 章 <i>图形</i> 中介绍，
其中包含有关现有组件以及如何创建自定义组件的信息。
""")

disc("""
第 11 章还包含有关 ReportLab 图表包及其组件（标签、轴、图例
和不同类型的图表，如条形图、折线图和饼图）的详细信息，
这些直接构建在图形库之上。
""")


##### FILL THEM IN

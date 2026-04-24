#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch7_custom.py
from tools.docco.rl_doc_utils import *

heading1("编写自定义 $Flowable$ 对象")
disc("""
Flowable 旨在成为创建可复用报表内容的开放标准，
您可以轻松创建自己的对象。我们希望随着时间的推移，
能够建立起一个贡献库，为 ReportLab 用户提供丰富的图表、
图形和其他"报表小部件"供其在自己的报表中使用。
本节将向您展示如何创建自己的 Flowable。""")

todo("""我们应该将 Figure 类放入标准库中，
因为它是一个非常实用的基类。""")




heading2("一个非常简单的 $Flowable$")

disc("""
回顾本用户指南 $pdfgen$ 章节中的 $hand$ 函数，
它生成了一个由贝塞尔曲线组合而成的手的封闭图形。
""")
illust(examples.hand, "一只手")
disc("""
要将此绘图或任何其他绘图嵌入到 Platypus Flowable 中，我们必须定义一个
$Flowable$ 的子类，
至少包含一个 $wrap$ 方法和一个 $draw$ 方法。
""")
eg(examples.testhandannotation)
disc("""
$wrap$ 方法必须提供绘图的尺寸——Platypus 主循环用它来决定该元素是否适合当前框架中的剩余空间。
$draw$ 方法在 Platypus 主循环将 $(0,0)$ 原点平移到相应框架中的适当位置后执行对象的绘制。
""")
disc("""
下面是 $HandAnnotation$ Flowable 的一些使用示例。
""")

from reportlab.lib.colors import blue, pink, yellow, cyan, brown
from reportlab.lib.units import inch

handnote()

disc("""默认设置。""")

handnote(size=inch)

disc("""仅一英寸高。""")

handnote(xoffset=3*inch, size=inch, strokecolor=blue, fillcolor=cyan)

disc("""一英寸高，向左偏移，使用蓝色和青色。""")


heading2("修改内置 $Flowable$")
disc("""要修改现有的 Flowable，您应该创建一个派生类，
并重写需要更改的方法以获得所需的行为。""")
disc("""例如，要创建旋转图像，您需要重写现有 Image 类的 wrap 和 draw 方法。""")
import os
from reportlab.platypus import *
I = 'docs/images/replogo.gif'

EmbeddedCode("""
class RotatedImage(Image):
    def wrap(self,availWidth,availHeight):
        h, w = Image.wrap(self,availHeight,availWidth)
        return w, h
    def draw(self):
        self.canv.rotate(90)
        Image.draw(self)
I = RotatedImage('%s')
I.hAlign = 'CENTER'
""" % I,'I')

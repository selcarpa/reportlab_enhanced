from tools.docco.rl_doc_utils import *
from reportlab.lib.codecharts import SingleByteEncodingChart

heading2('坐标系（默认用户空间）')

disc("""
默认情况下，页面上的位置由一对数字标识。例如，$(4.5*inch, 1*inch)$
标识了从左下角开始向右移动 4.5 英寸、向上移动 1 英寸的位置。
""")

disc("""例如，以下函数在 $canvas$ 上绘制了多个元素。""")

eg(examples.testcoords)

disc("""在默认用户空间中，"原点" ^(0,0)^ 位于左下角。
在默认用户空间中执行 $coords$ 函数（针对"演示迷你页面"），我们得到以下结果。""")

illust(examples.coords, '坐标系')

heading3("移动原点：$translate$ 方法")

disc("""通常，将"原点"移动到离开左下角的新位置是很有用的。
$canvas.translate(^x,y^)$ 方法将当前页面的原点移动到当前由 ^(x,y)^ 标识的位置。""")

disc("""例如，以下 translate 函数首先移动原点，然后绘制与上面相同的对象。""")

eg(examples.testtranslate)

disc("""这会产生以下结果。""")

illust(examples.translate, "移动原点：$translate$ 方法")


#illust(NOP) # execute some code

pencilnote()


disc("""
<i>注意：</i>如示例所示，将对象或对象的一部分绘制在"页面之外"是完全可能的。
特别是，一个常见的令人困惑的错误是平移操作将整个绘制移到了页面的可见区域之外。
如果程序生成了空白页面，可能所有绘制的对象都在页面之外。
""")

heading3("缩放：scale 操作")

disc("""另一个重要的操作是缩放。缩放操作 $canvas.scale(^dx,dy^)$
分别按 ^dx^、^dy^ 因子拉伸或缩小 ^x^ 和 ^y^ 维度。
通常 ^dx^ 和 ^dy^ 是相同的——例如，要在所有维度上将绘制缩小一半，
使用 $dx = dy = 0.5$。但为了说明的目的，我们展示一个 $dx$ 和 $dy$ 不同的示例。
""")

eg(examples.testscale)

disc("""这会产生之前显示操作的"矮胖"缩小版本。""")

illust(examples.scale, "缩放坐标系")


#illust(NOP) # execute some code

pencilnote()


disc("""<i>注意：</i>缩放也可能将对象或对象的部分移出页面，
或者可能导致对象"缩小到消失"。""")

disc("""缩放和平移可以组合使用，但操作的顺序很重要。""")

eg(examples.testscaletranslate)

disc("""这个示例函数首先保存当前 $canvas$ 状态，
然后执行 $scale$ 操作，接着执行 $translate$ 操作。
之后函数恢复状态（有效地移除缩放和平移的效果），
然后以不同的顺序执行<i>相同</i>的操作。请注意下面的效果。""")

illust(examples.scaletranslate, "缩放和平移")


#illust(NOP) # execute some code

pencilnote()


disc("""<em>注意：</em>缩放会缩小或放大所有内容，包括线宽，
因此使用 canvas.scale 方法以缩放的微观单位渲染微观绘制
可能会产生一个团块（因为所有线宽都会被放大大幅增加）。
同样，将以米为单位的飞机机翼缩放到厘米渲染时，可能会导致线条
缩小到消失的程度。对于工程或科学目的，
请在使用画布渲染之前在外部缩放和平移单位。""")

heading3("保存和恢复 $canvas$ 状态：$saveState$ 和 $restoreState$")

disc("""
$scaletranslate$ 函数使用了 $canvas$ 对象的一个重要特性：
保存和恢复 $canvas$ 当前参数的能力。
通过将一系列操作放在匹配的 $canvas.saveState()$ 和 $canvas.restoreState()$
操作对中，所有字体、颜色、线条样式、缩放、平移或 $canvas$ 图形状态
的其他方面的更改都可以恢复到 $saveState()$ 时的状态。
请记住，保存/恢复调用必须匹配：一个多余的保存或恢复操作可能导致
意外的不良行为。此外，请记住页面之间<i>不</i>保留任何 $canvas$ 状态，
保存/恢复机制不能跨页面使用。
""")

heading3("镜像")

disc("""
值得注意的是，缩放因子可以为负数，尽管这可能不是特别有用。
例如以下函数
""")

eg(examples.testmirror)

disc("""
创建了由 $coord$ 函数绘制的元素的镜像。
""")

illust(examples.mirror, "镜像图像")

disc("""
请注意，文本字符串是反向绘制的。
""")

heading2("颜色")
disc("""
根据 PDF 将使用的介质，PDF 中通常有两种类型的颜色。
最广为人知的屏幕颜色模型 RGB 可以在 PDF 中使用，
但在专业印刷中，另一种颜色模型 CMYK 主要被使用，
它对油墨如何应用到纸张上提供了更多控制。下面详细介绍这些颜色模型。
""")

heading3("RGB 颜色")
disc("""
$RGB$ 即加色表示遵循计算机屏幕通过添加不同强度的红光、绿光和蓝光
来混合出中间任意颜色的方式，其中白色是将三色光全部开到最大（$1,1,1$）形成的。
""")

disc("""
在 $pdfgen$ 中有三种指定 RGB 颜色的方式：通过名称（使用 $color$ 模块）、
通过红/绿/蓝（加色，$RGB$）值，或通过灰度级别。
下面的 $colors$ 函数演示了这四种方法中的每一种。
""")

eg(examples.testRGBcolors)
illust(examples.colorsRGB, "RGB 颜色模型")

heading4("RGB 颜色透明度")

disc("""
在 $pdfgen$ 中，对象可以绘制在其他对象之上以获得良好的效果。
通常有两种处理空间上重叠对象的方式，默认情况下顶层对象将遮盖
位于其下方的任何其他对象的部分。如果您需要透明效果，有两个选择：
""")

disc("""
1. 如果您的文档打算以专业方式印刷，并且您在 CMYK 颜色空间中工作，
则可以使用 overPrint（叠印）。在叠印模式下，颜色在打印机中物理混合，
从而产生新的颜色。默认情况下会应用 knockout（挖空），只显示顶部对象。
如果这是您打算使用的，请阅读 CMYK 部分。
""")

disc("""
2. 如果您的文档用于屏幕输出，并且您使用 RGB 颜色，
则可以设置 alpha 值，其中 alpha 是颜色不透明度的值。
默认 alpha 值为 $1$（完全不透明），您可以使用 0-1 范围内的任意实数值。
""")

disc("""
Alpha 透明度（$alpha$）类似于叠印，但在 RGB 颜色空间中工作。
下面的示例演示了 alpha 功能。请参考我们的网站
http://www.reportlab.com/snippets/ 并查找 overPrint 和 alpha 的代码片段，
以查看生成下图所示的代码。
""")

eg(examples.testalpha)
illust(examples.alpha, "Alpha 示例")

heading3("CMYK 颜色")
disc("""
$CMYK$ 即减色方法遵循打印机混合三种颜料（青色、品红和黄色）来形成颜色的方式。
由于混合化学品比组合光更困难，因此增加了第四个参数用于控制明暗。
例如，$CMY$ 颜料的化学组合通常无法产生完美的黑色——
而是产生一种浑浊的颜色——因此，为了获得黑色，打印机不使用 $CMY$ 颜料，
而是使用直接的黑色油墨。由于 $CMYK$ 更直接地映射到打印机硬件的工作方式，
以 $CMYK$ 指定的颜色在打印时可能会提供更好的保真度和更好的控制。
""")

disc("""
CMYK 颜色有两种表示方式：每种颜色可以用 0 到 1 之间的实数值表示，
也可以用 0 到 100 之间的整数值表示。根据您的偏好，
您可以使用 CMYKColor（用于实数值）或 PCMYKColor（用于整数值）。
0 表示"无油墨"，因此在白纸上打印得到白色。1（如果使用 PCMYKColor 则为 100）
表示"最大油墨量"。例如，CMYKColor(0,0,0,1) 是黑色，
CMYKColor(0,0,0,0) 表示"无油墨"，CMYKColor(0.5,0,0,0) 表示 50% 的青色。
""")
eg(examples.testCMYKcolors)
illust(examples.colorsCMYK, "CMYK 颜色模型")

heading2("颜色空间检查")
disc("""画布的 $enforceColorSpace$ 参数用于强制文档中使用的颜色模型的一致性。
它接受以下值：CMYK、RGB、SEP、SEP_BLACK、SEP_CMYK。
'SEP' 指命名颜色分色，例如 Pantone 专色——这些可以根据使用的参数
与 CMYK 或 RGB 混合。默认值为 'MIXED'，允许您使用任何颜色空间的颜色。
如果使用的任何颜色无法转换为指定的模型（例如 rgb 和 cmyk），则会引发异常
（更多信息请参见 test_pdfgen_general）。此方法不检查文档中包含的外部图像。
""")

heading2("颜色叠印")

disc("""
当两个 CMYK 着色对象在印刷中重叠时，要么"位于上方"的对象
会挖空其下方对象的颜色，要么两个对象的颜色将在重叠区域混合。
此行为可以使用属性 $overPrint$ 来设置。
""")

disc("""
$overPrint$ 函数将使重叠区域的颜色混合。在下面的示例中，
左侧矩形的颜色在重叠处应该出现混合——如果您看不到此效果，
可能需要在 PDF 查看软件中启用"叠印预览"选项。
某些 PDF 查看器（如 $evince$）不支持叠印；但 Adobe Acrobat Reader 支持它。
""")
illust(examples.overPrint, "overPrint 示例")

heading3("其他对象打印顺序示例")

disc("""
单词"SPUMONI"以白色绘制在彩色矩形之上，
产生了一种"移除"单词内部颜色的视觉效果。
""")

eg(examples.testspumoni)
illust(examples.spumoni, "颜色覆盖绘制")

disc("""
单词的最后几个字母不可见，因为默认的 $canvas$ 背景是白色的，
在白色背景上绘制白色字母不会产生可见效果。
""")

disc("""
这种逐层构建复杂绘制的方法可以在 $pdfgen$ 中使用非常多层——
物理上的限制比处理真实颜料时要少得多。
""")

eg(examples.testspumoni2)

disc("""
$spumoni2$ 函数在 $spumoni$ 绘制之上叠加了一个冰淇淋甜筒。
请注意，甜筒和冰淇淋球的不同部分也相互叠加。
""")
illust(examples.spumoni2, "逐层构建绘制")

heading2('标准字体和文本对象')

disc("""
在 $pdfgen$ 中可以以许多不同的颜色、字体和大小绘制文本。
$textsize$ 函数演示了如何更改文本的颜色、字体和大小，
以及如何在页面上放置文本。
""")

eg(examples.testtextsize)

disc("""
$textsize$ 函数生成以下页面。
""")

illust(examples.textsize, "不同字体和大小的文本")

disc("""
$pdfgen$ 中始终有多种字体可用。
""")

eg(examples.testfonts)

disc("""
$fonts$ 函数列出了始终可用的字体。这些字体不需要存储在 PDF 文档中，
因为 Acrobat Reader 中保证包含它们。
""")

illust(examples.fonts, "14 种标准字体")

disc("""Symbol 和 ZapfDingbats 字体无法正确显示，因为所需的字形不存在于这些字体中。""")

disc("""
有关如何使用任意字体的信息，请参见下一章。
""")


heading2("文本对象方法")

disc("""
要在 PDF 文档中专门呈现文本，请使用文本对象。
文本对象接口提供了在 $canvas$ 级别不直接可用的文本布局参数的详细控制。
此外，它生成的 PDF 更小，渲染速度比许多单独调用 $drawString$ 方法更快。
""")

eg("""textobject.setTextOrigin(x,y)""")
eg("""textobject.setTextTransform(a,b,c,d,e,f)""")
eg("""textobject.moveCursor(dx, dy) # from start of current LINE""")
eg("""(x,y) = textobject.getCursor()""")
eg("""x = textobject.getX(); y = textobject.getY()""")
eg("""textobject.setFont(psfontname, size, leading = None)""")
eg("""textobject.textOut(text)""")
eg("""textobject.textLine(text='')""")
eg("""textobject.textLines(stuff, trim=1)""")

disc("""
上面显示的文本对象方法与基本文本几何相关。
""")

disc("""
文本对象维护一个文本光标，在绘制文本时它在页面上移动。
例如，$setTextOrigin$ 将光标放置在已知位置，
$textLine$ 和 $textLines$ 方法将文本光标向下移动到已绘制的行之后。
""")

eg(examples.testcursormoves1)

disc("""
$cursormoves$ 函数依赖于设置原点后文本光标的自动移动来放置文本。
""")

illust(examples.cursormoves1, "文本光标的移动方式")

disc("""
也可以通过使用 $moveCursor$ 方法（它将光标从当前<i>行</i>的起始位置
偏移移动，而不是从当前光标位置移动，并且正向的 ^y^ 偏移
是向<i>下</i>移动（这与正常几何中正向 ^y^ 通常向上移动相反）
来更明确地控制光标的移动。
""")

eg(examples.testcursormoves2)

disc("""
这里 $textOut$ 不会向下移动一行，而 $textLine$ 函数会向下移动。
""")

illust(examples.cursormoves2, "文本光标的移动方式（续）")

heading3("字符间距")

eg("""textobject.setCharSpace(charSpace)""")

disc("""$setCharSpace$ 方法调整文本的一个参数——字符间距。""")

eg(examples.testcharspace)

disc("""
$charspace$ 函数演示了各种间距设置。
它生成以下页面。""")

illust(examples.charspace, "调整字符间距")

heading3("单词间距")

eg("""textobject.setWordSpace(wordSpace)""")

disc("$setWordSpace$ 方法调整单词之间的间距。")

eg(examples.testwordspace)

disc("""$wordspace$ 函数展示了不同单词间距设置的效果如下。""")

illust(examples.wordspace, "调整单词间距")

heading3("水平缩放")

eg("""textobject.setHorizScale(horizScale)""")

disc("""文本行可以通过 $setHorizScale$ 方法在水平方向上拉伸或缩小。""")

eg(examples.testhorizontalscale)

disc("""水平缩放参数 ^horizScale^ 以百分比给出（默认值为 100），
因此下面显示的 80 设置看起来较窄。
""")
illust(examples.horizontalscale, "调整水平文本缩放")

heading3("行间距（Leading）")

eg("""textobject.setLeading(leading)""")

disc("""一行文本起始位置到下一行起始位置之间的垂直偏移量称为行距（leading）偏移。
$setLeading$ 方法调整行距偏移。
""")

eg(examples.testleading)

disc("""如下所示，如果行距偏移设置得太小，一行的字符可能会覆盖
上一行字符的底部部分。""")

illust(examples.leading, "调整行距")

heading3("其他文本对象方法")

eg("""textobject.setTextRenderMode(mode)""")

disc("""$setTextRenderMode$ 方法允许将文本用作前景来裁剪背景绘制等。""")

eg("""textobject.setRise(rise)""")

disc("""
$setRise$ 方法将文本<super>上移</super>或<sub>下移</sub>
（例如用于创建上标或下标）。
""")

eg("""textobject.setFillColor(aColor);
textobject.setStrokeColor(self, aColor)
# and similar""")

disc("""
这些颜色更改操作更改文本的 <font color=darkviolet>颜色</font>，
其他方面与 $canvas$ 对象的颜色方法类似。""")

#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch4_platypus_concepts.py
from tools.docco.rl_doc_utils import *

#####################################################################################################3


heading1("PLATYPUS - 使用脚本的页面布局与排版")

heading2("设计目标")

disc("""
Platypus 代表"Page Layout and Typography Using Scripts"（使用脚本的页面布局与排版）。
它是一个高级页面布局库，让您能够以最小的努力通过编程方式创建复杂文档。
""")



disc("""
Platypus 的设计试图尽可能将"高级"布局决策与文档内容分离。
因此，例如，段落使用段落样式构建，页面使用页面模板构建，
目的是通过对一个包含段落样式和页面布局规范的共享文件中
少数几行的修改，就可以将具有数千页的数百篇文档重新格式化为
不同的样式规范。
""")


disc("""
Platypus 的整体设计可以被认为具有多个层次，
从上到下依次为""")

disc("<b>$DocTemplates$</b> 文档的最外层容器；")

disc("<b>$PageTemplates$</b> 各种类型页面布局的规范；")

disc("<b>$Frames$</b> 页面中可包含流动文本或图形的区域规范。")

disc("""<b>$Flowables$</b> 应"流入"文档的文本或图形元素（即图像、段落和表格之类的东西，
但不包括页脚或固定页面图形之类的东西）。""")

disc("""<b>$pdfgen.Canvas$</b> 最终从其他层接收文档绘制的最低层。""")

illust(examples.doctemplateillustration, "DocTemplate 结构示意图")

disc("""
上图图形化地展示了 $DocTemplates$、$PageTemplates$ 和 $Flowables$ 的概念。
然而，它具有误导性，因为每个 $PageTemplates$ 实际上可以指定任意数量页面的格式
（而不是图中可能暗示的只有一页）。
""")

disc("""
$DocTemplates$ 包含一个或多个 $PageTemplates$，每个 $PageTemplates$ 包含一个或多个
$Frames$。$Flowables$ 是可以<i>流入</i> $Frame$ 的东西，例如
$Paragraph$ 或 $Table$。
""")

disc("""
要使用 Platypus，您需要从 $DocTemplate$ 类创建一个文档，
并将 $Flowable$ 列表传递给其 $build$ 方法。
文档的 $build$ 方法知道如何将 flowable 列表处理成合理的内容。
""")

disc("""
在内部，$DocTemplate$ 类使用各种事件实现页面布局和格式化。
每个事件都有对应的处理方法，称为 $handle_XXX$，其中 $XXX$ 是事件名称。
一个典型的事件是 $frameBegin$，它发生在机制首次开始使用框架时。
""")

disc("""
一个 Platypus 故事（story）由一系列称为 $Flowables$ 的基本元素组成，
这些元素驱动数据驱动的 Platypus 格式化引擎。
要修改引擎的行为，一种特殊类型的 flowable，$ActionFlowables$，
告诉布局引擎例如跳到下一列或切换到另一个 $PageTemplate$。
""")


heading2("""入门""")

disc("""考虑以下代码序列，它提供了一个非常简单的 Platypus "hello world" 示例。""")

eg(examples.platypussetup)

disc("""首先我们从其他模块导入一些构造函数、一些段落样式和其他便捷工具。""")

eg(examples.platypusfirstpage)

disc("""我们用上面的函数定义文档第一页的固定特征。""")

eg(examples.platypusnextpage)

disc("""由于我们希望第一页之后的页面看起来与第一页不同，
我们为其他页面的固定特征定义了替代布局。
请注意，上面的两个函数使用 $pdfgen$ 级别的画布操作来绘制页面的注释。
""")

eg(examples.platypusgo)

disc("""
最后，我们创建一个故事（story）并构建文档。
请注意，我们在这里使用了一个"预制"文档模板，
它预先内置了页面模板。我们还使用了预构建的段落样式。
这里我们只使用了两种类型的 flowable——$Spacers$ 和 $Paragraphs$。
第一个 $Spacer$ 确保段落跳过标题字符串。
""")

disc("""
要查看此示例程序的输出，请运行模块
$tools/docco/examples.py$（从 ReportLab $source$ 发行版中）
作为"顶级脚本"。脚本解释 $python examples.py$ 将生成 Platypus 输出 $phello.pdf$。
""")


heading2("$Flowables$")
disc("""
$Flowables$ 是可以绘制的东西，具有 $wrap$、$draw$ 和可能的 $split$ 方法。
$Flowable$ 是要绘制的事物的抽象基类，其实例知道自己的大小
并在自己的坐标系中绘制（这要求基 API 在调用 $Flowable.draw$ 方法时
提供绝对坐标系）。要获取实例，使用 $f=Flowable()$。
""")
disc("""
应该注意的是，$Flowable$ 类是一个<i>抽象</i>类，通常只用作基类。
""")
k=startKeep()
disc("""
为了说明 $Flowables$ 的一般使用方式，我们展示了派生类 $Paragraph$
如何在画布上使用和绘制。$Paragraphs$ 非常重要，它们将拥有专门的章节。
""")
eg("""
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph
    from reportlab.pdfgen.canvas import Canvas
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    P=Paragraph('This is a very silly example',style)
    canv = Canvas('doc.pdf')
    aW = 460    # available width and height
    aH = 800
    w,h = P.wrap(aW, aH)    # find required space
    if w<=aW and h<=aH:
        P.drawOn(canv,0,aH)
        aH = aH - h         # reduce the available height
        canv.save()
    else:
        raise ValueError, "Not enough room"
""")
endKeep(k)
heading3("$Flowable$ 用户方法")
eg("""
    Flowable.draw()
""")
disc("""此方法将被调用以要求 flowable 实际渲染自身。
$Flowable$ 类不实现 $draw$。
调用代码应确保 flowable 具有一个 $canv$ 属性，
即应绘制到的 $pdfgen.Canvas$，并且 $Canvas$ 处于适当的状态
（关于平移、旋转等）。通常此方法只会被 $drawOn$ 方法内部调用。
派生类必须实现此方法。
""")
eg("""
    Flowable.drawOn(canvas,x,y)
""")
disc("""
这是控制程序用来将 flowable 渲染到特定画布的方法。
它处理到画布坐标 (<i>x</i>,<i>y</i>) 的平移，并确保
flowable 具有一个 $canv$ 属性，以便 $draw$ 方法
（在基类中未实现）可以在绝对坐标框架中渲染。
""")
eg("""
    Flowable.wrap(availWidth, availHeight)
""")
disc("""此方法将在被请求大小、绘制或其他操作之前由封闭框架调用。
它返回实际使用的大小。""")
eg("""
    Flowable.split(self, availWidth, availheight):
""")
disc("""此方法将在 wrap 失败时由更复杂的框架调用。
简单的 flowable 应返回 []，表示它们无法拆分。
聪明的 flowable 应拆分自身并返回一个 flowable 列表。
客户端代码有责任确保避免重复尝试拆分。
如果空间足够，split 方法应返回 [self]。
否则，flowable 应重新排列自身并返回一个 flowable 列表 $[f0,...]$，
这些将按顺序被考虑。实现的 split 方法应避免更改 $self$，
因为这将允许复杂的布局机制对 flowable 列表进行多次遍历。
""")

heading2("Flowable 定位指南")

disc("""两个默认返回零的方法，提供了关于 flowable 垂直间距的指导：
""")

eg("""
    Flowable.getSpaceAfter(self):
    Flowable.getSpaceBefore(self):
""")
disc("""这些方法返回应在 flowable 之后或之前留出多少空间。
该空间不属于 flowable 本身，即 flowable 的 $draw$ 方法在渲染时
不应考虑它。控制程序将使用返回的值来确定特定 flowable 在上下文中
需要多少空间。
""")

disc("""所有 flowable 都有一个 $hAlign$ 属性：$('LEFT', 'RIGHT', 'CENTER' 或 'CENTRE')$。
对于填满框架整个宽度的段落，这没有效果。对于表格、图像或其他
小于框架宽度的对象，这决定了它们的水平放置位置。

""")


disc("""接下来的章节将介绍最重要的特定类型的 flowable：段落和表格。""")


heading2("框架")
disc("""
$Frames$ 是活跃的容器，它们本身包含在 $PageTemplates$ 中。
$Frames$ 具有位置和大小，并维护剩余可绘制空间的概念。
命令
""")

eg("""
    Frame(x1, y1, width,height, leftPadding=6, bottomPadding=6,
            rightPadding=6, topPadding=6, id=None, showBoundary=0)
""")
disc("""创建一个 $Frame$ 实例，左下角位于坐标 $(x1,y1)$
（相对于使用时的画布），尺寸为 $width$ x $height$。
$Padding$ 参数是用于减少可用绘制空间的正值。
$id$ 参数是运行时使用的标识符，例如 'LeftColumn' 或 'RightColumn' 等。
如果 $showBoundary$ 参数非零，则在运行时绘制框架的边界
（这有时很有用）。
""")
heading3("$Frame$ 用户方法")
eg("""
    Frame.addFromList(drawlist, canvas)
""")
disc("""从 $drawlist$ 前端消耗 $Flowables$，直到框架填满。
如果无法放入一个对象，则抛出异常。""")

eg("""
    Frame.split(flowable,canv)
""")
disc('''要求 flowable 使用可用空间进行拆分，并返回 flowable 列表。
''')

eg("""
    Frame.drawBoundary(canvas)
""")
disc("将框架边界绘制为矩形（主要用于调试）。")
heading3("使用 $Frames$")
disc("""
$Frames$ 可以直接与画布和 flowable 一起使用来创建文档。
$Frame.addFromList$ 方法为您处理 $wrap$ 和 $drawOn$ 调用。
您不需要全部的 Platypus 机制就能将有用的内容输出到 PDF 中。
""")
eg("""
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
story = []

#add some flowables
story.append(Paragraph("This is a Heading",styleH))
story.append(Paragraph("This is a paragraph in <i>Normal</i> style.",
    styleN))
c  = Canvas('mydoc.pdf')
f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1)
f.addFromList(story,c)
c.save()
""")

heading2("文档与模板")

disc("""
$BaseDocTemplate$ 类实现了文档格式化的基本机制。
该类的实例包含一个或多个 $PageTemplates$ 列表，
可用于描述单个页面上信息的布局。
$build$ 方法可用于处理 $Flowables$ 列表以生成 <b>PDF</b> 文档。
""")

CPage(3.0)
heading3("$BaseDocTemplate$ 类")

eg("""
    BaseDocTemplate(self, filename,
                    pagesize=defaultPageSize,
                    pageTemplates=[],
                    showBoundary=0,
                    leftMargin=inch,
                    rightMargin=inch,
                    topMargin=inch,
                    bottomMargin=inch,
                    allowSplitting=1,
                    title=None,
                    author=None,
                    _pageBreakQuick=1,
                    encrypt=None)
""")

disc("""
创建一个适合创建基本文档的文档模板。
它附带了相当多的内部机制，但没有默认的页面模板。
必需的 $filename$ 可以是字符串，即接收所创建 <b>PDF</b> 文档的文件名；
也可以是具有 $write$ 方法的对象，如 $BytesIO$、$file$ 或 $socket$。
""")

disc("""
允许的参数应该是不言自明的，但 $showBoundary$ 控制是否绘制 $Frame$ 边界，
这对于调试非常有用。$allowSplitting$ 参数决定内置方法是否应尝试
在 $Frames$ 之间<i>拆分</i>单个 $Flowables$。
$_pageBreakQuick$ 参数决定进行分页时是否应尝试在结束页面之前
结束页面上的所有框架。encrypt 参数决定文档是否加密以及如何加密。
默认情况下，文档不加密。
如果 $encrypt$ 是字符串对象，它将用作 PDF 的用户密码。
如果 $encrypt$ 是 $reportlab.lib.pdfencrypt.StandardEncryption$ 的实例，
则使用此对象来加密 PDF。这允许对加密设置进行更精细的控制。
""")

heading4("用户 $BaseDocTemplate$ 方法")

disc("""这些对客户端程序员有直接兴趣，因为它们通常是被期望使用的。
""")
eg("""
    BaseDocTemplate.addPageTemplates(self,pageTemplates)
""")
disc("""
此方法用于向现有文档添加一个或一组 $PageTemplates$。
""")
eg("""
    BaseDocTemplate.build(self, flowables, filename=None, canvasmaker=canvas.Canvas)
""")
disc("""
这是应用程序程序员关注的主要方法。
假设文档实例已正确设置，$build$ 方法接受 <i>故事</i>
（以 flowable 列表的形式，即 $flowables$ 参数），
并循环遍历列表，逐个将 flowable 推入格式化机制。
实际上，这导致 $BaseDocTemplate$ 实例调用实例的 $handle_XXX$ 方法
来处理各种事件。
""")
heading4("用户虚拟 $BaseDocTemplate$ 方法")
disc("""
这些在基类中没有任何语义。它们旨在作为纯虚拟钩子
插入布局机制。直接派生类的创建者可以覆盖这些方法，
而不必担心影响布局引擎的属性。
""")
eg("""
    BaseDocTemplate.afterInit(self)
""")
disc("""
这在基类初始化之后调用；派生类可以覆盖此方法
以添加默认的 $PageTemplates$。
""")

eg("""
    BaseDocTemplate.afterPage(self)
""")
disc("""这在页面处理之后调用，并且紧接着当前页面模板的
afterDrawPage 方法之后。派生类可以使用此方法执行
依赖于页面信息的事情，例如字典中页面上的第一个和最后一个单词。
""")

eg("""
    BaseDocTemplate.beforeDocument(self)
""")

disc("""这在文档处理开始之前调用，但在处理机制
就绪之后。因此它可以用于对实例的 $pdfgen.canvas$ 等进行操作。
""")

eg("""
    BaseDocTemplate.beforePage(self)
""")

disc("""这在页面处理开始时调用，并且紧接着当前页面模板的
beforeDrawPage 方法之前。它可用于重置页面特定的信息容器。""")

eg("""
    BaseDocTemplate.filterFlowables(self,flowables)
""")

disc("""这在主 handle_flowable 方法的开始处被调用以过滤 flowable。
返回时，如果 flowables[0] 被设置为 None，则它将被丢弃，
并且主方法立即返回。
""")

eg("""
    BaseDocTemplate.afterFlowable(self, flowable)
""")

disc("""在 flowable 渲染之后调用。感兴趣的类可以使用此钩子
收集有关特定页面或框架上存在什么信息的信息。""")

heading4("$BaseDocTemplate$ 事件处理方法")
disc("""
这些方法构成了布局引擎的大部分。程序员通常不需要直接调用或覆盖这些方法，
除非他们试图修改布局引擎。当然，想要在特定事件 $XXX$ 处干预的经验丰富的程序员，
如果该事件不对应于某个虚拟方法，可以始终从派生类版本中覆盖并调用基方法。
我们通过为每个处理方法提供一个以 '_' 前缀的同名基类方法来简化这一操作。
""")

eg("""
    def handle_pageBegin(self):
        doStuff()
        BaseDocTemplate.handle_pageBegin(self)
        doMoreStuff()

    #using the synonym
    def handle_pageEnd(self):
        doStuff()
        self._handle_pageEnd()
        doMoreStuff()
""")
disc("""
这里我们仅列出方法，作为正在处理的事件的指示。
感兴趣的程序员可以查看源代码。
""")
eg("""
    handle_currentFrame(self,fx)
    handle_documentBegin(self)
    handle_flowable(self,flowables)
    handle_frameBegin(self,*args)
    handle_frameEnd(self)
    handle_nextFrame(self,fx)
    handle_nextPageTemplate(self,pt)
    handle_pageBegin(self)
    handle_pageBreak(self)
    handle_pageEnd(self)
""")

disc("""
使用文档模板可以非常简单；$SimpleDoctemplate$ 是从 $BaseDocTemplate$ 派生的类，
它提供了自己的 $PageTemplate$ 和 $Frame$ 设置。
""")

eg("""
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
story = []

#add some flowables
story.append(Paragraph("This is a Heading",styleH))
story.append(Paragraph("This is a paragraph in <i>Normal</i> style.",
    styleN))
doc = SimpleDocTemplate('mydoc.pdf',pagesize = letter)
doc.build(story)
""")
heading3("$PageTemplates$")
disc("""
$PageTemplate$ 类是一个语义相当少的容器类。
每个实例包含一个 $Frames$ 列表，并具有应在每页开始和结束时调用的方法。
""")
eg("PageTemplate(id=None,frames=[],onPage=_doNothing,onPageEnd=_doNothing)")
disc("""
用于初始化实例，$frames$ 参数应为 $Frames$ 列表，
而可选的 $onPage$ 和 $onPageEnd$ 参数是可调用对象，
其签名应为 $def XXX(canvas,document)$，
其中 $canvas$ 和 $document$ 分别是被绘制的画布和文档。
这些例程旨在用于绘制页面的非流动（即标准）部分。
这些属性函数与纯虚拟方法 $PageTemplate.beforPage$ 和 $PageTemplate.afterPage$
完全平行，后者具有签名 $beforPage(self,canvas,document)$。
这些方法允许使用类派生来定义标准行为，而属性允许实例级别的更改。
$id$ 参数在运行时用于执行 $PageTemplate$ 切换，
因此 $id='FirstPage'$ 或 $id='TwoColumns'$ 是典型的用法。
""")

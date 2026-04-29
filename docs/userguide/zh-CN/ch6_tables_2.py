from tools.docco.rl_doc_utils import *
from reportlab.platypus import Image,ListFlowable, ListItem
import reportlab

heading1("""其他有用的 $Flowables$""")
heading2("""$Preformatted(text, style, bulletText=None, dedent=0, maxLineLength=None, splitChars=None, newLineChars=None)$""")
disc("""
创建一个预格式化段落，不进行换行、行分割或其他文本处理。
文本中的 $XML$ 样式标签不会被处理。
如果 dedent 为非零值，$dedent$ 个公共前导空格将从每行开头移除。
""")
heading3("定义最大行长度")
disc("""
您可以使用 $maxLineLength$ 属性来定义最大行长度。如果行长度超过此最大值，该行将被自动分割。
""")
disc("""
行将在 $splitChars$ 中定义的任何单个字符处分割。如果未为此属性提供值，
行将在以下标准字符处分割：空格、冒号、句号、分号、逗号、连字符、正斜杠、反斜杠、左括号、左方括号和左花括号
""")
disc("""
可以在每个被分割行的开头自动插入字符。您可以将 $newLineChars$ 属性设置为要使用的字符。
""")
EmbeddedCode("""
from reportlab.lib.styles import getSampleStyleSheet
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Code']
text='''
class XPreformatted(Paragraph):
    def __init__(self, text, style, bulletText = None, frags=None, caseSensitive=1):
        self.caseSensitive = caseSensitive
        if maximumLineLength and text:
            text = self.stopLine(text, maximumLineLength, splitCharacters)
        cleaner = lambda text, dedent=dedent: ''.join(_dedenter(text or '',dedent))
        self._setup(text, style, bulletText, frags, cleaner)
'''
t=Preformatted(text,normalStyle,maxLineLength=60, newLineChars='> ')
""")
heading2("""$XPreformatted(text, style, bulletText=None, dedent=0, frags=None)$""")
disc("""
这是 $Paragraph$ 类的非重排形式；$text$ 中允许使用 XML 标签，
其含义与 $Paragraph$ 类中的相同。
与 $Preformatted$ 一样，如果 dedent 为非零值，$dedent$ 个公共前导空格将从每行开头移除。
""")
EmbeddedCode("""
from reportlab.lib.styles import getSampleStyleSheet
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Code']
text='''

   This is a non rearranging form of the <b>Paragraph</b> class;
   <b><font color=red>XML</font></b> tags are allowed in <i>text</i> and have the same

      meanings as for the <b>Paragraph</b> class.
   As for <b>Preformatted</b>, if dedent is non zero <font color="red" size="+1">dedent</font>
       common leading spaces will be removed from the
   front of each line.
   You can have &amp;amp; style entities as well for &amp; &lt; &gt; and &quot;.

'''
t=XPreformatted(text,normalStyle,dedent=3)
""")

heading2("""$Image(filename, width=None, height=None)$""")
disc("""创建一个可流动对象，其中包含由文件 $filename$ 中数据定义的图像，
$filename$ 可以是文件路径、类文件对象或 $reportlab.graphics.shapes.Drawing$ 的实例。
默认的 <b>PDF</b> 图像类型 <i>jpeg</i> 受到支持，如果安装了 <b>PIL</b> 扩展（Python 的），
还可以处理其他图像类型。如果指定了 $width$ 和/或 $height$，
它们将确定显示图像的尺寸，单位为<i>磅</i>。
如果任一维度未指定（或指定为 $None$），则假定图像的相应像素维度以<i>磅</i>为单位并直接使用。
""")
I="../images/lj8100.jpg"
eg("""
Image("lj8100.jpg")
""",after=0.1)
disc("""将显示为""")
try:
    getStory().append(Image(I))
except:
    disc("""此处应显示一张图片。""")
disc("""而""")
eg("""
im = Image("lj8100.jpg", width=2*inch, height=2*inch)
im.hAlign = 'CENTER'
""", after=0.1)
disc('生成')
try:
    im = Image(I, width=2*inch, height=2*inch)
    im.hAlign = 'CENTER'
    getStory().append(Image(I, width=2*inch, height=2*inch))
except:
    disc("""此处应显示一张图片。""")
heading2("""$Spacer(width, height)$""")
disc("""此对象的作用完全符合预期；它在故事中添加一定量的空间。
目前这仅适用于垂直空间。
""")
CPage(1)
heading2("""$PageBreak()$""")
disc("""此 $Flowable$ 表示分页符。它通过有效消耗分配给它的所有垂直空间来工作。
这对于单 $Frame$ 文档是足够的，但对于多帧文档仅相当于帧中断，
因此 $BaseDocTemplate$ 机制在内部检测 $pageBreaks$ 并对其进行特殊处理。
""")
CPage(1)
heading2("""$CondPageBreak(height)$""")
disc("""此 $Flowable$ 在当前 $Frame$ 中剩余垂直空间不足时尝试强制执行 $Frame$ 中断。
因此它的命名可能不太恰当，也许应该重命名为 $CondFrameBreak$。
""")
CPage(1)
heading2("""$KeepTogether(flowables)$""")
disc("""
此复合 $Flowable$ 接受一个 $Flowables$ 列表，并尝试将它们保持在同一个 $Frame$ 中。
如果列表 $flowables$ 中 $Flowables$ 的总高度超过当前帧的可用空间，
则会使用所有空间并强制执行帧中断。
""")
CPage(1)
heading2("""$TableOfContents()$""")
disc("""
可以使用 $TableOfContents$ 可流动对象来生成目录。

以下步骤用于向文档添加目录：
""")

disc("""创建 $TableOfContents$ 的实例。覆盖级别样式（可选）并将对象添加到故事中：""")

eg("""
toc = TableOfContents()
PS = ParagraphStyle
toc.levelStyles = [
    PS(fontName='Times-Bold', fontSize=14, name='TOCHeading1',
            leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
    PS(fontSize=12, name='TOCHeading2',
            leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12),
    PS(fontSize=10, name='TOCHeading3',
            leftIndent=60, firstLineIndent=-20, spaceBefore=0, leading=12),
    PS(fontSize=10, name='TOCHeading4',
            leftIndent=100, firstLineIndent=-20, spaceBefore=0, leading=12),
]
story.append(toc)
""")

disc("""目录条目可以通过手动调用 $TableOfContents$ 对象的 $addEntry$ 方法添加，
也可以通过在您使用的 $DocTemplate$ 的 $afterFlowable$ 方法中发送 $'TOCEntry'$ 通知来自动添加。

传递给 $notify$ 的数据是一个包含三到四项的列表，分别为级别编号、条目文本、页码和条目应指向的可选目标键。
此列表通常在文档模板的方法（如 afterFlowable()）中创建，
通过使用适当数据调用 notify() 方法发出通知，如下所示：
""")

eg('''
def afterFlowable(self, flowable):
    """Detect Level 1 and 2 headings, build outline,
    and track chapter title."""
    if isinstance(flowable, Paragraph):
        txt = flowable.getPlainText()
        if style == 'Heading1':
            # ...
            self.notify('TOCEntry', (0, txt, self.page))
        elif style == 'Heading2':
            # ...
            key = 'h2-%s' % self.seq.nextf('heading2')
            self.canv.bookmarkPage(key)
            self.notify('TOCEntry', (1, txt, self.page, key))
        # ...
''')

disc("""这样，每当样式为 $'Heading1'$ 或 $'Heading2'$ 的段落被添加到故事中时，它就会出现在目录中。
$Heading2$ 条目将是可点击的，因为提供了书签键。
""")

disc("""最后，您需要使用 DocTemplate 的 $multiBuild$ 方法，因为目录需要多次遍历才能生成：""")

eg("""
doc.multiBuild(story)
""")

disc("""以下是一个带有目录的文档的简单但完整的示例：""")

eg('''
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm

class MyDocTemplate(BaseDocTemplate):

    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')])
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))

h1 = PS(name = 'Heading1',
       fontSize = 14,
       leading = 16)

h2 = PS(name = 'Heading2',
       fontSize = 12,
       leading = 14,
       leftIndent = delta)

# Build story.
story = []
toc = TableOfContents()
# For conciseness we use the same styles for headings and TOC entries
toc.levelStyles = [h1, h2]
story.append(toc)
story.append(PageBreak())
story.append(Paragraph('First heading', h1))
story.append(Paragraph('Text in first heading', PS('body')))
story.append(Paragraph('First sub heading', h2))
story.append(Paragraph('Text in first sub heading', PS('body')))
story.append(PageBreak())
story.append(Paragraph('Second sub heading', h2))
story.append(Paragraph('Text in second sub heading', PS('body')))
story.append(Paragraph('Last heading', h1))

doc = MyDocTemplate('mintoc.pdf')
doc.multiBuild(story)
''')

CPage(1)
heading2("""$SimpleIndex()$""")
disc("""
可以使用 $SimpleIndex$ 可流动对象来生成索引。

以下步骤用于向文档添加索引：
""")

disc("""在段落中使用 index 标签来索引术语：""")

eg('''
story = []

...

story.append('The third <index item="word" />word of this paragraph is indexed.')
''')

disc("""创建 $SimpleIndex$ 的实例，并将其添加到故事中您希望其出现的位置：""")

eg('''
index = SimpleIndex(dot=' . ', headers=headers)
story.append(index)
''')

disc("""传递给 SimpleIndex 构造函数的参数在 ReportLab 参考文档中有说明。现在，使用 SimpleIndex.getCanvasMaker() 返回的 canvas maker 来构建文档：""")

eg("""
doc.build(story, canvasmaker=index.getCanvasMaker())
""")

disc("""要构建多级索引，请向 index 标签的 item 属性传递逗号分隔的项列表：""")

eg("""
<index item="terma,termb,termc" />
<index item="terma,termd" />
""")

disc("""terma 将代表最顶层级别，termc 代表最具体的术语。termd 和 termb 将出现在 terma 内的同一级别中。""")

disc("""如果需要索引包含逗号的术语，需要通过双写逗号来转义。为避免三个连续逗号的歧义（转义的逗号后跟列表分隔符，还是列表分隔符后跟转义的逗号？），
请在正确位置引入空格。术语开头或结尾的空格将被移除。""")

eg("""
<index item="comma(,,), ,, ,...   " />
""")

disc("""
这将索引术语 "comma (,)"、"," 和 "..."。
""")

heading2("""$ListFlowable(),ListItem()$""")
disc("""
使用这些类来创建有序和无序列表。列表可以嵌套。
""")

disc("""
$ListFlowable()$ 将创建一个有序列表，其中可以包含任何可流动对象。
该类有许多参数可以更改字体、颜色、大小、样式和列表编号的位置，
或无序列表中的项目符号位置。编号类型也可以设置为使用小写或大写字母（'A,B,C' 等）
或罗马数字（大写或小写），通过 bulletType 属性设置。
要将列表更改为无序类型，请设置 bulletType='bullet'。
""")

disc("""
$ListFlowable()$ 列表中的项目可以通过将其包装在 $ListItem()$ 类中并设置其属性来更改其默认外观。
""")

disc("""
以下将创建一个有序列表，并将第三个项目设置为无序子列表。
""")

EmbeddedCode("""
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()
style = styles["Normal"]
t = ListFlowable(
[
Paragraph("Item no.1", style),
ListItem(Paragraph("Item no. 2", style),bulletColor="green",value=7),
ListFlowable(
                [
                Paragraph("sublist item 1", style),
                ListItem(Paragraph('sublist item 2', style),bulletColor='red',value='square')
                ],
                bulletType='bullet',
                start='square',
                ),
Paragraph("Item no.4", style),
],
bulletType='i'
)
             """)

disc("""为了处理嵌套，$start$ 参数可以设置为可能的起始值列表；对于 $ul$（无序列表），
可接受的起始值是任何 Unicode 字符或 flowables.py 中已知的特定名称，例如
$bulletchar$、$circle$、$square$、$disc$、$diamond$、$diamondwx$、$rarrowhead$、$sparkle$、$squarelrs$ 或 $blackstar$。
对于 $ol$（有序列表），$start$ 可以是 $'1iaAI'$ 中的任何字符，表示不同的编号样式。
""")

heading2("""$BalancedColumns()$""")
disc("""使用 $BalancedColumns$ 类创建一个可流动对象，将其内容可流动对象分成两个或更多大致等大的列。
实际上，系统会合成 $n$ 个帧来容纳内容，该可流动对象尝试在它们之间平衡内容。
当总高度过大时，创建的帧将被分割，分割将保持平衡。
""")
eg("""
from reportlab.platypus.flowables import BalancedColumns
from reportlab.platypus.frames import ShowBoundaryValue
F = [
    list of flowables........
    ]
story.append(
    Balanced(
        F,          #the flowables we are balancing
        nCols = 2,  #the number of columns
        needed = 72,#the minimum space needed by the flowable
        spacBefore = 0,
        spaceAfter = 0,
        showBoundary = None,    #optional boundary showing
        leftPadding=None,       #these override the created frame
        rightPadding=None,      #paddings if specified else the
        topPadding=None,        #default frame paddings
        bottomPadding=None,     #are used
        innerPadding=None,      #the gap between frames if specified else
                                #use max(leftPadding,rightPadding)
        name='',                #for identification purposes when stuff goes awry
        endSlack=0.1,           #height disparity allowance ie 10% of available height
        )
    )
""")

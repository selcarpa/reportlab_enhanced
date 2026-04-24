#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch3_pdffeatures.py
from tools.docco.rl_doc_utils import *

heading1("PDF 特殊功能")
disc("""PDF 提供了许多功能，使电子文档的查看更加高效和舒适，
我们的库公开了其中许多功能。""")

heading2("表单")
disc("""表单（Form）功能允许您在 PDF 文件开头附近一次性创建一个图形和文本块，
然后在后续页面中简单地引用它。如果您要处理 5000 份重复的
业务表单——例如，单页发票或工资条——您只需存储一次背景，
然后在每页上绘制变化的文本。正确使用表单可以大幅减小
文件大小和生产时间，据说甚至可以加快打印速度。
""")
disc("""表单不需要引用整个页面；任何可能经常重复的内容
都应该放在表单中。""")
disc("""下面的示例展示了使用的基本流程。一个真正的
程序可能会在前面定义表单，然后从其他位置引用它们。""")


eg(examples.testforms)

heading2("链接和目标")
disc("""PDF 支持内部超链接。链接类型、目标类型和可由
点击触发的事件范围非常广泛。目前我们只支持从一个文档部分
跳转到另一个部分的基本能力，以及控制跳转后窗口缩放级别的能力。
bookmarkPage 方法定义了一个作为跳转终点的目标。""")
#todo("code example here...")

eg("""
    canvas.bookmarkPage(name,
                        fit="Fit",
                        left=None,
                        top=None,
                        bottom=None,
                        right=None,
                        zoom=None
                        )
""")
disc("""
默认情况下，$bookmarkPage$ 方法将页面本身定义为
目标。跳转到 bookmarkPage 定义的终点后，
PDF 浏览器将显示整个页面，并将其缩放以适应屏幕：""")

eg("""canvas.bookmarkPage(name)""")

disc("""可以通过提供 $fit$ 参数来指示 $bookmarkPage$ 方法
以多种不同方式显示页面。""")

eg("")

t = Table([
           ['fit','所需参数','含义'],
           ['Fit',None,'整个页面适应窗口（默认）'],
           ['FitH','top','顶部坐标位于窗口顶部，宽度缩放以适应'],
           ['FitV','left','左侧坐标位于窗口左侧，高度缩放以适应'],
           ['FitR','left bottom right top','缩放窗口以适应指定矩形'],
           ['XYZ','left top zoom','精细控制。如果省略某个参数，\nPDF 浏览器会将其解释为"保持原样"']
          ])
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,1),'Times-Bold',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))

getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - 不同 fit 类型所需的属性""")

disc("""
注意：$fit$ 设置区分大小写，因此 $fit="FIT"$ 是无效的。
""")


disc("""
有时您希望跳转目标是页面的某个部分。
$FitR$ 适配模式允许您标识一个特定的矩形，
将该区域缩放以填充整个页面。
""")

disc("""
要将显示设置为页面的特定 x 和 y 坐标，并直接控制缩放，
请使用 fit="XYZ"。
""")

eg("""
canvas.bookmarkPage('my_bookmark',fit="XYZ",left=0,top=200)
""")



disc("""
此目标位于页面最左侧，屏幕顶部在位置 200。
因为 $zoom$ 未设置，所以缩放保持用户之前设置的值。
""")

eg("""
canvas.bookmarkPage('my_bookmark',fit="XYZ",left=0,top=200,zoom=2)
""")

disc("""这次缩放设置为将页面放大到正常大小的 2 倍。""")

disc("""
注意：$XYZ$ 和 $FitR$ 适配类型要求其位置参数
（$top, bottom, left, right$）以默认用户空间坐标指定。
它们忽略画布图形状态中生效的任何几何变换。
""")



pencilnote()

disc("""
<i>注意：</i>现在 bookmarkPage 如此通用，之前有两个书签方法
仍受支持但已弃用。它们是 $bookmarkHorizontalAbsolute$
和 $bookmarkHorizontal$。
""")

heading3("定义内部链接")
eg("""
 canvas.linkAbsolute(contents, destinationname, Rect=None, addtopage=1, name=None,
 thickness=0, color=None, dashArray=None, **kw)
 """)

disc("""
    $linkAbsolute$ 方法定义了跳转的起点。当用户
    使用动态查看器（如 Acrobat Reader）浏览生成的文档时，
    当鼠标指针在 $Rect$ 指定的矩形内点击时，查看器将跳转到
    与 $destinationname$ 关联的终点。
    与 $bookmarkHorizontalAbsolute$ 的情况一样，
    矩形 $Rect$ 必须以默认用户空间坐标指定。
    $contents$ 参数指定一段文本，当用户左键点击该区域时
    在查看器中显示。
""")

disc("""
矩形 $Rect$ 必须以元组 ^(x1,y1,x2,y2)^ 的形式指定，
标识默认用户空间中矩形的左下角和右上角。
""")

disc("""
例如以下代码
""")

eg("""
    canvas.bookmarkPage("Meaning_of_life")
""")

disc("""
将当前位置的整个页面定义为一个位置，标识符为
$Meaning_of_life$。要在绘制可能的另一页面时创建指向它的矩形链接，
我们可以使用以下代码：
""")

eg("""
 canvas.linkAbsolute("Find the Meaning of Life", "Meaning_of_life",
                     (inch, inch, 6*inch, 2*inch))
""")

disc("""
默认情况下，在交互式查看期间，链接周围会出现一个矩形。
使用关键字参数 $Border='[0 0 0]'$ 来取消查看期间链接周围的可见矩形。
例如
""")

eg("""
 canvas.linkAbsolute("Meaning of Life", "Meaning_of_life",
                     (inch, inch, 6*inch, 2*inch), Border='[0 0 0]')
""")

disc("""$thickness$、$color$ 和 $dashArray$ 参数可以在未指定 Border 参数时
用于指定边框。如果指定了 Border，它必须是 PDF 数组的字符串表示
或 $PDFArray$（参见 pdfdoc 模块）。$color$ 参数（应为 $Color$ 实例）
等效于关键字参数 $C$，该参数应解析为 PDF 颜色定义（通常是三元素的 PDF 数组）。
""")
disc("""$canvas.linkRect$ 方法在意图上与 $linkAbsolute$ 方法类似，
但有一个额外的参数 $relative=1$，因此旨在遵循本地用户空间变换。""")

heading2("大纲树")
disc("""Acrobat Reader 有一个导航页面，可以容纳文档大纲；
当您打开本指南时，它通常应该是可见的。我们提供了一些简单的方法来添加
大纲条目。通常，制作文档的程序（如本用户指南）
会在到达文档中的每个标题时调用方法
$canvas.addOutlineEntry(^self, title, key, level=0,
closed=None^)$。
""")

disc("""^title^ 是将在左侧窗格中显示的标题。^key^ 必须是一个在文档内
唯一的字符串，用于命名书签，与超链接一样。^level^ 为零——
最高级别——除非另有指定，一次向下跳超过一个级别是错误的
（例如，在级别 0 标题后面跟随级别 2 标题）。
最后，^closed^ 参数指定大纲窗格中的节点默认是关闭的还是打开的。""")

disc("""下面的代码片段取自格式化本用户指南的文档模板。
一个中央处理器依次查看每个段落，当出现新章节时
创建新的大纲条目，将章节标题文本作为标题文本。
键从章节编号获取（此处未显示），因此第 2 章的键为 'ch2'。
大纲条目指向的书签目标是整个页面，
但也可以轻松地指向单个段落。
""")

eg("""
#abridged code from our document template
if paragraph.style == 'Heading1':
    self.chapter = paragraph.getPlainText()
    key = 'ch%d' % self.chapterNo
    self.canv.bookmarkPage(key)
    self.canv.addOutlineEntry(paragraph.getPlainText(),
                                            key, 0, 0)
    """)

heading2("页面过渡效果")


eg("""
 canvas.setPageTransition(self, effectname=None, duration=1,
                        direction=0,dimension='H',motion='I')
                        """)

disc("""
$setPageTransition$ 方法指定一个页面将如何被下一页替换。
例如，将页面过渡效果设置为"溶解"，当前页面在交互式查看期间
被下一页替换时会看起来像融化消失。这些效果在幻灯片演示等场景中
可以为文档增添吸引力。
请参阅参考手册以获取更多关于如何使用此方法的详细信息。
""")

heading2("内部文件注释")

eg("""
 canvas.setAuthor(name)
 canvas.setTitle(title)
 canvas.setSubject(subj)
 """)

disc("""
这些方法不会在文档上自动产生可见效果。
它们为文档添加内部注释。这些注释可以使用浏览器的
"文档信息"菜单项查看，也可以作为一种简单的标准方式，
向不需要解析整个文件的归档软件提供有关文档的基本信息。
要查找注释，请使用标准文本编辑器
（如 MS/Windows 上的 $notepad$ 或 Unix 上的 $vi$ 或 $emacs$）
查看 $*.pdf$ 输出文件，并在文件内容中搜索字符串 $/Author$。
""")

eg(examples.testannotations)

disc("""
如果您希望主题、标题和作者在查看和打印文档时自动显示，
您必须像其他文本一样将它们绘制到文档上。
""")

illust(examples.annotations, "设置文档内部注释")

heading2("加密")

heading3("关于 PDF 文件加密")

disc("""
Adobe 的 PDF 标准允许您在加密 PDF 文件时执行三项相关操作：
""")
bullet("""对文件应用密码保护，使用户必须提供有效密码才能阅读文件，
""")
bullet("""加密文件内容，使其在解密之前毫无用处，以及
""")
bullet("""控制用户在查看文档时是否可以打印、复制粘贴或修改文档。
""")

disc("""
PDF 安全处理器允许为文档指定两个不同的密码：
""")

bullet("""'所有者'密码（又称'安全密码'或'主密码'）
""")

bullet("""'用户'密码（又称'打开密码'）
""")

disc("""
当用户提供其中任一密码时，PDF 文件将被打开、解密并在屏幕上显示。
""")

disc("""
如果提供的是所有者密码，则文件以完全控制权限打开——您可以对其进行任何操作，
包括更改安全设置和密码，或使用新密码重新加密。
""")

disc("""
     如果提供的是用户密码，则以更受限的模式打开文件。限制是在文件加密时设置的，
将允许或拒绝用户执行以下操作：
""")

bullet("""
修改文档内容
""")

bullet("""
从文档复制文本和图形
""")

bullet("""
添加或修改文本注释和交互式表单字段
""")

bullet("""
打印文档
""")

disc("""
请注意，所有受密码保护的 PDF 文件都是加密的，但并非所有加密的 PDF 都受密码保护。
如果文档的用户密码为空字符串，打开文件时将不会提示输入密码。
如果您仅使用所有者密码保护文档，打开文件时也不会提示输入密码。
如果在加密 PDF 文件时将所有者密码和用户密码设置为相同的字符串，
文档将始终以用户访问权限打开。这意味着可以创建一个例如任何人都无法打印的文件，
即使是创建该文件的人也不行。
""")

t = Table([
           ['所有者密码\n已设置？','用户密码\n已设置？','结果'],
           ['Y','-','打开文件时无需密码。\n限制适用于所有人。'],
           ['-','Y','打开文件时需要用户密码。\n限制适用于所有人。'],
           ['Y','Y','打开文件时需要密码。\n仅在提供用户密码时适用限制。'],
          ],[90, 90, 260])

t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,0),'Times-Bold',10,12),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))

getStory().append(t)

disc("""
当 PDF 文件被加密时，加密应用于文件中的所有字符串和流。
这防止了没有密码的人简单地从 PDF 文件中删除密码以获取访问权限——
它使文件在没有实际密码的情况下毫无用处。
""")
disc("""
PDF 的标准加密方法使用 MD5 消息摘要算法
（如 RFC 1321《MD5 消息摘要算法》中所述）和一种称为 RC4 的加密算法。
RC4 是一种对称流密码——相同的算法用于加密和解密，
并且算法不会改变数据的长度。
""")

heading3("如何使用加密")

disc("""
     可以通过向 canvas 对象传递参数来加密文档。
     """)

disc("""
     如果参数是字符串对象，它将用作 PDF 的用户密码。
     """)

disc("""
     参数也可以是 $reportlab.lib.pdfencrypt.StandardEncryption$ 类的实例，
     这允许对加密设置进行更精细的控制。
     """)

disc("""
     $StandardEncryption$ 构造函数接受以下参数：
     """)

eg("""
    def __init__(self, userPassword,
            ownerPassword=None,
            canPrint=1,
            canModify=1,
            canCopy=1,
            canAnnotate=1,
            strength=40):
    """)

disc("""
     $userPassword$ 和 $ownerPassword$ 参数设置加密 PDF 上的相应密码。
     """)

disc("""
     布尔标志 $canPrint$、$canModify$、$canCopy$、$canAnnotate$ 确定当仅提供用户密码时
    用户是否可以对 PDF 执行相应操作。
    """)
disc("""
    如果用户在打开 PDF 时提供所有者密码，则无论标志如何设置，都可以执行所有操作。
    """)

heading3("示例")

disc("""
     要创建一个名为 hello.pdf 的文档，用户密码为 'rptlab'，且不允许打印，
     请使用以下代码：
     """)

eg("""
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt

enc=pdfencrypt.StandardEncryption("rptlab",canPrint=0)

def hello(c):
    c.drawString(100,100,"Hello World")
c = canvas.Canvas("hello.pdf",encrypt=enc)
hello(c)
c.showPage()
c.save()

""")

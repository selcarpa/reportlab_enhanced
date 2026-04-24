#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch5_paragraphs.py
from tools.docco.rl_doc_utils import *

#begin chapter oon paragraphs
heading1("段落")
disc("""
$reportlab.platypus.Paragraph$ 类是 Platypus $Flowables$ 中最有用的类之一；
它能够格式化相当任意的文本，并支持使用 XML 风格的标记进行内联字体样式和颜色更改。
格式化文本的整体形状可以设置为两端对齐、右对齐、左对齐或居中。
XML 标记甚至可以用来插入希腊字母或创建上下标。
""")
disc("""以下文本创建了一个 $Paragraph$ 类的实例：""")
eg("""Paragraph(text, style, bulletText=None)""")
disc("""$text$ 参数包含段落的文本；多余的空白字符会从文本两端和内部换行符后被去除。
这使得在 <b>Python</b> 脚本中可以方便地使用缩进的三引号文本。
$bulletText$ 参数提供了段落默认项目符号的文本。
段落的文本和项目符号的字体及其他属性通过 style 参数来设置。
""")
disc("""
$style$ 参数应该是 $ParagraphStyle$ 类的一个实例，通常通过以下方式获取：""")
eg("""
from reportlab.lib.styles import ParagraphStyle
""")
disc("""
这个容器类提供了一种结构化的方式来设置多个默认段落属性。
样式被组织在一个称为 $stylesheet$ 的字典样式对象中，
允许通过 $stylesheet['BodyText']$ 的方式访问样式。系统提供了一个示例样式表。
""")
eg("""
from reportlab.lib.styles import getSampleStyleSheet
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Normal']
""")
disc("""
可以为 $Paragraph$ 设置的选项可以从 $ParagraphStyle$ 的默认值中看到。
以下划线（'_'）开头的值源自 $reportlab.rl_config$ 模块中的默认值，
而后者又源自 $reportlab.rl_settings$ 模块。
""")
heading4("$class ParagraphStyle$")
eg("""
class ParagraphStyle(PropertySet):
    defaults = {
        'fontName':_baseFontName,
        'fontSize':10,
        'leading':12,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_LEFT,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':_baseFontName,
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': black,
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform':None,
        'endDots':None,
        'splitLongWords':1,
        'underlineWidth': _baseUnderlineWidth,
        'bulletAnchor': 'start',
        'justifyLastLine': 0,
        'justifyBreaks': 0,
        'spaceShrinkage': _spaceShrinkage,
        'strikeWidth': _baseStrikeWidth,    #stroke width
        'underlineOffset': _baseUnderlineOffset,    #fraction of fontsize to offset underlines
        'underlineGap': _baseUnderlineGap,      #gap for double/triple underline
        'strikeOffset': _baseStrikeOffset,  #fraction of fontsize to offset strikethrough
        'strikeGap': _baseStrikeGap,        #gap for double/triple strike
        'linkUnderline': _platypus_link_underline,
        #'underlineColor':  None,
        #'strikeColor': None,
        'hyphenationLang': _hyphenationLang,
        'uriWasteReduce': _uriWasteReduce,
        'embeddedHyphenation': _embeddedHyphenation,
        }
""")

heading2("使用段落样式")

#this will be used in the ParaBox demos.
sample = """You are hereby charged that on the 28th day of May, 1970, you did
willfully, unlawfully, and with malice of forethought, publish an
alleged English-Hungarian phrase book with intent to cause a breach
of the peace.  How do you plead?"""


disc("""$Paragraph$ 和 $ParagraphStyle$ 类共同处理大多数常见的格式化需求。
以下示例以各种样式绘制段落，并添加了一个边界框，以便您可以确切地看到段落占用了多少空间。""")

s1 = ParagraphStyle('Normal')
parabox(sample, s1, '默认的 $ParagraphStyle$')

disc("""$spaceBefore$ 和 $spaceAfter$ 两个属性正如其名称所描述的那样工作，
但在框架的顶部或底部有所不同。在框架顶部，$spaceBefore$ 会被忽略；
在框架底部，$spaceAfter$ 会被忽略。
这意味着您可以指定 'Heading2' 样式在页面中间时有两英寸的前置间距，
但在页面顶部不会产生大量空白。
这两个属性应被视为对 Frame 的"请求"，不属于段落本身占用的空间。""")

disc("""$fontSize$ 和 $fontName$ 标签的含义是显而易见的，但设置 $leading$ 非常重要。
这是相邻文本行之间的间距；一个很好的经验法则是将其设置为比字号大 20%。
要获得双倍行距的文本，请使用较大的 $leading$。
如果将 $autoLeading$（默认值为 $"off"$）设置为 $"min"$（使用观察到的行距，即使小于指定值）
或 $"max"$（使用观察值和指定值中的较大者），系统将尝试逐行确定行距。
当行中包含不同字号等情况时，这可能很有用。""")

disc("""下图展示了前后间距和增大的行距：""")

parabox(sample,
        ParagraphStyle('Spaced',
                       spaceBefore=6,
                       spaceAfter=6,
                       leading=16),
        '前后间距和增大的行距'
        )

disc("""$borderPadding$ 属性调整段落与其背景边框之间的内边距。
它可以是一个单一值，也可以是一个包含 2 到 4 个值的元组。
这些值的应用方式与层叠样式表（CSS）相同。
如果给出单个值，则该值应用于所有四个边。
如果给出多个值，则按从顶部开始的顺时针顺序应用到各边。
如果给出两个或三个值，则缺失的值取自对边。
请注意，在以下示例中，黄色框是由段落本身绘制的。""")

parabox(sample,
        ParagraphStyle('padded',
                       borderPadding=(7, 2, 20),
                       borderColor='#000000',
                       borderWidth=1,
                       backColor='#FFFF00'),
        '可变内边距'
        )

disc("""$leftIndent$ 和 $rightIndent$ 属性正如您所期望的那样工作；
$firstLineIndent$ 会被添加到第一行的 $leftIndent$ 上。
如果您想要整齐的左边缘，请记住将 $firstLineIndent$ 设置为 0。""")

parabox(sample,
        ParagraphStyle('indented',
                       firstLineIndent=+24,
                       leftIndent=24,
                       rightIndent=24),
        '左右各三分之一英寸缩进，首行三分之二英寸缩进'
        )

disc("""将 $firstLineIndent$ 设置为负数，$leftIndent$ 设置得更大，
并使用不同的字体（稍后我们将展示如何操作！），可以实现定义列表的效果：。""")

parabox('<b><i>Judge Pickles: </i></b>' + sample,
        ParagraphStyle('dl',
                       leftIndent=36),
        '定义列表'
        )

disc("""$alignment$ 有四个可能的值，定义为模块 <i>reportlab.lib.enums</i> 中的常量。
它们分别是 TA_LEFT、TA_CENTER（或 TA_CENTRE）、TA_RIGHT 和 TA_JUSTIFY，
对应值为 0、1、2 和 4。它们的作用正如您所期望的那样。""")

disc("""将 $wordWrap$ 设置为 $'CJK'$ 可以获得亚洲语言的换行方式。
对于普通的西方文本，您可以通过 $allowWidows$ 和 $allowOrphans$ 的值
来更改换行算法处理<i>孤行</i>（widows）和<i>孤字</i>（orphans）的方式。
这两者通常都应设置为 $0$，但由于历史原因，我们允许了<i>孤行</i>。
文本的默认颜色可以通过 $textColor$ 设置，段落背景颜色可以通过 $backColor$ 设置。
段落的边框属性可以通过 $borderWidth$、$borderPadding$、$borderColor$ 和 $borderRadius$ 来修改。""")

disc("""$textTransform$ 属性可以是 <b><i>None</i></b>、<i>'uppercase'</i> 或 <i>'lowercase'</i> 以获得相应的效果，
以及 <i>'capitalize'</i> 来实现首字母大写。""")
disc("""$endDots$ 属性可以是 <b><i>None</i></b>、一个字符串，或一个具有 text 属性以及可选的 fontName、fontSize、textColor、backColor 和 dy（y 偏移量）属性的对象，
用于指定左/右对齐段落最后一行的尾部内容。""")
disc("""$splitLongWords$ 属性可以设置为假值，以避免拆分非常长的单词。""")
disc("""$bulletAnchor$ 属性可以是 <i>'start'</i>、<i>'middle'</i>、<i>'end'</i> 或 <i>'numeric'</i>，
用于控制项目符号的锚定位置。""")
disc("""$justifyBreaks$ 属性控制使用 $&lt;br/&gt;$ 标签故意断开的行是否应该两端对齐。""")
disc("""$spaceShrinkage$ 属性是一个分数值，指定段落行的间距可以缩小多少以使其适合；
通常设置为类似 0.05 的值。""")
disc("""$underlineWidth$、$underlineOffset$、$underlineGap$ 和 $underlineColor$ 属性控制使用 $&lt;u&gt;$ 或链接标签时的下划线行为。
这些标签可以覆盖这些属性的值。width 和 offset 的属性值是 $fraction * Letter$，
其中 letter 可以是 $P$、$L$、$f$ 或 $F$ 之一，表示字号比例。
$P$ 使用标签处的字号，$F$ 是标签内的最大字号，$f$ 是标签内的初始字号。
$L$ 表示全局（段落样式）字号。
$strikeWidth$、$strikeOffset$、$strikeGap$ 和 $strikeColor$ 属性对删除线执行相同的控制。
""")
disc("""$linkUnderline$ 属性控制链接标签是否自动添加下划线。""")
disc("""如果安装了 $pyphen$ Python 模块，$hyphenationLang$ 属性控制将使用哪种语言对没有显式嵌入连字符的单词进行断字处理。""")
disc("""如果设置了 $embeddedHyphenation$，系统将尝试在嵌入的连字符处拆分单词。""")
disc("""$uriWasteReduce$ 属性控制我们如何尝试拆分长 URI。
它是我们将一行中浪费空间视为过多的比例阈值。
$reportlab.rl_settings$ 模块中的默认值为 <i>0.5</i>，这意味着如果我们至少浪费了一半的行空间，
就会尝试拆分看起来像 URI 的单词。""")
disc("""目前断字和 URI 拆分功能默认是关闭的。
您需要通过使用文件 $~/.rl_settings$ 或在 Python 路径中添加模块 $reportlab_settings.py$ 来修改默认设置。合适的值如下：""")
eg("""
    hyphenationLanguage='en_GB'
    embeddedHyphenation=1
    uriWasteReduce=0.3
    """)



heading2("段落 XML 标记标签")
disc("""XML 标记可用于修改或指定整体段落样式，也可用于指定段落内标记。""")

heading3("最外层的 &lt; para &gt; 标签")


disc("""
段落文本可以选择性地被包裹在
&lt;para attributes....&gt;
&lt;/para&gt;
标签中。开始 &lt;para&gt; 标签的属性（如果有）会影响与 $Paragraph$ 的 $text$ 和/或 $bulletText$ 一起使用的样式。
""")
disc(" ")
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.paraparser import _addAttributeNames, _paraAttrMap, _bulletAttrMap
from reportlab.lib import colors

def getAttrs(A):
    _addAttributeNames(A)
    S={}
    for k, v in A.items():
        a = v[0]
        if a not in S:
            S[a] = [k]
        else:
            S[a].append(k)

    K = list(sorted(S.keys()))
    K.sort()
    D=[('Attribute','Synonyms')]
    for k in K:
        D.append((k,", ".join(list(sorted(S[k])))))
    cols=2*[None]
    rows=len(D)*[None]
    return D,cols,rows

story = []
t=Table(*getAttrs(_paraAttrMap))
t.setStyle(TableStyle([
            ('FONT',(0,0),(-1,1),'Times-Bold',10,12),
            ('FONT',(0,1),(-1,-1),'Courier',8,8),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
getStory().append(t)
caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - 样式属性的同义词""")

disc("""我们为 Python 属性名提供了一些有用的同义词，
包括小写版本，以及 HTML 标准中存在的等效属性（如果有的话）。
这些新增内容使得构建 XML 输出应用程序更加容易，
因为许多段落内标记可能不需要翻译。
下表显示了最外层段落标签中允许的属性和同义词。""")

CPage(1)
heading2("段落内标记")
disc("""<![CDATA[在每个段落中，我们使用一组基本的 XML 标签来提供标记。
最基本的标签包括粗体 (<b>...</b>)、斜体 (<i>...</i>) 和下划线 (<u>...</u>)。
其他允许的标签有 strong (<strong>...</strong>) 和删除线 (<strike>...</strike>)。
<link> 和 <a> 标签可用于引用 URI、文档或当前文档中的书签。
<a> 标签的变体可用于标记文档中的位置。
还允许使用换行 (<br/>) 标签。]]>
""")

parabox2("""<b>You are hereby charged</b> that on the 28th day of May, 1970, you did
willfully, unlawfully, and <i>with malice of forethought</i>, publish an
alleged English-Hungarian phrase book with intent to cause a breach
of the peace.  <u>How do you plead</u>?""", "简单的粗体和斜体标签")
parabox2("""This <a href="#MYANCHOR" color="blue">is a link to</a> an anchor tag ie <a name="MYANCHOR"/><font color="green">here</font>.
This <link href="#MYANCHOR" color="blue" fontName="Helvetica">is another link to</link> the same anchor tag.""",
"锚点和链接")
disc("""<b>link</b> 标签可以用作引用，但不能用作锚点。
a 和 link 超链接标签有额外的属性 <i>fontName</i>、<i>fontSize</i>、<i>color</i> 和 <i>backColor</i>。
超链接引用可以使用的方案包括 <b>http:</b><i>（外部网页）</i>、<b>pdf:</b><i>（不同的 PDF 文档）</i>
或 <b>document:</b><i>（相同的 PDF 文档）</i>；缺少方案时被视为 <b>document</b>，
当引用以 # 开头时也是如此（在这种情况下锚点应省略 #）。
任何其他方案都被视为某种 URI。
""")

parabox2("""<strong>You are hereby charged</strong> that on the 28th day of May, 1970, you did
willfully, unlawfully, <strike>and with malice of forethought</strike>, <br/>publish an
alleged English-Hungarian phrase book with intent to cause a breach
of the peace. How do you plead?""", "Strong、strike 和 break 标签")

heading3("$&lt;font&gt;$ 标签")
disc("""$&lt;font&gt;$ 标签可用于更改段落中任何子字符串的字体名称、大小和文本颜色。
合法的属性包括 $size$、$face$、$name$（与 $face$ 相同）、$color$ 和 $fg$（与 $color$ 相同）。
$name$ 是字体族名称，不带任何 'bold' 或 'italic' 后缀。
颜色可以是 HTML 颜色名称或以多种方式编码的十六进制字符串；
有关允许的格式，请参见 ^reportlab.lib.colors^。""")

parabox2("""<font face="times" color="red">You are hereby charged</font> that on the 28th day of May, 1970, you did
willfully, unlawfully, and <font size=14>with malice of forethought</font>,
publish an
alleged English-Hungarian phrase book with intent to cause a breach
of the peace.  How do you plead?""", "$font$ 标签")

heading3("上标和下标")
disc("""上标和下标通过 <![CDATA[<super>/<sup> 和 <sub> 标签支持，
其工作方式正如您所期望的那样。
此外，这三个标签还有 rise 和 size 属性，可以选择性地设置上标/下标文本的上升/下降量和字号。
此外，大多数希腊字母可以通过 <greek></greek> 标签或使用 mathML 实体名称来访问。]]>""")

##parabox2("""<greek>epsilon</greek><super><greek>iota</greek>
##<greek>pi</greek></super> = -1""", "Greek letters and subscripts")

parabox2("""Equation (&alpha;): <greek>e</greek> <super rise=9 size=6><greek>ip</greek></super>  = -1""",
         "希腊字母和上标")

heading3("内联图像")
disc("""我们可以使用 &lt;img/&gt; 标签在段落中嵌入图像，该标签具有 $src$、$width$、$height$ 属性，含义不言自明。
$valign$ 属性可以设置为类似 CSS 的值，包括 "baseline"、"sub"、"super"、"top"、"text-top"、"middle"、"bottom"、"text-bottom"；
该值也可以是数字百分比或绝对值。
""")
parabox2("""<para autoLeading="off" fontSize=12>This &lt;img/&gt; <img src="docs/images/testimg.gif" valign="top"/> is aligned <b>top</b>.<br/><br/>
This &lt;img/&gt; <img src="docs/images/testimg.gif" valign="bottom"/> is aligned <b>bottom</b>.<br/><br/>
This &lt;img/&gt; <img src="docs/images/testimg.gif" valign="middle"/> is aligned <b>middle</b>.<br/><br/>
This &lt;img/&gt; <img src="docs/images/testimg.gif" valign="-4"/> is aligned <b>-4</b>.<br/><br/>
This &lt;img/&gt; <img src="docs/images/testimg.gif" valign="+4"/> is aligned <b>+4</b>.<br/><br/>
This &lt;img/&gt; <img src="docs/images/testimg.gif" width="10"/> has width <b>10</b>.<br/><br/>
</para>""","内联图像")
disc("""$src$ 属性可以引用远程位置，例如 $src="https://www.reportlab.com/images/logo.gif"$。
默认情况下，我们将 $rl_config.trustedShemes$ 设置为 $['https','http', 'file', 'data', 'ftp']$，
$rl_config.trustedHosts=None$，后者表示无限制。
您可以使用覆盖文件（如 $reportlab_settings.py$ 或 $~/.reportlab_settings$）修改这些变量。
或者通过环境变量 $RL_trustedSchemes$ 和 $RL_trustedHosts$ 以逗号分隔的字符串来设置。
请注意，$trustedHosts$ 的值可以包含 <b>glob</b> 通配符，因此 <i>*.reportlab.com</i> 将匹配相应的域名。
<br/><span color="red"><b>*注意*</b></span> 使用 <i>trustedHosts</i> 和/或 <i>trustedSchemes</i> 可能无法控制查看器应用程序检测到 $URI$ 模式时的行为和操作。""")

heading3("$&lt;u&gt;$ 和 $&lt;strike&gt;$ 标签")
disc("""这些标签可用于执行显式的下划线或删除线操作。
这些标签具有 $width$、$offset$、$color$、$gap$ 和 $kind$ 属性。
$kind$ 属性控制绘制的线条数量（默认 $kind=1$），当 $kind>1$ 时，
$gap$ 属性控制线条之间的距离。""")

heading3("$&lt;nobr&gt;$ 标签")
disc("""如果启用了断字功能，$&lt;nobr&gt;$ 标签会抑制它，
因此 $&lt;nobr&gt;averylongwordthatwontbebroken&lt;/nobr&gt; 将不会被拆分。""")

heading3("段落编号和列表")
disc("""$&lt;seq&gt;$ 标签为编号列表、章节标题等提供了全面的支持。
它充当 ^reportlab.lib.sequencer^ 中 $Sequencer$ 类的接口。
在整个文档中，它们被用于编号标题和图表。
您可以创建任意多个独立的"计数器"，通过 $id$ 属性访问；
每次访问时计数器值会递增一。
$seqreset$ 标签用于重置计数器。
如果您希望从 1 以外的数字重新开始，请使用语法 &lt;seqreset id="mycounter" base="42"&gt;。
让我们试一试：""")

parabox2("""<seq id="spam"/>, <seq id="spam"/>, <seq id="spam"/>.
Reset<seqreset id="spam"/>.  <seq id="spam"/>, <seq id="spam"/>,
<seq id="spam"/>.""",  "基本序列")

disc("""您可以通过使用 &lt;seqdefault id="Counter"&gt; 标签将一个计数器 ID 指定为 <i>默认</i> 计数器，
从而省去每次指定 ID 的麻烦；之后每当未指定计数器 ID 时就会使用它。
这可以节省一些输入，特别是在处理多级列表时；您只需在进入或退出某个级别时更改计数器 ID。""")

parabox2("""<seqdefault id="spam"/>Continued... <seq/>,
<seq/>, <seq/>, <seq/>, <seq/>, <seq/>, <seq/>.""",
"默认序列")

disc("""最后，可以使用 Python 字符串格式化的变体和 &lt;seq&gt; 标签中的 $template$ 属性来访问多级序列。
这用于所有图表的标题以及二级标题。
子字符串 $%(counter)s$ 提取计数器的当前值而不递增它；
附加加号如 $%(counter)s$ 则会递增计数器。
图表标题使用的模式如下所示：""")

parabox2("""Figure <seq template="%(Chapter)s-%(FigureNo+)s"/> - Multi-level templates""",
"多级模板")

disc("""我们稍微做了一点手脚——真正的文档使用的是 'Figure'，但上面的文本使用的是 'FigureNo'——否则我们会搞乱我们的编号！""")

heading2("项目符号和段落编号")
disc("""除了三个缩进属性之外，还需要一些其他参数来正确处理项目符号和编号列表。
我们在这里讨论这个话题，因为您现在已经看到了如何处理编号。
段落可以在其构造函数中传入一个可选的 ^bulletText^ 参数；
或者，项目符号文本可以放在段落头部的 $<![CDATA[<bullet>..</bullet>]]>$ 标签中。
这段文本将绘制在段落的第一行，其 x 原点由样式的 $bulletIndent$ 属性决定，
字体由 $bulletFontName$ 属性指定。
"项目符号"可以是单个字符（比如说一个圆点！），也可以是某个编号序列中的数字片段，
甚至是定义列表中使用的简短标题。
字体可能提供各种项目符号字符，但我们建议首先尝试 Unicode 项目符号（$&bull;$），
它可以写作 $&amp;bull;$、$&amp;#x2022;$ 或（在 utf8 中）$\\xe2\\x80\\xa2$）：""")

t=Table(*getAttrs(_bulletAttrMap))
t.setStyle([
            ('FONT',(0,0),(-1,1),'Times-Bold',10,12),
            ('FONT',(0,1),(-1,-1),'Courier',8,8),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ])
getStory().append(t)

caption("""表 <seq template="%(Chapter)s-%(Table+)s"/> - &lt;bullet&gt; 属性和同义词""")
disc("""&lt;bullet&gt; 标签在给定段落中只允许使用一次，其使用会覆盖 ^Paragraph^ 创建时指定的隐式项目符号样式和 ^bulletText^。
""")
parabox("""<bullet>&bull;</bullet>this is a bullet point.  Spam
spam spam spam spam spam spam spam spam spam spam spam
spam spam spam spam spam spam spam spam spam spam """,
        styleSheet['Bullet'],
        '项目符号的基本用法')

disc("""编号使用完全相同的技术，只是使用了一个序列标签。
也可以在项目符号中放置多字符字符串；通过较深的缩进和粗体项目符号字体，
您可以创建一个紧凑的定义列表。""")

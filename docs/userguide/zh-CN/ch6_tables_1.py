#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/ch6_tables.py
from tools.docco.rl_doc_utils import *
from reportlab.platypus import Image,ListFlowable, ListItem
import reportlab

heading1("表格与 TableStyle")
disc("""
$Table$ 和 $LongTable$ 类继承自 $Flowable$ 类，用于实现简单的文本网格机制。
$LongTable$ 类在计算列宽时使用贪心算法，适用于需要较高处理速度的长表格。
$Table$ 的单元格可以包含任何可以转换为 <b>Python</b> $string$ 的内容，或 $Flowables$（或 $Flowables$ 的列表）。
""")

disc("""
目前的表格是在高效绘制与规范化和功能性之间的折衷方案。
我们假设读者对 HTML 表格有一定的了解。简而言之，它们具有以下特点：
""")

bullet("""可以包含任何可转换为字符串的内容；可流动对象（如其他表格）；或完整的子故事""")

bullet("""如果您不提供行高，它们可以自动计算行高以适应数据。
（它们也可以自动计算列宽，但通常由设计者手动设置列宽效果更好，而且绘制速度更快。）""")

bullet("""如果需要，它们可以跨页分割（参见 canSplit 属性）。
您可以指定在表格顶部和底部重复显示的行数（例如在第 2、3、4 页等再次显示表头）""")

bullet("""它们具有简单而强大的着色和网格线指定方式，非常适合财务或数据库表格，
在这些场景中您可能事先不知道行数。您可以轻松地说"让最后一行加粗并在其上方画一条线" """)

bullet("""样式与数据分离，因此您可以声明少量表格样式，并将它们用于一系列报表。
样式也可以"继承"，就像段落一样。""")

disc("""然而，与 HTML 表格相比有一个主要限制。
它们定义的是一个简单的矩形网格。没有简单的行或列合并功能；
如果您需要合并单元格，必须将表格嵌套在表格单元格内，
或者使用更复杂的方案，即合并区域的起始单元格包含实际内容。""")

disc("""
$Tables$ 的创建方式是向构造函数传递可选的列宽序列、可选的行高序列，以及按行排列的数据。
表格的绘制可以通过使用 $TableStyle$ 实例来控制。这允许控制线条（如果有的话）的颜色和粗细，
以及文本的字体、对齐方式和内边距。系统提供了基本的自动行高和/或列宽计算机制。
""")

heading2('$Table$ 用户方法')
disc("""以下是客户端程序员感兴趣的主要方法。""")

heading4("""$Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,
repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None, spaceAfter=None, cornerRadii=None)$""")

disc("""$data$ 参数是一个由单元格值序列组成的序列，每个单元格值应该可以使用 $str$ 函数转换为字符串值，
或者是一个 $Flowable$ 实例（如 $Paragraph$），或者是此类实例的列表（或元组）。
如果单元格值是 $Flowable$ 或 $Flowable$ 列表，它们必须具有确定的宽度，或者包含该单元格的列必须具有固定宽度。
第一行的单元格值在 $data[0]$ 中，即值按行排列。第 $i$、$j$<sup>th.</sup> 个单元格的值在 $data[i][j]$ 中。
单元格值中的换行符 $'\\n'$ 被视为换行字符，在<i>绘制</i>时用于将单元格格式化为多行文本。
""")
disc("""其他参数的含义比较直观，$colWidths$ 参数是一个数字序列或可能的 $None$，
表示各列的宽度。$colWidths$ 中的元素数量决定了表格的列数。
值为 $None$ 表示相应列的宽度应自动计算。""")

disc("""$rowHeights$ 参数是一个数字序列或可能的 $None$，表示各行的高度。
$rowHeights$ 中的元素数量决定了表格的行数。
值为 $None$ 表示相应行的高度应自动计算。""")

disc("""$style$ 参数可以是表格的初始样式。""")
disc("""$splitByRow$ 参数仅当表格同时太高和太宽而无法适应当前上下文时才需要。
在这种情况下，您必须决定是先"平铺"向下再向右，还是先向右再向下。
此参数是一个布尔值，指示当当前绘制区域空间不足且调用者希望 $Table$ 分割时，
$Table$ 应先尝试按行分割再尝试按列分割。
目前按列分割 $Table$ 尚未实现，因此将 $splitByRow$ 设置为 $False$ 将导致 $NotImplementedError$。""")

disc("""$repeatRows$ 参数指定当 $Table$ 被要求分割自身时应重复的前导行数或行号元组。
如果是元组，它应指定哪些前导行应被重复；这适用于表格首次出现时比后续分割部分有更多前导行的情况。
$repeatCols$ 参数目前被忽略，因为 $Table$ 不能按列分割。""")
disc("""$rowSplitRange$ 参数可用于将表格的分割控制在其行的子集内；这可以防止在表格开头或结尾附近分割。""")
disc("""$spaceBefore$ 和 $spaceAfter$ 参数可用于在 $platypus$ 故事中渲染表格时在表格前后添加额外空间。""")
disc("""$style$ 参数可以是表格的初始样式。""")
disc("""$cornerRadii$ 参数可以是左上、右上、左下和右下圆角半径的列表。
正的非零半径表示该角应为圆角。此参数将覆盖参数 $style$ 列表中的任何 $ROUNDEDCORNERS$ 命令（即它具有优先权）。""")
heading4('$Table.setStyle(tblStyle)$')
disc("""
此方法将 $TableStyle$ 类（下面将讨论）的特定实例应用到 $Table$ 实例上。
这是让 $tables$ 以美观格式显示的唯一方法。
""")
disc("""
连续使用 $setStyle$ 方法会以累加方式应用样式。
也就是说，后应用的样式在重叠处会覆盖先应用的样式。
""")

heading2('$TableStyle$')
disc("""
此类通过传递一个<i>命令</i>序列来创建，每条命令是一个元组，
由其第一个元素（字符串）标识；命令元组的其余元素表示命令的起始和结束单元格坐标，
以及可能的粗细和颜色等参数。
""")
heading2("$TableStyle$ 用户方法")
heading3("$TableStyle(commandSequence)$")
disc("""创建方法使用参数中的命令序列初始化 $TableStyle$，示例如下：""")
eg("""
    LIST_STYLE = TableStyle(
        [('LINEABOVE', (0,0), (-1,0), 2, colors.green),
        ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
        )
""")
heading3("$TableStyle.add(commandSequence)$")
disc("""此方法允许您向现有的 $TableStyle$ 添加命令，即您可以在多条语句中构建 $TableStyles$。
""")
eg("""
    LIST_STYLE.add('BACKGROUND', (0,0), (-1,0), colors.Color(0,0.7,0.7))
""")
heading3("$TableStyle.getCommands()$")
disc("""此方法返回实例的命令序列。""")
eg("""
    cmds = LIST_STYLE.getCommands()
""")
heading2("$TableStyle$ 命令")
disc("""传递给 $TableStyles$ 的命令分为三大类，分别影响表格背景、绘制线条或设置单元格样式。
""")
disc("""每条命令的第一个元素是其标识符，第二个和第三个参数确定受影响单元格框的坐标，
负坐标从极限值向回计数，类似于 <b>Python</b> 的索引方式。
坐标以 (列, 行) 的形式给出，遵循电子表格的 'A1' 模型，
而不是数学家更习惯的 'RC' 排序。
左上角单元格为 (0, 0)，右下角为 (-1, -1)。根据命令的不同，
从索引 3 开始可能有各种额外参数。
""")
heading3("""$TableStyle$ 单元格格式化命令""")
disc("""所有单元格格式化命令都以标识符开头，后跟起始和结束单元格定义，可能还有其他参数。
单元格格式化命令如下：""")
npeg("""
FONT                    - 接受字体名称，可选的字号和可选的行距。
FONTNAME (或 FACE)      - 接受字体名称。
FONTSIZE (或 SIZE)      - 接受以磅为单位的字号；行距可能会不同步。
LEADING                 - 接受以磅为单位的行距。
TEXTCOLOR               - 接受颜色名称或 (R,G,B) 元组。
ALIGNMENT (或 ALIGN)    - 接受 LEFT、RIGHT、CENTRE (或 CENTER) 或 DECIMAL 之一。
LEFTPADDING             - 接受整数，默认为 6。
RIGHTPADDING            - 接受整数，默认为 6。
BOTTOMPADDING           - 接受整数，默认为 3。
TOPPADDING              - 接受整数，默认为 3。
BACKGROUND              - 接受由对象、字符串名称或数字元组/列表定义的颜色，
                          或接受描述所需渐变填充的列表/元组，该列表/元组应包含三个元素，
                          格式为 [DIRECTION, startColor, endColor]，其中 DIRECTION 为 VERTICAL 或 HORIZONTAL。
ROWBACKGROUNDS          - 接受循环使用的颜色列表。
COLBACKGROUNDS          - 接受循环使用的颜色列表。
VALIGN                  - 接受 TOP、MIDDLE 或默认的 BOTTOM 之一
""")
disc("""此命令设置相关单元格的背景颜色。以下示例展示了 $BACKGROUND$ 和 $TEXTCOLOR$ 命令的使用效果：""")
EmbeddedCode("""
data=  [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t=Table(data)
t.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),
                        ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))
""")
disc("""要查看对齐样式的效果，我们需要一些宽度和网格线，但应该很容易看出样式的来源。""")
EmbeddedCode("""
data=  [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t=Table(data,5*[0.4*inch], 4*[0.4*inch])
t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                        ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                        ('VALIGN',(0,0),(0,-1),'TOP'),
                        ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
""")
heading3("""$TableStyle$ 线条命令""")
disc("""
    线条命令以标识符开头，后跟起始和结束单元格坐标，然后始终跟以所需线条的粗细（以磅为单位）和颜色。
    颜色可以是名称，也可以指定为 (R, G, B) 元组，其中 R、G 和 B 为浮点数，(0, 0, 0) 表示黑色。
    线条命令名称有：GRID、BOX、OUTLINE、INNERGRID、LINEBELOW、LINEABOVE、LINEBEFORE
    和 LINEAFTER。BOX 和 OUTLINE 等效，GRID 等效于同时应用 BOX 和 INNERGRID。
""")
CPage(4.0)
disc("""通过以下示例我们可以看到一些线条命令的效果。
""")
EmbeddedCode("""
data=  [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
                    ('BOX',(0,0),(1,-1),2,colors.red),
                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ])
""")
disc("""线条命令在表格分割时会产生问题；以下示例展示了表格在不同位置的分割效果""")
EmbeddedCode("""
data=  [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
t=Table(data,style=[
                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                ('GRID',(1,1),(-2,-2),1,colors.green),
                ('BOX',(0,0),(1,-1),2,colors.red),
                ('BOX',(0,0),(-1,-1),2,colors.black),
                ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                ])
""")
t=getStory()[-1]
getStory().append(Spacer(0,6))
for s in t.split(4*inch,30):
    getStory().append(s)
    getStory().append(Spacer(0,6))
getStory().append(Spacer(0,6))
for s in t.split(4*inch,36):
    getStory().append(s)
    getStory().append(Spacer(0,6))

disc("""分别为未分割时、在第一行或第二行分割时的效果。""")

CPage(4.0)
heading3("""复杂单元格值""")
disc("""
如上所述，我们可以使用复杂的单元格值，包括 $Paragraphs$、$Images$ 和其他 $Flowables$，或它们的列表。
要查看其实际效果，请看以下代码及其生成的表格。
请注意，$Image$ 具有白色背景，这会遮挡您为单元格选择的任何背景颜色。
要获得更好的效果，您应该使用透明背景。
""")
import os, reportlab.platypus
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
I = '../images/replogo.gif'
EmbeddedCode("""
I = Image('%s')
I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
I.drawWidth = 1.25*inch
P0 = Paragraph('''
               <b>A pa<font color=red>r</font>a<i>graph</i></b>
               <super><font color=yellow>1</font></super>''',
               styleSheet["BodyText"])
P = Paragraph('''
       <para align=center spaceb=3>The <b>ReportLab Left
       <font color=red>Logo</font></b>
       Image</para>''',
       styleSheet["BodyText"])
data=  [['A',   'B', 'C',     P0, 'D'],
        ['00', '01', '02', [I,P], '04'],
        ['10', '11', '12', [P,I], '14'],
        ['20', '21', '22',  '23', '24'],
        ['30', '31', '32',  '33', '34']]

t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
                    ('BOX',(0,0),(1,-1),2,colors.red),
                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                    ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                    ('BOX',(0,0),(-1,-1),2,colors.black),
                    ('GRID',(0,0),(-1,-1),0.5,colors.black),
                    ('VALIGN',(3,0),(3,0),'BOTTOM'),
                    ('BACKGROUND',(3,0),(3,0),colors.limegreen),
                    ('BACKGROUND',(3,1),(3,1),colors.khaki),
                    ('ALIGN',(3,1),(3,1),'CENTER'),
                    ('BACKGROUND',(3,2),(3,2),colors.beige),
                    ('ALIGN',(3,2),(3,2),'LEFT'),
                    ])

t._argW[3]=1.5*inch
"""%I)
heading3("""$TableStyle$ 合并命令""")
disc("""我们的 $Table$ 类支持合并概念，但其指定方式与 HTML 不同。样式规范为
""")
eg("""
SPAN, (sc,sr), (ec,er)
""")
disc("""表示 $sc$ 到 $ec$ 列、$sr$ 到 $er$ 行的单元格应合并为一个超级单元格，
其内容由单元格 $(sc, sr)$ 决定。其他单元格应存在，但应包含空字符串，否则可能会得到意外结果。
""")
EmbeddedCode("""
data=  [['Top\\nLeft', '', '02', '03', '04'],
        ['', '', '12', '13', '14'],
        ['20', '21', '22', 'Bottom\\nRight', ''],
        ['30', '31', '32', '', '']]
t=Table(data,style=[
                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                ('BACKGROUND',(0,0),(1,1),colors.palegreen),
                ('SPAN',(0,0),(1,1)),
                ('BACKGROUND',(-2,-2),(-1,-1), colors.pink),
                ('SPAN',(-2,-2),(-1,-1)),
                ])
""")

disc("""请注意，我们不需要对 $GRID$ 命令过于保守。合并后的单元格不会被网格线穿过。
""")
heading3("""$TableStyle$ 杂项命令""")
disc("""要控制 $Table$ 的分割，可以使用 $NOSPLIT$ 命令。样式规范为
""")
eg("""
NOSPLIT, (sc,sr), (ec,er)
""")
disc("""要求 $sc$ 到 $ec$ 列、$sr$ 到 $er$ 行中的单元格不可被分割。""")

eg("")
eg("")
disc("""要控制 $Table$ 的圆角，可以使用 $ROUNDEDCORNERS$ 命令。样式规范为
""")
eg("""
ROUNDEDCORNERS, [tl, tr, bl, br]
""")
disc("""指定左上、右上、左下和右下的半径。值为 $0$ 表示方角。将整个数组替换为 $None$ 可关闭所有圆角。
<br/>圆角处的边框将弯曲为一个八分之一圆弧。""")

heading3("""特殊的 $TableStyle$ 索引""")
disc("""在任何样式命令中，第一个行索引可以设置为特殊字符串 $'splitlast'$ 或 $'splitfirst'$，
表示该样式仅用于分割表格的最后一行或续表的第一行。这允许在分割点附近实现更美观的效果。""")

heading1("""编程 $Flowables$""")

disc("""以下可流动对象允许您在包装时有条件地求值和执行表达式与语句：""")

heading2("""$DocAssign(self, var, expr, life='forever')$""")

disc("""将名称为 $var$ 的变量赋值为表达式 $expr$ 的值。例如：""")

eg("""
DocAssign('i',3)
""")

heading2("""$DocExec(self, stmt, lifetime='forever')$""")

disc("""执行语句 $stmt$。例如：""")

eg("""
DocExec('i-=1')
""")

heading2("""$DocPara(self, expr, format=None, style=None, klass=None, escape=True)$""")

disc("""创建一个段落，其文本为表达式 $expr$ 的值。
如果指定了 format，它应使用 %(__expr__)s 对表达式 expr 进行字符串插值（如果有的话）。
它也可以使用 %(name)s 插值命名空间中的其他变量。例如：""")

eg("""
DocPara('i',format='The value of i is %(__expr__)d',style=normal)
""")

heading2("""$DocAssert(self, cond, format=None)$""")

disc("""如果 $cond$ 的求值结果为 $False$，则抛出包含 $format$ 字符串的 $AssertionError$。""")

eg("""
DocAssert(val, 'val is False')
""")

heading2("""$DocIf(self, cond, thenBlock, elseBlock=[])$""")

disc("""如果 $cond$ 的求值结果为 $True$，此可流动对象将被替换为 $thenBlock$，否则替换为 $elseBlock$。""")

eg("""
DocIf('i>3',Paragraph('The value of i is larger than 3',normal),\\
        Paragraph('The value of i is not larger than 3',normal))
""")

heading2("""$DocWhile(self, cond, whileBlock)$""")

disc("""当 $cond$ 的求值结果为 $True$ 时，循环运行 $whileBlock$。例如：""")

eg("""
DocAssign('i',5)
DocWhile('i',[DocPara('i',format='The value of i is %(__expr__)d',style=normal),DocExec('i-=1')])
""")

disc("""此示例生成一组如下形式的段落：""")

eg("""
The value of i is 5
The value of i is 4
The value of i is 3
The value of i is 2
The value of i is 1
""")

from tools.docco.rl_doc_utils import *

heading2("交互式表单")
heading3("交互式表单概述")

disc("""PDF 标准允许各种交互式元素，
ReportLab 工具包目前只支持其中一小部分功能，应被视为正在进行中的工作。
目前我们允许通过 <i>复选框</i>、<i>单选按钮</i>、<i>下拉选择</i> 和 <i>列表框</i> 控件进行选择；
文本值可以通过 <i>文本字段</i> 控件输入。所有控件都通过调用 <i>canvas.acroform</i> 属性上的方法来创建。"""
)
heading3("示例")
disc("以下展示了在当前页面上创建交互式元素的基本机制。")
eg("""
        canvas.acroform.checkbox(
                name='CB0',
                tooltip='Field CB0',
                checked=True,
                x=72,y=72+4*36,
                buttonStyle='diamond',
                borderStyle='bevelled',
                borderWidth=2,
                borderColor=red,
                fillColor=green,
                textColor=blue,
                forceBorder=True)
""")
alStyle=TableStyle([
            ('SPAN',(0,0),(-1,0)),
            ('FONT',(0,0),(-1,0),'Helvetica-Bold',10,12),
            ('FONT',(0,1),(-1,1),'Helvetica-BoldOblique',8,9.6),
            ('FONT',(0,2),(0,-1),'Helvetica-Bold',7,8.4),
            ('FONT',(1,2),(1,-1),'Helvetica',7,8.4),
            ('FONT',(2,2),(2,-1),'Helvetica-Oblique',7,8.4),
            ('ALIGN',(0,0),(-1,0),'CENTER'),
            ('ALIGN',(1,1),(1,1),'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ])

disc("""<b>注意</b> <i>acroform</i> 画布属性是按需自动创建的，并且一个文档中只允许一个表单。""")
heading3("复选框用法")
disc("""<i>canvas.acroform.checkbox</i> 方法在当前页面上创建一个 <i>复选框</i> 控件。复选框的值为 <b>YES</b> 或 <b>OFF</b>。
参数如下""")
t = Table([
            ['canvas.acroform.checkbox 参数','',''],
            ['参数','含义','默认值'],
            ["name","参数的名称","None"],
            ["x","页面上的水平位置（绝对坐标）","0"],
            ["y","页面上的垂直位置（绝对坐标）","0"],
            ["size","外框尺寸 size x size","20"],
            ["checked","如果为 True，复选框初始为选中状态","False"],
            ["buttonStyle","复选框样式（见下文）","'check'"],
            ["shape","控件的外形轮廓（见下文）","'square'"],
            ["fillColor","用于填充控件的颜色","None"],
            ["textColor","符号或文本的颜色","None"],
            ["borderWidth","边框宽度","1"],
            ["borderColor","控件的边框颜色","None"],
            ["borderStyle","边框样式名称","'solid'"],
            ["tooltip","鼠标悬停在控件上时显示的文本","None"],
            ["annotationFlags","空格分隔的注释标志字符串","'print'"],
            ["fieldFlags","空格分隔的字段标志（见下文）","'required'"],
            ["forceBorder","为 True 时强制绘制边框","False"],
            ["relative","为 True 时遵循当前画布变换","False"],
            ["dashLen ","当 borderStyle=='dashed' 时使用的虚线长度","3"],
          ],[90, 260, 90],style=alStyle,repeatRows=2)
getStory().append(t)

heading3("单选按钮用法")
disc("""<i>canvas.acroform.radio</i> 方法在当前页面上创建一个 <i>单选按钮</i> 控件。单选按钮的值是单选组
所选中的值，如果没有选中则为 <b>OFF</b>。
参数如下""")
t = Table([
            ['canvas.acroform.radio 参数','',''],
            ['参数','含义','默认值'],
            ["name","单选按钮的组（即参数）名称","None"],
            ["value","单选按钮的组名称","None"],
            ["x","页面上的水平位置（绝对坐标）","0"],
            ["y","页面上的垂直位置（绝对坐标）","0"],
            ["size","外框尺寸 size x size","20"],
            ["selected","如果为 True，此单选按钮是其组中选中的那个","False"],
            ["buttonStyle","复选框样式（见下文）","'check'"],
            ["shape","控件的外形轮廓（见下文）","'square'"],
            ["fillColor","用于填充控件的颜色","None"],
            ["textColor","符号或文本的颜色","None"],
            ["borderWidth","边框宽度","1"],
            ["borderColor","控件的边框颜色","None"],
            ["borderStyle","边框样式名称","'solid'"],
            ["tooltip","鼠标悬停在控件上时显示的文本","None"],
            ["annotationFlags","空格分隔的注释标志字符串","'print'"],
            ["fieldFlags","空格分隔的字段标志（见下文）","'noToggleToOff required radio'"],
            ["forceBorder","为 True 时强制绘制边框","False"],
            ["relative","为 True 时遵循当前画布变换","False"],
            ["dashLen ","当 borderStyle=='dashed' 时使用的虚线长度","3"],
          ],[90, 260, 90],style=alStyle,repeatRows=2)
getStory().append(t)
heading3("列表框用法")
disc("""<i>canvas.acroform.listbox</i> 方法在当前页面上创建一个 <i>列表框</i> 控件。列表框包含一个
选项列表，根据 fieldFlags 的设置，可以选择其中一个或多个。
""")
t = Table([
            ['canvas.acroform.listbox 参数','',''],
            ['参数','含义','默认值'],
            ["name","单选按钮的组（即参数）名称","None"],
            ["options","可用选项的列表或元组","[]"],
            ["value","选中选项的单个字符串或字符串列表","[]"],
            ["x","页面上的水平位置（绝对坐标）","0"],
            ["y","页面上的垂直位置（绝对坐标）","0"],
            ["width","控件宽度","120"],
            ["height","控件高度","36"],
            ["fontName","要使用的 Type 1 字体名称","'Helvetica'"],
            ["fontSize","要使用的字体大小","12"],
            ["fillColor","用于填充控件的颜色","None"],
            ["textColor","符号或文本的颜色","None"],
            ["borderWidth","边框宽度","1"],
            ["borderColor","控件的边框颜色","None"],
            ["borderStyle","边框样式名称","'solid'"],
            ["tooltip","鼠标悬停在控件上时显示的文本","None"],
            ["annotationFlags","空格分隔的注释标志字符串","'print'"],
            ["fieldFlags","空格分隔的字段标志（见下文）","''"],
            ["forceBorder","为 True 时强制绘制边框","False"],
            ["relative","为 True 时遵循当前画布变换","False"],
            ["dashLen ","当 borderStyle=='dashed' 时使用的虚线长度","3"],
          ],[90, 260, 90],style=alStyle,repeatRows=2)
getStory().append(t)
heading3("下拉选择用法")
disc("""<i>canvas.acroform.choice</i> 方法在当前页面上创建一个 <i>下拉选择</i> 控件。下拉选择包含一个
选项列表，根据 fieldFlags 的设置，可以选择其中一个或多个。如果在 <i>fieldFlags</i> 中添加 <i>edit</i>，
则结果可以被编辑。
""")
t = Table([
            ['canvas.acroform.choice 参数','',''],
            ['参数','含义','默认值'],
            ["name","单选按钮的组（即参数）名称","None"],
            ["options","可用选项的列表或元组","[]"],
            ["value","选中选项的单个字符串或字符串列表","[]"],
            ["x","页面上的水平位置（绝对坐标）","0"],
            ["y","页面上的垂直位置（绝对坐标）","0"],
            ["width","控件宽度","120"],
            ["height","控件高度","36"],
            ["fontName","要使用的 Type 1 字体名称","'Helvetica'"],
            ["fontSize","要使用的字体大小","12"],
            ["fillColor","用于填充控件的颜色","None"],
            ["textColor","符号或文本的颜色","None"],
            ["borderWidth","边框宽度","1"],
            ["borderColor","控件的边框颜色","None"],
            ["borderStyle","边框样式名称","'solid'"],
            ["tooltip","鼠标悬停在控件上时显示的文本","None"],
            ["annotationFlags","空格分隔的注释标志字符串","'print'"],
            ["fieldFlags","空格分隔的字段标志（见下文）","'combo'"],
            ["forceBorder","为 True 时强制绘制边框","False"],
            ["relative","为 True 时遵循当前画布变换","False"],
            ["dashLen ","当 borderStyle=='dashed' 时使用的虚线长度","3"],
            ["maxlen ","控件值的最大长度，或 None","None"],
          ],[90, 260, 90],style=alStyle,repeatRows=2)
getStory().append(t)

heading3("文本字段用法")
disc("""<i>canvas.acroform.textfield</i> 方法在当前页面上创建一个 <i>文本字段</i> 输入控件。
文本字段可以被编辑以更改控件的值。
""")
t = Table([
            ['canvas.acroform.textfield 参数','',''],
            ['参数','含义','默认值'],
            ["name","单选按钮的组（即参数）名称","None"],
            ["value","文本字段的值","''"],
            ["maxlen ","控件值的最大长度，或 None","100"],
            ["x","页面上的水平位置（绝对坐标）","0"],
            ["y","页面上的垂直位置（绝对坐标）","0"],
            ["width","控件宽度","120"],
            ["height","控件高度","36"],
            ["fontName","要使用的 Type 1 字体名称","'Helvetica'"],
            ["fontSize","要使用的字体大小","12"],
            ["fillColor","用于填充控件的颜色","None"],
            ["textColor","符号或文本的颜色","None"],
            ["borderWidth","边框宽度","1"],
            ["borderColor","控件的边框颜色","None"],
            ["borderStyle","边框样式名称","'solid'"],
            ["tooltip","鼠标悬停在控件上时显示的文本","None"],
            ["annotationFlags","空格分隔的注释标志字符串","'print'"],
            ["fieldFlags","空格分隔的字段标志（见下文）","''"],
            ["forceBorder","为 True 时强制绘制边框","False"],
            ["relative","为 True 时遵循当前画布变换","False"],
            ["dashLen ","当 borderStyle=='dashed' 时使用的虚线长度","3"],
          ],[90, 260, 90],style=alStyle,repeatRows=2)
getStory().append(t)

heading3("按钮样式")
disc("""按钮样式参数表示按钮被选中时应显示什么样的符号样式。有几种选择""")
eg("""  check
  cross
  circle
  star
  diamond
""")
disc("""请注意，文档渲染器可能会使其中一些符号与其预期应用不匹配。
Acrobat Reader 更倾向于使用自己的渲染，覆盖规范规定应显示的内容
（特别是当使用表单高亮功能时）""")

heading3("控件形状")
disc("""shape 参数描述复选框或单选按钮控件的外形轮廓，可以使用""")
eg("""  circle
  square
""")

disc("""渲染器可能会自行决定控件的外观；因此 Acrobat Reader 更倾向于为单选按钮使用圆形轮廓。""")

heading3("边框样式")
disc("""borderStyle 参数改变页面上控件的三维外观，可选值为""")
eg("""  solid
  dashed
  inset
  bevelled
  underlined
    """)
heading3("fieldFlags 参数")
disc("""fieldFlags 参数可以是整数或包含空格分隔标记的字符串，其值如下表所示。
更多信息请参阅 PDF 规范。""")
t = Table([
            ['字段标志标记和值','',''],
            ['标记','含义','值'],
            ["readOnly","控件为只读","1<<0"],
            ["required","控件为必填","1<<1"],
            ["noExport","不导出控件值","1<<2"],
            ["noToggleToOff","单选按钮只有一个必须为开","1<<14"],
            ["radio","由 radio 方法添加","1<<15"],
            ["pushButton","如果按钮是按压式按钮","1<<16"],
            ["radiosInUnison","具有相同值的单选按钮同时切换","1<<25"],
            ["multiline","用于多行文本控件","1<<12"],
            ["password","密码文本字段","1<<13"],
            ["fileSelect","文件选择控件","1<<20"],         #1.4
            ["doNotSpellCheck","不进行拼写检查","1<<22"],   #1.4
            ["doNotScroll","文本字段不滚动","1<<23"],        #1.4
            ["comb","根据 maxlen 值创建梳状文本","1<<24"],                #1.5
            ["richText","如果使用富文本","1<<25"],            #1.5
            ["combo","用于选择字段","1<<17"],
            ["edit","如果选择可编辑","1<<18"],
            ["sort","如果值应排序","1<<19"],
            ["multiSelect","如果选择允许多选","1<<21"],        #1.4
            ["commitOnSelChange","ReportLab 不使用","1<<26"],  #1.5
          ],[90, 260, 90],style=alStyle,repeatRows=2)
getStory().append(t)
heading3("annotationFlags 参数")
disc("""PDF 控件是注释，具有注释属性，如下表所示""")
t = Table([
            ['注释标志标记和值','',''],
            ['标记','含义','值'],
            ["invisible","控件不显示","1<<0"],
            ["hidden","控件被隐藏","1<<1"],
            ["print","控件将打印","1<<2"],
            ["nozoom","注释不随渲染页面缩放","1<<3"],
            ["norotate","控件不随页面旋转","1<<4"],
            ["noview","不渲染控件","1<<5"],
            ["readonly","控件不可交互","1<<6"],
            ["locked","控件不可更改","1<<7"],           #1.4
            ["togglenoview","控件在某些事件后可查看","1<<8"],       #1.9
            ["lockedcontents","控件内容固定","1<<9"],   #1.7
          ],[90, 260, 90],style=alStyle)
getStory().append(t)

#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
#history https://hg.reportlab.com/hg-public/reportlab/log/tip/docs/userguide/app_demos.py
from tools.docco.rl_doc_utils import *

Appendix1("ReportLab 演示程序")
disc("""在 $reportlab/demos$ 的子目录中有许多可运行的示例，
展示了 reportlab 几乎所有方面的用法。""")

heading2("""Odyssey""")
disc("""
odyssey.py、dodyssey.py 和 fodyssey.py 这三个脚本都使用 odyssey.txt 文件
来生成 PDF 文档。附带的 odyssey.txt 较短；更长且更具挑战性的版本
可在 ftp://ftp.reportlab.com/odyssey.full.zip 找到。
""")
eg("""
Windows
cd reportlab\\demos\\odyssey
python odyssey.py
start odyssey.pdf

Linux
cd reportlab/demos/odyssey
python odyssey.py
acrord odyssey.pdf
""")
disc("""odyssey.py 脚本展示了简单的格式化。它运行速度相当快，
但它所做的只是收集文本并将其强制放到画布页面上。它根本不进行段落操作，
所以您会看到 XML &lt; &amp; &gt; 标签。
""")
disc("""fodyssey.py 和 dodyssey.py 脚本处理段落格式化，因此您可以看到
颜色变化等效果。这两个脚本都使用文档模板类，dodyssey.py 脚本还展示了
双栏布局的能力，并使用了多个页面模板。
""")

heading2("""标准字体和颜色""")
disc("""在 $reportlab/demos/stdfonts$ 目录中，stdfonts.py 脚本可以用来
展示 ReportLab 的标准字体。使用以下命令运行脚本：""")
eg("""
cd reportlab\\demos\\stdfonts
python stdfonts.py
""")
disc("""
这将生成两个 PDF 文档，StandardFonts_MacRoman.pdf 和
StandardFonts_WinAnsi.pdf，分别展示了两种最常见的内置字体编码。
""")
disc("""$reportlab/demos/colors$ 中的 colortest.py 脚本演示了 reportlab
设置和使用颜色的不同方式。""")
disc("""尝试运行该脚本并查看输出文档 colortest.pdf。它展示了不同的颜色空间
以及 $reportlab.lib.colors$ 模块中命名的大量颜色。
""")
heading2("""Py2pdf""")
disc("""Dinu Gherman 贡献了这个实用的脚本，它使用 reportlab 从 Python 脚本
生成美观的带语法高亮的 PDF 文档，包括类、方法和函数的书签。
要获取主脚本的美观版本，请尝试：""")
eg("""
cd reportlab/demos/py2pdf
python py2pdf.py py2pdf.py
acrord py2pdf.pdf
""")
disc("""也就是说，我们使用 py2pdf 生成了 py2pdf.py 的美观版本，
输出文档具有相同的根名和 .pdf 扩展名。
""")
disc("""
py2pdf.py 脚本有许多选项，超出了本简单介绍的范围；
请参阅脚本开头的注释。
""")
heading2("Gadflypaper")
disc("""
$reportlab/demos/gadflypaper$ 中的 Python 脚本 gfe.py 使用内联式的
文档准备方式。该脚本几乎完全由 Aaron Watters 编写，生成了一个描述 Aaron 的
$gadfly$ Python 内存数据库的文档。要生成该文档，请使用：
""")
eg("""
cd reportlab\\gadflypaper
python gfe.py
start gfe.pdf
""")
disc("""
PDF 文档中的所有内容都是由脚本生成的，这就是为什么这是一种内联式的
文档生产方式。因此，要生成一个标题后跟一些文本，脚本使用 $header$ 和 $p$
函数，它们接受一些文本并追加到全局 story 列表中。
""")
eg('''
header("Conclusion")

p("""The revamped query engine design in Gadfly 2 supports
..........
and integration.""")
''')
heading2("""Pythonpoint""")
disc("""Andy Robinson 不断改进 pythonpoint.py 脚本（位于
$reportlab\\demos\\pythonpoint$），使其成为一个非常实用的脚本。
它接受一个包含 XML 标记的输入文件，并使用 xmllib 风格的解析器
将标签映射为 PDF 幻灯片。在它自己的目录中运行时，
pythonpoint.py 默认使用 pythonpoint.xml 文件作为输入，
并生成 pythonpoint.pdf，这就是 Pythonpoint 的文档！
您还可以用一篇较早的论文来查看它的效果：""")
eg("""
cd reportlab\\demos\\pythonpoint
python pythonpoint.py monterey.xml
start monterey.pdf
""")
disc("""
Pythonpoint 不仅是自我文档化的，而且也展示了 reportlab 和 PDF 的功能。
它使用了 reportlab 的许多功能（文档模板、表格等）。
PDF 的高级功能如淡入效果和书签也得到了很好的展示。
使用 XML 文档的方式可以与 gadflypaper 演示的 <i>内联</i> 风格形成对比；
内容与格式完全分离。
""")

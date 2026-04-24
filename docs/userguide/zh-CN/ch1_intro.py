#Copyright ReportLab Europe Ltd. 2000-2017
#see license.txt for license details
__version__ = '$Id$'
from tools.docco.rl_doc_utils import *
from reportlab.platypus.tableofcontents import TableOfContents
import reportlab
from reportlab.lib.utils import TimeStamp

title("ReportLab PDF 库")
title("用户指南")
centred('ReportLab Version ' + reportlab.Version)
centred(TimeStamp().datetime.strftime('Document generated on %Y/%m/%d %H:%M:%S %Z'))

nextTemplate("TOC")

headingTOC()

toc = TableOfContents()
PS = ParagraphStyle
toc.levelStyles = [
    PS(fontName='Times-Bold', fontSize=14, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
    PS(fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12),
    PS(fontSize=10, name='TOCHeading3', leftIndent=60, firstLineIndent=-20, spaceBefore=0, leading=12),
    PS(fontSize=10, name='TOCHeading4', leftIndent=100, firstLineIndent=-20, spaceBefore=0, leading=12),
]
getStory().append(toc)

nextTemplate("Normal")

########################################################################
#
#               Chapter 1
#
########################################################################


heading1("简介")


heading2("关于本文档")
disc("""本文档是 ReportLab PDF 库的入门介绍。我们假定读者具有一定的编程经验，
并建议熟悉 Python 编程语言。如果您刚刚接触 Python，下一节将告诉您去哪里寻找入门资源。
""")

disc("""
本手册并未涵盖 100% 的功能，但会解释所有主要概念，帮助您快速入门，
并为您指出其他学习资源。
通读本手册后，您应该已经准备好开始编写程序来生成复杂的报表了。
""")

disc("""在本章中，我们将介绍以下基础知识：""")
bullet("ReportLab 是做什么的，我为什么要使用它？")
bullet("什么是 Python？")
bullet("如何安装和运行？")

todo("""
我们需要您的帮助来确保本手册的完整性和实用性。
请将任何反馈发送到我们的用户邮件列表，
入口在 <a href="http://www.reportlab.com/">www.reportlab.com</a>。
""")

heading2("什么是 ReportLab PDF 库？")
disc("""这是一个软件库，让您可以使用 Python 编程语言直接创建 Adobe 便携文档格式（PDF）文档。
它还能以多种位图和矢量格式以及 PDF 格式创建图表和数据图形。""")

disc("""PDF 是电子文档的全球标准。它支持高质量打印，同时借助免费提供的 Acrobat Reader，
在不同平台间完全可移植。任何以前生成硬拷贝报告或驱动打印机的应用程序，
都可以从生成 PDF 文档中获益；PDF 文档可以被归档、
通过电子邮件发送、放置在网站上，或以传统方式打印。
然而，PDF 文件格式是一种复杂的索引二进制格式，无法直接手动输入。
PDF 格式规范超过 600 页，PDF 文件必须提供精确的字节偏移量——
在有效的 PDF 文档中任何位置多放一个字符都可能使其无效。
这使得 PDF 的生成比 HTML 更加困难。""")

disc("""世界上大多数 PDF 文档都是由 Adobe 的 Acrobat 工具或 JAWS PDF Creator 等竞争对手的产品生成的，
它们充当"打印驱动程序"。任何想要自动化生成 PDF 的人通常会使用 Quark、Word 或 Framemaker
等产品，通过宏或插件在循环中运行，并连接到 Acrobat。
涉及多种语言和产品的处理管线可能速度较慢且不够灵活。
""")


disc("""ReportLab 库根据您的图形命令直接创建 PDF。中间没有额外的步骤。
您的应用程序可以极快地生成报告——有时比传统报表生成工具快几个数量级。
这种方法与其他几个库类似——C 语言的 PDFlib、Java 的 iText、.NET 的 iTextSharp 等。
然而，ReportLab 库的不同之处在于它可以在更高的层次上工作，
拥有一个功能齐全的文档排版引擎，可以处理完整的表格和图表。""")


disc("""此外，由于您使用的是一种功能强大的通用编程语言来编写程序，
在数据来源、数据转换方式和输出类型方面没有任何限制。
而且您可以在整个报表系列中复用代码。""")

disc("""ReportLab 库至少在以下场景中有用：""")
bullet("Web 上的动态 PDF 生成")
bullet("大批量的企业报表和数据库出版")
bullet("""作为其他应用程序的可嵌入打印引擎，包括一种"报表语言"，
让用户可以自定义报表。<i>这对于跨平台应用尤其重要，
因为它们无法依赖每个操作系统上一致的打印或预览 API。</i>""")
bullet("""一个用于包含图表、表格和文本的复杂文档的"构建系统"，
如管理报告、统计报告和科学论文""")
bullet("""一步完成从 XML 到 PDF 的转换""")


heading2("ReportLab 的商业软件")
disc("""
ReportLab 库构成了我们 PDF 生成商业解决方案——Report Markup Language (RML)——的基础。
该产品可在我们的网站上获取评估版并附带完整文档。
我们相信 RML 是开发丰富 PDF 工作流最快、最简单的方式。
您使用类似于 HTML 级别的标记语言，用您喜欢的模板系统来填充 RML 文档；
然后调用我们的 rml2pdf API 函数来生成 PDF。
这也是 ReportLab 团队用来构建 reportlab.com 上所有解决方案的方式。
主要区别如下：
""")
bullet("""拥有两本手册、一份正式规范（DTD）和大量自文档化测试的完整文档。（相比之下，我们努力确保开源文档的准确性，但并不总是能跟上代码的更新）""")
bullet("""使用高级标记语言而不是构建 Python 对象图""")
bullet("""不需要 Python 专业知识——您的同事可能会在您离职后感谢您！""")
bullet("""支持矢量图形和其他 PDF 文档的嵌入""")
bullet("""许多有用的功能只需一个标签即可实现，而在开源包中则需要大量编码""")
bullet("""包含商业支持""")


disc("""
我们请求开源开发者考虑在适当的情况下尝试 RML。
您可以在我们的网站上注册并在购买前试用。
费用合理，并与项目规模挂钩，收入帮助我们投入更多时间开发本软件。""")


heading2("什么是 Python？")
disc("""
Python 是一种<i>解释型、交互式、面向对象</i>的编程语言。它常被拿来与 Tcl、Perl、Scheme 或 Java 进行比较。
""")

disc("""
Python 结合了非凡的强大功能和非常清晰的语法。它具有模块、类、异常、非常高级的动态数据类型和动态类型系统。
它提供了许多系统调用和库的接口，以及各种窗口系统（X11、Motif、Tk、Mac、MFC）的接口。
新的内置模块可以很容易地用 C 或 C++ 编写。
Python 还可以用作需要可编程接口的应用程序的扩展语言。
""")


disc("""
Python 与 Java 同龄，多年来一直在稳步增长其流行度；自我们的库首次发布以来，
它已经进入了主流。许多 ReportLab 库用户已经是 Python 的忠实拥趸，
但如果您还不是，我们认为由于其表达能力和从任何地方获取数据的能力，
Python 是文档生成应用的绝佳选择。
""")

disc("""
Python 受版权保护，但<b>可自由使用和分发，包括商业用途</b>。
""")

heading2("致谢")
disc("""许多人参与了 ReportLab 的开发。我们特别要感谢以下人员
（按字母顺序排列）：
<nobr>Albertas Agejevas,
Alex Buck,
Andre Reitz,
Andrew Cutler,
Andrew Mercer,
Ben Echols,
Benjamin Dumke,
Benn B,
Chad Miller,
Chris Buergi,
Chris Lee,
Christian Jacobs,
Dinu Gherman,
Edward Greve,
Eric Johnson,
Felix Labrecque,
Fubu @ bitbucket,
Gary Poster,
Germán M. Bravo,
Guillaume Francois,
Hans Brand,
Henning Vonbargen,
Hosam Aly,
Ian Stevens,
James Martin-Collar,
Jeff Bauer,
Jerome Alet,
Jerry Casiano,
Jorge Godoy,
Keven D Smith,
Kyle MacFarlane,
Magnus Lie Hetland,
Marcel Tromp,
Marius Gedminas,
Mark de Wit,
Matthew Duggan,
Matthias Kirst,
Matthias Klose,
Max M,
Michael Egorov,
Michael Spector,
Mike Folwell,
Mirko Dziadzka,
Moshe Wagner,
Nate Silva,
Paul McNett,
Peter Johnson,
PJACock,
Publio da Costa Melo,
Randolph Bentson,
Robert Alsina,
Robert Hölzl,
Robert Kern,
Ron Peleg,
Ruby Yocum,
Simon King,
Stephan Richter,
Steve Halasz,
Stoneleaf @ bitbucket,
T Blatter,
Tim Roberts,
Tomasz Swiderski,
Ty Sarna,
Volker Haas,
Yoann Roman,</nobr>
以及更多贡献者。""")


disc("""特别感谢 Just van Rossum 在字体技术方面提供的宝贵帮助。""")

disc("""Moshe Wagner 和 Hosam Aly 为 RTL 补丁做出了重要贡献，值得特别感谢，该补丁尚未合并到主干。""")

disc("""Marius Gedminas 在 TrueType 字体方面的工作功不可没，我们很高兴将其纳入工具包。
最后感谢 Michal Kosmulski 提供的 DarkGarden 字体和 Bitstream Inc. 提供的 Vera 字体。""")

heading2("安装与设置")

disc("""为避免重复，安装说明保存在我们发行版中的 README 文件中，
可在 ^https://hg.reportlab.com/hg-public/reportlab/^ 在线查看。""")

disc("""本版本（%s）的 ReportLab 需要 Python 版本 %s.%s+ 或更高版本。
如果您需要使用 Python 2，请使用适合您的最新 ReportLab 2.7 版本。
""" % ((reportlab.Version,)+reportlab.__min_python_version__))



heading2("参与贡献")
disc("""ReportLab 是一个开源项目。虽然我们是一家商业公司，
但我们免费提供核心 PDF 生成源代码，即使是商业用途也不收费，
我们也不直接从这些模块获取收入。与任何其他开源项目一样，
我们同样欢迎社区的帮助。您可以通过以下方式提供帮助：""")

bullet("""对核心 API 的总体反馈。它是否适合您的需求？
有没有什么不顺手的地方？有没有什么感觉笨拙和别扭的地方？""")

bullet("""用于报表的新对象或库的实用工具。
我们为报表对象制定了开放标准，所以如果您写了一个漂亮的图表或表格类，
何不贡献出来呢？""")

bullet("""代码片段和案例研究：如果您生成了一些漂亮的输出，
请在 ^http://www.reportlab.com^ 在线注册并提交您的输出片段
（带或不带脚本都可以）。如果 ReportLab 在工作中为您解决了问题，
请写一个简短的"案例研究"并提交。如果您的网站使用我们的工具生成报表，
请让我们链接到您的网站。我们将很乐意在我们的网站上展示您的作品
（并标注您的姓名和公司名称）！""")

bullet("""参与核心代码开发：我们有一长串需要改进或实现的内容。
如果您发现缺少某些功能或只是想帮忙，请告诉我们！""")

disc("""对于任何想要了解更多信息或参与贡献的人来说，第一步是加入邮件列表。
要订阅，请访问 $http://two.pairlist.net/mailman/listinfo/reportlab-users$。
在那里您还可以浏览邮件列表的归档和贡献。邮件列表是报告错误和获取支持的地方。""")

disc("""代码现在托管在我们的网站（$http://hg.reportlab.com/hg-public/reportlab/$）
上的 Mercurial 仓库中，同时还有问题跟踪器和 Wiki。
每个人都应该可以自由贡献，但如果您正在积极改进某些功能
或想让某个问题引起注意，请通过邮件列表告知我们。""")



heading2("站点配置")
disc("""有许多选项很可能需要为整个站点进行全局配置。
Python 脚本模块 $reportlab/rl_config.py$ 汇总了各种设置文件。
您可能需要检查文件 $reportlab/rl_settings.py$，
其中包含当前所用变量的默认值。$rl_settings$ 有几个覆盖来源：
模块 $reportlab.local_rl_settings$、$reportlab_settings$
（Python 路径上任意位置的脚本文件），以及文件 $~/.reportlab_settings$
（注意没有 .py 后缀）。临时更改可以通过环境变量进行，
环境变量是 $rl_settings.py$ 中的变量加上 $RL_$ 前缀，
例如 $RL_verbose=1$。
""")
heading3("常用的 rl_config 变量")
bullet("""verbose：设置为整数值以控制诊断输出。""")
bullet("""shapeChecking：将其设置为零可关闭图形模块中的大量错误检查""")
bullet("""defaultEncoding：将其设置为 WinAnsiEncoding 或 MacRomanEncoding。""")
bullet("""defaultPageSize：将其设置为 reportlab/lib/pagesizes.py 中定义的值之一；
默认设置为 pagesizes.A4；其他值包括 pagesizes.letter 等。""")
bullet("""defaultImageCaching：设置为零可阻止在硬盘上创建 .a85 文件。
默认行为是创建这些预处理过的 PDF 兼容图像文件以加快加载速度""")
bullet("""T1SearchPath：这是一个字符串列表，表示可以查询 Type 1 字体信息的目录""")
bullet("""TTFSearchPath：这是一个字符串列表，表示可以查询 TrueType 字体信息的目录""")
bullet("""CMapSearchPath：这是一个字符串列表，表示可以查询字体编码映射信息的目录。""")
bullet("""showBoundary：设置为非零值可显示边界线。""")
bullet("""pageCompression：设置为非零值可尝试生成压缩的 PDF。""")
bullet("""allowtableBoundsErrors：设置为 0 可在 Platypus 表格元素过大时强制报错""")
bullet("""emptyTableAction：控制空表格的行为，可以是 'error'（默认值）、'indicate' 或 'ignore'。""")
bullet("""trustedHosts：如果不是 $None$，则为受信任主机的 glob 模式列表；这些模式可用于段落文本中的 &lt;img&gt; 标签等位置。""")
bullet("""trustedSchemes：与 $trustedHosts$ 配合使用的允许 $URL$ 方案列表""")
disc("""完整的变量列表请参见文件 $reportlab/rl_settings.py$。""")
heading3("其他修改方式")
disc("""对 reportlab 工具包环境进行更复杂的修改可以使用以下模块之一：
$reportlab.local_rl_mods$（reportlab 文件夹中的 .py 脚本）、
$reportlab_mods$（Python 路径上的 .py 文件）或 $~/.reportlab_mods$（注意没有 .py 后缀）。""")

heading2("了解更多关于 Python 的知识")

disc("""
如果您是 Python 的完全初学者，您应该查看越来越多的 Python 编程资源中的一个或多个。
以下是在网络上免费提供的资源：
""")


bullet("""<b>Python 文档。</b>
Python.org 网站上的文档列表。
$http://www.python.org/doc/$
""")


bullet("""<b>Python 教程。</b>
官方 Python 教程，最初由 Guido van Rossum 亲自撰写。
$http://docs.python.org/tutorial/$
""")


bullet("""<b>学习编程。</b>
Alan Gauld 编写的编程教程。着重讲解 Python，但也使用其他语言。
$http://www.freenetpages.co.uk/hp/alan.gauld/$
""")


bullet("""<b>即时 Python</b>。
Magnus Lie Hetland 编写的 6 页极简速成课程。
$http://www.hetland.org/python/instant-python.php$
""")


bullet("""<b>Dive Into Python</b>。
面向有经验程序员的免费 Python 教程。
$http://www.diveintopython.net/$
""")


from reportlab.lib.codecharts import SingleByteEncodingChart
from tools.docco.stylesheet import getStyleSheet
styles = getStyleSheet()
indent0_style = styles['Indent0']
indent1_style = styles['Indent1']

heading2("3.x 版本系列的目标")
disc("""ReportLab 3.0 的发布旨在帮助迁移到 Python 3.x。
Python 3.x 将成为未来 Ubuntu 版本的标准，并日益普及，
越来越多的主要 Python 包已经可以在 Python 3 上运行。""")


bullet("""Python 3.x 兼容性。同一行代码应该能在 3.6 及更高版本上运行""")
bullet(""" __init__.py 限制为 >=3.6""")
bullet("""__init__.py 允许导入可选的 reportlab.local_rl_mods 以支持猴子补丁等操作。""")
bullet("""rl_config 现在导入 rl_settings，以及可选的 local_rl_settings、reportlab_settings.py 和 ~/.reportlab_settings""")
bullet("""ReportLab C 扩展现在位于 reportlab 内部；不再需要 _rl_accel。所有 _rl_accel 导入现在都通过 reportlab.lib.rl_accel 进行""")
bullet("""xmllib 已移除，连同导致问题的 paraparser 相关代码，取而代之的是 HTMLParser。""")
bullet("""一些过时的 C 扩展（sgmlop 和 pyHnj）已被移除""")
bullet("""改进了对多线程系统中 _rl_accel C 扩展模块的支持。""")
bullet("""移除了 reportlab/lib/ 中的 para.py 和 pycanvas.py。这些更适合放在第三方包中，
第三方包可以利用上面提到的猴子补丁功能。""")
bullet("""增加了在不转换为 RGB 的情况下输出灰度和 1 位 PIL 图像的功能。（由 Matthew Duggan 贡献）""")
bullet("""高亮注释（由 Ben Echols 贡献）""")
bullet("""完全兼容 pip、easy_install、wheels 等工具""")




disc("""详细的发布说明可在
$http://www.reportlab.com/software/documentation/relnotes/30/$ 查看""")



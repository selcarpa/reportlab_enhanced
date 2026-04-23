# reportlab-enhanced

[English](README.md)

[ReportLab](https://www.reportlab.com/) 的增强版 fork —— 用于生成 PDF 文档、图表和矢量图形的开源 Python 库。

## 特性

- 生成包含文本、图片、表格和图表的富 PDF 文档
- 高级排版引擎 (Platypus)，支持 flowable、分栏和页面模板
- 底层 Canvas API，支持直接 PDF 绘图操作
- 图表和图形，支持 SVG/PS/位图渲染
- TrueType 和 Type1 字体处理
- **增强功能**：TrueType 字体缺失字形自动回退
- 纯 Python 实现（v4.0 起无需 C 扩展）
- Python >= 3.9

## 相对于上游的增强

此 fork 基于 ReportLab 4.x 构建，增加了以下功能：

- **TTFont 字体回退**：TrueType 字体遇到缺失字形时自动回退到备选字体，通过环境变量 `REPORTLAB_FONT_FALLBACK=1` 控制
- 针对字体处理和 CJK 支持的持续改进

完整变更记录请参阅 [CHANGES.md](CHANGES.md)。

## 安装

```bash
pip install reportlab-enhanced
```

开发安装：

```bash
git clone https://github.com/selcarpa/reportlab_enhanced.git
cd reportlab-enhanced
pip install -e .
```

### 可选依赖

```bash
pip install reportlab-enhanced[accel]      # rl_accel 加速
pip install reportlab-enhanced[renderpm]   # rl_renderPM 位图渲染
pip install reportlab-enhanced[pycairo]    # Cairo 渲染
pip install reportlab-enhanced[bidi]       # 双向文本支持
pip install reportlab-enhanced[shaping]    # HarfBuzz 文字整形
```

## 快速开始

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=A4)
c.drawString(100, 750, "你好，reportlab-enhanced！")
c.save()
```

使用高级 Platypus API：

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("doc.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = [Paragraph("你好，reportlab-enhanced！", styles["Title"])]
doc.build(story)
```

## 文档

原始 ReportLab 文档可在 [docs.reportlab.com](https://docs.reportlab.com/) 查看。

构建内置 PDF 手册：

```bash
cd docs && python genAll.py
```

将在 `docs/` 目录下生成三份 PDF 参考手册。

## 开发

本项目大量使用 **vibe coding**，以 [Claude Code](https://claude.ai/code)（Anthropic Claude）作为开发伙伴，参与代码生成、重构和文档编写。

### 运行测试

```bash
python setup.py tests-preinstall
# 或
cd tests && python runAll.py
```

### 贡献

欢迎贡献！请在 [GitHub](https://github.com/selcarpa/reportlab_enhanced) 上提交 issue 或 pull request。

## 致谢

本项目 fork 自 ReportLab Inc. 的 [ReportLab](https://www.reportlab.com/)，最初由 Andy Robinson、Robin Becker 及 ReportLab 团队创建。上游项目自 2000 年起持续开发，为本增强版提供了基础。

## 许可证

BSD 许可证。详见 [LICENSE](LICENSE)。

- Copyright (c) 2025-2026, selcarpa
- Copyright (c) 2000-2024, ReportLab Inc.

# tests_resource

本目录存放单元测试所需的外部字体文件。字体文件较大，不纳入版本控制。

## 初始化

从以下地址下载字体资源包：

```
https://reportlab-enhanced.tain.one/test-resource.zip
```

解压到本目录：

```bash
cd tests_resource
unzip test-resource.zip
```

缺少字体时，相关测试会自动跳过（SKIP），不影响其他测试。

## 使用的字体

| 字体 | 文件名 | 用途 |
|------|--------|------|
| Source Han Sans K Light | `SourceHanSansK-Light.otf` | OTF(CFF) 渲染测试 |
| NotoSansKR Bold | `NotoSansKR-Bold.ttf` | OTF(TTF) 渲染测试 |
| NotoSansSC | `NotoSansSC-Regular.otf` | 简体中文回退测试 |
| NotoSansKR | `NotoSansKR-Regular.otf` | 韩文回退测试 |
| TheanoDidot | `TheanoDidot.otf` | 希腊文回退测试 |
| GentiumBookPlusBI | `GentiumBookPlus-BoldItalic.otf` | 拉丁扩展回退测试 |
| NotoEmoji | `NotoEmoji-VariableFont_wght.otf` | Emoji 回退测试 |

## 测试输出

PDF 渲染测试的输出文件生成在 `tests/pdf-out/` 目录下，已加入 `.gitignore`。
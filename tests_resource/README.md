# tests_resource

本目录存放单元测试所需的外部 TTF 字体文件。字体文件较大，不纳入版本控制。

## 初始化

请手动下载以下 TTF 字体文件到本目录：

```bash
cd tests_resource
```

### 下载地址

- **NotoSansSC-Regular.ttf**（简体中文）
  Google Fonts: https://fonts.google.com/noto/fonts?query=noto+sans+sc
  或 GitHub: https://github.com/notofonts/noto-cjk/releases

- **NotoSansKR-Bold.ttf**（韩文）
  Google Fonts: https://fonts.google.com/noto/fonts?query=noto+sans+kr

- **Gentium-BoldItalic.ttf**（拉丁扩展）
  https://software.sil.org/gentium/

- **TheanoDidot-Regular.ttf**（希腊字母）
  https://github.com/akrylov/theanodidot

- **NotoEmoji-Regular.ttf**（Emoji，黑白矢量轮廓版）
  https://github.com/googlefonts/noto-emoji
  注意：需要 **monochrome** 版本（矢量轮廓），不是 NotoColorEmoji（彩色位图，PDF 不可用）

> 注意：上述 URL 可能随上游变更，如下载失败请从对应项目页面手动获取。

## 所需文件清单

| 文件名 | 用途 |
|--------|------|
| `NotoSansSC-Regular.ttf` | 简体中文 fallback 测试 |
| `NotoSansKR-Bold.ttf` | 韩文 fallback 测试 |
| `Gentium-BoldItalic.ttf` | 拉丁扩展字符 fallback 测试 |
| `TheanoDidot-Regular.ttf` | 希腊字母 fallback 测试 |
| `NotoEmoji-Regular.ttf` | Emoji fallback 测试（黑白矢量版，非 Color 版） |

所有字体文件必须为 **TTF 格式**。

若本目录中缺少所需字体文件，相关测试用例将被跳过（标记为 SKIP）。

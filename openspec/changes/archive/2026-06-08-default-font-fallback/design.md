## Context

TTFont 字体回退功能已在 2026-04 通过 `2026-04-23-ttfont-fallback` change 实现，当前通过 `REPORTLAB_FONT_FALLBACK` 环境变量控制开关，默认关闭。经过多轮测试验证，功能已稳定可靠。

当前 `substitutionFonts` property 的 getter 每次调用时检查 `os.environ.get('REPORTLAB_FONT_FALLBACK', '0') != '1'`，若未设置或不为 `'1'` 则返回 `[]`。

## Goals / Non-Goals

**Goals:**
- 移除环境变量开关，使字体回退功能默认始终启用
- 更新所有文档反映新行为
- 版本升级至 0.1.0

**Non-Goals:**
- 不修改 `substitutionFonts` 的其他行为（getter/setter 接口不变）
- 不修改 `defaultTTFFallbackFonts` 配置机制
- 不修改回退查找逻辑本身

## Decisions

### 1. `substitutionFonts` getter 简化为直接返回 `self._substitutionFonts`

**决策**: 移除 `os.environ` 检查，getter 直接返回 `self._substitutionFonts`。

**理由**:
- 环境变量检查是临时方案，用于功能稳定前的风险控制
- 功能已通过完整测试验证，可以作为默认行为
- 简化代码，减少运行时开销（每次 getter 调用不再读取环境变量）

**替代方案**: 保留环境变量但默认值改为 `'1'` — 被否决，因为增加了不必要的复杂性。

### 2. 测试用例移除环境变量设置/清理代码

**决策**: 所有 `test_ttfont_fallback_*.py` 文件中的 `setUp/tearDown` 环境变量操作全部移除。

**理由**: 功能默认启用，测试不再需要显式设置环境变量。

### 3. 文档统一更新

**决策**: 同步更新中英文 README、userguide、plan 文档和 CHANGES.md。

## Risks / Trade-offs

- **[风险]** 已有用户依赖环境变量来禁用回退 → **缓解**: 这是增强 fork，功能设计上就是让回退默认启用；如需禁用可不设置 `substitutionFonts`
- **[风险]** 0.1.0 版本号暗示首次正式发布 → **缓解**: 符合项目当前状态

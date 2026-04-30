# Release 发布指南

## 版本管理

版本号统一在 `pyproject.toml` 中定义（单一来源）：

```toml
[project]
version = "4.4.10"
```

运行时通过 `importlib.metadata.version('reportlab-enhanced')` 获取版本。

workflow 会自动验证标签版本与 `pyproject.toml` 中版本一致性。

## 发布流程

### 正式发布

```bash
# 1. 更新版本号
vim pyproject.toml
# version = "x.y.z"

# 2. 提交代码
git add .
git commit -m "Release x.y.z"
git push origin master

# 3. 打标签并推送
git tag x.y.z-release
git push origin x.y.z-release
```

### Dry Run 测试

在正式发布前，可通过 GitHub Actions 手动触发 Dry Run 模式验证流程：

1. 进入 GitHub → Actions → Release and Deploy
2. 点击 "Run workflow"
3. 勾选 **"Dry run mode"**
4. 点击运行

**Dry Run 验证内容：**
- ✅ 版本一致性检查
- ✅ 测试套件运行
- ✅ 文档构建
- ✅ Pages 部署
- ✅ wheel + sdist 构建
- ❌ 不发布到 PyPI
- ❌ 不创建 GitHub Release

## 自动化流程

打标签后自动执行：

```
check-version      → 验证版本一致性
       ↓
test               → 运行测试套件
       ↓
build-docs         → 构建 MkDocs 文档
       ↓                        ↓
deploy-pages       → 部署到 GitHub Pages
                        ↓
publish-pypi       → 构建 wheel + sdist → 发布到 PyPI
       ↓
create-github-release → 创建 GitHub Release
```

## 发布前检查清单

- [ ] 更新 `pyproject.toml` 中的 `version`
- [ ] 确认版本号格式正确：`x.y.z`
- [ ] 推送代码到 master
- [ ] 推送标签：`x.y.z-release`

## PyPI Trusted Publisher 配置（一次性）

首次发布前需要在 PyPI 配置：

1. 登录 pypi.org → 项目设置 → Publishing
2. 添加 Trusted Publisher：
   - Owner: `selcarpa`
   - Repository: `reportlab_enhanced`
   - Workflow: `release.yml`
   - Environment: `release`

3. GitHub 仓库 → Settings → Environments → 新建 `release` 环境

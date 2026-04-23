# 发布到 PyPI

## 前置条件

1. 注册 [PyPI](https://pypi.org/) 账号
2. 注册 [TestPyPI](https://test.pypi.org/) 账号（可选，用于测试发布）
3. 安装构建工具：

```bash
pip install build twine
```

## 构建发行包

```bash
# 清理旧构建产物
rm -rf dist/ build/ *.egg-info

# 构建 sdist 和 wheel
python -m build
```

构建产物在 `dist/` 目录下：
- `reportlab_enhanced-<version>.tar.gz`（源码包）
- `reportlab_enhanced-<version>-py3-none-any.whl`（wheel 包）

> 注意：setup.py 中 `name="reportlab-enhanced"`，所以 PyPI 上的包名是 `reportlab-enhanced`，但构建产物文件名中 `-` 会被替换为 `_`。

## 检查包

```bash
# 检查包的元数据和内容
twine check dist/*
```

## 发布到 TestPyPI（推荐先测试）

```bash
twine upload --repository testpypi dist/*
```

验证：

```bash
pip install --index-url https://test.pypi.org/simple/ reportlab-enhanced
```

## 发布到 PyPI

```bash
twine upload dist/*
```

验证：

```bash
pip install reportlab-enhanced
```

## 版本号管理

版本号定义在 `src/reportlab/__init__.py` 的 `Version` 变量中。发布新版本前修改此值。

当前 setup.py 中 `__version__='4.4.5'` 是 setup.py 自身的版本（用于构建过程），实际包版本由 `get_version()` 从 `__init__.py` 的 `Version` 读取。

## 注意事项

- 同版本号不能重复上传，每次发布必须递增版本号
- 首次发布后，包名即被占用，后续只能同账号上传
- `license.txt` 在 `reportlab_files` 列表中，会作为 `package_data` 打包进去
- setup.py 会在构建时自动下载 T1 字体曲线文件和 glyphlist（可用 `--no-download-t1-files` 跳过）

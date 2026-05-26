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
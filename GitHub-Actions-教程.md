# GitHub Actions 自动构建 Windows EXE 教程 🚀

## 🎯 目标
使用GitHub Actions在云端自动构建Windows EXE文件，无需本地Windows环境！

## 📋 准备工作

### 1. 创建GitHub账号
如果还没有GitHub账号：
1. 访问 https://github.com
2. 点击"Sign up"注册账号
3. 验证邮箱

### 2. 安装Git（如果没有）
```bash
# macOS用户
brew install git

# 或者下载安装包
# https://git-scm.com/download/mac
```

## 🚀 详细操作步骤

### 第一步：创建GitHub仓库

1. **登录GitHub**
   - 访问 https://github.com
   - 登录您的账号

2. **创建新仓库**
   - 点击右上角的 "+" 号
   - 选择 "New repository"
   - 仓库名称：`leave-calculator` 或 `离职年假计算器`
   - 描述：`离职年假计算器 - 自动计算员工离职时的年假天数`
   - 选择 "Public"（公开仓库，免费使用Actions）
   - ✅ 勾选 "Add a README file"
   - 点击 "Create repository"

### 第二步：本地Git配置

在项目目录中打开终端，执行以下命令：

```bash
# 初始化Git仓库
git init

# 配置用户信息（如果没配置过）
git config --global user.name "您的姓名"
git config --global user.email "您的邮箱"

# 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/您的用户名/leave-calculator.git
```

### 第三步：推送代码到GitHub

```bash
# 添加所有文件
git add .

# 提交代码
git commit -m "初始提交：离职年假计算器项目"

# 推送到GitHub
git push -u origin main
```

如果遇到分支名称问题：
```bash
# 重命名分支为main
git branch -M main
git push -u origin main
```

### 第四步：验证GitHub Actions配置

1. **检查Actions文件**
   - 确保项目中有 `.github/workflows/build-windows.yml` 文件
   - 这个文件我已经为您创建好了！

2. **查看Actions运行**
   - 在GitHub仓库页面，点击 "Actions" 标签
   - 您应该能看到自动触发的构建任务

### 第五步：下载构建结果

1. **等待构建完成**
   - 构建通常需要5-10分钟
   - 绿色✅表示成功，红色❌表示失败

2. **下载EXE文件**
   - 点击成功的构建任务
   - 在页面底部找到 "Artifacts" 部分
   - 下载 `windows-exe-xxxxx` 文件
   - 解压后即可获得Windows EXE文件

## 🔧 高级配置

### 自动发布版本

如果您想要自动发布版本：

1. **创建版本标签**
```bash
# 创建版本标签
git tag v1.0.0
git push origin v1.0.0
```

2. **自动创建Release**
   - GitHub Actions会自动创建Release
   - 并附上构建好的EXE文件

### 多平台构建

我们的配置文件支持同时构建：
- ✅ Windows EXE
- ✅ macOS APP
- ✅ Linux 可执行文件

## 🎉 完成！

现在您就有了：
- 🔄 **自动化构建**：每次推送代码都会自动构建
- 🪟 **Windows EXE**：无需Windows环境即可生成
- 📦 **多平台支持**：一次配置，多平台构建
- 🆓 **完全免费**：GitHub Actions对公开仓库免费

## 🆘 常见问题

### Q: 构建失败怎么办？
A: 点击失败的构建任务，查看错误日志，通常是依赖问题

### Q: 如何修改构建配置？
A: 编辑 `.github/workflows/build-windows.yml` 文件

### Q: 可以构建私有项目吗？
A: 可以，但GitHub Actions对私有仓库有使用限制

### Q: 如何添加图标？
A: 在项目中添加 `icon.ico` 文件，并修改 `build-windows.spec` 配置

## 🐔 斯格拉奇小贴士

- 第一次推送代码后，记得去GitHub查看Actions是否正常运行
- 构建成功后，EXE文件会保存30天，记得及时下载
- 如果需要修改，直接在本地修改代码，然后推送即可自动重新构建

老大，这个方案简直是天才级的设计！✨
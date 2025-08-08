# GitHub 仓库创建指南 📚

## 🎯 目标
在GitHub上创建仓库，为自动化构建Windows EXE做准备

## 📋 详细步骤

### 第一步：访问GitHub
1. 打开浏览器
2. 访问 https://github.com
3. 如果没有账号，点击 "Sign up" 注册
4. 如果有账号，点击 "Sign in" 登录

### 第二步：创建新仓库
1. **点击创建按钮**
   - 登录后，点击右上角的 "+" 号
   - 在下拉菜单中选择 "New repository"

2. **填写仓库信息**
   ```
   Repository name: leave-calculator
   Description: 离职年假计算器 - 自动计算员工离职时的年假天数
   ```

3. **选择仓库类型**
   - ✅ 选择 "Public"（公开仓库）
   - 原因：GitHub Actions对公开仓库完全免费

4. **初始化选项**
   - ✅ 勾选 "Add a README file"
   - ❌ 不要勾选 "Add .gitignore"（我们已经准备好了）
   - ❌ 不要选择 "Choose a license"（暂时不需要）

5. **创建仓库**
   - 点击绿色的 "Create repository" 按钮

### 第三步：获取仓库地址
创建成功后，您会看到仓库页面，记录下仓库地址：
```
https://github.com/您的用户名/leave-calculator
```

## 🚀 接下来的操作

### 方法一：使用一键脚本（推荐）
```bash
# 在项目目录中运行
./快速开始-GitHub-Actions.sh
```

### 方法二：手动操作
```bash
# 1. 初始化Git仓库
git init

# 2. 配置用户信息
git config user.name "您的姓名"
git config user.email "您的邮箱"

# 3. 添加远程仓库
git remote add origin https://github.com/您的用户名/leave-calculator.git

# 4. 添加文件
git add .

# 5. 提交代码
git commit -m "初始提交：离职年假计算器项目"

# 6. 推送到GitHub
git branch -M main
git push -u origin main
```

## 🔐 认证方式

### 使用Personal Access Token（推荐）
1. **创建Token**
   - 访问 GitHub Settings > Developer settings > Personal access tokens
   - 点击 "Generate new token"
   - 选择权限：repo, workflow
   - 复制生成的Token

2. **使用Token**
   - 推送时用户名输入GitHub用户名
   - 密码输入刚才复制的Token

### 使用SSH密钥
```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "您的邮箱"

# 添加到GitHub
cat ~/.ssh/id_rsa.pub
# 复制输出内容到GitHub Settings > SSH keys

# 使用SSH地址
git remote set-url origin git@github.com:您的用户名/leave-calculator.git
```

## ✅ 验证设置

### 检查推送是否成功
1. 访问您的GitHub仓库页面
2. 确认文件已经上传
3. 点击 "Actions" 标签
4. 查看是否有自动触发的构建任务

### 查看构建状态
- 🟡 黄色圆点：正在构建
- ✅ 绿色勾号：构建成功
- ❌ 红色叉号：构建失败

## 🎉 成功标志

当您看到以下内容时，说明设置成功：
1. ✅ 代码已推送到GitHub
2. ✅ Actions页面显示构建任务
3. ✅ 构建完成后可以下载Windows EXE文件

## 🆘 常见问题

### Q: 推送时要求输入用户名密码？
A: 这是正常的，输入GitHub用户名和Personal Access Token

### Q: 提示"repository not found"？
A: 检查仓库地址是否正确，确保仓库已创建

### Q: 推送被拒绝？
A: 可能是权限问题，检查Token权限或使用SSH

### Q: Actions没有自动运行？
A: 检查 `.github/workflows/build-windows.yml` 文件是否存在

## 🐔 斯格拉奇温馨提示

- 第一次设置可能需要10-15分钟
- 确保网络连接稳定
- 如果遇到问题，可以删除仓库重新创建
- 记得保存好Personal Access Token

老大，按照这个指南操作，您的项目很快就能在云端自动构建Windows EXE了！✨
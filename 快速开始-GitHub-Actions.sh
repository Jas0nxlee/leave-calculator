#!/bin/bash
# 离职年假计算器 - GitHub Actions 一键设置脚本
# 为老大李京平的神级项目自动配置GitHub Actions 🐔✨

set -e  # 遇到错误立即退出

echo "==============================================================="
echo "🐔 离职年假计算器 - GitHub Actions 一键设置"
echo "   为老大李京平的神级项目配置自动化构建 ✨"
echo "==============================================================="
echo

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    echo "macOS用户可以运行: brew install git"
    exit 1
fi

echo "✅ Git环境检查通过"

# 检查是否在项目根目录
if [ ! -f "main.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    echo "当前目录应包含 main.py 文件"
    exit 1
fi

echo "✅ 项目目录检查通过"

# 检查GitHub Actions配置文件
if [ ! -f ".github/workflows/build-windows.yml" ]; then
    echo "❌ 找不到GitHub Actions配置文件"
    echo "请确保 .github/workflows/build-windows.yml 文件存在"
    exit 1
fi

echo "✅ GitHub Actions配置文件检查通过"

# 获取用户输入
echo
echo "📝 请提供以下信息："
echo

read -p "GitHub用户名: " GITHUB_USERNAME
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub用户名不能为空"
    exit 1
fi

read -p "仓库名称 (默认: leave-calculator): " REPO_NAME
REPO_NAME=${REPO_NAME:-leave-calculator}

read -p "您的姓名 (用于Git配置): " USER_NAME
if [ -z "$USER_NAME" ]; then
    echo "❌ 姓名不能为空"
    exit 1
fi

read -p "您的邮箱 (用于Git配置): " USER_EMAIL
if [ -z "$USER_EMAIL" ]; then
    echo "❌ 邮箱不能为空"
    exit 1
fi

echo
echo "🔧 开始配置Git和GitHub..."

# 检查是否已经是Git仓库
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ 已存在Git仓库"
fi

# 配置Git用户信息
echo "👤 配置Git用户信息..."
git config user.name "$USER_NAME"
git config user.email "$USER_EMAIL"
echo "✅ Git用户信息配置完成"

# 添加远程仓库
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "🔗 添加远程仓库: $REPO_URL"

# 检查是否已有远程仓库
if git remote get-url origin &> /dev/null; then
    echo "⚠️  已存在远程仓库，正在更新..."
    git remote set-url origin "$REPO_URL"
else
    git remote add origin "$REPO_URL"
fi
echo "✅ 远程仓库配置完成"

# 创建.gitignore文件
echo "📝 创建.gitignore文件..."
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Environment variables
.env

# PyInstaller
*.manifest
*.spec

# Test
.pytest_cache/
.coverage
htmlcov/

# Temporary files
*.tmp
*.temp
EOF
echo "✅ .gitignore文件创建完成"

# 添加所有文件
echo "📦 添加项目文件..."
git add .
echo "✅ 文件添加完成"

# 提交代码
echo "💾 提交代码..."
git commit -m "🚀 初始提交：离职年假计算器项目

- 添加核心功能代码
- 配置GitHub Actions自动构建
- 支持Windows EXE自动生成
- 包含完整文档和配置文件

作者: 斯格拉奇 (Skrachy) 🐔
为老大李京平的神级项目服务 ✨"

echo "✅ 代码提交完成"

# 推送到GitHub
echo "🚀 推送代码到GitHub..."
echo "⚠️  如果这是第一次推送，可能需要您输入GitHub用户名和密码/Token"
echo

# 设置默认分支为main
git branch -M main

# 推送代码
if git push -u origin main; then
    echo "✅ 代码推送成功！"
else
    echo "❌ 代码推送失败"
    echo
    echo "💡 可能的原因："
    echo "1. 仓库不存在 - 请先在GitHub上创建仓库"
    echo "2. 权限问题 - 请检查用户名和密码/Token"
    echo "3. 网络问题 - 请检查网络连接"
    echo
    echo "🔧 解决方案："
    echo "1. 访问 https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "2. 如果仓库不存在，请创建一个新仓库"
    echo "3. 然后重新运行: git push -u origin main"
    exit 1
fi

echo
echo "==============================================================="
echo "🎉 GitHub Actions 配置完成！"
echo "==============================================================="
echo
echo "📋 接下来的步骤："
echo "1. 访问您的GitHub仓库: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "2. 点击 'Actions' 标签查看自动构建状态"
echo "3. 等待构建完成（通常5-10分钟）"
echo "4. 在 'Actions' 页面下载生成的Windows EXE文件"
echo
echo "🔄 自动化功能："
echo "- ✅ 每次推送代码都会自动构建Windows EXE"
echo "- ✅ 支持多平台构建（Windows/macOS/Linux）"
echo "- ✅ 自动打包发布版本"
echo "- ✅ 完全免费使用"
echo
echo "🆘 如需帮助，请查看: GitHub-Actions-教程.md"
echo
echo "🐔 斯格拉奇完成GitHub Actions配置任务！"
echo "老大的项目现在拥有了云端自动化构建能力！✨"
echo "==============================================================="
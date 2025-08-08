#!/bin/bash

# 🚨 GitHub敏感文件彻底清除脚本
# 作者: 斯格拉奇 (程序"鸡"员)
# 用途: 从Git历史中彻底删除.env文件

echo "🚨 开始清除GitHub中的敏感文件..."
echo "⚠️  警告：此操作将重写Git历史，请确保已备份重要数据！"
echo ""

# 检查Git环境
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "❌ 当前目录不是Git仓库"
    exit 1
fi

echo "📋 当前仓库状态："
git remote -v
echo ""

# 确认操作
read -p "🤔 确定要从Git历史中彻底删除.env文件吗？(输入 YES 继续): " confirm
if [ "$confirm" != "YES" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo ""
echo "🔄 步骤1: 从Git历史中彻底删除.env文件..."

# 使用git filter-branch删除文件
git filter-branch --force --index-filter \
    'git rm --cached --ignore-unmatch .env' \
    --prune-empty --tag-name-filter cat -- --all

if [ $? -eq 0 ]; then
    echo "✅ 成功从Git历史中删除.env文件"
else
    echo "❌ 删除失败，请检查错误信息"
    exit 1
fi

echo ""
echo "🔄 步骤2: 清理引用和垃圾回收..."

# 清理引用
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin

# 垃圾回收
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ 清理完成"

echo ""
echo "🔄 步骤3: 强制推送到远程仓库..."
echo "⚠️  这将重写远程仓库的历史！"

read -p "🤔 确定要强制推送到GitHub吗？(输入 YES 继续): " push_confirm
if [ "$push_confirm" != "YES" ]; then
    echo "⚠️  本地历史已清理，但未推送到远程仓库"
    echo "💡 如需推送，请手动执行: git push --force --all"
    exit 0
fi

# 强制推送所有分支
git push --force --all

if [ $? -eq 0 ]; then
    echo "✅ 成功推送到远程仓库"
else
    echo "❌ 推送失败，请检查网络连接和权限"
    exit 1
fi

# 强制推送标签（如果有）
git push --force --tags 2>/dev/null

echo ""
echo "🎉 清除完成！"
echo ""
echo "📋 后续建议："
echo "1. 🔒 立即更换.env文件中的所有敏感信息（API密钥、密码等）"
echo "2. 🔍 检查GitHub仓库，确认.env文件已从历史中消失"
echo "3. 📝 确保.gitignore文件包含.env规则"
echo "4. 🚨 通知团队成员重新克隆仓库（如果是协作项目）"
echo ""
echo "⚠️  重要提醒："
echo "- 如果.env中包含API密钥，请立即在对应平台重新生成"
echo "- 如果包含数据库密码，请立即修改数据库密码"
echo "- 考虑启用GitHub的密钥扫描功能"
echo ""
echo "🐔 斯格拉奇提醒：安全第一，预防为主！"
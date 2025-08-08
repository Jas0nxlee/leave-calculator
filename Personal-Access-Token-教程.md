# GitHub Personal Access Token 创建教程 🔐

## 🎯 为什么需要Personal Access Token？

GitHub从2021年8月开始，不再支持使用密码进行Git操作，必须使用Personal Access Token (PAT)。这是为了提高安全性。

## 📋 创建步骤

### 第一步：登录GitHub
1. 打开浏览器，访问 https://github.com
2. 使用您的用户名和密码登录

### 第二步：进入设置页面
1. 点击右上角的头像
2. 在下拉菜单中选择 "Settings"

### 第三步：进入开发者设置
1. 在左侧菜单中，滚动到最底部
2. 点击 "Developer settings"

### 第四步：创建Personal Access Token
1. 在左侧菜单中点击 "Personal access tokens"
2. 选择 "Tokens (classic)"
3. 点击 "Generate new token"
4. 选择 "Generate new token (classic)"

### 第五步：配置Token
1. **Note (备注)**: 填写 `离职年假计算器项目`
2. **Expiration (过期时间)**: 选择 `90 days` 或 `No expiration`
3. **Select scopes (选择权限)**:
   - ✅ **repo** (完整的仓库访问权限)
   - ✅ **workflow** (GitHub Actions工作流权限)
   - ✅ **write:packages** (包写入权限，可选)

### 第六步：生成Token
1. 滚动到页面底部
2. 点击绿色的 "Generate token" 按钮
3. **重要**: 立即复制生成的Token！
4. **警告**: Token只会显示一次，请妥善保存！

## 🔑 Token示例
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 💻 如何使用Token

### 方法一：在推送时输入
```bash
git push -u origin main
```
- Username: 输入您的GitHub用户名
- Password: 输入刚才复制的Token（不是您的GitHub密码！）

### 方法二：配置Git记住Token
```bash
# 配置Git记住凭据（推荐）
git config --global credential.helper store

# 第一次推送时输入Token，之后会自动记住
git push -u origin main
```

### 方法三：在URL中包含Token
```bash
# 设置包含Token的远程仓库地址
git remote set-url origin https://您的用户名:您的Token@github.com/您的用户名/leave-calculator.git
```

## ⚠️ 安全注意事项

### 保护您的Token
- 🔒 **绝对不要**将Token提交到代码仓库中
- 🔒 **绝对不要**在公开场合分享Token
- 🔒 **定期更换**Token（建议每90天）
- 🔒 **不使用时**及时删除Token

### 如果Token泄露
1. 立即访问 https://github.com/settings/tokens
2. 找到泄露的Token
3. 点击 "Delete" 删除
4. 重新创建新的Token

## 🆘 常见问题

### Q: 推送时提示"Authentication failed"？
A: 检查以下几点：
- 用户名是否正确
- 是否输入了Token而不是密码
- Token是否有正确的权限（repo + workflow）

### Q: Token过期了怎么办？
A: 
1. 访问 https://github.com/settings/tokens
2. 点击过期Token旁边的 "Regenerate token"
3. 或者删除旧Token，创建新Token

### Q: 忘记保存Token怎么办？
A: Token只显示一次，如果忘记保存：
1. 删除当前Token
2. 重新创建新Token
3. 妥善保存新Token

## 🎉 验证Token是否工作

创建Token后，运行以下命令验证：
```bash
# 测试Token是否有效
git ls-remote origin

# 如果显示分支信息，说明Token工作正常
```

## 🐔 斯格拉奇温馨提示

老大，Token就像是您的数字钥匙🔑：
- 创建时要选择合适的权限
- 使用时要小心保护
- 过期前要及时更新
- 泄露后要立即删除

有了这个Token，您就可以愉快地推送代码到GitHub，让我们的自动化构建系统为您服务了！✨

记住：**用户名 + Token = 推送成功** 🚀
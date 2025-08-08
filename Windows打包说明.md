# Windows EXE 打包说明 🪟

## 🎯 目标
将"离职年假计算器"打包成Windows可执行的exe文件

## 🚨 重要说明
由于PyInstaller的限制，**无法在macOS上直接生成Windows的exe文件**。需要在Windows环境中进行打包。

## 📋 解决方案

### 方案一：在Windows系统上打包（推荐）

#### 1. 准备Windows环境
- Windows 10/11 系统
- Python 3.8+ 已安装
- Git 已安装（可选）

#### 2. 获取项目代码
```bash
# 方法1: 使用Git克隆
git clone <项目地址>

# 方法2: 直接复制项目文件夹到Windows系统
```

#### 3. 安装依赖
```cmd
# 进入项目目录
cd 离职年假计算

# 安装Python依赖
pip install -r requirements.txt

# 安装PyInstaller
pip install pyinstaller
```

#### 4. 一键打包
```cmd
# 运行Windows批处理脚本
build.bat

# 或直接运行Python脚本
python build.py
```

#### 5. 获取exe文件
打包完成后，在以下目录找到exe文件：
- `dist/离职年假计算器.exe` - 主要可执行文件
- `release/` - 完整发布包

### 方案二：使用虚拟机

#### 1. 安装虚拟机软件
- VMware Fusion (macOS)
- Parallels Desktop (macOS)
- VirtualBox (免费)

#### 2. 创建Windows虚拟机
- 安装Windows 10/11
- 安装Python 3.8+
- 配置开发环境

#### 3. 在虚拟机中打包
按照方案一的步骤在虚拟机中进行打包

### 方案三：使用云服务器

#### 1. 租用Windows云服务器
- 阿里云ECS (Windows Server)
- 腾讯云CVM (Windows Server)
- AWS EC2 (Windows)

#### 2. 配置环境并打包
在云服务器上按照方案一的步骤进行

### 方案四：使用GitHub Actions（自动化）

#### 1. 创建GitHub仓库
将项目代码上传到GitHub

#### 2. 配置GitHub Actions
创建 `.github/workflows/build-windows.yml`：

```yaml
name: Build Windows EXE

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build EXE
      run: python build.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: windows-exe
        path: dist/
```

#### 3. 自动构建
每次推送代码后，GitHub会自动在Windows环境中构建exe文件

## 🔧 Windows专用配置

### build.spec 修改
为了更好地支持Windows，可以在build.spec中添加：

```python
# Windows特定配置
exe = EXE(
    # ... 其他配置 ...
    console=False,  # 不显示控制台
    icon='icon.ico',  # Windows图标文件
    version_file='version.txt',  # 版本信息
    uac_admin=False,  # 不需要管理员权限
)
```

### 添加Windows图标
1. 准备一个 `.ico` 格式的图标文件
2. 放在项目根目录
3. 在build.spec中指定图标路径

### 版本信息文件
创建 `version.txt` 文件：
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', '斯格拉奇工作室'),
        StringStruct('FileDescription', '离职年假计算器'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('ProductName', '离职年假计算器'),
        StringStruct('ProductVersion', '1.0.0.0')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

## 📦 预期输出

成功打包后将得到：
- `离职年假计算器.exe` - 约20-30MB的独立可执行文件
- 无需安装Python环境即可在Windows上运行
- 包含所有必要的依赖库和资源文件

## 🎯 推荐方案

**最推荐方案一**：直接在Windows系统上打包
- 最简单直接
- 兼容性最好
- 打包速度最快

如果没有Windows系统，推荐使用**方案四**：GitHub Actions
- 完全自动化
- 免费使用
- 可以同时生成多个平台的版本

## 🆘 需要帮助？

如果您需要我协助设置任何一种方案，请告诉我：
1. 您选择哪种方案
2. 您当前的环境情况
3. 遇到的具体问题

我会立即为您提供详细的操作指导！🐔✨
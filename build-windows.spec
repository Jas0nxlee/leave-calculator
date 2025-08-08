# -*- mode: python ; coding: utf-8 -*-
"""
离职年假计算器 - Windows专用PyInstaller配置
专为生成Windows exe文件优化 🪟🐔

作者: 斯格拉奇 (Skrachy) 🤖
版本: 1.0.0
"""

import os
from pathlib import Path

# 项目根目录
project_dir = Path(SPECPATH)
src_dir = project_dir / "src"

# 数据文件配置
datas = [
    # 配置文件模板
    (str(project_dir / ".env.template"), "."),
    # 文档文件
    (str(project_dir / "docs"), "docs"),
    # README文件
    (str(project_dir / "README.md"), "."),
]

# 隐藏导入模块（Windows特定优化）
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkcalendar',
    'requests',
    'dotenv',
    'json',
    'datetime',
    'pathlib',
    'logging',
    'threading',
    'queue',
    'urllib3',
    'ssl',
    'certifi',
    # Windows特定模块
    'win32api',
    'win32con',
    'win32gui',
    'pywintypes',
]

# 排除不需要的模块（Windows优化）
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'cv2',
    'tensorflow',
    'torch',
    'jupyter',
    'IPython',
    'notebook',
    'pytest',
    'black',
    'flake8',
    'mypy',
    'isort',
    # macOS/Linux特定模块
    'AppKit',
    'Foundation',
    'objc',
    'PyObjC',
    'gi',
    'gtk',
    'qt5',
    'PySide2',
    'PyQt5',
]

# 分析阶段配置
a = Analysis(
    [str(project_dir / "main.py")],  # 主入口文件
    pathex=[str(project_dir), str(src_dir)],  # 搜索路径
    binaries=[],  # 二进制文件
    datas=datas,  # 数据文件
    hiddenimports=hiddenimports,  # 隐藏导入
    hookspath=[],  # Hook路径
    hooksconfig={},  # Hook配置
    runtime_hooks=[],  # 运行时Hook
    excludes=excludes,  # 排除模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,  # 加密（可选）
    noarchive=False,
)

# PYZ归档配置
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Windows EXE配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='离职年假计算器',  # exe文件名
    debug=False,  # 调试模式
    bootloader_ignore_signals=False,
    strip=False,  # 去除符号表
    upx=True,  # UPX压缩（如果可用）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口（Windows GUI应用）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows特定配置
    icon=None,  # 图标文件路径（如果有的话）
    version_file=None,  # 版本信息文件
    uac_admin=False,  # 不需要管理员权限
    uac_uiaccess=False,  # 不需要UI访问权限
    # 添加Windows清单文件（可选）
    manifest=None,
)
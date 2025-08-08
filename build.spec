# -*- mode: python ; coding: utf-8 -*-
"""
离职年假计算器 - PyInstaller 打包配置
专为老大李京平的神级项目定制 🐔✨

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

# 隐藏导入模块（解决动态导入问题）
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
]

# 排除不需要的模块（减小exe体积）
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

# EXE可执行文件配置
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
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 图标文件（可选）
    version_file=None,  # 版本信息文件（可选）
)

# macOS应用包配置（仅在macOS上生效）
if os.name == 'posix':
    app = BUNDLE(
        exe,
        name='离职年假计算器.app',
        icon=None,
        bundle_identifier='com.skrachy.leave-calculator',
        info_plist={
            'CFBundleName': '离职年假计算器',
            'CFBundleDisplayName': '离职年假计算器',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleIdentifier': 'com.skrachy.leave-calculator',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
        },
    )
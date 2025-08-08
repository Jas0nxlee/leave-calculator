@echo off
chcp 65001 >nul
title 离职年假计算器 - Windows EXE 打包工具

echo.
echo ===============================================================
echo 🪟 离职年假计算器 - Windows EXE 专用打包工具
echo    为老大李京平的神级项目生成Windows可执行文件 ✨
echo ===============================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python环境
    echo 请先安装Python 3.8或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

REM 检查是否在项目根目录
if not exist "main.py" (
    echo ❌ 错误：请在项目根目录运行此脚本
    echo 当前目录应包含 main.py 文件
    pause
    exit /b 1
)

echo ✅ 项目文件检查通过
echo.

REM 运行Windows专用打包脚本
echo 🚀 开始Windows EXE打包...
echo.
python build-windows.py

REM 检查打包结果
if errorlevel 1 (
    echo.
    echo ❌ Windows EXE打包失败！
    echo 请检查错误信息并重试
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 Windows EXE打包成功！
    echo.
    echo 📁 生成的文件位置：
    echo    - dist\ 目录：包含可执行文件
    echo    - release-windows\ 目录：完整发布包
    echo.
    echo 💡 使用提示：
    echo    - 双击 dist\离职年假计算器.exe 即可运行
    echo    - 可将整个 release-windows 文件夹分发给其他用户
    echo    - 无需安装Python环境即可在Windows上运行
    echo.
    
    REM 询问是否打开输出目录
    set /p open_dir="是否打开输出目录？(Y/n): "
    if /i "%open_dir%"=="n" goto end
    if /i "%open_dir%"=="no" goto end
    
    REM 打开输出目录
    if exist "dist" (
        explorer dist
    )
    if exist "release-windows" (
        explorer release-windows
    )
)

:end
echo.
echo 🐔 斯格拉奇完成Windows打包任务！
pause
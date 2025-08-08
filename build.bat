@echo off
chcp 65001 >nul
title 离职年假计算器 - 自动打包工具

echo.
echo ========================================
echo 🐔 离职年假计算器 - Windows自动打包
echo    老大李京平的神级项目专用 ✨
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+并添加到系统PATH
    pause
    exit /b 1
)

REM 运行Python打包脚本
echo 🚀 启动自动打包脚本...
python build.py

REM 检查打包结果
if errorlevel 1 (
    echo.
    echo ❌ 打包失败！请检查错误信息
    pause
    exit /b 1
) else (
    echo.
    echo ✅ 打包成功！
    echo 📁 可执行文件位于 dist\ 目录
    echo 📦 发布包位于 release\ 目录
    echo.
    echo 🐔 斯格拉奇任务完成！老大的项目已成功打包！
    pause
)
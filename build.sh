#!/bin/bash
# 离职年假计算器 - macOS/Linux自动打包脚本
# 老大李京平的神级项目专用 🐔✨

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印横幅
echo ""
echo "========================================"
echo "🐔 离职年假计算器 - 自动打包工具"
echo "   老大李京平的神级项目专用 ✨"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python未安装${NC}"
        echo "请先安装Python 3.8+:"
        echo "  macOS: brew install python"
        echo "  Ubuntu: sudo apt install python3 python3-pip"
        echo "  CentOS: sudo yum install python3 python3-pip"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# 检查Python版本
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✅ Python版本: $PYTHON_VERSION${NC}"

# 检查是否在项目目录
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 给脚本执行权限
chmod +x "$0"

# 运行Python打包脚本
echo -e "${BLUE}🚀 启动自动打包脚本...${NC}"
$PYTHON_CMD build.py

# 检查打包结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 打包成功！${NC}"
    echo -e "${GREEN}📁 可执行文件位于 dist/ 目录${NC}"
    echo -e "${GREEN}📦 发布包位于 release/ 目录${NC}"
    echo ""
    echo -e "${YELLOW}🐔 斯格拉奇任务完成！老大的项目已成功打包！${NC}"
    
    # 在macOS上，尝试打开输出目录
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ -d "dist" ]; then
            echo "正在打开输出目录..."
            open dist/
        fi
    fi
else
    echo ""
    echo -e "${RED}❌ 打包失败！请检查错误信息${NC}"
    exit 1
fi

echo ""
echo "按回车键退出..."
read
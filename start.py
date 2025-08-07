#!/usr/bin/env python3
"""
离职年假计算器 - 快速启动脚本
自动检查虚拟环境并启动程序

作者: 斯格拉奇 (Skrachy) 🐔🤖
版本: 1.0.0
"""

import os
import sys
import subprocess
from pathlib import Path


def is_in_virtual_env():
    """检查是否在虚拟环境中"""
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )


def find_python_executable(venv_dir):
    """查找虚拟环境中的Python可执行文件"""
    if os.name == 'nt':  # Windows
        return venv_dir / "Scripts" / "python.exe"
    else:  # macOS/Linux
        return venv_dir / "bin" / "python"


def main():
    """主函数"""
    project_dir = Path(__file__).parent.absolute()
    venv_dir = project_dir / "venv"
    main_script = project_dir / "main.py"
    
    print("🐔 离职年假计算器 - 快速启动")
    print("=" * 50)
    
    # 如果已经在虚拟环境中，直接运行
    if is_in_virtual_env():
        print("✅ 已在虚拟环境中，直接启动程序...")
        try:
            import main
            main.main()
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            sys.exit(1)
        return
    
    # 检查虚拟环境是否存在
    if not venv_dir.exists():
        print("❌ 虚拟环境不存在")
        print("请先运行以下命令设置虚拟环境:")
        print("  python setup_venv.py")
        print("\n或手动创建:")
        print("  python -m venv venv")
        print("  # 然后激活虚拟环境并安装依赖")
        input("\n按回车键退出...")
        sys.exit(1)
    
    # 查找Python可执行文件
    python_exe = find_python_executable(venv_dir)
    if not python_exe.exists():
        print(f"❌ 找不到虚拟环境中的Python: {python_exe}")
        print("虚拟环境可能已损坏，请重新创建:")
        print("  python setup_venv.py")
        input("\n按回车键退出...")
        sys.exit(1)
    
    # 在虚拟环境中运行主程序
    print(f"🔧 使用虚拟环境启动: {venv_dir}")
    try:
        result = subprocess.run([
            str(python_exe),
            str(main_script)
        ], cwd=project_dir)
        
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
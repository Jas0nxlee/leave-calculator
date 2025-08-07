#!/usr/bin/env python3
"""
虚拟环境设置脚本
自动创建和配置项目虚拟环境

作者: 斯格拉奇 (Skrachy) 🐔🤖
版本: 1.0.0
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, cwd=None, check=True):
    """运行命令并返回结果"""
    print(f"执行命令: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        raise


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment(project_dir):
    """创建虚拟环境"""
    venv_dir = project_dir / "venv"
    
    if venv_dir.exists():
        print(f"⚠️  虚拟环境已存在: {venv_dir}")
        response = input("是否重新创建? (y/N): ").strip().lower()
        if response == 'y':
            print("删除现有虚拟环境...")
            import shutil
            shutil.rmtree(venv_dir)
        else:
            print("使用现有虚拟环境")
            return venv_dir
    
    print(f"🔧 创建虚拟环境: {venv_dir}")
    run_command(f"python -m venv {venv_dir}", cwd=project_dir)
    
    return venv_dir


def get_activation_command(venv_dir):
    """获取虚拟环境激活命令"""
    system = platform.system().lower()
    
    if system == "windows":
        return str(venv_dir / "Scripts" / "activate.bat")
    else:
        return f"source {venv_dir / 'bin' / 'activate'}"


def install_dependencies(project_dir, venv_dir):
    """安装项目依赖"""
    system = platform.system().lower()
    
    if system == "windows":
        pip_path = venv_dir / "Scripts" / "pip"
        python_path = venv_dir / "Scripts" / "python"
    else:
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"
    
    print("📦 升级pip...")
    run_command(f"{python_path} -m pip install --upgrade pip", cwd=project_dir)
    
    # 选择安装类型
    print("\n📋 选择安装类型:")
    print("1. 核心依赖 (仅运行程序所需)")
    print("2. 完整开发依赖 (包含测试和开发工具)")
    
    while True:
        choice = input("请选择 (1/2) [默认: 1]: ").strip()
        if choice == "" or choice == "1":
            requirements_file = project_dir / "requirements-core.txt"
            break
        elif choice == "2":
            requirements_file = project_dir / "requirements-dev.txt"
            break
        else:
            print("❌ 无效选择，请输入 1 或 2")
    
    if requirements_file.exists():
        print(f"📦 安装依赖: {requirements_file.name}")
        try:
            run_command(f"{pip_path} install -r {requirements_file.name}", cwd=project_dir)
            print("✅ 依赖安装完成！")
        except Exception as e:
            print(f"⚠️  部分依赖安装失败: {e}")
            print("可以稍后手动安装缺失的依赖")
    else:
        print(f"⚠️  {requirements_file.name}文件不存在，跳过依赖安装")


def create_activation_scripts(project_dir, venv_dir):
    """创建激活脚本"""
    system = platform.system().lower()
    
    # 创建激活脚本
    if system == "windows":
        activate_script = project_dir / "activate.bat"
        with open(activate_script, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
echo 🐔 激活离职年假计算器虚拟环境...
call "{venv_dir}\\Scripts\\activate.bat"
echo ✅ 虚拟环境已激活！
echo.
echo 💡 使用方法:
echo   python main.py          - 启动应用程序
echo   python run_tests.py     - 运行测试
echo   deactivate              - 退出虚拟环境
echo.
""")
    else:
        activate_script = project_dir / "activate.sh"
        with open(activate_script, 'w', encoding='utf-8') as f:
            f.write(f"""#!/bin/bash
echo "🐔 激活离职年假计算器虚拟环境..."
source "{venv_dir}/bin/activate"
echo "✅ 虚拟环境已激活！"
echo ""
echo "💡 使用方法:"
echo "  python main.py          - 启动应用程序"
echo "  python run_tests.py     - 运行测试"
echo "  deactivate              - 退出虚拟环境"
echo ""
""")
        # 添加执行权限
        os.chmod(activate_script, 0o755)
    
    print(f"📝 创建激活脚本: {activate_script}")


def create_env_file(project_dir):
    """创建.env文件"""
    env_file = project_dir / ".env"
    template_file = project_dir / ".env.template"
    
    if env_file.exists():
        print("⚠️  .env文件已存在，跳过创建")
        return
    
    if template_file.exists():
        print("📝 从模板创建.env文件...")
        import shutil
        shutil.copy2(template_file, env_file)
        print(f"✅ 已创建.env文件: {env_file}")
        print("⚠️  请编辑.env文件，配置企业微信参数")
    else:
        print("⚠️  .env.template文件不存在，请手动创建.env文件")


def main():
    """主函数"""
    print("=" * 60)
    print("🐔 离职年假计算器 - 虚拟环境设置")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 获取项目目录
    project_dir = Path(__file__).parent.absolute()
    print(f"📁 项目目录: {project_dir}")
    
    try:
        # 创建虚拟环境
        venv_dir = create_virtual_environment(project_dir)
        
        # 安装依赖
        install_dependencies(project_dir, venv_dir)
        
        # 创建激活脚本
        create_activation_scripts(project_dir, venv_dir)
        
        # 创建.env文件
        create_env_file(project_dir)
        
        print("\n" + "=" * 60)
        print("🎉 虚拟环境设置完成！")
        print("=" * 60)
        
        # 显示使用说明
        system = platform.system().lower()
        if system == "windows":
            print("💡 激活虚拟环境:")
            print("   activate.bat")
            print("\n或者:")
            print(f"   {get_activation_command(venv_dir)}")
        else:
            print("💡 激活虚拟环境:")
            print("   ./activate.sh")
            print("\n或者:")
            print(f"   {get_activation_command(venv_dir)}")
        
        print("\n📋 后续步骤:")
        print("1. 激活虚拟环境")
        print("2. 编辑.env文件，配置企业微信参数")
        print("3. 运行 python main.py 启动应用程序")
        print("4. 运行 python run_tests.py --type unit 测试功能")
        
    except Exception as e:
        print(f"\n❌ 设置失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
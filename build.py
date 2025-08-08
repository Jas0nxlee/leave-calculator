#!/usr/bin/env python3
"""
离职年假计算器 - 自动化打包脚本
一键生成exe可执行文件 🐔🚀

作者: 斯格拉奇 (Skrachy) 🤖
版本: 1.0.0
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform


def print_banner():
    """打印启动横幅"""
    # 设置控制台编码为UTF-8，解决Windows下的Unicode显示问题
    if platform.system() == "Windows":
        try:
            # 尝试设置控制台编码为UTF-8
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
        except:
            # 如果设置失败，使用ASCII安全的版本
            print("=" * 70)
            print("Leave Calculator - Automated Build Tool")
            print("   Customized for Boss Li Jingping's Project")
            print("=" * 70)
            return
    
    print("=" * 70)
    print("🐔 离职年假计算器 - 自动化打包工具")
    print("   为老大李京平的神级项目量身定制 ✨")
    print("=" * 70)


def check_environment():
    """检查打包环境"""
    print("\n🔍 检查打包环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {sys.version}")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 检查项目文件
    project_dir = Path(__file__).parent
    main_file = project_dir / "main.py"
    spec_file = project_dir / "build.spec"
    
    if not main_file.exists():
        print(f"❌ 找不到主程序文件: {main_file}")
        return False
    print(f"✅ 主程序文件: {main_file}")
    
    if not spec_file.exists():
        print(f"❌ 找不到打包配置文件: {spec_file}")
        return False
    print(f"✅ 打包配置文件: {spec_file}")
    
    return True


def clean_build_dirs():
    """清理构建目录"""
    print("\n🧹 清理旧的构建文件...")
    
    project_dir = Path(__file__).parent
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ 已清理: {dir_path}")
            except Exception as e:
                print(f"⚠️  清理失败 {dir_path}: {e}")
    
    # 清理.pyc文件
    for pyc_file in project_dir.rglob("*.pyc"):
        try:
            pyc_file.unlink()
        except Exception:
            pass


def install_dependencies():
    """安装打包依赖"""
    print("\n📦 检查并安装依赖...")
    
    try:
        # 确保PyInstaller是最新版本
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "pyinstaller"
        ], check=True, capture_output=True)
        print("✅ PyInstaller已更新到最新版本")
        
        # 安装项目依赖
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ 项目依赖已安装")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    
    return True


def build_executable():
    """构建可执行文件"""
    print("\n🔨 开始构建可执行文件...")
    print("这可能需要几分钟时间，请耐心等待... ☕")
    
    project_dir = Path(__file__).parent
    spec_file = project_dir / "build.spec"
    
    try:
        # 运行PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", str(spec_file)]
        print(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 构建成功！")
            return True
        else:
            print("❌ 构建失败！")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False


def check_output():
    """检查输出文件"""
    print("\n📋 检查构建结果...")
    
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist"
    
    if not dist_dir.exists():
        print("❌ 输出目录不存在")
        return False
    
    # 查找可执行文件
    system = platform.system()
    if system == "Windows":
        exe_pattern = "*.exe"
    elif system == "Darwin":  # macOS
        exe_pattern = "*.app"
    else:  # Linux
        exe_pattern = "*"
    
    exe_files = list(dist_dir.glob(exe_pattern))
    
    if not exe_files:
        print(f"❌ 在 {dist_dir} 中找不到可执行文件")
        return False
    
    for exe_file in exe_files:
        file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ 生成文件: {exe_file.name} ({file_size:.1f} MB)")
    
    return True


def create_release_package():
    """创建发布包"""
    print("\n📦 创建发布包...")
    
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist"
    release_dir = project_dir / "release"
    
    # 创建release目录
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    try:
        # 复制可执行文件
        for item in dist_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, release_dir)
            elif item.is_dir():
                shutil.copytree(item, release_dir / item.name)
        
        # 复制必要文件
        files_to_copy = [
            "README.md",
            ".env.template",
        ]
        
        for file_name in files_to_copy:
            src_file = project_dir / file_name
            if src_file.exists():
                shutil.copy2(src_file, release_dir)
                print(f"✅ 已复制: {file_name}")
        
        # 复制docs目录
        docs_dir = project_dir / "docs"
        if docs_dir.exists():
            shutil.copytree(docs_dir, release_dir / "docs")
            print("✅ 已复制: docs目录")
        
        print(f"✅ 发布包已创建: {release_dir}")
        return True
        
    except Exception as e:
        print(f"❌ 创建发布包失败: {e}")
        return False


def main():
    """主函数"""
    print_banner()
    
    try:
        # 检查环境
        if not check_environment():
            print("\n❌ 环境检查失败，无法继续打包")
            return False
        
        # 清理构建目录
        clean_build_dirs()
        
        # 安装依赖
        if not install_dependencies():
            print("\n❌ 依赖安装失败，无法继续打包")
            return False
        
        # 构建可执行文件
        if not build_executable():
            print("\n❌ 构建失败")
            return False
        
        # 检查输出
        if not check_output():
            print("\n❌ 输出检查失败")
            return False
        
        # 创建发布包
        if not create_release_package():
            print("\n⚠️  发布包创建失败，但exe文件已生成")
        
        print("\n" + "=" * 70)
        print("🎉 打包完成！老大的神级项目已成功打包为exe！")
        print("📁 输出目录: dist/")
        print("📦 发布包: release/")
        print("=" * 70)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n👋 打包被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 打包过程中发生未知错误: {e}")
        return False


if __name__ == "__main__":
    success = main()
    
    # 检查是否在CI环境中运行
    is_ci = os.getenv('CI') or os.getenv('GITHUB_ACTIONS')
    
    if not success:
        if not is_ci:
            print("\n按回车键退出...")
            input()
        sys.exit(1)
    else:
        print("\n🐔 斯格拉奇完成任务！老大的项目已成功打包！✨")
        if not is_ci:
            print("按回车键退出...")
            input()
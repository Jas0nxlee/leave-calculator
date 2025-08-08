#!/usr/bin/env python3
"""
离职年假计算器 - Windows专用打包脚本
专门用于在Windows系统上生成exe文件 🪟🐔

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
    print("=" * 70)
    print("🪟 离职年假计算器 - Windows EXE 专用打包工具")
    print("   为老大李京平的神级项目生成Windows可执行文件 ✨")
    print("=" * 70)


def check_windows_environment():
    """检查Windows环境"""
    print("\n🔍 检查Windows打包环境...")
    
    # 检查操作系统
    if platform.system() != "Windows":
        print("⚠️  当前系统不是Windows，生成的exe可能无法在Windows上正常运行")
        print(f"当前系统: {platform.system()}")
        response = input("是否继续？(y/N): ")
        if response.lower() != 'y':
            return False
    else:
        print(f"✅ 操作系统: Windows {platform.release()}")
    
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
        print("正在安装PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                         check=True, capture_output=True)
            print("✅ PyInstaller安装成功")
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False
    
    # 检查项目文件
    project_dir = Path(__file__).parent
    main_file = project_dir / "main.py"
    spec_file = project_dir / "build-windows.spec"
    
    if not main_file.exists():
        print(f"❌ 找不到主程序文件: {main_file}")
        return False
    print(f"✅ 主程序文件: {main_file}")
    
    if not spec_file.exists():
        print(f"❌ 找不到Windows打包配置文件: {spec_file}")
        print("将使用默认配置文件: build.spec")
        spec_file = project_dir / "build.spec"
        if not spec_file.exists():
            print(f"❌ 找不到任何打包配置文件")
            return False
    print(f"✅ 打包配置文件: {spec_file}")
    
    return True


def install_windows_dependencies():
    """安装Windows特定依赖"""
    print("\n📦 安装Windows依赖...")
    
    windows_packages = [
        "pyinstaller",
        "pywin32",  # Windows API支持
    ]
    
    for package in windows_packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "--upgrade", package
            ], check=True, capture_output=True)
            print(f"✅ {package} 已安装/更新")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  {package} 安装失败: {e}")
    
    # 安装项目依赖
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ 项目依赖已安装")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  项目依赖安装失败: {e}")
    
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


def build_windows_exe():
    """构建Windows EXE文件"""
    print("\n🔨 开始构建Windows EXE文件...")
    print("这可能需要几分钟时间，请耐心等待... ☕")
    
    project_dir = Path(__file__).parent
    
    # 优先使用Windows专用配置
    spec_file = project_dir / "build-windows.spec"
    if not spec_file.exists():
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
            print("✅ Windows EXE构建成功！")
            return True
        else:
            print("❌ 构建失败！")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False


def check_exe_output():
    """检查EXE输出文件"""
    print("\n📋 检查Windows EXE构建结果...")
    
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist"
    
    if not dist_dir.exists():
        print("❌ 输出目录不存在")
        return False
    
    # 查找exe文件
    exe_files = list(dist_dir.glob("*.exe"))
    
    if not exe_files:
        # 查找其他可执行文件
        exe_files = [f for f in dist_dir.iterdir() 
                    if f.is_file() and not f.suffix in ['.txt', '.log']]
    
    if not exe_files:
        print(f"❌ 在 {dist_dir} 中找不到可执行文件")
        return False
    
    for exe_file in exe_files:
        file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ 生成Windows文件: {exe_file.name} ({file_size:.1f} MB)")
    
    return True


def create_windows_release():
    """创建Windows发布包"""
    print("\n📦 创建Windows发布包...")
    
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist"
    release_dir = project_dir / "release-windows"
    
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
            "Windows打包说明.md",
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
        
        # 创建Windows使用说明
        windows_readme = release_dir / "Windows使用说明.txt"
        with open(windows_readme, 'w', encoding='utf-8') as f:
            f.write("""离职年假计算器 - Windows版本

使用方法：
1. 双击 "离职年假计算器.exe" 启动程序
2. 首次运行会自动创建配置文件
3. 根据界面提示输入员工信息
4. 点击"计算年假"按钮获取结果

注意事项：
- 本程序无需安装，可直接运行
- 如需企业微信通知功能，请配置.env文件
- 遇到问题请查看docs目录中的详细文档

技术支持：斯格拉奇 (Skrachy) 🐔
""")
        
        print(f"✅ Windows发布包已创建: {release_dir}")
        return True
        
    except Exception as e:
        print(f"❌ 创建Windows发布包失败: {e}")
        return False


def main():
    """主函数"""
    print_banner()
    
    try:
        # 检查Windows环境
        if not check_windows_environment():
            print("\n❌ Windows环境检查失败，无法继续打包")
            return False
        
        # 清理构建目录
        clean_build_dirs()
        
        # 安装Windows依赖
        if not install_windows_dependencies():
            print("\n⚠️  依赖安装有问题，但继续尝试打包...")
        
        # 构建Windows EXE
        if not build_windows_exe():
            print("\n❌ Windows EXE构建失败")
            return False
        
        # 检查输出
        if not check_exe_output():
            print("\n❌ EXE输出检查失败")
            return False
        
        # 创建Windows发布包
        if not create_windows_release():
            print("\n⚠️  Windows发布包创建失败，但exe文件已生成")
        
        print("\n" + "=" * 70)
        print("🎉 Windows EXE打包完成！老大的神级项目已成功打包为Windows可执行文件！")
        print("📁 EXE文件目录: dist/")
        print("📦 Windows发布包: release-windows/")
        print("🪟 可在任何Windows系统上直接运行！")
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
    
    if not success:
        print("\n按回车键退出...")
        input()
        sys.exit(1)
    else:
        print("\n🐔 斯格拉奇完成Windows打包任务！老大的项目已成功生成Windows EXE！✨")
        print("按回车键退出...")
        input()
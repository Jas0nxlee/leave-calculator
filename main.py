#!/usr/bin/env python3
"""
离职员工剩余年假计算器
主程序入口

作者: 斯格拉奇 (Skrachy) 🐔🤖
版本: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def setup_logging():
    """设置日志配置"""
    # 创建logs目录
    logs_dir = current_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            # 文件处理器
            logging.FileHandler(
                logs_dir / "leave_calculator.log",
                encoding='utf-8'
            ),
            # 控制台处理器
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 设置第三方库的日志级别
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

def check_virtual_environment():
    """检查是否在虚拟环境中运行"""
    logger = logging.getLogger(__name__)
    
    # 检查虚拟环境
    in_venv = (
        hasattr(sys, 'real_prefix') or  # virtualenv
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or  # venv
        os.environ.get('VIRTUAL_ENV') is not None  # 环境变量
    )
    
    if in_venv:
        venv_path = os.environ.get('VIRTUAL_ENV', sys.prefix)
        logger.info(f"✅ 运行在虚拟环境中: {venv_path}")
        return True
    else:
        logger.warning("⚠️  未检测到虚拟环境")
        logger.info("建议使用虚拟环境运行程序:")
        logger.info("  1. 运行 python setup_venv.py 自动设置")
        logger.info("  2. 或手动创建: python -m venv venv")
        logger.info("  3. 激活虚拟环境后再运行程序")
        return False

def check_environment():
    """检查运行环境"""
    logger = logging.getLogger(__name__)
    
    # 检查虚拟环境（警告但不阻止运行）
    check_virtual_environment()
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        logger.error("需要Python 3.8或更高版本")
        return False
    
    # 检查.env文件
    env_file = current_dir / ".env"
    if not env_file.exists():
        logger.warning(f".env文件不存在: {env_file}")
        logger.info("请复制.env.template为.env并配置企业微信参数")
        
        # 尝试复制模板文件
        template_file = current_dir / ".env.template"
        if template_file.exists():
            try:
                import shutil
                shutil.copy2(template_file, env_file)
                logger.info(f"已创建.env文件，请编辑配置: {env_file}")
            except Exception as e:
                logger.error(f"创建.env文件失败: {e}")
    
    # 检查必要的依赖
    try:
        import tkinter
        logger.info("tkinter GUI库检查通过")
    except ImportError:
        logger.error("tkinter库未安装，请安装Python的tkinter支持")
        return False
    
    try:
        import requests
        logger.info("requests HTTP库检查通过")
    except ImportError:
        logger.error("requests库未安装，请运行: pip install requests")
        return False
    
    try:
        import dotenv
        logger.info("python-dotenv配置库检查通过")
    except ImportError:
        logger.error("python-dotenv库未安装，请运行: pip install python-dotenv")
        return False
    
    # 检查可选依赖
    try:
        import tkcalendar
        logger.info("tkcalendar日期选择器检查通过")
    except ImportError:
        logger.warning("tkcalendar库未安装，将使用文本输入框代替日期选择器")
        logger.info("建议安装: pip install tkcalendar")
    
    return True

def main():
    """主函数"""
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("🐔 离职员工剩余年假计算器启动中...")
    logger.info("=" * 60)
    
    try:
        # 检查运行环境
        if not check_environment():
            logger.error("环境检查失败，程序退出")
            input("按回车键退出...")
            sys.exit(1)
        
        logger.info("环境检查通过，正在启动GUI界面...")
        
        # 导入并启动GUI
        from gui.main_window import MainWindow
        
        # 创建并运行主窗口
        app = MainWindow()
        logger.info("GUI界面已创建，开始运行...")
        
        app.run()
        
        logger.info("程序正常退出")
        
    except ImportError as e:
        error_msg = f"模块导入失败: {e}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        print("请检查依赖是否正确安装:")
        print("pip install -r requirements.txt")
        input("\n按回车键退出...")
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"程序运行时发生未知错误: {e}"
        logger.error(error_msg, exc_info=True)
        print(f"\n❌ {error_msg}")
        print("详细错误信息请查看日志文件")
        input("\n按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
测试运行脚本
提供便捷的测试执行和报告生成功能
"""
import os
import sys
import subprocess
import argparse
import time
from pathlib import Path


def run_command(cmd, description=""):
    """运行命令并处理结果"""
    print(f"\n{'='*60}")
    print(f"执行: {description or cmd}")
    print(f"{'='*60}")
    
    start_time = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    end_time = time.time()
    
    print(f"执行时间: {end_time - start_time:.2f}秒")
    
    if result.stdout:
        print("输出:")
        print(result.stdout)
    
    if result.stderr:
        print("错误:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"命令执行失败，退出码: {result.returncode}")
        return False
    
    return True


def check_dependencies():
    """检查测试依赖"""
    print("检查测试依赖...")
    
    required_packages = [
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'pytest-xdist',  # 并行测试
        'pytest-timeout',  # 超时控制
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少以下测试依赖: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("所有测试依赖已安装 ✓")
    return True


def run_unit_tests():
    """运行单元测试"""
    cmd = "python -m pytest tests/test_models.py tests/test_leave_calculator.py tests/test_services.py -v --tb=short"
    return run_command(cmd, "单元测试")


def run_integration_tests():
    """运行集成测试"""
    cmd = "python -m pytest tests/test_integration.py tests/test_controller.py -v --tb=short"
    return run_command(cmd, "集成测试")


def run_gui_tests():
    """运行GUI测试"""
    cmd = "python -m pytest tests/test_gui.py -v --tb=short"
    return run_command(cmd, "GUI测试")


def run_e2e_tests():
    """运行端到端测试"""
    cmd = "python -m pytest tests/test_e2e.py -v --tb=short"
    return run_command(cmd, "端到端测试")


def run_performance_tests():
    """运行性能测试"""
    cmd = "python -m pytest tests/test_performance.py -v --tb=short -m performance"
    return run_command(cmd, "性能测试")


def run_all_tests():
    """运行所有测试"""
    cmd = "python -m pytest tests/ -v --tb=short"
    return run_command(cmd, "所有测试")


def run_tests_with_coverage():
    """运行测试并生成覆盖率报告"""
    cmd = "python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing --cov-report=xml --cov-fail-under=80"
    return run_command(cmd, "测试覆盖率分析")


def run_smoke_tests():
    """运行冒烟测试"""
    cmd = "python -m pytest tests/ -m smoke -v --tb=short"
    return run_command(cmd, "冒烟测试")


def run_parallel_tests():
    """运行并行测试"""
    cmd = "python -m pytest tests/ -n auto -v --tb=short"
    return run_command(cmd, "并行测试")


def generate_test_report():
    """生成测试报告"""
    print("\n生成测试报告...")
    
    # 生成HTML覆盖率报告
    if os.path.exists("htmlcov"):
        print("HTML覆盖率报告已生成: htmlcov/index.html")
    
    # 生成XML覆盖率报告
    if os.path.exists("coverage.xml"):
        print("XML覆盖率报告已生成: coverage.xml")
    
    # 生成pytest报告
    cmd = "python -m pytest tests/ --html=test_report.html --self-contained-html"
    if run_command(cmd, "生成HTML测试报告"):
        print("HTML测试报告已生成: test_report.html")


def clean_test_artifacts():
    """清理测试产物"""
    print("清理测试产物...")
    
    artifacts = [
        ".pytest_cache",
        "htmlcov",
        "coverage.xml",
        ".coverage",
        "test_report.html",
        "tests/pytest.log",
        "__pycache__",
        "src/__pycache__",
        "tests/__pycache__",
    ]
    
    for artifact in artifacts:
        if os.path.exists(artifact):
            if os.path.isdir(artifact):
                import shutil
                shutil.rmtree(artifact)
                print(f"删除目录: {artifact}")
            else:
                os.remove(artifact)
                print(f"删除文件: {artifact}")
    
    # 递归删除__pycache__目录
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                import shutil
                shutil.rmtree(dir_path)
                print(f"删除缓存目录: {dir_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="离职年假计算器测试运行脚本")
    parser.add_argument("--type", choices=[
        "unit", "integration", "gui", "e2e", "performance", 
        "all", "coverage", "smoke", "parallel"
    ], default="all", help="测试类型")
    parser.add_argument("--clean", action="store_true", help="清理测试产物")
    parser.add_argument("--report", action="store_true", help="生成测试报告")
    parser.add_argument("--check-deps", action="store_true", help="检查测试依赖")
    
    args = parser.parse_args()
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 检查是否在项目根目录
    if not os.path.exists("src") or not os.path.exists("tests"):
        print("错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 清理测试产物
    if args.clean:
        clean_test_artifacts()
        return
    
    # 检查依赖
    if args.check_deps:
        if not check_dependencies():
            sys.exit(1)
        return
    
    # 检查测试依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    
    # 运行测试
    success = True
    
    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "integration":
        success = run_integration_tests()
    elif args.type == "gui":
        success = run_gui_tests()
    elif args.type == "e2e":
        success = run_e2e_tests()
    elif args.type == "performance":
        success = run_performance_tests()
    elif args.type == "coverage":
        success = run_tests_with_coverage()
    elif args.type == "smoke":
        success = run_smoke_tests()
    elif args.type == "parallel":
        success = run_parallel_tests()
    elif args.type == "all":
        success = run_all_tests()
    
    # 生成报告
    if args.report and success:
        generate_test_report()
    
    # 输出结果
    if success:
        print(f"\n{'='*60}")
        print("✅ 测试执行成功!")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("❌ 测试执行失败!")
        print(f"{'='*60}")
        sys.exit(1)


if __name__ == "__main__":
    main()
# 技术栈选择 - 离职员工剩余年假计算程序

## 1. 技术栈概览

### 1.1 核心技术选择

| 技术领域 | 选择方案 | 版本要求 | 选择理由 |
|----------|----------|----------|----------|
| **编程语言** | Python | 3.8+ | 跨平台、丰富生态、快速开发 |
| **GUI框架** | tkinter | 内置 | 无额外依赖、轻量级、稳定 |
| **HTTP客户端** | requests | 2.28+ | 简单易用、功能完善、社区支持好 |
| **配置管理** | python-dotenv | 1.0+ | 环境变量管理、安全性好 |
| **日期处理** | datetime | 内置 | 标准库、功能完整 |
| **数据验证** | dataclasses | 内置 | 类型安全、代码简洁 |
| **日志记录** | logging | 内置 | 标准库、功能强大 |
| **测试框架** | pytest | 7.0+ | 功能丰富、插件生态好 |

### 1.2 架构模式
- **设计模式**: MVC (Model-View-Controller)
- **架构风格**: 分层架构 (Layered Architecture)
- **错误处理**: 异常链模式
- **配置管理**: 环境变量 + 配置类

## 2. 详细技术选择分析

### 2.1 GUI框架选择

#### 选择：tkinter
**优势**:
- ✅ Python内置，无需额外安装
- ✅ 跨平台支持（Windows/macOS/Linux）
- ✅ 学习成本低，文档完善
- ✅ 适合简单桌面应用
- ✅ 稳定性好，兼容性强

**劣势**:
- ❌ 界面美观度一般
- ❌ 现代UI组件有限
- ❌ 自定义样式能力弱

**替代方案对比**:
```python
# tkinter - 选择方案
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# PyQt5/6 - 备选方案
# 优势: 界面美观、功能强大
# 劣势: 许可证复杂、打包体积大、学习成本高

# Kivy - 备选方案  
# 优势: 现代化、触摸支持
# 劣势: 桌面应用不是主要场景、学习成本高
```

### 2.2 HTTP客户端选择

#### 选择：requests
**优势**:
- ✅ API设计优雅，使用简单
- ✅ 功能完整（认证、会话、重试等）
- ✅ 社区支持好，文档详细
- ✅ 错误处理机制完善

**实现示例**:
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.timeout = timeout
```

### 2.3 配置管理选择

#### 选择：python-dotenv + dataclasses
**优势**:
- ✅ 环境变量管理标准化
- ✅ 敏感信息安全存储
- ✅ 类型安全的配置类
- ✅ 开发/生产环境隔离

**实现示例**:
```python
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class WeChatConfig:
    corp_id: str
    corp_secret: str
    agent_id: str
    base_url: str = "https://qyapi.weixin.qq.com"
    timeout: int = 30
    retry_count: int = 3
    
    @classmethod
    def from_env(cls) -> 'WeChatConfig':
        return cls(
            corp_id=os.getenv("WECHAT_CORP_ID"),
            corp_secret=os.getenv("WECHAT_CORP_SECRET"),
            agent_id=os.getenv("WECHAT_AGENT_ID"),
            timeout=int(os.getenv("API_TIMEOUT", "30")),
            retry_count=int(os.getenv("API_RETRY_COUNT", "3"))
        )
```

### 2.4 数据处理选择

#### 日期处理：datetime + dateutil
```python
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class DateService:
    @staticmethod
    def parse_date(date_str: str) -> date:
        """解析日期字符串"""
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    
    @staticmethod
    def get_year_days(year: int) -> int:
        """获取年份总天数"""
        return 366 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 365
    
    @staticmethod
    def days_from_year_start(target_date: date) -> int:
        """计算从年初到指定日期的天数"""
        year_start = date(target_date.year, 1, 1)
        return (target_date - year_start).days + 1
```

#### 数据验证：dataclasses + typing
```python
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str] = None
    
@dataclass
class CalculationInput:
    employee_name: str
    resignation_date: date
    
    def validate(self) -> ValidationResult:
        if not self.employee_name.strip():
            return ValidationResult(False, "员工姓名不能为空")
        
        if self.resignation_date > date.today():
            return ValidationResult(False, "离职日期不能超过当前日期")
        
        return ValidationResult(True)
```

## 3. 依赖管理

### 3.1 核心依赖

```txt
# requirements.txt
requests>=2.28.0,<3.0.0
python-dotenv>=1.0.0,<2.0.0
tkcalendar>=1.6.0,<2.0.0

# 开发依赖
pytest>=7.0.0,<8.0.0
pytest-cov>=4.0.0,<5.0.0
black>=22.0.0,<24.0.0
flake8>=5.0.0,<7.0.0
mypy>=1.0.0,<2.0.0

# 打包依赖
pyinstaller>=5.0.0,<6.0.0
```

### 3.2 版本锁定策略

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="annual-leave-calculator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0,<3.0.0",
        "python-dotenv>=1.0.0,<2.0.0", 
        "tkcalendar>=1.6.0,<2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pytest-cov>=4.0.0,<5.0.0",
            "black>=22.0.0,<24.0.0",
            "flake8>=5.0.0,<7.0.0",
            "mypy>=1.0.0,<2.0.0",
        ],
        "build": [
            "pyinstaller>=5.0.0,<6.0.0",
        ]
    }
)
```

## 4. 开发工具链

### 4.1 代码质量工具

```yaml
# .github/workflows/quality.yml
name: Code Quality
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          pip install -e .[dev]
      
      - name: Code formatting check
        run: black --check src tests
      
      - name: Linting
        run: flake8 src tests
      
      - name: Type checking
        run: mypy src
      
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
```

### 4.2 开发环境配置

```python
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.mypy_cache
  | \.pytest_cache
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

## 5. 部署和分发

### 5.1 打包策略

#### 选择：PyInstaller
**优势**:
- ✅ 生成独立可执行文件
- ✅ 跨平台支持
- ✅ 自动处理依赖
- ✅ 支持图标和版本信息

```python
# build.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config/.env.template', 'config'),
        ('docs/*.md', 'docs'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='annual_leave_calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'
)
```

### 5.2 构建脚本

```bash
#!/bin/bash
# build.sh

echo "开始构建年假计算程序..."

# 清理旧的构建文件
rm -rf build/ dist/

# 安装依赖
pip install -e .[build]

# 运行测试
pytest

# 构建可执行文件
pyinstaller build.spec

# 复制配置文件
cp config/.env.template dist/

echo "构建完成！可执行文件位于 dist/ 目录"
```

## 6. 性能考虑

### 6.1 启动性能
- 延迟导入非核心模块
- 最小化启动时的网络请求
- 使用轻量级GUI组件

### 6.2 运行时性能
- API响应缓存
- 连接池复用
- 异步UI更新

```python
import threading
from concurrent.futures import ThreadPoolExecutor

class AsyncAPIService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    def fetch_leave_data_async(self, employee_name: str, callback):
        """异步获取假期数据"""
        future = self.executor.submit(self._fetch_leave_data, employee_name)
        future.add_done_callback(lambda f: callback(f.result()))
```

## 7. 安全考虑

### 7.1 依赖安全
- 定期更新依赖版本
- 使用安全扫描工具
- 锁定依赖版本范围

### 7.2 代码安全
- 输入验证和清理
- 敏感信息不硬编码
- 错误信息不泄露敏感数据

```python
# 安全的配置加载
class SecureConfig:
    @staticmethod
    def load_config() -> WeChatConfig:
        config = WeChatConfig.from_env()
        
        # 验证必要字段
        if not all([config.corp_id, config.corp_secret]):
            raise ConfigError("缺少必要的企业微信配置")
        
        # 清理敏感信息的日志输出
        logger.info(f"加载配置完成，企业ID: {config.corp_id[:8]}***")
        
        return config
```

## 8. 扩展性设计

### 8.1 插件架构预留
```python
from abc import ABC, abstractmethod

class CalculatorPlugin(ABC):
    @abstractmethod
    def calculate(self, input_data: dict) -> float:
        pass

class StandardCalculator(CalculatorPlugin):
    def calculate(self, input_data: dict) -> float:
        # 标准计算逻辑
        pass

class CustomCalculator(CalculatorPlugin):
    def calculate(self, input_data: dict) -> float:
        # 自定义计算逻辑
        pass
```

### 8.2 配置化设计
```python
@dataclass
class CalculationConfig:
    algorithm_type: str = "standard"
    working_days_per_year: int = 365
    annual_leave_base_hours: int = 120
    calculation_precision: int = 2
```

这个技术栈选择确保了项目的可维护性、扩展性和稳定性，同时保持了开发的简单性和部署的便利性。🚀⚙️
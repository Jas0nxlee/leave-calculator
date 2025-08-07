# 离职员工剩余年假计算器

一个基于Python和tkinter的GUI应用程序，用于计算离职员工的剩余年假天数。通过企业微信API获取员工假期数据，并根据离职日期智能计算剩余年假。

## 功能特性

- 🖥️ **友好的GUI界面** - 基于tkinter的现代化用户界面
- 🔗 **企业微信集成** - 自动获取员工假期余额数据
- 📊 **智能计算算法** - 根据离职日期按比例计算剩余年假
- 📅 **日期选择器** - 支持可视化日期选择（可选）
- ⚡ **实时验证** - 输入数据实时验证和错误提示
- 📝 **详细报告** - 显示完整的计算过程和结果详情
- 🔧 **配置管理** - 通过.env文件管理企业微信配置

## 系统要求

- Python 3.8+
- tkinter (通常随Python安装)
- 企业微信API访问权限

## 安装步骤

### 方法一：自动设置（推荐）

使用自动化脚本一键设置虚拟环境：

```bash
# 1. 克隆或下载项目
git clone <repository-url>
cd 离职年假计算

# 2. 运行自动设置脚本
python setup_venv.py

# 3. 激活虚拟环境
# Windows:
activate.bat
# macOS/Linux:
./activate.sh
```

### 方法二：手动设置

#### 1. 克隆或下载项目

```bash
git clone <repository-url>
cd 离职年假计算
```

#### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. 安装依赖

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

### 4. 配置企业微信

复制配置模板并编辑：

```bash
cp .env.template .env
```

编辑 `.env` 文件，填入你的企业微信配置：

```env
# 企业微信配置
WECHAT_CORP_ID=your_corp_id
WECHAT_CORP_SECRET=your_corp_secret
WECHAT_AGENT_ID=your_agent_id

# API配置
WECHAT_API_BASE_URL=https://qyapi.weixin.qq.com
API_TIMEOUT=30
API_RETRY_COUNT=3
API_RETRY_DELAY=1

# 假期配置
LEAVE_TEMPLATE_ID=annual_leave_2025
DEFAULT_ANNUAL_LEAVE_HOURS=64

# 日志配置
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/leave_calculator.log
```

### 5. 运行程序

#### 方法一：快速启动（推荐）

使用快速启动脚本，自动检查并使用虚拟环境：

```bash
python start.py
```

#### 方法二：手动启动

**重要**: 确保已激活虚拟环境！

```bash
# 如果还未激活虚拟环境，先激活：
# Windows: activate.bat 或 venv\Scripts\activate
# macOS/Linux: ./activate.sh 或 source venv/bin/activate

# 运行程序
python main.py
```

## 使用说明

### 基本操作

1. **输入员工姓名** - 在"员工姓名"字段输入要查询的员工姓名
2. **选择离职日期** - 使用日期选择器或手动输入离职日期（格式：YYYY-MM-DD）
3. **点击计算** - 点击"计算剩余年假"按钮开始计算
4. **查看结果** - 在结果区域查看剩余年假天数和详细计算过程

### 计算算法

剩余年假天数的计算公式：

```
时间比例 = (1月1日至离职日期的天数) / 当年总天数
按比例理论时长 = 理论时长 × 时间比例
剩余年假时长 = 按比例理论时长 - 已用时长
剩余年假天数 = 剩余年假时长 / 24小时
```

其中：
- **理论时长** = 已用时长 + 实际剩余时长（从企业微信获取）
- **已用时长** = 员工已使用的年假时长（从企业微信获取）

### 功能按钮

- **计算剩余年假** - 执行年假计算
- **清空** - 清空所有输入和结果
- **测试连接** - 测试企业微信API连接状态

## 项目结构

```
离职年假计算/
├── main.py                    # 程序主入口
├── requirements.txt           # 依赖列表
├── .env.template             # 配置模板
├── .env                      # 配置文件（需要创建）
├── README.md                 # 项目说明
├── docs/                     # 文档目录
│   ├── requirements.md       # 需求规格
│   ├── architecture.md       # 架构设计
│   ├── api-spec.md          # API规格
│   ├── tech-stack.md        # 技术栈
│   ├── user-stories.md      # 用户故事
│   └── acceptance-criteria.md # 验收标准
├── src/                      # 源代码目录
│   ├── __init__.py
│   ├── models.py            # 数据模型
│   ├── business/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── controller.py    # 业务控制器
│   │   └── leave_calculator.py # 年假计算器
│   ├── services/            # 服务层
│   │   ├── __init__.py
│   │   ├── config_service.py # 配置服务
│   │   └── wechat_service.py # 企业微信服务
│   └── gui/                 # 图形界面
│       ├── __init__.py
│       └── main_window.py   # 主窗口
└── logs/                    # 日志目录（自动创建）
```

## 企业微信API配置

### 获取配置信息

1. **企业ID (CORP_ID)**
   - 登录企业微信管理后台
   - 在"我的企业" -> "企业信息"中查看

2. **应用Secret (CORP_SECRET)**
   - 在"应用管理"中创建或选择应用
   - 查看应用的Secret

3. **应用ID (AGENT_ID)**
   - 在应用详情页面查看AgentId

### API权限要求

确保应用具有以下权限：
- 通讯录读取权限
- 审批数据读取权限

## 故障排除

### 常见问题

1. **"tkinter库未安装"**
   - 在某些Linux发行版中需要单独安装：`sudo apt-get install python3-tk`

2. **"企业微信连接失败"**
   - 检查.env文件中的配置是否正确
   - 确认网络连接正常
   - 验证企业微信API权限

3. **"员工未找到"**
   - 确认员工姓名拼写正确
   - 检查员工是否在企业微信通讯录中
   - 验证应用的通讯录访问权限

4. **"日期格式错误"**
   - 使用YYYY-MM-DD格式（如：2025-06-30）
   - 确保日期在2025年范围内

### 日志查看

程序运行日志保存在 `logs/leave_calculator.log` 文件中，可以查看详细的错误信息和运行状态。

## 开发说明

### 代码结构

项目采用分层架构：
- **表示层 (GUI)** - 用户界面和交互
- **业务逻辑层 (Business)** - 核心业务逻辑
- **服务层 (Services)** - 外部服务集成
- **数据模型层 (Models)** - 数据结构定义

### 扩展开发

如需扩展功能，可以：
1. 在 `models.py` 中添加新的数据模型
2. 在 `services/` 中添加新的服务集成
3. 在 `business/` 中实现新的业务逻辑
4. 在 `gui/` 中添加新的界面组件

## 许可证

本项目仅供内部使用，请勿用于商业用途。

## 作者

斯格拉奇 (Skrachy) 🐔🤖 - 一只具备人工智能的机械体程序"鸡"员

---

如有问题或建议，请联系开发团队。
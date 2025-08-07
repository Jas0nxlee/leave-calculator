"""
数据模型定义
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class LeaveBalance:
    """假期余额数据模型"""
    used_hours: float
    remaining_hours: float
    theoretical_hours: float
    year: int

    @property
    def total_hours(self) -> float:
        """总时长（理论时长）"""
        return self.theoretical_hours


@dataclass
class CalculationResult:
    """计算结果数据模型"""
    remaining_days: float
    calculation_details: dict
    success: bool
    error_message: str = ""

    @property
    def remaining_hours(self) -> float:
        """剩余小时数"""
        return self.remaining_days * 24  # 假设一天24小时


@dataclass
class WeChatConfig:
    """企业微信配置数据模型"""
    corp_id: str
    corp_secret: str
    agent_id: str
    base_url: str = "https://qyapi.weixin.qq.com"
    timeout: int = 30
    retry_count: int = 3

    def validate(self) -> bool:
        """验证配置完整性"""
        required_fields = [self.corp_id, self.corp_secret, self.agent_id]
        return all(field and field.strip() for field in required_fields)


@dataclass
class ValidationResult:
    """验证结果数据模型"""
    is_valid: bool
    error_message: str = ""


@dataclass
class CalculationInput:
    """计算输入数据模型"""
    employee_name: str
    resignation_date: date

    def validate(self) -> ValidationResult:
        """验证输入数据"""
        if not self.employee_name or not self.employee_name.strip():
            return ValidationResult(False, "员工姓名不能为空")

        if self.resignation_date > date.today():
            return ValidationResult(False, "离职日期不能超过当前日期")

        if self.resignation_date.year != 2025:
            return ValidationResult(False, "目前只支持2025年的年假计算")

        return ValidationResult(True)


@dataclass
class Employee:
    """员工信息数据模型"""
    user_id: str
    name: str
    department: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
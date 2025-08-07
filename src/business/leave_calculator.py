"""
年假计算业务逻辑模块
"""
import logging
from datetime import date, datetime
from typing import Dict, Any

from models import LeaveBalance, CalculationResult, CalculationInput


class LeaveCalculator:
    """年假计算器"""

    def __init__(self):
        """初始化年假计算器"""
        self.logger = logging.getLogger(__name__)

    def calculate_remaining_leave(
        self,
        leave_balance: LeaveBalance,
        resignation_date: date
    ) -> CalculationResult:
        """
        计算剩余年假天数
        
        算法：
        1. 理论时长 = 已用时长 + 实际剩余时长
        2. 时间比例 = (当年1月1日至离职日期天数) / 当年总天数
        3. 剩余年假 = 理论时长 × 时间比例 - 已用时长
        
        Args:
            leave_balance: 假期余额信息
            resignation_date: 离职日期
            
        Returns:
            CalculationResult: 计算结果
        """
        try:
            # 计算时间比例
            time_ratio = self.calculate_time_ratio(resignation_date)
            
            # 计算应得年假时长
            entitled_hours = leave_balance.theoretical_hours * time_ratio
            
            # 计算剩余年假时长
            remaining_hours = entitled_hours - leave_balance.used_hours
            
            # 确保结果不为负数
            remaining_hours = max(0, remaining_hours)
            
            # 转换为天数（假设每天24小时）
            remaining_days = remaining_hours / 24
            
            # 保留2位小数
            remaining_days = round(remaining_days, 2)
            
            # 构建详细计算信息
            calculation_details = {
                "theoretical_hours": leave_balance.theoretical_hours,
                "used_hours": leave_balance.used_hours,
                "remaining_hours_before_calc": leave_balance.remaining_hours,
                "resignation_date": resignation_date.strftime("%Y-%m-%d"),
                "time_ratio": round(time_ratio, 4),
                "entitled_hours": round(entitled_hours, 2),
                "final_remaining_hours": round(remaining_hours, 2),
                "final_remaining_days": remaining_days,
                "calculation_formula": (
                    f"剩余年假 = ({leave_balance.theoretical_hours} × {time_ratio:.4f}) - {leave_balance.used_hours} "
                    f"= {entitled_hours:.2f} - {leave_balance.used_hours} = {remaining_hours:.2f}小时 = {remaining_days}天"
                )
            }
            
            self.logger.info(f"年假计算完成: {remaining_days}天")
            
            return CalculationResult(
                remaining_days=remaining_days,
                calculation_details=calculation_details,
                success=True
            )
            
        except Exception as e:
            error_msg = f"年假计算失败: {str(e)}"
            self.logger.error(error_msg)
            
            return CalculationResult(
                remaining_days=0.0,
                calculation_details={},
                success=False,
                error_message=error_msg
            )

    def calculate_time_ratio(self, resignation_date: date) -> float:
        """
        计算时间比例
        
        Args:
            resignation_date: 离职日期
            
        Returns:
            float: 时间比例 (0-1之间)
        """
        year = resignation_date.year
        
        # 计算年初到离职日期的天数
        year_start = date(year, 1, 1)
        days_worked = (resignation_date - year_start).days + 1  # 包含离职当天
        
        # 计算当年总天数
        total_days = self.get_year_total_days(year)
        
        # 计算比例
        ratio = days_worked / total_days
        
        self.logger.debug(f"时间比例计算: {days_worked}/{total_days} = {ratio:.4f}")
        
        return ratio

    def get_year_total_days(self, year: int) -> int:
        """
        获取指定年份的总天数
        
        Args:
            year: 年份
            
        Returns:
            int: 总天数
        """
        if self.is_leap_year(year):
            return 366
        else:
            return 365

    def is_leap_year(self, year: int) -> bool:
        """
        判断是否为闰年
        
        Args:
            year: 年份
            
        Returns:
            bool: 是否为闰年
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def get_days_from_year_start(self, target_date: date) -> int:
        """
        计算从年初到指定日期的天数
        
        Args:
            target_date: 目标日期
            
        Returns:
            int: 天数
        """
        year_start = date(target_date.year, 1, 1)
        return (target_date - year_start).days + 1

    def validate_calculation_input(self, input_data: CalculationInput) -> bool:
        """
        验证计算输入数据
        
        Args:
            input_data: 输入数据
            
        Returns:
            bool: 是否有效
        """
        validation_result = input_data.validate()
        if not validation_result.is_valid:
            self.logger.warning(f"输入数据验证失败: {validation_result.error_message}")
            return False
        
        return True

    def get_calculation_summary(self, result: CalculationResult) -> str:
        """
        获取计算结果摘要
        
        Args:
            result: 计算结果
            
        Returns:
            str: 结果摘要
        """
        if not result.success:
            return f"计算失败: {result.error_message}"
        
        details = result.calculation_details
        return (
            f"剩余年假: {result.remaining_days}天\n"
            f"理论时长: {details.get('theoretical_hours', 0)}小时\n"
            f"已用时长: {details.get('used_hours', 0)}小时\n"
            f"时间比例: {details.get('time_ratio', 0):.2%}\n"
            f"计算公式: {details.get('calculation_formula', '')}"
        )
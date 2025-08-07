"""
业务控制器模块
"""
import logging
from datetime import datetime
from typing import Optional

from models import CalculationInput, CalculationResult, ValidationResult
from services.wechat_service import WeChatWorkService, WeChatAPIError, EmployeeNotFoundError
from services.config_service import ConfigService
from .leave_calculator import LeaveCalculator


class BusinessController:
    """业务流程控制器"""

    def __init__(self):
        """初始化业务控制器"""
        self.logger = logging.getLogger(__name__)
        self.config_service = ConfigService()
        self.calculator = LeaveCalculator()
        self._wechat_service: Optional[WeChatWorkService] = None

    @property
    def wechat_service(self) -> WeChatWorkService:
        """获取企业微信服务实例（懒加载）"""
        if self._wechat_service is None:
            self._wechat_service = WeChatWorkService(self.config_service)
        return self._wechat_service

    def process_leave_calculation(self, employee_name: str, resignation_date_str: str) -> CalculationResult:
        """
        处理年假计算流程
        
        Args:
            employee_name: 员工姓名
            resignation_date_str: 离职日期字符串 (YYYY-MM-DD)
            
        Returns:
            CalculationResult: 计算结果
        """
        try:
            # 1. 验证和解析输入数据
            validation_result = self._validate_input(employee_name, resignation_date_str)
            if not validation_result.is_valid:
                return CalculationResult(
                    remaining_days=0.0,
                    calculation_details={},
                    success=False,
                    error_message=validation_result.error_message
                )

            resignation_date = datetime.strptime(resignation_date_str, "%Y-%m-%d").date()
            calculation_input = CalculationInput(
                employee_name=employee_name.strip(),
                resignation_date=resignation_date
            )

            # 2. 验证业务规则
            input_validation = calculation_input.validate()
            if not input_validation.is_valid:
                return CalculationResult(
                    remaining_days=0.0,
                    calculation_details={},
                    success=False,
                    error_message=input_validation.error_message
                )

            # 3. 查找员工信息
            self.logger.info(f"开始处理员工 {employee_name} 的年假计算")
            
            try:
                employee = self.wechat_service.find_employee_by_name(employee_name)
                self.logger.info(f"找到员工: {employee.name} (ID: {employee.user_id})")
            except EmployeeNotFoundError as e:
                return CalculationResult(
                    remaining_days=0.0,
                    calculation_details={},
                    success=False,
                    error_message=f"未找到员工 '{employee_name}'，请检查姓名是否正确"
                )

            # 4. 获取假期余额
            try:
                leave_balance = self.wechat_service.get_leave_balance(employee, 2025)
                self.logger.info(f"获取到假期余额: 理论{leave_balance.theoretical_hours}h, "
                               f"已用{leave_balance.used_hours}h, 剩余{leave_balance.remaining_hours}h")
            except WeChatAPIError as e:
                return CalculationResult(
                    remaining_days=0.0,
                    calculation_details={},
                    success=False,
                    error_message=f"获取假期余额失败: {e.errmsg}"
                )

            # 5. 计算剩余年假
            result = self.calculator.calculate_remaining_leave(leave_balance, resignation_date)
            
            if result.success:
                self.logger.info(f"年假计算完成: {result.remaining_days}天")
            else:
                self.logger.error(f"年假计算失败: {result.error_message}")

            return result

        except ValueError as e:
            error_msg = f"日期格式错误: {str(e)}"
            self.logger.error(error_msg)
            return CalculationResult(
                remaining_days=0.0,
                calculation_details={},
                success=False,
                error_message=error_msg
            )
        except Exception as e:
            error_msg = f"处理过程中发生未知错误: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return CalculationResult(
                remaining_days=0.0,
                calculation_details={},
                success=False,
                error_message=error_msg
            )

    def _validate_input(self, employee_name: str, resignation_date_str: str) -> ValidationResult:
        """
        验证输入数据
        
        Args:
            employee_name: 员工姓名
            resignation_date_str: 离职日期字符串
            
        Returns:
            ValidationResult: 验证结果
        """
        # 验证员工姓名
        if not employee_name or not employee_name.strip():
            return ValidationResult(False, "员工姓名不能为空")

        # 验证日期格式
        if not resignation_date_str or not resignation_date_str.strip():
            return ValidationResult(False, "离职日期不能为空")

        try:
            datetime.strptime(resignation_date_str, "%Y-%m-%d")
        except ValueError:
            return ValidationResult(False, "日期格式错误，请使用 YYYY-MM-DD 格式")

        return ValidationResult(True)

    def test_wechat_connection(self) -> tuple[bool, str]:
        """
        测试企业微信连接
        
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        try:
            if self.wechat_service.test_connection():
                return True, "企业微信连接测试成功"
            else:
                return False, "企业微信连接测试失败"
        except Exception as e:
            return False, f"企业微信连接测试失败: {str(e)}"

    def get_config_status(self) -> dict:
        """
        获取配置状态
        
        Returns:
            dict: 配置状态信息
        """
        return self.config_service.get_config_status()

    def handle_api_error(self, error: WeChatAPIError) -> str:
        """
        处理API错误，返回用户友好的错误信息
        
        Args:
            error: API错误
            
        Returns:
            str: 用户友好的错误信息
        """
        error_messages = {
            40001: "企业微信配置错误，请检查企业ID和密钥",
            40014: "访问令牌无效，请检查企业微信配置",
            42001: "访问令牌已过期，正在重新获取",
            60011: "员工不存在，请检查员工姓名",
            60020: "部门不存在，请联系管理员检查配置"
        }
        
        user_message = error_messages.get(error.errcode, f"企业微信API错误: {error.errmsg}")
        self.logger.error(f"API错误 [{error.errcode}]: {error.errmsg}")
        
        return user_message

    def get_calculation_history(self) -> list:
        """
        获取计算历史记录（预留接口）
        
        Returns:
            list: 历史记录列表
        """
        # 这里可以实现计算历史记录的存储和检索
        # 例如存储到本地文件或数据库
        return []

    def export_calculation_result(self, result: CalculationResult, employee_name: str) -> str:
        """
        导出计算结果（预留接口）
        
        Args:
            result: 计算结果
            employee_name: 员工姓名
            
        Returns:
            str: 导出文件路径
        """
        # 这里可以实现结果导出功能
        # 例如导出为Excel或PDF文件
        return ""
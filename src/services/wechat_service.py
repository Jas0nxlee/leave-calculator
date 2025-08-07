"""
企业微信API服务模块
"""
import time
import logging
import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from models import WeChatConfig, LeaveBalance, Employee


class WeChatAPIError(Exception):
    """企业微信API异常"""
    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"企业微信API错误 [{errcode}]: {errmsg}")


class TokenExpiredError(WeChatAPIError):
    """Token过期异常"""
    pass


class EmployeeNotFoundError(WeChatAPIError):
    """员工未找到异常"""
    pass


class WeChatWorkService:
    """企业微信API服务"""

    def __init__(self, config_service: 'ConfigService'):
        """
        初始化企业微信服务
        
        Args:
            config_service: 配置服务实例
        """
        self.config = config_service.get_wechat_config()
        self.annual_leave_config = config_service.get_annual_leave_config()
        self.logger = logging.getLogger(__name__)
        self._access_token = None
        self._token_expires_at = None
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        """创建HTTP会话"""
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.config.retry_count,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.timeout = self.config.timeout
        
        return session

    def _handle_api_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理API响应"""
        errcode = response_data.get("errcode", -1)
        errmsg = response_data.get("errmsg", "未知错误")

        if errcode == 0:
            return response_data

        # Token相关错误
        if errcode in [40001, 40014, 42001]:
            self._access_token = None
            self._token_expires_at = None
            raise TokenExpiredError(errcode, errmsg)

        # 用户不存在
        if errcode == 60011:
            raise EmployeeNotFoundError(errcode, errmsg)

        # 其他错误
        raise WeChatAPIError(errcode, errmsg)

    def get_access_token(self) -> str:
        """
        获取访问令牌
        
        Returns:
            str: 访问令牌
            
        Raises:
            WeChatAPIError: API调用失败时抛出
        """
        # 检查缓存的token是否有效
        now = time.time()
        if (self._access_token and self._token_expires_at and 
            now < self._token_expires_at):
            return self._access_token

        # 获取新的token
        url = f"{self.config.base_url}/cgi-bin/gettoken"
        params = {
            "corpid": self.config.corp_id,
            "corpsecret": self.config.corp_secret
        }

        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            result = self._handle_api_response(data)
            
            self._access_token = result["access_token"]
            expires_in = result.get("expires_in", 7200)
            # 提前5分钟过期，避免边界情况
            self._token_expires_at = now + expires_in - 300
            
            self.logger.info("成功获取企业微信访问令牌")
            return self._access_token
            
        except requests.RequestException as e:
            self.logger.error(f"获取访问令牌网络请求失败: {str(e)}")
            raise WeChatAPIError(-1, f"网络请求失败: {str(e)}")

    def find_employee_by_name(self, name: str) -> Employee:
        """
        根据姓名查找员工信息
        
        Args:
            name: 员工姓名
            
        Returns:
            Employee: 员工信息对象
            
        Raises:
            EmployeeNotFoundError: 员工不存在时抛出
            WeChatAPIError: API调用失败时抛出
        """
        try:
            # 获取access_token
            self.logger.info(f"🔍 开始查找员工: {name}")
            self.logger.info("🔑 获取企业微信access_token...")
            access_token = self.get_access_token()
            self.logger.info(f"✅ 成功获取access_token: {access_token[:20]}...")
            
            # 构建请求URL
            url = f"{self.config.base_url}/cgi-bin/user/list"
            
            # 构建请求参数
            params = {
                "access_token": access_token,
                "department_id": 1,  # 根部门ID，获取所有用户
                "fetch_child": 1     # 递归获取子部门用户
            }
            
            self.logger.info(f"🌐 请求URL: {url}")
            self.logger.info(f"📋 请求参数: {params}")
            
            # 发送GET请求
            response = self._session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"📥 企业微信用户列表API完整响应: {data}")
            
            result = self._handle_api_response(data)
            
            # 查找员工
            userlist = result.get("userlist", [])
            self.logger.info(f"📊 获取到 {len(userlist)} 个用户")
            
            for i, user in enumerate(userlist):
                user_name = user.get("name", "")
                user_id = user.get("userid", "")
                self.logger.info(f"👤 用户 {i+1}: {user_name} (ID: {user_id})")
                
                if user_name == name:
                    self.logger.info(f"✅ 找到匹配员工: {user_name} (ID: {user_id})")
                    self.logger.info(f"📋 完整用户信息: {user}")
                    
                    return Employee(
                        user_id=user_id,
                        name=user_name,
                        department=user.get("department", [None])[0] if user.get("department") else None,
                        position=user.get("position"),
                        email=user.get("email")
                    )
            
            # 如果没有找到员工
            self.logger.error(f"❌ 未找到员工: {name}")
            raise EmployeeNotFoundError(60011, f"未找到员工: {name}")
            
        except requests.RequestException as e:
            self.logger.error(f"❌ 网络请求失败: {str(e)}")
            raise WeChatAPIError(-1, f"网络请求失败: {str(e)}")
        except Exception as e:
            self.logger.error(f"❌ 查找员工时发生未知错误: {str(e)}")
            raise WeChatAPIError(-1, f"查找员工失败: {str(e)}")

    def get_leave_balance(self, employee: Employee, year: int = 2025) -> LeaveBalance:
        """
        获取员工假期余额
        
        使用企业微信官方API: /cgi-bin/oa/vacation/getuservacationquota
        参考文档: https://developer.work.weixin.qq.com/document/path/93376
        
        Args:
            employee: 员工信息
            year: 年份
            
        Returns:
            LeaveBalance: 假期余额信息
            
        Raises:
            WeChatAPIError: API调用失败时抛出
        """
        # 正常模式：调用企业微信API
        try:
            # 获取access_token
            self.logger.info("=" * 80)
            self.logger.info(f"开始获取员工 {employee.name}({employee.user_id}) 的年假余额")
            self.logger.info("=" * 80)
            
            self.logger.info("🔑 开始获取企业微信access_token...")
            access_token = self.get_access_token()
            self.logger.info(f"✅ 成功获取access_token: {access_token[:20]}...{access_token[-10:]}")
            
            # 构建请求URL
            url = f"{self.config.base_url}/cgi-bin/oa/vacation/getuservacationquota"
            
            # 构建请求参数
            params = {
                "access_token": access_token
            }
            
            # 构建请求体
            data = {
                "userid": employee.user_id,
                "vacation_type": 1  # 1表示年假
            }
            
            self.logger.info(f"📡 准备调用企业微信年假API:")
            self.logger.info(f"   - 员工姓名: {employee.name}")
            self.logger.info(f"   - 员工ID: {employee.user_id}")
            self.logger.info(f"   - 查询年份: {year}")
            self.logger.info(f"   - URL: {url}")
            self.logger.info(f"   - 请求参数: {params}")
            self.logger.info(f"   - 请求体: {data}")
            
            # 发送POST请求
            self.logger.info("📡 发送POST请求到企业微信API...")
            response = self._session.post(url, params=params, json=data)
            
            self.logger.info(f"📥 收到HTTP响应:")
            self.logger.info(f"   - 状态码: {response.status_code}")
            self.logger.info(f"   - 响应头: {dict(response.headers)}")
            self.logger.info(f"   - 响应大小: {len(response.content)} 字节")
            
            response.raise_for_status()
            self.logger.info(f"✅ HTTP请求成功")
            
            # 解析JSON响应
            try:
                result = response.json()
                self.logger.info(f"📋 企业微信年假余额API完整响应:")
                self.logger.info(f"{result}")
            except Exception as json_error:
                self.logger.error(f"❌ JSON解析失败:")
                self.logger.error(f"   - 错误: {str(json_error)}")
                self.logger.error(f"   - 原始响应: {response.text}")
                raise WeChatAPIError(-1, f"API响应JSON解析失败: {str(json_error)}")
            
            api_result = self._handle_api_response(result)
            self.logger.info(f"🔍 API响应处理结果: {api_result}")
            
            # 获取假期数据
            lists = api_result.get("lists", [])
            self.logger.info(f"📊 解析假期数据列表:")
            self.logger.info(f"   - 假期类型总数: {len(lists)}")
            
            if not lists:
                self.logger.warning("⚠️  假期列表为空")
            
            # 详细显示每个假期类型
            self.logger.info("📝 所有假期类型详细信息:")
            for i, leave_item in enumerate(lists, 1):
                leave_name = leave_item.get("vacationname", "N/A")
                used = leave_item.get("usedduration", 0)
                left = leave_item.get("leftduration", 0)
                assigned = leave_item.get("assigned", 0)
                real_assigned = leave_item.get("real_assigned", 0)
                
                self.logger.info(f"   [{i}] 假期类型: {leave_name}")
                self.logger.info(f"       - ID: {leave_item.get('id', 'N/A')}")
                self.logger.info(f"       - usedduration: {used} 秒 ({used/3600:.2f} 小时)")
                self.logger.info(f"       - leftduration: {left} 秒 ({left/3600:.2f} 小时)")
                self.logger.info(f"       - assigned: {assigned} 秒 ({assigned/3600:.2f} 小时)")
                self.logger.info(f"       - real_assigned: {real_assigned} 秒 ({real_assigned/3600:.2f} 小时)")
                self.logger.info(f"       - vacationname: {leave_name}")
                self.logger.info(f"       - 总计时长: {used + left} 秒 ({(used + left)/3600:.2f} 小时)")
                self.logger.info(f"       - 原始数据: {leave_item}")
                self.logger.info("")
            
            if not lists:
                self.logger.warning(f"⚠️ 员工 {employee.name} 没有年假数据")
                # 使用默认配置
                default_hours = float(self.annual_leave_config['default_hours'])
                self.logger.info(f"🔧 使用默认配置: {default_hours}小时")
                return LeaveBalance(
                    used_hours=0.0,
                    remaining_hours=default_hours,
                    theoretical_hours=default_hours,
                    year=year
                )
            
            # 从配置中获取目标假期名称列表
            target_vacation_names = self.annual_leave_config.get('target_vacation_names', [])
            
            # 查找年假数据 - 直接使用环境变量中配置的假期名称进行精确匹配
            annual_leave_data = None
            
            self.logger.info(f"🔍 开始搜索年假数据:")
            self.logger.info(f"   - 目标假期名称: {target_vacation_names}")
            
            match_priority = "无"
            
            # 直接使用环境变量中的假期名称进行精确匹配
            for i, leave_item in enumerate(lists, 1):
                vacation_name = leave_item.get("vacationname", "")
                self.logger.info(f"     检查假期 [{i}]: {vacation_name}")
                
                # 检查是否与配置的目标假期名称完全匹配
                if vacation_name in target_vacation_names:
                    annual_leave_data = leave_item
                    match_priority = f"精确匹配 (目标假期: {vacation_name})"
                    self.logger.info(f"       ✅ 精确匹配成功! 假期名称: {vacation_name}")
                    break
                else:
                    self.logger.info(f"       ✗ 不匹配目标假期名称")
            
            if not annual_leave_data:
                self.logger.error(f"❌ 未找到年假数据:")
                self.logger.error(f"   - 搜索关键词: {annual_leave_keywords}")
                self.logger.error(f"   - 当前年份: {current_year}")
                self.logger.error(f"   - 可用假期类型: {[item.get('vacationname', 'N/A') for item in lists]}")
                self.logger.error(f"   - 假期类型详情:")
                for i, leave_item in enumerate(lists, 1):
                    leave_name = leave_item.get("vacationname", "N/A")
                    self.logger.error(f"     {i}. {leave_name}: ID={leave_item.get('id', 'N/A')}")
                raise WeChatAPIError(-1, f"员工 {employee.name} 没有年假数据")
            
            self.logger.info(f"✅ 找到年假数据:")
            self.logger.info(f"   - 假期名称: {annual_leave_data.get('vacationname')}")
            self.logger.info(f"   - 匹配优先级: {match_priority}")
            self.logger.info(f"   - 假期ID: {annual_leave_data.get('id')}")
            
            # 解析假期数据（企业微信返回的时长单位是秒）
            used_seconds = annual_leave_data.get("usedduration", 0)
            remaining_seconds = annual_leave_data.get("leftduration", 0)
            assigned_seconds = annual_leave_data.get("assigned", 0)
            real_assigned_seconds = annual_leave_data.get("real_assigned", 0)
            
            self.logger.info(f"📊 年假原始数据 (秒):")
            self.logger.info(f"   - 已使用时长: {used_seconds} 秒")
            self.logger.info(f"   - 剩余时长: {remaining_seconds} 秒")
            self.logger.info(f"   - 分配时长: {assigned_seconds} 秒")
            self.logger.info(f"   - 实际分配: {real_assigned_seconds} 秒")
            
            # 转换为小时（1小时 = 3600秒）
            used_hours = used_seconds / 3600.0
            remaining_hours = remaining_seconds / 3600.0
            assigned_hours = assigned_seconds / 3600.0
            real_assigned_hours = real_assigned_seconds / 3600.0
            
            # 计算理论总时长（根据企业微信API文档：理论时长 = 已使用 + 剩余）
            theoretical_hours = used_hours + remaining_hours
            
            self.logger.info(f"📊 年假转换数据 (小时):")
            self.logger.info(f"   - 已使用: {used_hours:.2f} 小时")
            self.logger.info(f"   - 剩余: {remaining_hours:.2f} 小时")
            self.logger.info(f"   - 分配时长: {assigned_hours:.2f} 小时")
            self.logger.info(f"   - 实际分配: {real_assigned_hours:.2f} 小时")
            self.logger.info(f"   - 理论总时长: {theoretical_hours:.2f} 小时")
            
            # 数据有效性检查
            self.logger.info(f"🔍 数据有效性检查:")
            self.logger.info(f"   - 理论总时长 > 0: {theoretical_hours > 0}")
            self.logger.info(f"   - 分配时长 > 0: {assigned_hours > 0}")
            self.logger.info(f"   - 实际分配 > 0: {real_assigned_hours > 0}")
            
            # 如果理论时长为0，显示详细的调试信息并报错
            if theoretical_hours <= 0 and assigned_hours <= 0 and real_assigned_hours <= 0:
                self.logger.error(f"❌ 年假数据异常 - 所有时长均为0:")
                self.logger.error(f"   - 理论总时长: {theoretical_hours:.2f} 小时")
                self.logger.error(f"   - 分配时长: {assigned_hours:.2f} 小时")
                self.logger.error(f"   - 实际分配: {real_assigned_hours:.2f} 小时")
                self.logger.error(f"   - 完整年假数据: {annual_leave_data}")
                self.logger.error(f"   - 所有假期汇总:")
                for i, leave_item in enumerate(lists, 1):
                    name = leave_item.get("vacationname", "N/A")
                    used = leave_item.get("usedduration", 0)
                    left = leave_item.get("leftduration", 0)
                    assigned = leave_item.get("assigned", 0)
                    self.logger.error(f"     {i}. {name}: 已用={used}秒, 剩余={left}秒, 分配={assigned}秒")
                
                # 不使用默认配置，直接报错
                raise WeChatAPIError(-1, f"员工 {employee.name} 在企业微信中没有年假数据")
            
            self.logger.info(f"✅ 年假数据有效，准备返回结果")
            self.logger.info("=" * 80)
            
            return LeaveBalance(
                used_hours=used_hours,
                remaining_hours=remaining_hours,
                theoretical_hours=theoretical_hours,
                year=year
            )
            
        except requests.RequestException as e:
            self.logger.error(f"❌ 网络请求异常:")
            self.logger.error(f"   - 异常类型: {type(e).__name__}")
            self.logger.error(f"   - 异常信息: {str(e)}")
            self.logger.error(f"   - 请求URL: {url if 'url' in locals() else 'N/A'}")
            self.logger.error(f"   - 请求参数: {params if 'params' in locals() else 'N/A'}")
            raise WeChatAPIError(-1, f"网络请求失败: {str(e)}")
        except Exception as e:
            self.logger.error(f"❌ 获取年假余额失败:")
            self.logger.error(f"   - 异常类型: {type(e).__name__}")
            self.logger.error(f"   - 异常信息: {str(e)}")
            self.logger.error(f"   - 员工姓名: {employee.name}")
            if isinstance(e, WeChatAPIError):
                raise
            raise WeChatAPIError(-1, f"解析假期余额数据失败: {str(e)}")

    def _get_approval_records(self, employee_id: str, year: int) -> list:
        """
        获取审批记录（示例方法）
        
        这是一个示例方法，展示如何通过审批记录计算假期余额
        实际使用时需要根据企业的审批模板ID和字段配置进行调整
        """
        access_token = self.get_access_token()
        url = f"{self.config.base_url}/cgi-bin/oa/getapprovaldata"
        
        # 计算查询时间范围（整年）
        start_time = int(time.mktime(time.strptime(f"{year}-01-01", "%Y-%m-%d")))
        end_time = int(time.mktime(time.strptime(f"{year}-12-31", "%Y-%m-%d")))
        
        data = {
            "starttime": start_time,
            "endtime": end_time,
            "cursor": 0,
            "size": 100,
            "filters": [
                {
                    "key": "applyer",
                    "value": employee_id
                }
                # 可以添加更多过滤条件，如模板ID等
            ]
        }
        
        try:
            response = self._session.post(
                url,
                params={"access_token": access_token},
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            return self._handle_api_response(result).get("data", [])
            
        except requests.RequestException as e:
            self.logger.error(f"获取审批记录失败: {str(e)}")
            raise WeChatAPIError(-1, f"网络请求失败: {str(e)}")

    def test_connection(self) -> bool:
        """
        测试企业微信连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.get_access_token()
            return True
        except Exception as e:
            self.logger.error(f"企业微信连接测试失败: {str(e)}")
            return False
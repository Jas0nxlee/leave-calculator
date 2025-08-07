"""
配置服务模块
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from models import WeChatConfig


class ConfigService:
    """配置管理服务"""

    def __init__(self, env_file: Optional[str] = None):
        """
        初始化配置服务
        
        Args:
            env_file: 环境配置文件路径，默认为 .env
        """
        self._config_cache = {}
        self._load_environment(env_file)

    def _load_environment(self, env_file: Optional[str] = None) -> None:
        """加载环境变量"""
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            # 尝试加载默认的 .env 文件
            load_dotenv()

    def get_wechat_config(self) -> WeChatConfig:
        """
        获取企业微信配置
        
        Returns:
            WeChatConfig: 企业微信配置对象
            
        Raises:
            ValueError: 当配置不完整时抛出异常
        """
        if "wechat" in self._config_cache:
            return self._config_cache["wechat"]

        config = WeChatConfig(
            corp_id=os.getenv("WECHAT_CORP_ID", ""),
            corp_secret=os.getenv("WECHAT_CORP_SECRET", ""),
            agent_id=os.getenv("WECHAT_AGENT_ID", ""),
            base_url=os.getenv("WECHAT_BASE_URL", "https://qyapi.weixin.qq.com"),
            timeout=int(os.getenv("API_TIMEOUT", "30")),
            retry_count=int(os.getenv("API_RETRY_COUNT", "3"))
        )

        if not config.validate():
            raise ValueError("企业微信配置不完整，请检查 .env 文件中的配置项")

        self._config_cache["wechat"] = config
        return config

    def get_log_config(self) -> dict:
        """
        获取日志配置
        
        Returns:
            dict: 日志配置字典
        """
        return {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "file": os.getenv("LOG_FILE", "logs/app.log"),
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }

    def get_annual_leave_config(self) -> dict:
        """
        获取年假配置
        
        Returns:
            dict: 年假配置字典
        """
        # 获取目标假期名称列表
        target_names = os.getenv("TARGET_VACATION_NAMES", "年假,年休假,annual,Annual,ANNUAL")
        target_names_list = [name.strip() for name in target_names.split(",") if name.strip()]
        
        return {
            "template_id": os.getenv("ANNUAL_LEAVE_TEMPLATE_ID", ""),
            "default_hours": int(os.getenv("DEFAULT_ANNUAL_LEAVE_HOURS", "120")),
            "working_hours_per_day": 8,
            "target_vacation_names": target_names_list
        }

    def validate_config(self) -> bool:
        """
        验证所有配置的完整性
        
        Returns:
            bool: 配置是否完整有效
        """
        try:
            wechat_config = self.get_wechat_config()
            return wechat_config.validate()
        except Exception as e:
            logging.error(f"配置验证失败: {str(e)}")
            return False

    def reload_config(self) -> None:
        """重新加载配置"""
        self._config_cache.clear()
        self._load_environment()

    def get_config_status(self) -> dict:
        """
        获取配置状态信息
        
        Returns:
            dict: 配置状态信息
        """
        try:
            wechat_config = self.get_wechat_config()
            return {
                "wechat_configured": wechat_config.validate(),
                "corp_id_set": bool(wechat_config.corp_id),
                "corp_secret_set": bool(wechat_config.corp_secret),
                "agent_id_set": bool(wechat_config.agent_id),
                "base_url": wechat_config.base_url
            }
        except Exception:
            return {
                "wechat_configured": False,
                "corp_id_set": False,
                "corp_secret_set": False,
                "agent_id_set": False,
                "base_url": ""
            }
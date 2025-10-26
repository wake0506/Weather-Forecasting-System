import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        
        # 心知天气API配置
        self.weather_api_key = os.getenv("SENIVERSE_API_KEY")
        self.weather_api_url = "https://api.seniverse.com/v3"
        
        # 应用配置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.cache_duration = int(os.getenv("CACHE_DURATION", "1800"))
        self.update_interval = int(os.getenv("UPDATE_INTERVAL", "1800"))
    
    def validate(self):
        """验证配置是否完整"""
        if not self.weather_api_key:
            raise ValueError("SENIVERSE_API_KEY 未设置，请在 .env 文件中配置")
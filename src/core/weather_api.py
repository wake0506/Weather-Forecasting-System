import requests
import json
import os
from datetime import datetime
from typing import Dict, Optional, List

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("SENIVERSE_API_KEY")
        self.base_url = "https://api.seniverse.com/v3"
    
    def get_weather_data(self, city: str) -> Dict:
        """获取实时天气数据"""
        url = f"{self.base_url}/weather/now.json"
        params = {
            "key": self.api_key,
            "location": city,
            "language": "zh-Hans",
            "unit": "c"
        }
        
        try:
            print(f"🌤️ 正在获取 {city} 的天气数据...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "results" not in data:
                raise Exception(f"API返回错误: {data}")
            
            result = data["results"][0]
            now_data = result["now"]
            location_data = result["location"]
            
            # 解析数据
            parsed_data = {
                "city": location_data["name"],
                "temperature": float(now_data["temperature"]),
                "weather_description": now_data["text"],
                "update_time": datetime.now().isoformat(),
                "data_source": "心知天气"
            }
            
            # 尝试添加可选字段
            optional_fields = {
                "humidity": "humidity",
                "wind_speed": "wind_speed", 
                "wind_direction": "wind_direction",
                "pressure": "pressure",
                "visibility": "visibility"
            }
            
            for key, field in optional_fields.items():
                if field in now_data:
                    parsed_data[key] = now_data[field]
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"获取天气数据失败: {str(e)}")
    
    def get_three_day_forecast(self, city: str) -> Optional[List[Dict]]:
        """获取3天天气预报"""
        url = f"{self.base_url}/weather/daily.json"
        params = {
            "key": self.api_key,
            "location": city,
            "language": "zh-Hans",
            "unit": "c",
            "start": 0,
            "days": 3
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "results" in data and data["results"]:
                return data["results"][0]["daily"]
            return None
            
        except Exception:
            return None
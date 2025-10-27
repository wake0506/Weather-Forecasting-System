"""
Weather API 模块
天气数据获取接口
"""

import requests
import os
from typing import Dict


def get_weather_data(city: str) -> Dict:
    """
    获取天气数据

    Args:
        city: 城市名称

    Returns:
        天气数据字典

    Raises:
        Exception: 当API请求失败时
    """
    # 这里使用模拟数据，实际项目中应该调用真实API
    # 例如：心知天气、和风天气等

    print(f"获取 {city} 的天气数据...")

    # 模拟数据 - 在实际项目中替换为真实API调用
    mock_data = {
        "北京": {
            "temperature": 28.5,
            "condition": "晴朗",
            "humidity": 45,
            "wind_speed": 12.0,
        },
        "上海": {
            "temperature": 32.0,
            "condition": "多云",
            "humidity": 65,
            "wind_speed": 8.5,
        },
        "广州": {
            "temperature": 35.5,
            "condition": "炎热",
            "humidity": 70,
            "wind_speed": 6.0,
        },
        "深圳": {
            "temperature": 34.0,
            "condition": "晴",
            "humidity": 68,
            "wind_speed": 7.2,
        },
    }

    if city in mock_data:
        data = mock_data[city]
        return {
            "city": city,
            "temperature": data["temperature"],
            "condition": data["condition"],
            "humidity": data["humidity"],
            "wind_speed": data["wind_speed"],
        }
    else:
        # 默认数据
        return {
            "city": city,
            "temperature": 25.0,
            "condition": "晴",
            "humidity": 50,
            "wind_speed": 10.0,
        }


# 为了确保测试能够导入，我们也可以添加一个简单的类
class WeatherAPI:
    """天气API客户端"""

    def __init__(self):
        self.base_url = "https://api.example.com"

    def get_current_weather(self, city: str) -> Dict:
        """获取当前天气（委托给 get_weather_data）"""
        return get_weather_data(city)

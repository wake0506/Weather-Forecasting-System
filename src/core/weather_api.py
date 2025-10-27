import requests
import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city: str) -> Dict:
    """
    获取真实天气数据 - 使用心知天气API

    Args:
        city: 城市名称

    Returns:
        天气数据字典

    Raises:
        Exception: 当API请求失败时
    """
    api_key = os.getenv('SENIVERSE_API_KEY')
    
    if not api_key:
        raise Exception("心知天气API密钥未配置，请检查.env文件中的SENIVERSE_API_KEY")
    
    print(f"正在获取 {city} 的实时天气数据...")
    
    # 心知天气API参数
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        'key': api_key,
        'location': city,
        'language': 'zh-Hans',
        'unit': 'c'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 检查API响应
        if 'results' not in data or not data['results']:
            raise Exception(f"API返回数据格式错误: {data}")
        
        weather_info = data['results'][0]['now']
        location_info = data['results'][0]['location']
        
        # 构建返回数据
        weather_data = {
            "city": location_info['name'],
            "temperature": float(weather_info['temperature']),
            "condition": weather_info['text'],
            "humidity": int(weather_info['humidity']),
            "wind_speed": float(weather_info['wind_speed']),
        }
        
        print(f"成功获取 {city} 的天气数据")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"天气API请求失败: {e}")
    except (KeyError, ValueError, IndexError) as e:
        raise Exception(f"天气数据解析失败: {e}")


# 为了确保测试能够导入，保留原有类
class WeatherAPI:
    """天气API客户端"""

    def __init__(self):
        self.base_url = "https://api.seniverse.com/v3"

    def get_current_weather(self, city: str) -> Dict:
        """获取当前天气"""
        return get_weather_data(city)
"""
Weather API 模块
提供天气数据获取功能
"""

try:
    import requests
except ImportError:
    # 如果 requests 不可用，使用模拟数据
    pass

def get_weather_data(city):
    """
    获取天气数据
    
    Args:
        city (str): 城市名称
        
    Returns:
        dict: 天气数据
    """
    # 模拟数据 - 实际项目中可以替换为真实API调用
    mock_data = {
        '北京': {'temperature': 28.5, 'condition': '晴朗', 'humidity': 45, 'wind_speed': 12.0},
        '上海': {'temperature': 32.0, 'condition': '多云', 'humidity': 65, 'wind_speed': 8.5},
        '广州': {'temperature': 35.5, 'condition': '炎热', 'humidity': 70, 'wind_speed': 6.0},
        '深圳': {'temperature': 34.0, 'condition': '晴', 'humidity': 68, 'wind_speed': 7.2},
        '杭州': {'temperature': 30.0, 'condition': '多云', 'humidity': 60, 'wind_speed': 5.5},
        '成都': {'temperature': 26.0, 'condition': '阴', 'humidity': 75, 'wind_speed': 4.0}
    }
    
    if city in mock_data:
        result = mock_data[city].copy()
        result['city'] = city
        return result
    
    # 对于其他城市返回模拟数据
    import random
    conditions = ['晴', '多云', '阴', '小雨']
    return {
        'city': city,
        'temperature': round(random.uniform(10, 30), 1),
        'condition': random.choice(conditions),
        'humidity': random.randint(40, 80),
        'wind_speed': round(random.uniform(5, 15), 1)
    }

def get_weather_from_api(city):
    """
    从真实API获取天气数据（需要实现）
    """
    # 这里可以集成真实的天气API，如：
    # OpenWeatherMap, 和风天气等
    # response = requests.get(f"https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}")
    # return response.json()
    
    # 暂时返回模拟数据
    return get_weather_data(city)

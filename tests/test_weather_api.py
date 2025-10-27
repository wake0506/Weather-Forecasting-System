import pytest
from src.core.weather_api import get_weather_data


class TestWeatherAPI:
    """天气API测试"""

    def test_get_weather_data_success(self):
        """测试成功获取天气数据"""
        result = get_weather_data("北京")

        assert result["city"] == "北京"
        assert "temperature" in result
        assert "condition" in result
        assert "humidity" in result
        assert "wind_speed" in result

    def test_get_weather_data_different_cities(self):
        """测试不同城市的天气数据"""
        cities = ["北京", "上海", "广州"]

        for city in cities:
            result = get_weather_data(city)
            assert result["city"] == city
            assert isinstance(result["temperature"], (int, float))
            assert isinstance(result["humidity"], int)

    def test_get_weather_data_unknown_city(self):
        """测试未知城市的默认数据"""
        result = get_weather_data("未知城市")

        assert result["city"] == "未知城市"
        assert result["temperature"] == 25.0  # 默认温度
        assert result["condition"] == "晴"  # 默认天气

#import pytest
from src.core.forecasting_engine import ForecastingEngine


class TestForecastingEngine:
    """天气预报引擎测试"""

    def test_forecasting_engine_initialization(self):
        """测试预测引擎初始化"""
        engine = ForecastingEngine()
        assert engine.temperature_threshold == 35.0
        assert engine.rain_threshold == 80
        assert engine.wind_threshold == 20.0

    def test_check_forecast_normal_conditions(self):
        """测试正常天气条件下的预测"""
        engine = ForecastingEngine()
        weather_data = {
            "temperature": 25.0,
            "humidity": 50,
            "wind_speed": 10.0,
            "condition": "晴朗",
        }

        result = engine.check_forecast(weather_data)
        assert result["has_forecast"] is False
        assert "正常" in result["message"]

    def test_check_forecast_high_temperature(self):
        """测试高温预警"""
        engine = ForecastingEngine()
        weather_data = {
            "temperature": 38.0,
            "humidity": 50,
            "wind_speed": 10.0,
            "condition": "炎热",
        }

        result = engine.check_forecast(weather_data)
        assert result["has_forecast"] is True
        assert "高温预警" in result["message"]
        assert "38.0" in result["message"]

    def test_check_forecast_custom_threshold(self):
        """测试自定义阈值"""
        engine = ForecastingEngine()
        weather_data = {
            "temperature": 32.0,
            "humidity": 50,
            "wind_speed": 10.0,
            "condition": "晴朗",
        }

        # 使用较低的阈值
        result = engine.check_forecast(weather_data, temp_threshold=30.0)
        assert result["has_forecast"] is True

    def test_set_thresholds(self):
        """测试设置阈值"""
        engine = ForecastingEngine()
        engine.set_thresholds(temp=40.0, rain=90, wind=25.0)

        assert engine.temperature_threshold == 40.0
        assert engine.rain_threshold == 90
        assert engine.wind_threshold == 25.0

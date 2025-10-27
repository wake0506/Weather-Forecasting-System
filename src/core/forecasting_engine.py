"""
Weather Forecasting Engine
天气预测引擎核心模块
"""


class ForecastingEngine:
    """天气预测引擎"""

    def __init__(self):
        self.temperature_threshold = 35.0
        self.rain_threshold = 80
        self.wind_threshold = 20.0

    def check_forecast(self, weather_data, temp_threshold=None):
        """
        检查天气预测条件

        Args:
            weather_data: 天气数据字典
            temp_threshold: 温度阈值

        Returns:
            预测结果字典
        """
        if temp_threshold is None:
            temp_threshold = self.temperature_threshold

        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
       

        forecasts = []

        # 温度预测
        if temperature > temp_threshold:
            forecasts.append(f"高温预警: {temperature}°C")

        # 降雨预测
        if humidity > self.rain_threshold:
            forecasts.append(f"高湿预警: {humidity}%")

        # 大风预测
        if wind_speed > self.wind_threshold:
            forecasts.append(f"大风预警: {wind_speed}km/h")

        if forecasts:
            return {
                "has_forecast": True,
                "message": " | ".join(forecasts),
                "forecasts": forecasts,
            }
        else:
            return {"has_forecast": False, "message": "天气条件正常", "forecasts": []}

    def set_thresholds(self, temp=None, rain=None, wind=None):
        """设置预测阈值"""
        if temp is not None:
            self.temperature_threshold = temp
        if rain is not None:
            self.rain_threshold = rain
        if wind is not None:
            self.wind_threshold = wind

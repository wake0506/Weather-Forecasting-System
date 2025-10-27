from typing import Dict, List


class ConsoleNotifier:
    def send_weather_report(self, weather_data: Dict):
        """发送天气报告到控制台"""
        print("\n" + "=" * 50)
        print(f"🌤️  实时天气报告 - {weather_data['city']}")
        print("=" * 50)

        # 显示基础天气信息
        print(f"📍 城市: {weather_data['city']}")
        print(f"🌡️ 温度: {weather_data['temperature']}°C")
        print(f"☁️ 天气: {weather_data['weather_description']}")

        # 安全显示可选字段
        humidity = weather_data.get("humidity")
        if humidity is not None:
            print(f"💧 湿度: {humidity}%")

        wind_speed = weather_data.get("wind_speed")
        wind_direction = weather_data.get("wind_direction")
        if wind_speed is not None and wind_direction is not None:
            print(f"💨 风速: {wind_speed} km/h")
            print(f"🧭 风向: {wind_direction}")

        pressure = weather_data.get("pressure")
        if pressure is not None:
            print(f"📊 气压: {pressure} hPa")

        visibility = weather_data.get("visibility")
        if visibility is not None:
            print(f"👁️ 能见度: {visibility} km")

        print(f"\n🕒 更新时间: {weather_data['update_time'][:19]}")
        print(f"📡 数据来源: {weather_data.get('data_source', '心知天气')}")
        print("=" * 50)

    def send_forecast_report(self, forecast_data: List[Dict], city: str):
        """发送天气预报报告"""
        if not forecast_data:
            print("\n⚠️  无法获取天气预报数据")
            return

        print("\n" + "=" * 50)
        print(f"📅  三天天气预报 - {city}")
        print("=" * 50)

        for day in forecast_data:
            date = day["date"]
            weather_day = day["text_day"]
            weather_night = day["text_night"]
            temp_max = day["high"]
            temp_min = day["low"]

            print(f"\n📅 {date}")
            print(f"   ☀️ 白天: {weather_day}")
            print(f"   🌙 夜间: {weather_night}")
            print(f"   🌡️ 温度: {temp_min}°C ~ {temp_max}°C")

            wind_direction = day.get("wind_direction")
            wind_scale = day.get("wind_scale")
            if wind_direction and wind_scale:
                print(f"   💨 风力: {wind_direction} {wind_scale}")

        print("=" * 50)

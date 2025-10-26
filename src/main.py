#!/usr/bin/env python3
import argparse
import sys
import os
import traceback

try:
    # 添加src目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

    from src.core.weather_api import WeatherAPI
    from src.notification.console_notifier import ConsoleNotifier
    from src.config.settings import Settings

    def main():
        parser = argparse.ArgumentParser(description='简易天气查询系统')
        parser.add_argument('--city', required=True, help='要查询的城市名称（中文，如：北京、上海）')
        parser.add_argument('--forecast', '-f', action='store_true', help='显示三天天气预报')
        
        args = parser.parse_args()
        
        # 初始化配置和组件
        settings = Settings()
        settings.validate()
        
        weather_api = WeatherAPI()
        notifier = ConsoleNotifier()
        
        # 获取实时天气数据
        weather_data = weather_api.get_weather_data(args.city)
        
        # 显示实时天气报告
        notifier.send_weather_report(weather_data)
        
        # 显示天气预报（如果请求）
        if args.forecast:
            forecast_data = weather_api.get_three_day_forecast(args.city)
            if forecast_data:
                notifier.send_forecast_report(forecast_data, args.city)
            else:
                print("\n⚠️  无法获取天气预报数据")
            
    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"❌ 程序出错: {e}")
    print("详细错误信息:")
    traceback.print_exc()
    sys.exit(1)
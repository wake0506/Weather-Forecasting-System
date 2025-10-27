import argparse
import sys
from src.core.weather_api import get_weather_data
from src.core.forecasting_engine import ForecastingEngine

# 尝试导入简化版数据管理器
try:
    from src.core.data_manager_simple import SimpleDataManager
    DATA_MANAGER_AVAILABLE = True
except ImportError:
    DATA_MANAGER_AVAILABLE = False
    print("Note: Database features not available")

def main():
    """Main application entry point"""
    print("Weather Forecasting System starting...")

    parser = argparse.ArgumentParser(description="Weather Forecasting System")
    parser.add_argument("--city", required=True, help="City name")
    parser.add_argument(
        "--threshold", type=float, default=35.0, help="Temperature threshold for alerts"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--save-data", action="store_true", help="Save data to database")
    parser.add_argument("--show-history", type=int, help="Show weather history for last N days")
    parser.add_argument("--show-stats", type=int, default=7, help="Show statistics for last N days")
    # 在 ArgumentParser 中添加新参数
    parser.add_argument("--show-date", type=str, help="Show weather for specific date (YYYY-MM-DD)")
    parser.add_argument("--daily-summary", type=int, help="Show daily summary for last N days")
    args = parser.parse_args()

    try:
        # 初始化数据管理器（如果可用）
        data_manager = None
        if DATA_MANAGER_AVAILABLE:
            data_manager = SimpleDataManager()
        
        # 显示历史数据
        if args.show_history and data_manager:
            history = data_manager.get_recent_weather(args.city, args.show_history)
            if history:
                print(f"\nLast {args.show_history} hours weather history for {args.city}:")
                for record in history[:10]:
                    recorded_time = record['recorded_at'][:16] if record['recorded_at'] else 'N/A'
                    alert = "ALERT" if record['forecast_alert'] else "NORMAL"
                    print(f"  {recorded_time} | {record['temperature']}C | {record['condition']} | {alert}")
                
                # 显示统计信息
                stats = data_manager.get_city_statistics(args.city, args.show_stats)
                if stats and stats.get('record_count', 0) > 0:
                    print(f"\nStatistics (last {stats['period_days']} days):")
                    print(f"  City: {stats['city']}")
                    print(f"  Records: {stats['record_count']}")
                    print(f"  Avg Temp: {stats['average_temperature']}C")
                    print(f"  Max Temp: {stats['max_temperature']}C")
                    print(f"  Min Temp: {stats['min_temperature']}C")
                    print(f"  Avg Humidity: {stats['average_humidity']}%")
            else:
                print(f"No historical data found for {args.city}")
            return

        # 获取天气数据
        if args.verbose:
            print(f"Fetching weather data for {args.city}...")

        weather_data = get_weather_data(args.city)

        # 创建预测引擎
        forecast_engine = ForecastingEngine()

        # 检查预测条件
        forecast_result = forecast_engine.check_forecast(weather_data, args.threshold)

        # 显示结果
        print(f"\nWeather Report for {weather_data['city']}:")
        print(f"Temperature: {weather_data['temperature']}C")
        print(f"Condition: {weather_data['condition']}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} km/h")

        print(f"\nForecast Analysis (Threshold: {args.threshold}C):")
        if forecast_result["has_forecast"]:
            print(f"ALERT: {forecast_result['message']}")
        else:
            print("Weather conditions are normal")

        # 保存数据到数据库
        if args.save_data and data_manager:
            save_result = data_manager.save_weather_data(weather_data, forecast_result, args.threshold)
            if args.verbose:
                if save_result['local_success']:
                    print("Data saved to local database")
                else:
                    print("Failed to save data to database")
        elif args.save_data and not data_manager:
            print("Database not available - cannot save data")

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
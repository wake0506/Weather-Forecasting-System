#!/usr/bin/env python3
"""
Weather Forecasting System - Main Application
"""

import argparse
import sys
from src.core.weather_api import get_weather_data
from src.core.forecasting_engine import ForecastingEngine

def main():
    """Main application entry point"""
    print("Weather Forecasting System starting...")
    
    parser = argparse.ArgumentParser(description="Weather Forecasting System")
    parser.add_argument("--city", required=True, help="City name")
    parser.add_argument("--threshold", type=float, default=35.0, help="Temperature threshold for alerts")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    try:
        # Get weather data
        if args.verbose:
            print(f"���️  Fetching weather data for {args.city}...")
        
        weather_data = get_weather_data(args.city)
        
        # Create forecasting engine
        forecast_engine = ForecastingEngine()
        
        # Check forecast conditions
        forecast_result = forecast_engine.check_forecast(weather_data, args.threshold)
        
        # Display results
        print(f"\n��� Weather Report for {weather_data['city']}:")
        print(f"���️  Temperature: {weather_data['temperature']}°C")
        print(f"☁️  Condition: {weather_data['condition']}")
        print(f"��� Humidity: {weather_data['humidity']}%")
        print(f"��� Wind Speed: {weather_data['wind_speed']} km/h")
        
        print(f"\n��� Forecast Analysis (Threshold: {args.threshold}°C):")
        if forecast_result['has_forecast']:
            print(f"⚠️  {forecast_result['message']}")
        else:
            print("✅ Weather conditions are normal")
            
    except Exception as e:
        print(f"❌ Error getting weather data: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
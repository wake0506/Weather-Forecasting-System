from src.models.database_simple import SimpleDatabaseManager

class SimpleDataManager:
    """简化版数据管理器 - 支持日期查询"""
    
    def __init__(self):
        self.db_manager = SimpleDatabaseManager()
    
    def save_weather_data(self, weather_data, forecast_result, threshold=35.0):
        """保存天气数据"""
        record_id = self.db_manager.save_weather_record(weather_data, forecast_result, threshold)
        
        return {
            'local_success': record_id is not None,
            'dagshub_success': False,
            'record_id': record_id
        }
    
    def get_recent_weather(self, city, days=1):
        """获取最近指定天数内的天气数据"""
        return self.db_manager.get_recent_weather(city, days)
    
    def get_weather_by_date(self, city, target_date):
        """按具体日期查询天气数据"""
        return self.db_manager.get_weather_by_date(city, target_date)
    
    def get_daily_summary(self, city, days=7):
        """获取每日天气摘要"""
        return self.db_manager.get_daily_summary(city, days)
    
    def get_city_statistics(self, city, days=7):
        """获取城市统计信息"""
        return self.db_manager.get_city_statistics(city, days)
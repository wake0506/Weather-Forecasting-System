import sqlite3
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class SimpleDatabaseManager:
    """简化版数据库管理器 - 完整版"""
    
    def __init__(self):
        self.db_path = './data/weather_data.db'
        os.makedirs('./data', exist_ok=True)
        self._create_tables()
    
    def _create_tables(self):
        """创建数据表 - 添加日期字段"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL NOT NULL,
                condition TEXT NOT NULL,
                humidity INTEGER NOT NULL,
                wind_speed REAL NOT NULL,
                forecast_alert BOOLEAN DEFAULT 0,
                alert_message TEXT,
                threshold REAL DEFAULT 35.0,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                recorded_date DATE,  -- 新增：日期字段（精确到天）
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'seniverse_api'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database tables created successfully")
    
    def save_weather_record(self, weather_data, forecast_result, threshold=35.0):
        """保存天气记录 - 添加日期字段"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 使用当前时间作为记录时间
        current_time = datetime.now()
        recorded_at = current_time.strftime('%Y-%m-%d %H:%M:%S')
        recorded_date = current_time.strftime('%Y-%m-%d')  # 新增：日期字段
        
        cursor.execute('''
            INSERT INTO weather_records 
            (city, temperature, condition, humidity, wind_speed, forecast_alert, alert_message, threshold, recorded_at, recorded_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['city'],
            weather_data['temperature'],
            weather_data['condition'],
            weather_data['humidity'],
            weather_data['wind_speed'],
            1 if forecast_result.get('has_forecast', False) else 0,
            forecast_result.get('message', ''),
            threshold,
            recorded_at,
            recorded_date  # 新增：日期字段
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        print(f"Weather data saved for {weather_data['city']} on {recorded_date} (ID: {record_id})")
        return record_id
    
    def get_recent_weather(self, city, days=1):
        """获取最近指定天数内的天气数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 计算时间阈值
        time_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT * FROM weather_records 
            WHERE city = ? AND recorded_at >= ?
            ORDER BY recorded_at DESC
        ''', (city, time_threshold))
        
        records = cursor.fetchall()
        conn.close()
        
        # 转换为字典列表
        columns = ['id', 'city', 'temperature', 'condition', 'humidity', 'wind_speed', 
                  'forecast_alert', 'alert_message', 'threshold', 'recorded_at', 'recorded_date', 'created_at', 'source']
        
        return [dict(zip(columns, record)) for record in records]
    
    def get_weather_by_date(self, city, target_date):
        """按具体日期查询天气数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM weather_records 
            WHERE city = ? AND recorded_date = ?
            ORDER BY recorded_at DESC
        ''', (city, target_date))
        
        records = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'city', 'temperature', 'condition', 'humidity', 'wind_speed', 
                  'forecast_alert', 'alert_message', 'threshold', 'recorded_at', 'recorded_date', 'created_at', 'source']
        
        return [dict(zip(columns, record)) for record in records]
    
    def get_weather_by_date_range(self, city, start_date, end_date):
        """按日期范围查询天气数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM weather_records 
            WHERE city = ? AND recorded_date BETWEEN ? AND ?
            ORDER BY recorded_at DESC
        ''', (city, start_date, end_date))
        
        records = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'city', 'temperature', 'condition', 'humidity', 'wind_speed', 
                  'forecast_alert', 'alert_message', 'threshold', 'recorded_at', 'recorded_date', 'created_at', 'source']
        
        return [dict(zip(columns, record)) for record in records]
    
    def get_daily_summary(self, city, days=7):
        """获取每日天气摘要"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 计算时间阈值
        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT 
                recorded_date,
                COUNT(*) as record_count,
                AVG(temperature) as avg_temp,
                MAX(temperature) as max_temp,
                MIN(temperature) as min_temp,
                AVG(humidity) as avg_humidity
            FROM weather_records 
            WHERE city = ? AND recorded_date >= ?
            GROUP BY recorded_date
            ORDER BY recorded_date DESC
        ''', (city, date_threshold))
        
        results = cursor.fetchall()
        conn.close()
        
        daily_summaries = []
        for row in results:
            daily_summaries.append({
                'date': row[0],
                'record_count': row[1],
                'average_temperature': round(row[2], 2) if row[2] else 0,
                'max_temperature': round(row[3], 2) if row[3] else 0,
                'min_temperature': round(row[4], 2) if row[4] else 0,
                'average_humidity': round(row[5], 2) if row[5] else 0
            })
        
        return daily_summaries
    
    def get_city_statistics(self, city, days=7):
        """获取城市统计信息 - 按真实天数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 计算时间阈值
        time_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT 
                AVG(temperature) as avg_temp,
                MAX(temperature) as max_temp,
                MIN(temperature) as min_temp,
                AVG(humidity) as avg_humidity,
                COUNT(*) as record_count
            FROM weather_records 
            WHERE city = ? AND recorded_at >= ?
        ''', (city, time_threshold))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] is not None:
            return {
                'city': city,
                'period_days': days,
                'average_temperature': round(result[0], 2),
                'max_temperature': round(result[1], 2),
                'min_temperature': round(result[2], 2),
                'average_humidity': round(result[3], 2),
                'record_count': result[4]
            }
        return {}
    
    def init_sample_data(self):
        """初始化示例数据 - 添加时间戳和日期字段"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM weather_records")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 添加示例数据，包含不同的时间戳和日期
            base_time = datetime.now()
            sample_data = [
                ('北京', 28.5, '晴朗', 45, 12.0, 0, '', 35.0, 
                 (base_time - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                 (base_time - timedelta(hours=2)).strftime('%Y-%m-%d')),
                ('北京', 26.0, '多云', 50, 10.0, 0, '', 35.0, 
                 (base_time - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                 (base_time - timedelta(days=1)).strftime('%Y-%m-%d')),
                ('北京', 30.0, '晴', 40, 8.0, 0, '', 35.0, 
                 (base_time - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
                 (base_time - timedelta(days=2)).strftime('%Y-%m-%d')),
                ('上海', 32.0, '多云', 65, 8.5, 0, '', 35.0, 
                 (base_time - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                 base_time.strftime('%Y-%m-%d')),
                ('上海', 30.5, '阴', 70, 7.0, 0, '', 35.0, 
                 (base_time - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                 (base_time - timedelta(days=1)).strftime('%Y-%m-%d')),
                ('广州', 35.5, '炎热', 70, 6.0, 1, '高温预警: 35.5C', 35.0, 
                 base_time.strftime('%Y-%m-%d %H:%M:%S'),
                 base_time.strftime('%Y-%m-%d'))
            ]
            
            cursor.executemany('''
                INSERT INTO weather_records 
                (city, temperature, condition, humidity, wind_speed, forecast_alert, alert_message, threshold, recorded_at, recorded_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
            
            conn.commit()
            print("Sample data with dates initialized successfully")
        else:
            print(f"Database already contains {count} records")
        
        conn.close()
    
    def cleanup_old_records(self, days=30):
        """清理旧记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        time_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            DELETE FROM weather_records 
            WHERE recorded_at < ?
        ''', (time_threshold,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"Cleaned up {deleted_count} records older than {days} days")
        return deleted_count
    
    def _get_connection(self):
        """获取数据库连接（供内部使用）"""
        return sqlite3.connect(self.db_path)

if __name__ == "__main__":
    # 测试数据库
    print("Testing database with date features...")
    db = SimpleDatabaseManager()
    db.init_sample_data()
    
    # 测试时间过滤
    print("\nTesting 1-day history for Beijing:")
    records = db.get_recent_weather("北京", 1)
    print(f"Found {len(records)} records from last 1 day")
    
    print("\nTesting daily summary:")
    summary = db.get_daily_summary("北京", 3)
    for day in summary:
        print(f"  {day['date']}: {day['record_count']} records, avg {day['average_temperature']}C")
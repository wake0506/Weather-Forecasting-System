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
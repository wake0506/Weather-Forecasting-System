class WeatherApp {
    constructor() {
        this.cityInput = document.getElementById('cityInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.weatherCard = document.getElementById('weatherCard');
        this.alert = document.getElementById('alert');
        
        this.cityData = {
            '北京': { temp: 28.5, condition: '晴朗', humidity: 45, wind: 12.0 },
            '上海': { temp: 32.0, condition: '多云', humidity: 65, wind: 8.5 },
            '广州': { temp: 35.5, condition: '炎热', humidity: 70, wind: 6.0 },
            '深圳': { temp: 34.0, condition: '晴', humidity: 68, wind: 7.2 },
            '杭州': { temp: 30.0, condition: '多云', humidity: 60, wind: 5.5 },
            '成都': { temp: 26.0, condition: '阴', humidity: 75, wind: 4.0 }
        };
        
        this.init();
    }
    
    init() {
        this.searchBtn.addEventListener('click', () => this.search());
        this.cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.search();
        });
    }
    
    async search() {
        const city = this.cityInput.value.trim();
        if (!city) return this.showAlert('请输入城市名称', 'info');
        
        this.showLoading();
        
        try {
            await this.delay(800);
            const data = this.getWeatherData(city);
            this.displayWeather(data);
            this.checkAlerts(data);
        } catch (error) {
            this.showAlert('城市未找到，请重试', 'warning');
        }
    }
    
    getWeatherData(city) {
        if (this.cityData[city]) {
            return { city, ...this.cityData[city] };
        }
        
        const conditions = ['晴', '多云', '阴', '小雨'];
        return {
            city,
            temp: (Math.random() * 20 + 10).toFixed(1),
            condition: conditions[Math.floor(Math.random() * conditions.length)],
            humidity: Math.floor(Math.random() * 40 + 40),
            wind: (Math.random() * 15 + 5).toFixed(1)
        };
    }
    
    displayWeather(data) {
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('temperature').textContent = `${data.temp}°C`;
        document.getElementById('condition').textContent = data.condition;
        document.getElementById('humidity').textContent = `${data.humidity}%`;
        document.getElementById('windSpeed').textContent = `${data.wind} km/h`;
        
        this.weatherCard.classList.remove('hidden');
    }
    
    checkAlerts(data) {
        const alerts = [];
        
        if (data.temp > 35) {
            alerts.push(`高温警报: ${data.temp}°C`);
        }
        if (data.humidity > 80) {
            alerts.push(`高湿警报: ${data.humidity}%`);
        }
        if (data.wind > 15) {
            alerts.push(`大风警报: ${data.wind} km/h`);
        }
        
        if (alerts.length > 0) {
            this.showAlert(alerts.join(' | '), 'warning');
        } else {
            this.hideAlert();
        }
    }
    
    showAlert(message, type = 'info') {
        this.alert.textContent = message;
        this.alert.className = `alert ${type}`;
        this.alert.classList.remove('hidden');
    }
    
    hideAlert() {
        this.alert.classList.add('hidden');
    }
    
    showLoading() {
        this.searchBtn.textContent = '查询中...';
        this.searchBtn.disabled = true;
        
        setTimeout(() => {
            this.searchBtn.textContent = '查询';
            this.searchBtn.disabled = false;
        }, 800);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

new WeatherApp();

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("QWEATHER_API_KEY")
print(f"API Key: {api_key}")

# 测试不同的API端点
test_urls = [
    "https://devapi.qweather.com/v2/city/lookup",
    "https://geoapi.qweather.com/v2/city/lookup"  # 尝试这个端点
]

for url in test_urls:
    print(f"\n测试端点: {url}")
    params = {
        "location": "北京",
        "key": api_key,
        "adm": "cn",
        "number": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功! 响应: {data}")
            break
        else:
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {e}")
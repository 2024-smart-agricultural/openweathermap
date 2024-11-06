import os
import requests
import json
from datetime import datetime

# 대한민국 주요 도시 목록 (예시)
cities = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Jeonju", "Gwangju", "Suwon"]

# API 키와 기본 URL 설정
api_key = os.getenv('OWM_API_KEY')
base_url = "http://api.openweathermap.org/data/2.5/weather"

# 데이터 저장할 파일 설정
output_file = "data/weather_data.json"

# 기존 데이터 읽어오기 (파일이 있는 경우)
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        weather_data = json.load(f)
else:
    weather_data = {}

# 각 도시의 날씨 데이터를 가져와서 저장
for city in cities:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        city_data = response.json()
        # 타임스탬프 추가하여 중복 방지 (날짜/시간별로 저장)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if city not in weather_data:
            weather_data[city] = []
        weather_data[city].append({"timestamp": timestamp, "data": city_data})
    else:
        print(f"Failed to get data for {city}: {response.status_code}")

# JSON 파일로 저장
with open(output_file, "w") as f:
    json.dump(weather_data, f, indent=4)

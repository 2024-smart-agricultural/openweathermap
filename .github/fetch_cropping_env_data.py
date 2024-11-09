# 작기별 스마트팜 빅데이터 제공 서비스 - 농가별 작기 정보
import os
import requests
import json
from datetime import datetime
import pytz

# API 키 및 기본 URL 설정
SERVICE_KEY = os.getenv('SERVICE_KEY')  # GitHub Secrets에 저장된 서비스 키를 환경 변수로 가져옴
CROPPING_SERIAL_NO = 'YOUR_CROPPING_SERIAL_NO'  # 작기 번호를 입력하세요
total_pages = 28  # Set total pages as integer
BASE_URL_TEMPLATE = "http://www.smartfarmkorea.net/Agree_WS/webservices/CropseasonRestService/getCroppingSeasonEnvDataList/{service_key}/{cropping_serial_no}/{page_num}"

# Output file setup
output_file = 'data/cropping_env_data.json'

def fetch_all_cropping_env_data():
    all_data = []
    for page_num in range(1, total_pages + 1):  # Loop from page 1 to total_pages
        url = BASE_URL_TEMPLATE.format(service_key=SERVICE_KEY, cropping_serial_no=CROPPING_SERIAL_NO, page_num=page_num)
        
        try:
            # API request
            response = requests.get(url)
            response.raise_for_status()  # Raise error for unsuccessful requests

            # Process response data
            data = response.json()  # Parse response as JSON
            all_data.extend(data)  # Aggregate data across all pages

        except requests.exceptions.RequestException as e:
            print(f"Error during API request (Page {page_num}): {e}")
        
    # Generate timestamp in Korean Standard Time
    tz_kst = pytz.timezone('Asia/Seoul')  # Set timezone to KST
    current_time = datetime.now(tz_kst)  # Get current time in KST
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp

    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"timestamp": timestamp, "data": all_data}, f, indent=4, ensure_ascii=False)

    print(f"Successfully fetched cropping environment data. Timestamp: {timestamp}")

if __name__ == "__main__":
    fetch_all_cropping_env_data()

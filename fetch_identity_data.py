import os
import requests
import json
from datetime import datetime

# API 키 및 기본 URL 설정
SERVICE_KEY = 'YOUR_SERVICE_KEY'  # 여기에 발급받은 서비스 키를 입력하세요
BASE_URL = f"http://www.smartfarmkorea.net/Agree_WS/webservices/ProvideRestService/getIdentityDataList/{SERVICE_KEY}"

# 데이터 저장할 파일 설정
output_file = 'data/identity_data.json'

def fetch_identity_data():
    try:
        # API 호출
        response = requests.get(BASE_URL)
        response.raise_for_status()  # 요청이 성공하지 않으면 예외 발생

        # 응답 데이터 처리
        data = response.json()  # JSON 형식으로 응답 데이터 파싱
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 타임스탬프 추가

        # JSON 파일로 저장
        with open(output_file, 'w') as f:
            json.dump({"timestamp": timestamp, "data": data}, f, indent=4)

        print(f"아이덴티티 데이터를 성공적으로 가져왔습니다. 타임스탬프: {timestamp}")

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")

if __name__ == "__main__":
    fetch_identity_data()
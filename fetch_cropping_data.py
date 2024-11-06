import os
import requests
import json
from datetime import datetime

# API 키 및 기본 URL 설정
SERVICE_KEY = os.getenv('SERVICE_KEY')  # GitHub Secrets에 저장된 서비스 키를 환경 변수로 가져옴
USER_ID = os.getenv('USER_ID')  # GitHub Secrets에 저장된 사용자 ID를 환경 변수로 가져옴
BASE_URL = f"http://www.smartfarmkorea.net/Agree_WS/webservices/ProvideRestService/getCroppingSeasonDataList/{SERVICE_KEY}/{USER_ID}"

# 데이터 저장할 파일 설정
output_file = 'data/cropping_data.json'

def fetch_cropping_data():
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

        print(f"작기 정보를 성공적으로 가져왔습니다. 타임스탬프: {timestamp}")

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")

if __name__ == "__main__":
    fetch_cropping_data()

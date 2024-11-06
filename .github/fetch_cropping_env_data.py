# 작기별 스마트팜 빅데이터 제공 서비스 - 농가별 작기 정보
import os
import requests
import json
from datetime import datetime
import pytz

# API 키 및 기본 URL 설정
SERVICE_KEY = os.getenv('SERVICE_KEY')  # GitHub Secrets에 저장된 서비스 키를 환경 변수로 가져옴
CROPPING_SERIAL_NO = 'YOUR_CROPPING_SERIAL_NO'  # 작기 번호를 입력하세요
PAGE_NUM = '28'
BASE_URL = f"http://www.smartfarmkorea.net/Agree_WS/webservices/CropseasonRestService/getCroppingSeasonEnvDataList/{SERVICE_KEY}/{CROPPING_SERIAL_NO}/{PAGE_NUM}"

# 데이터 저장할 파일 설정
output_file = 'data/cropping_env_data.json'


def fetch_all_cropping_env_data():
    all_data = []
    for page_num in range(1, total_pages + 1):  # 1부터 total_pages까지 반복
        BASE_URL = f"http://www.smartfarmkorea.net/Agree_WS/webservices/CropseasonRestService/getCroppingSeasonEnvDataList/{SERVICE_KEY}/{CROPPING_SERIAL_NO}/{page_num}"
        
        try:
            # API 호출
            response = requests.get(BASE_URL)
            response.raise_for_status()  # 요청이 성공하지 않으면 예외 발생

            # 응답 데이터 처리
            data = response.json()  # JSON 형식으로 응답 데이터 파싱
            all_data.extend(data)  # 모든 페이지의 데이터를 통합

        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생 (페이지 {page_num}): {e}")
        
    # 현재 한국 시간으로 타임스탬프 생성
    tz_kst = pytz.timezone('Asia/Seoul')  # 한국 표준시 설정
    current_time = datetime.now(tz_kst)  # 현재 시간 가져오기
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")  # KST 기준으로 포맷

    # JSON 파일로 저장
    with open(output_file, 'w') as f:
        json.dump({"timestamp": timestamp, "data": data}, f, indent=4)

    print(f"농가별 작기 환경 정보를 성공적으로 가져왔습니다. 타임스탬프: {timestamp}")

if __name__ == "__main__":
    fetch_all_cropping_env_data()

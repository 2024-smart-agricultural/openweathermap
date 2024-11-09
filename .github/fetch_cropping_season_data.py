# 작기별 스마트팜 빅데이터 제공 서비스 - 농가별 작기 정보
import os
import requests
import json
from datetime import datetime
import pytz

# API 키 및 기본 URL 설정
SERVICE_KEY = os.getenv('SERVICE_KEY')  # 환경 변수에서 서비스 키 가져오기
YEAR_RANGE = ['2021', '2022', '2023', '2024']  # 데이터를 가져올 연도 설정
BASE_URL = "http://www.smartfarmkorea.net/Agree_WS/webservices/CropseasonRestService/getCroppingSeasonDataList"

# 데이터 저장할 파일 설정
output_file = 'data/cropping_season_data.json'

def fetch_cropping_season_data(year):
    try:
        # URL에 서비스 키와 연도를 삽입하여 호출
        url = f"{BASE_URL}/{SERVICE_KEY}/{year}"
        response = requests.get(url)
        response.raise_for_status()  # 상태 코드가 정상적이지 않으면 예외 발생

        # JSON 응답 데이터 파싱
        data = response.json()

        # 응답 형식 확인
        if isinstance(data, list) and data[0].get("statusCode") == "00":
            return data
        else:
            print(f"{year}년의 데이터가 예상 형식과 다릅니다.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"{year}년 데이터 요청 중 오류 발생: {e}")
        return None
        
def main():
    all_data = {}
    tz_kst = pytz.timezone('Asia/Seoul')  # 한국 표준시 설정
    current_time = datetime.now(tz_kst)  # 현재 KST 시간 가져오기
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")  # 타임스탬프 포맷

    # 각 연도에 대해 데이터 가져오기
    for year in YEAR_RANGE:
        print(f"{year}년 데이터를 가져오는 중...")
        yearly_data = fetch_cropping_season_data(year)
        if yearly_data:
            all_data[year] = yearly_data
        else:
            print(f"{year}년의 데이터가 없습니다.")

    # 타임스탬프와 함께 JSON 파일로 저장
    if all_data:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"timestamp": timestamp, "data": all_data}, f, indent=4, ensure_ascii=False)
        print(f"작기 정보 데이터를 성공적으로 저장했습니다. 타임스탬프: {timestamp}")
    else:
        print("모든 연도의 데이터를 가져오는 데 실패했습니다.")

if __name__ == "__main__":
    main()

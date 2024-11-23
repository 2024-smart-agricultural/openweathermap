import requests
import json
import os
from datetime import datetime

API_URL = "http://www.smartfarmkorea.net/Agree_WS/webservices/InnovationValleyRestService/getEnvDataList"
SERVICE_KEY = os.getenv("SERVICE_KEY")  # GitHub Secrets에 저장된 API 키 사용

# 필수 파라미터
FACILITY_ID = "C010901_C01090101_001"  # 예시 시설 ID (수정 가능)
USER_ID = "inv_01"  # 예시 농가 ID (수정 가능)
MEASURE_DATE = datetime.now().strftime("%Y%m%d")  # 현재 날짜

def fetch_data():
    params = {
        'serviceKey': SERVICE_KEY,
        'fcltyId': FACILITY_ID,
        'userId': USER_ID,
        'measDate': MEASURE_DATE
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        save_data(data)
    else:
        print(f"Error: {response.status_code}, {response.text}")

def save_data(data):
    # 데이터를 가공하여 필요한 정보만 추출
    processed_data = []
    for item in data.get("envDataList", []):
        entry = {
            "분야": "시설원예",
            "측정일시": item.get("measDate"),
            "센서값": item.get("senVal"),
            "항목코드": item.get("fatrCode"),
            "품목코드": item.get("itemCode"),
            "분류코드": item.get("sectCode"),
            "측정 장소": item.get("locCode"),
            "측정 시설": item.get("facCode"),
            "데이터 단위": item.get("unit"),
            "측정 시간": item.get("measTime"),
            "데이터 신뢰도": item.get("reliability"),
            "제어 정보": item.get("controlInfo"),
            "센서 ID": item.get("sensorId"),
            "데이터 수집 주기": item.get("collectionFreq"),
            "날씨 정보": item.get("weatherInfo"),
            "작물 상태": item.get("cropStatus"),
            "작물 위치": item.get("cropLocation"),
            "제어 설정": item.get("controlSettings"),
            "이상 데이터 표시": item.get("anomalyIndicator"),
            "온실 구역 정보": item.get("greenhouseSection")
        }
        processed_data.append(entry)
    
    # JSON 파일로 저장
    with open("data/smartfarm_data.json", "w", encoding="utf-8") as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

    print("Data saved successfully!")

if __name__ == "__main__":
    fetch_data()

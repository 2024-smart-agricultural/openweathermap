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
            "분류코드": item.get("sectCode")
        }
        processed_data.append(entry)
    
    # JSON 파일로 저장
    with open("data/smartfarm_data.json", "w", encoding="utf-8") as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

    print("Data saved successfully!")

if __name__ == "__main__":
    fetch_data()

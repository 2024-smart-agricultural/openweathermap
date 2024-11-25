import requests
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "http://www.smartfarmkorea.net/Agree_WS/webservices/InnovationValleyRestService/getEnvDataList"
SERVICE_KEY = os.getenv("BIGDATA_API_KEY")  # GitHub Secrets에 저장된 API 키 사용

# 필수 파라미터 - 모든 시설 ID 목록
FACILITY_IDS = [
    "C010901_C01090101",  # 상주 창업보육시설
    "C010901_C01090102",  # 상주 임대형스마트팜
    "C010901_C01090103",  # 상주 실증단지
    "C010901_C01090104",  # 상주 경영형
    "C010902_C01090201",  # 김제 창업보육시설
    "C010902_C01090202",  # 김제 임대형스마트팜
    "C010902_C01090203",  # 김제 실증단지
    "C010902_C01090204",  # 김제 경영형
    "C010903_C01090301",  # 고흥 창업보육시설
    "C010903_C01090302",  # 고흥 임대형스마트팜
    "C010903_C01090303",  # 고흥 실증단지
    "C010904_C01090401",  # 밀양 창업보육시설
    "C010904_C01090402",  # 밀양 임대형스마트팜
    "C010904_C01090403"   # 밀양 실증단지
]

START_YEAR = 2021
MEASURE_DATE = datetime.now().strftime("%Y%m%d")  # 현재 날짜

def fetch_data():
    all_processed_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_facility = {
            executor.submit(fetch_facility_data, facility_id): facility_id for facility_id in FACILITY_IDS
        }
        for future in as_completed(future_to_facility):
            try:
                data = future.result()
                all_processed_data.extend(data)
            except Exception as exc:
                facility_id = future_to_facility[future]
                print(f"Facility {facility_id} generated an exception: {exc}")
    save_data(all_processed_data)

def fetch_facility_data(facility_id):
    processed_data = []
    for year in range(START_YEAR, datetime.now().year + 1):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    MEASURE_DATE = f"{year}{month:02d}{day:02d}"
                except ValueError:
                    continue
                params = {
                    'serviceKey': SERVICE_KEY,
                    'fcltyId': facility_id,
                    'measDate': MEASURE_DATE
                }
                response = requests.get(API_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    processed_data.extend(process_data(data))
                else:
                    print(f"Error fetching data for facility {facility_id} on {MEASURE_DATE}: {response.status_code}, {response.text}")
    return processed_data
    
def process_data(data):
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
    return processed_data

def save_data(data):
    # JSON 파일로 저장
    with open("smartfarm_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Data saved successfully!")

if __name__ == "__main__":
    fetch_data()

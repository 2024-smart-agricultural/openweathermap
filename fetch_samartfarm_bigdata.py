import os
import requests
import json
from datetime import datetime

# API 키와 기본 URL 설정
api_key = os.getenv('BIGDATA_API_KEY')  # 여기에 발급받은 API 키를 입력하세요
base_url = 'https://data.smartfarmkorea.net/openApi/openApiList.do'

# 데이터 저장할 파일 설정
output_file = 'data/smartfarm_bigdata.json'

# 가져오고 싶은 모든 메뉴 ID 설정 (예시)
menu_ids = [
    'M060502',  # 기후 정보
    'M060503',  # 작물 데이터
    'M060504',  # 병해충 데이터
    # 필요한 추가 메뉴 ID를 여기에 추가
]

# 기존 데이터 읽어오기 (파일이 있는 경우)
if os.path.exists(output_file):
    with open(output_file, 'r') as f:
        smartfarm_data = json.load(f)
else:
    smartfarm_data = {}

# 모든 메뉴 ID에 대해 API 호출 및 데이터 저장
for menu_id in menu_ids:
    params = {
        'menuId': menu_id,
        'apiKey': API_KEY,
    }

    try:
        # API 호출
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # 요청이 성공하지 않으면 예외 발생

        # 응답 데이터 처리
        new_data = response.json()  # JSON 형식으로 응답 데이터 파싱
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 타임스탬프 추가

        # 새로운 데이터를 추가
        if menu_id not in smartfarm_data:
            smartfarm_data[menu_id] = []
        smartfarm_data[menu_id].append({"timestamp": timestamp, "data": new_data})

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")

# JSON 파일로 저장
with open(output_file, 'w') as f:
    json.dump(smartfarm_data, f, indent=4)

print(f"모든 데이터를 성공적으로 가져왔습니다.")

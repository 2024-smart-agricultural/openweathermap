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
menu_ids = {
    "identity_info": "M060502",  # 아이덴티티 정보
    "crop_info": "M060503",       # 작기 정보
    "environment_info": "M060504", # 환경 정보
    "growth_info_strawberry": "M060505", # 생육 정보(딸기)
    "growth_info_chrysanthemum": "M060506", # 생육 정보(국화)
    "growth_info_cantaloupe": "M060507", # 생육 정보(참외)
    "growth_info_others": "M060508", # 생육 정보(기타)
    "farm_growth_info": "M060509", # 농가별 생육 정보
    "farm_environment_info": "M060510", # 농가별 환경 정보
    "farm_control_info": "M060511", # 농가별 제어 정보
}

# 데이터 저장할 파일 설정
output_file = 'data/smartfarm_data.json'

# 기존 데이터 읽어오기 (파일이 있는 경우)
if os.path.exists(output_file):
    with open(output_file, 'r') as f:
        smartfarm_data = json.load(f)
else:
    smartfarm_data = {}

# 모든 메뉴 ID에 대해 API 호출 및 데이터 저장
for key, menu_id in menu_ids.items():
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
        if key not in smartfarm_data:
            smartfarm_data[key] = []
        smartfarm_data[key].append({"timestamp": timestamp, "data": new_data})

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생 ({key}): {e}")

# JSON 파일로 저장
with open(output_file, 'w') as f:
    json.dump(smartfarm_data, f, indent=4)

print(f"모든 데이터를 성공적으로 가져왔습니다.")

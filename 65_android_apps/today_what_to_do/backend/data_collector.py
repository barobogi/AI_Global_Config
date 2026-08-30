"""
Phase 0/1 공공데이터 실데이터 수집 및 API 구조 분석 스크립트 (대한민국 17개 시도전국 확장판)
위치: backend/data_collector.py
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "backend" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.split("#", 1)[0].strip()
        env[key.strip()] = value
    return env

# 대한민국 17개 전 광역시도 대표 거점 42개 센터 좌표 (WGS84 100% 실존 좌표)
NATIONWIDE_SPOTS = [
    # 서울특별시
    {"name": "서울시청/명동", "mapx": "126.9780", "mapy": "37.5665", "radius": "8000"},
    {"name": "서울 강남역/서초", "mapx": "127.0276", "mapy": "37.4979", "radius": "8000"},
    {"name": "서울 홍대/합정", "mapx": "126.9227", "mapy": "37.5563", "radius": "8000"},
    {"name": "서울 잠실 롯데월드", "mapx": "127.0982", "mapy": "37.5113", "radius": "8000"},
    {"name": "서울 종로/인사동", "mapx": "126.9858", "mapy": "37.5744", "radius": "8000"},

    # 인천광역시
    {"name": "인천 송도국제도시", "mapx": "126.6394", "mapy": "37.3925", "radius": "8000"},
    {"name": "인천 차이나타운/신포", "mapx": "126.6186", "mapy": "37.4754", "radius": "8000"},
    {"name": "인천 구월동/남동구", "mapx": "126.7022", "mapy": "37.4475", "radius": "8000"},

    # 경기도
    {"name": "수원 화성/행궁동", "mapx": "127.0134", "mapy": "37.2847", "radius": "8000"},
    {"name": "수원 영통/광교호수공원", "mapx": "127.0601", "mapy": "37.2830", "radius": "8000"},
    {"name": "성남 분당/율동공원", "mapx": "127.1481", "mapy": "37.3775", "radius": "8000"},
    {"name": "성남 판교테크노밸리", "mapx": "127.1112", "mapy": "37.3948", "radius": "8000"},
    {"name": "부천 상동호수공원", "mapx": "126.7533", "mapy": "37.5054", "radius": "8000"},
    {"name": "고양 일산 호수공원", "mapx": "126.7687", "mapy": "37.6584", "radius": "8000"},
    {"name": "용인 보정동/에버랜드", "mapx": "127.1822", "mapy": "37.2856", "radius": "8000"},
    {"name": "남양주 다산/한강공원", "mapx": "127.1601", "mapy": "37.6080", "radius": "8000"},

    # 부산광역시
    {"name": "부산 해운대/센텀", "mapx": "129.1604", "mapy": "35.1587", "radius": "8000"},
    {"name": "부산 서면/전포", "mapx": "129.0592", "mapy": "35.1555", "radius": "8000"},
    {"name": "부산 광안리/수영", "mapx": "129.1189", "mapy": "35.1532", "radius": "8000"},
    {"name": "부산 남포동/자갈치", "mapx": "129.0306", "mapy": "35.0975", "radius": "8000"},

    # 대구광역시
    {"name": "대구 동성로/반월당", "mapx": "128.5962", "mapy": "35.8694", "radius": "8000"},
    {"name": "대구 수성못/두산동", "mapx": "128.6166", "mapy": "35.8260", "radius": "8000"},

    # 광주광역시
    {"name": "광주 ACC/문화전당", "mapx": "126.9204", "mapy": "35.1466", "radius": "8000"},
    {"name": "광주 상무지구/치평동", "mapx": "126.8520", "mapy": "35.1530", "radius": "8000"},

    # 대전광역시
    {"name": "대전 둔산/한밭수목원", "mapx": "127.3882", "mapy": "36.3685", "radius": "8000"},
    {"name": "대전 유성온천/봉명동", "mapx": "127.3414", "mapy": "36.3536", "radius": "8000"},

    # 울산광역시
    {"name": "울산 태화강국가정원", "mapx": "129.2982", "mapy": "35.5488", "radius": "8000"},
    {"name": "울산 삼산동/울산역", "mapx": "129.3337", "mapy": "35.5390", "radius": "8000"},

    # 세종특별자치시
    {"name": "세종 호수공원/어진동", "mapx": "127.2721", "mapy": "36.4965", "radius": "8000"},

    # 강원특별자치도
    {"name": "강원 강릉 경포대", "mapx": "128.8967", "mapy": "37.7952", "radius": "8000"},
    {"name": "강원 춘천 공지천", "mapx": "127.7088", "mapy": "37.8697", "radius": "8000"},
    {"name": "강원 속초 해수욕장", "mapx": "128.6015", "mapy": "38.1906", "radius": "8000"},

    # 충청북도
    {"name": "충북 청주 성안길", "mapx": "127.4883", "mapy": "36.6345", "radius": "8000"},
    {"name": "충북 충주 탄금호", "mapx": "127.9258", "mapy": "36.9912", "radius": "8000"},

    # 충청남도
    {"name": "충남 천안 아산역", "mapx": "127.1044", "mapy": "36.7946", "radius": "8000"},
    {"name": "충남 공주 한옥마을", "mapx": "127.1166", "mapy": "36.4632", "radius": "8000"},

    # 전북특별자치도
    {"name": "전북 전주 한옥마을", "mapx": "127.1524", "mapy": "35.8148", "radius": "8000"},
    {"name": "전북 군산 근대역사거리", "mapx": "126.7118", "mapy": "35.9892", "radius": "8000"},

    # 전라남도
    {"name": "전남 여수 돌산/해양", "mapx": "127.7472", "mapy": "34.7292", "radius": "8000"},
    {"name": "전남 순천만 국가정원", "mapx": "127.5098", "mapy": "34.9333", "radius": "8000"},

    # 경상북도
    {"name": "경북 경주 첨성대/대릉원", "mapx": "129.2190", "mapy": "35.8348", "radius": "8000"},
    {"name": "경북 포항 영일대/호미곶", "mapx": "129.3780", "mapy": "36.0560", "radius": "8000"},

    # 경상남도
    {"name": "경남 창원 상남동", "mapx": "128.6811", "mapy": "35.2215", "radius": "8000"},
    {"name": "경남 통영 동피랑", "mapx": "128.4282", "mapy": "34.8452", "radius": "8000"},

    # 제주특별자치도
    {"name": "제주 제주시/용두암", "mapx": "126.5160", "mapy": "33.5134", "radius": "8000"},
    {"name": "제주 서귀포/성산일출봉", "mapx": "126.9426", "mapy": "33.4581", "radius": "8000"}
]

SEOUL_SPOTS = NATIONWIDE_SPOTS

def fetch_location_based(service_key: str, spot: dict, num_rows: int = 50) -> list:
    url = "https://apis.data.go.kr/B551011/KorService2/locationBasedList2"
    params = {
        "serviceKey": service_key,
        "numOfRows": num_rows,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
        "mapX": spot["mapx"],
        "mapY": spot["mapy"],
        "radius": spot["radius"],
        "arrange": "E"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            body = data.get("response", {}).get("body", {})
            items = body.get("items", {}).get("item", [])
            if isinstance(items, dict):
                items = [items]
            return items
    except Exception as e:
        print(f"   ⚠️ API 호출 예외 ({spot['name']}): {e}")
    return []

def fetch_pet_location_based(service_key: str, spot: dict, num_rows: int = 25) -> list:
    url = "https://apis.data.go.kr/B551011/KorPetTourService/locationBasedList"
    params = {
        "serviceKey": service_key,
        "numOfRows": num_rows,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
        "mapX": spot["mapx"],
        "mapY": spot["mapy"],
        "radius": spot["radius"],
        "arrange": "E"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            body = data.get("response", {}).get("body", {})
            items = body.get("items", {}).get("item", [])
            if isinstance(items, dict):
                items = [items]
            return items
    except Exception as e:
        print(f"   ⚠️ 반려동물 API 예외 ({spot['name']}): {e}")
    return []

def fetch_detail_intro(service_key: str, content_id: str, content_type_id: str) -> dict:
    url = "https://apis.data.go.kr/B551011/KorService2/detailIntro2"
    params = {
        "serviceKey": service_key,
        "numOfRows": 1,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
        "contentId": content_id,
        "contentTypeId": content_type_id
    }
    try:
        res = requests.get(url, params=params, timeout=8)
        if res.status_code == 200:
            data = res.json()
            body = data.get("response", {}).get("body", {})
            items = body.get("items", {}).get("item", [])
            if isinstance(items, list) and items:
                return items[0]
            elif isinstance(items, dict):
                return items
    except Exception:
        pass
    return {}

def collect_all():
    env = load_env(ENV_PATH)
    kto_key = env.get("KTO_SERVICE_KEY")
    pet_key = env.get("KTO_PET_SERVICE_KEY")

    if not kto_key:
        print("에러: .env에서 KTO_SERVICE_KEY를 찾을 수 없습니다.")
        return

    print(f"🚀 [Phase 0/1] 대한민국 17개 광역시도 전역 {len(NATIONWIDE_SPOTS)}개 거점 공공데이터 실데이터 수집 시작...")
    collected_places = {}
    
    # 1. 전국 17개 시도 관광정보 수집
    for spot in NATIONWIDE_SPOTS:
        print(f"📍 {spot['name']} 주변 관광정보 조회 중...")
        items = fetch_location_based(kto_key, spot, num_rows=45)
        print(f"   ➔ {len(items)}건 수신")
        for item in items:
            cid = item.get("contentid")
            if cid and cid not in collected_places:
                item["source_spot"] = spot["name"]
                item["is_pet_spot"] = False
                collected_places[cid] = item
        time.sleep(0.15)

    # 2. 반려동물 동반정보 수집
    if pet_key:
        for spot in NATIONWIDE_SPOTS:
            print(f"🐾 {spot['name']} 주변 반려동물 동반 장소 조회 중...")
            pet_items = fetch_pet_location_based(pet_key, spot, num_rows=20)
            print(f"   ➔ {len(pet_items)}건 수신")
            for item in pet_items:
                cid = item.get("contentid")
                if cid:
                    if cid in collected_places:
                        collected_places[cid]["is_pet_spot"] = True
                        collected_places[cid]["pet_info"] = item
                    else:
                        item["source_spot"] = spot["name"]
                        item["is_pet_spot"] = True
                        collected_places[cid] = item
            time.sleep(0.15)

    print(f"\n✅ 총 {len(collected_places)}개 대한민국 전국 고유 장소 수집 완료. 지역별 고른 상세정보(Intro) 보강 중...")

    # 3. 전국 각 지역별 고른 상세 정보(detailIntro2: 휴무일/운영시간/이용요금) 보강
    enriched_count = 0
    # 고른 보강을 위해 거점별로 최소 3개 이상 보강되도록 인덱스 분산
    spot_places = {}
    for cid, place in collected_places.items():
        src = place.get("source_spot", "기타")
        if src not in spot_places:
            spot_places[src] = []
        spot_places[src].append((cid, place))

    places_to_enrich = []
    for src, items in spot_places.items():
        places_to_enrich.extend(items[:5]) # 각 거점당 상위 5개씩 골고루 수집

    print(f"   ➔ 전국 각 거점별 총 {len(places_to_enrich)}개 대표 명소 상세정보(운영시간/휴무일/요금) 수집 진행...")

    for cid, place in places_to_enrich:
        ctid = place.get("contenttypeid", "12")
        intro = fetch_detail_intro(kto_key, cid, ctid)
        if intro:
            place["detail_intro"] = intro
            enriched_count += 1
        time.sleep(0.08)

    print(f"   ➔ 총 {enriched_count}개 전국 명소 상세 정보(운영시간/휴무일) 보강 완료.")

    # 4. JSON 파일로 저장 (기존 데이터와 안전 병합)
    out_file = DATA_DIR / "places_raw.json"
    
    # 기존 파일이 있을 경우 병합
    if out_file.exists():
        try:
            with open(out_file, "r", encoding="utf-8") as f:
                existing_list = json.load(f)
                for item in existing_list:
                    cid = item.get("contentid")
                    if cid and cid not in collected_places:
                        collected_places[cid] = item
        except Exception:
            pass

    final_places = list(collected_places.values())
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_places, f, ensure_ascii=False, indent=2)

    print(f"🎉 [성공] 총 {len(final_places)}개 대한민국 17개 시도 전역 실데이터가 {out_file}에 저장되었습니다!")

if __name__ == "__main__":
    collect_all()

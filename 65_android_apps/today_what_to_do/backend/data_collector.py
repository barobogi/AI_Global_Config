"""
Phase 0/1 공공데이터 실데이터 수집 및 API 구조 분석 스크립트
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

# 수도권 및 주요 지역 좌표 (WGS84)
NATIONWIDE_SPOTS = [
    {"name": "수원 화성/행궁동", "mapx": "127.0134", "mapy": "37.2847", "radius": "8000"},
    {"name": "수원 영통/광교호수공원", "mapx": "127.0601", "mapy": "37.2830", "radius": "8000"},
    {"name": "성남 분당/율동공원", "mapx": "127.1481", "mapy": "37.3775", "radius": "8000"},
    {"name": "성남 판교테크노밸리", "mapx": "127.1112", "mapy": "37.3948", "radius": "8000"},
    {"name": "용인 보정동/에버랜드", "mapx": "127.1822", "mapy": "37.2856", "radius": "8000"},
    {"name": "서울시청/명동", "mapx": "126.9780", "mapy": "37.5665", "radius": "5000"},
    {"name": "서울 강남역/서초", "mapx": "127.0276", "mapy": "37.4979", "radius": "5000"},
    {"name": "서울 홍대/합정", "mapx": "126.9227", "mapy": "37.5563", "radius": "5000"},
    {"name": "서울 잠실 롯데월드", "mapx": "127.0982", "mapy": "37.5113", "radius": "5000"},
    {"name": "서울 종로/인사동", "mapx": "126.9858", "mapy": "37.5744", "radius": "5000"},
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
        "arrange": "E", # 거리순 정렬
    }
    try:
        resp = requests.get(url, params=params, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            return items if isinstance(items, list) else ([items] if items else [])
    except Exception as e:
        print(f"[{spot['name']}] locationBasedList2 호출 실패: {e}")
    return []

def fetch_pet_location_based(service_key: str, spot: dict, num_rows: int = 30) -> list:
    url = "https://apis.data.go.kr/B551011/KorPetTourService2/locationBasedList2"
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
        "arrange": "E",
    }
    try:
        resp = requests.get(url, params=params, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            return items if isinstance(items, list) else ([items] if items else [])
    except Exception as e:
        print(f"[{spot['name']}] KorPetTourService2 locationBasedList2 실패: {e}")
    return []

def fetch_detail_common(service_key: str, content_id: str) -> dict:
    url = "https://apis.data.go.kr/B551011/KorService2/detailCommon2"
    params = {
        "serviceKey": service_key,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
        "contentId": content_id,
        "overviewYN": "Y",
        "addrinfoYN": "Y",
        "mapinfoYN": "Y",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            items = resp.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if items:
                return items[0] if isinstance(items, list) else items
    except Exception:
        pass
    return {}

def fetch_detail_intro(service_key: str, content_id: str, content_type_id: str) -> dict:
    url = "https://apis.data.go.kr/B551011/KorService2/detailIntro2"
    params = {
        "serviceKey": service_key,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
        "contentId": content_id,
        "contentTypeId": content_type_id,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            items = resp.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if items:
                return items[0] if isinstance(items, list) else items
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

    print("🚀 [Phase 0] 서울 주요 거점별 실제 위치기반 공공데이터 수집 시작...")
    collected_places = {}
    
    # 1. 관광정보 수집
    for spot in SEOUL_SPOTS:
        print(f"📍 {spot['name']} 주변 관광정보 조회 중...")
        items = fetch_location_based(kto_key, spot, num_rows=40)
        print(f"   ➔ {len(items)}건 수신")
        for item in items:
            cid = item.get("contentid")
            if cid and cid not in collected_places:
                item["source_spot"] = spot["name"]
                item["is_pet_spot"] = False
                collected_places[cid] = item
        time.sleep(0.2)

    # 2. 반려동물 동반정보 수집
    for spot in SEOUL_SPOTS:
        print(f"🐾 {spot['name']} 주변 반려동물 동반 장소 조회 중...")
        pet_items = fetch_pet_location_based(pet_key, spot, num_rows=25)
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
        time.sleep(0.2)

    print(f"\n✅ 총 {len(collected_places)}개 고유 장소 수집 완료. 상위 장소 상세정보(Intro/Common) 보강 중...")

    # 3. 상위 25개 장소에 대해 상세 정보(detailIntro2: 휴무일/운영시간/이용요금) 보강
    sample_detail_intros = []
    enriched_count = 0
    for cid, place in list(collected_places.items())[:35]:
        ctid = place.get("contenttypeid", "12")
        intro = fetch_detail_intro(kto_key, cid, ctid)
        if intro:
            place["detail_intro"] = intro
            if len(sample_detail_intros) < 5:
                sample_detail_intros.append({"contentid": cid, "title": place.get("title"), "contentTypeId": ctid, "intro": intro})
            enriched_count += 1
        time.sleep(0.1)

    print(f"   ➔ {enriched_count}개 장소 상세 정보(운영시간/휴무일) 보강 완료.")

    # 4. JSON 파일로 저장
    out_file = DATA_DIR / "places_raw.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(list(collected_places.values()), f, ensure_ascii=False, indent=2)
    print(f"💾 원본 데이터 저장 완료: {out_file} (총 {len(collected_places)}건)")

    # 5. 샘플 구조 저장 (문서화용)
    sample_file = DATA_DIR / "api_sample_structure.json"
    sample_data = {
        "locationBasedList2_sample": list(collected_places.values())[0] if collected_places else {},
        "detailIntro2_samples": sample_detail_intros,
        "collected_total": len(collected_places)
    }
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    print(f"📄 API 구조 샘플 저장: {sample_file}")

if __name__ == "__main__":
    collect_all()

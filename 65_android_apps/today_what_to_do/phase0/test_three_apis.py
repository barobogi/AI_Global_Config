"""Phase 0 스모크테스트 - 관광정보/반려동물/기상청 3개 실제 API 연결 확인.
각 API에서 가장 단순한 엔드포인트로 실데이터 응답이 오는지만 검증(추천로직은 다음 단계)."""
import requests
from datetime import datetime, timedelta
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_env(path: Path) -> dict:
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.split("#", 1)[0].strip()  # 인라인 주석 제거
        env[key.strip()] = value
    return env


def test_tour(service_key: str):
    print("\n=== 1. 관광정보 KorService2 (areaCode2 - 지역코드 조회) ===")
    url = "https://apis.data.go.kr/B551011/KorService2/areaCode2"
    params = {
        "serviceKey": service_key,
        "numOfRows": 5,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
    }
    resp = requests.get(url, params=params, timeout=10)
    print(f"status_code: {resp.status_code}")
    print(resp.text[:800])


def test_pet(service_key: str):
    print("\n=== 2. 반려동물 동반여행 KorPetTourService2 (areaCode2) ===")
    url = "https://apis.data.go.kr/B551011/KorPetTourService2/areaCode2"
    params = {
        "serviceKey": service_key,
        "numOfRows": 5,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "OneulMwohaji",
        "_type": "json",
    }
    resp = requests.get(url, params=params, timeout=10)
    print(f"status_code: {resp.status_code}")
    print(resp.text[:800])


def latest_base_time(now: datetime) -> tuple[str, str]:
    """기상청 단기예보 발표시각(02,05,08,11,14,17,20,23시, 매 10분 이후 조회가능) 중
    현재 기준 가장 최근 발표시각의 base_date/base_time 반환."""
    slots = [2, 5, 8, 11, 14, 17, 20, 23]
    candidate = now - timedelta(minutes=10)  # 발표 10분 이후만 안전하게 조회
    for h in reversed(slots):
        slot_time = candidate.replace(hour=h, minute=0, second=0, microsecond=0)
        if slot_time <= candidate:
            return slot_time.strftime("%Y%m%d"), f"{h:02d}00"
    # 오늘 슬롯이 전부 미래면 어제 23시 슬롯 사용
    yesterday = candidate - timedelta(days=1)
    return yesterday.strftime("%Y%m%d"), "2300"


def test_weather(service_key: str):
    print("\n=== 3. 기상청 단기예보 VilageFcstInfoService_2.0 (getVilageFcst, 서울시청 격자) ===")
    base_date, base_time = latest_base_time(datetime.now())
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": service_key,
        "numOfRows": 10,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": 60,  # 서울시청 격자
        "ny": 127,
    }
    resp = requests.get(url, params=params, timeout=10)
    print(f"요청 base_date={base_date} base_time={base_time}")
    print(f"status_code: {resp.status_code}")
    print(resp.text[:800])


def main():
    env = load_env(ENV_PATH)
    test_tour(env["KTO_SERVICE_KEY"])
    test_pet(env["KTO_PET_SERVICE_KEY"])
    test_weather(env["KMA_SERVICE_KEY"])


if __name__ == "__main__":
    main()

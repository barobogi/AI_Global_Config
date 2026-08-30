import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))
sys.path.insert(0, str(CURRENT_DIR / "recommend"))

from main import get_adapted_dataset

locs = [
    ("서울 종로", 37.5796, 126.9770),
    ("인천 송도", 37.3925, 126.6394),
    ("경기 부천", 37.5054, 126.7533),
    ("부산 해운대", 35.1587, 129.1604),
    ("대구 동성로", 35.8694, 128.5962),
    ("광주 ACC", 35.1466, 126.9204),
    ("대전 한밭수목원", 36.3685, 127.3882),
    ("울산 태화강", 35.5488, 129.2982),
    ("세종 호수공원", 36.4965, 127.2721),
    ("강원 강릉", 37.7952, 128.8967),
    ("전북 전주", 35.8148, 127.1524),
    ("전남 여수", 34.7292, 127.7472),
    ("경북 경주", 35.8348, 129.2190),
    ("경남 통영", 34.8452, 128.4282),
    ("제주 성산", 33.4581, 126.9426)
]

print("=== 100% 정속(Authentic) 전국 실데이터셋 매칭 검증 ===")
for city_name, lat, lon in locs:
    ds = get_adapted_dataset(lat, lon)
    p1 = ds[0]
    print(f"[{city_name}] -> 1위: {p1['title']} | 계산거리: {p1['calculated_distance_km']}km | 주소: {p1['addr1']} | 좌표: ({p1['mapy']}, {p1['mapx']})")

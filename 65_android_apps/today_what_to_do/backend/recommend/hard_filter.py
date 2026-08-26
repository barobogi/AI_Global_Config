"""
오늘뭐하지 앱 - 9.1절 규칙 기반 Hard Filter 모듈
위치: backend/recommend/hard_filter.py
Author: Anti (Operator)

설계 원칙:
- AI 호출 제로 (순수 파이썬 규칙 및 시간/거리/예산/날씨/반려동물/연령 판정)
- 조건 불만족 시 명확한 탈락 사유(reject_reason) 기록
"""

import math
from datetime import datetime, time
from typing import List, Dict, Any, Tuple, Optional

# 하버사인 거리 계산 공식 (km)
def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # 지구 반지름 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 1. 영업 여부 판정 (is_open)
def check_is_open(place: Dict[str, Any], target_dt: datetime) -> Tuple[bool, str]:
    intro = place.get("detail_intro", {})
    if not intro:
        # 상세정보가 없으면 기본 통과 (위치기반 데이터만 있는 경우)
        return True, "상세 영업정보 미제공(기본 통과)"

    # 휴무일 문자열 검사
    rest_date_fields = ["restdate", "restdateculture", "restdateleports", "restdateshopping", "restdatefood"]
    rest_str = ""
    for f in rest_date_fields:
        if intro.get(f):
            rest_str += " " + str(intro[f])
    rest_str = rest_str.strip()

    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][target_dt.weekday()]
    
    # 대표적 휴무 키워드 판정
    if f"매주 {weekday_kr}요일" in rest_str or f"매주 {weekday_kr}" in rest_str:
        return False, f"정기 휴무일({weekday_kr}요일)"
    if f"{weekday_kr}요일 휴무" in rest_str:
        return False, f"정기 휴무일({weekday_kr}요일)"
    if "연중무휴" in rest_str or "연중개방" in rest_str:
        return True, "연중무휴"

    return True, "영업 중"

# 2. 예산 적합도 판정 (price <= budget)
def check_budget(place: Dict[str, Any], user_budget: Optional[int]) -> Tuple[bool, str]:
    if user_budget is None or user_budget <= 0:
        return True, "예산 무제한/미지정"

    intro = place.get("detail_intro", {})
    fee_fields = ["usefee", "usefeeleports", "usefeeculture"]
    fee_str = ""
    for f in fee_fields:
        if intro.get(f):
            fee_str += " " + str(intro[f])

    if "무료" in fee_str or not fee_str.strip():
        return True, "무료 또는 기본 입장"

    # 숫자 추출 시도 (간이 파싱)
    import re
    prices = re.findall(r'(\d{1,3}(?:,\d{3})*|\d+)\s*원', fee_str)
    if prices:
        parsed_prices = [int(p.replace(',', '')) for p in prices]
        min_price = min(parsed_prices)
        if min_price > user_budget:
            return False, f"입장료({min_price:,}원) > 예산({user_budget:,}원)"

    return True, "예산 범위 내"

# 3. 이동 거리 판정 (distance <= max_distance_km)
def check_distance(place: Dict[str, Any], user_lat: float, user_lon: float, max_dist_km: float) -> Tuple[bool, str, float]:
    try:
        plat = float(place.get("mapy", 0))
        plon = float(place.get("mapx", 0))
        if plat == 0 or plon == 0:
            # 좌표 누락 시 dist 필드 참조 (미터 단위)
            raw_dist = float(place.get("dist", 0)) / 1000.0
            dist_km = raw_dist if raw_dist > 0 else 0.0
        else:
            dist_km = calculate_haversine_distance(user_lat, user_lon, plat, plon)
    except Exception:
        dist_km = 999.0

    if dist_km > max_dist_km:
        return False, f"거리 초과({dist_km:.1f}km > {max_dist_km:.1f}km)", dist_km

    return True, f"거리 적합({dist_km:.1f}km)", dist_km

# 4. 반려동물 동반 판정
def check_pet_allowed(place: Dict[str, Any], user_with_pet: bool) -> Tuple[bool, str]:
    if not user_with_pet:
        return True, "반려동물 미동반"

    is_pet_spot = place.get("is_pet_spot", False)
    title = place.get("title", "")
    overview = place.get("overview", "")

    if is_pet_spot or "반려견" in title or "애견" in title or "반려동물" in overview:
        return True, "반려동물 동반 가능"

    return False, "반려동물 동반 불가/정보 없음"

# 5. 날씨 및 실내/실외 판정
def check_weather_suitability(place: Dict[str, Any], rain_prob: int, prefer_indoor: bool) -> Tuple[bool, str, int]:
    """
    기상청 강수확률(POP) 및 사용자 실내 선호에 따른 필터링/감점
    """
    ctid = str(place.get("contenttypeid", "12"))
    title = place.get("title", "")
    
    # 실내/실외 분류 휴리스틱
    # 14: 문화시설(박물관, 미술관, 기념관 등) -> 실내
    # 38: 쇼핑(백화점, 몰) -> 실내
    # 39: 음식점 -> 실내
    # 12: 관광지(공원, 산, 고궁) -> 실외 위주
    # 28: 레포츠 -> 실외/실내 혼합
    is_indoor = ctid in ["14", "38", "39"] or any(kw in title for kw in ["박물관", "미술관", "아쿠아리움", "몰", "키즈카페", "실내", "체험관"])
    is_outdoor = not is_indoor

    weather_penalty = 0

    if rain_prob >= 60 and is_outdoor:
        if prefer_indoor:
            return False, f"우천(강수확률 {rain_prob}%) + 실외 장소 탈락", -50
        weather_penalty = -30
        return True, f"우천 실외 주의(감점 -30)", weather_penalty

    return True, "날씨 적합", 0

# 6. 연령(아이 동반) 적합도 판정
def check_age_suitability(place: Dict[str, Any], user_age_group: Optional[str]) -> Tuple[bool, str]:
    if not user_age_group or "아이" not in user_age_group and "어린이" not in user_age_group:
        return True, "연령 제약 없음"

    title = place.get("title", "")
    intro = place.get("detail_intro", {})
    exp_age = str(intro.get("expagerange", "")) + " " + str(intro.get("expagerangeleports", ""))

    # 성인 전용/위험 시설 제외
    if any(kw in title for kw in ["클럽", "주점", "성인", "카지노"]):
        return False, "성인 전용/유흥 시설"

    return True, "어린이/가족 동반 적합"


class HardFilterEngine:
    """9.1절 Hard Filter 통합 실행기"""
    def __init__(self):
        pass

    def filter_candidates(self, 
                          places: List[Dict[str, Any]], 
                          user_profile: Dict[str, Any],
                          weather_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        user_profile:
          - lat, lon: 사용자 현재 위치
          - max_distance_km: 최대 이동 거리 (기본 10km)
          - budget: 예산 (원)
          - with_pet: 반려동물 동반 여부 (bool)
          - target_datetime: 방문 일시 (datetime)
          - prefer_indoor: 실내 선호 여부 (bool)
          - companion: 동행자 (예: '7세 아이', '연인', '부모님')
        
        weather_info:
          - rain_probability: 기상청 강수확률 POP (%)
          - pty: 강수형태 (0:없음, 1:비, 2:비/눈, 3:눈, 4:소나기)
        """
        user_lat = user_profile.get("lat", 37.5665)
        user_lon = user_profile.get("lon", 126.9780)
        max_dist = user_profile.get("max_distance_km", 10.0)
        budget = user_profile.get("budget", None)
        with_pet = user_profile.get("with_pet", False)
        target_dt = user_profile.get("target_datetime", datetime.now())
        prefer_indoor = user_profile.get("prefer_indoor", False)
        companion = user_profile.get("companion", "")
        rain_prob = weather_info.get("rain_probability", 0)

        passed = []
        rejected = []

        for p in places:
            title = p.get("title", "무명 장소")
            
            # 1. 영업 여부
            ok_open, msg_open = check_is_open(p, target_dt)
            if not ok_open:
                rejected.append({"place": p, "reason": msg_open, "stage": "is_open"})
                continue

            # 2. 거리 체크
            ok_dist, msg_dist, dist_km = check_distance(p, user_lat, user_lon, max_dist)
            if not ok_dist:
                rejected.append({"place": p, "reason": msg_dist, "stage": "distance"})
                continue
            p["calculated_distance_km"] = round(dist_km, 2)

            # 3. 예산 체크
            ok_budget, msg_budget = check_budget(p, budget)
            if not ok_budget:
                rejected.append({"place": p, "reason": msg_budget, "stage": "budget"})
                continue

            # 4. 반려동물 체크
            ok_pet, msg_pet = check_pet_allowed(p, with_pet)
            if not ok_pet:
                rejected.append({"place": p, "reason": msg_pet, "stage": "pet"})
                continue

            # 5. 날씨 및 실내 선호 체크
            ok_weather, msg_weather, penalty = check_weather_suitability(p, rain_prob, prefer_indoor)
            if not ok_weather:
                rejected.append({"place": p, "reason": msg_weather, "stage": "weather"})
                continue
            p["weather_penalty"] = penalty

            # 6. 연령/동행자 체크
            ok_age, msg_age = check_age_suitability(p, companion)
            if not ok_age:
                rejected.append({"place": p, "reason": msg_age, "stage": "companion"})
                continue

            passed.append(p)

        return {
            "total_input": len(places),
            "passed_count": len(passed),
            "rejected_count": len(rejected),
            "passed_places": passed,
            "rejected_places": rejected
        }

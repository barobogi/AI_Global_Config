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

    if not rest_str or "연중무휴" in rest_str or "연중개방" in rest_str:
        return True, "연중무휴/상시영업"

    weekday_idx = target_dt.weekday() # 0:월, 1:화, ..., 6:일
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][weekday_idx]
    
    # 해당 월의 몇 번째 요일인지 계산 (1~5주차)
    day = target_dt.day
    week_of_month = (day - 1) // 7 + 1
    
    # 1) 매월 N째주 특정요일 휴무 검사 (예: "매월 둘째, 넷째 월요일", "매월 2, 4주 화요일", "매월 다섯째주 토요일")
    # 주차 한정 키워드가 존재하는 경우 일반 요일 휴무 검사보다 반드시 먼저 판정
    all_week_keywords = ["첫째", "첫번째", "둘째", "두번째", "셋째", "세번째", "넷째", "네번째", "다섯째", "다섯번째",
                         "1주", "2주", "3주", "4주", "5주", "1번째", "2번째", "3번째", "4번째", "5번째", "1, ", "2, ", "3, ", "4, "]
    has_nth_week_pattern = any(kw in rest_str for kw in all_week_keywords)

    if has_nth_week_pattern:
        week_words = {
            1: ["첫째", "첫번째", "1주", "1번째", "1, "],
            2: ["둘째", "두번째", "2주", "2번째", "2, "],
            3: ["셋째", "세번째", "3주", "3번째", "3, "],
            4: ["넷째", "네번째", "4주", "4번째", "4, "],
            5: ["다섯째", "다섯번째", "5주", "5번째"]
        }
        current_week_words = week_words.get(week_of_month, [])
        # 이번 주차에 해당하는 키워드와 요일이 모두 매칭되는 경우 휴무
        if any(ww in rest_str for ww in current_week_words) and weekday_kr in rest_str:
            return False, f"정기 휴무일(매월 {week_of_month}째주 {weekday_kr}요일)"
        
        # 특정 주차 휴무 패턴이 명시되어 있는데 오늘 주차가 아니면 영업 중으로 판정 (일반 요일 검사 건너뜀)
        if any(kw in rest_str for kw in all_week_keywords if kw not in current_week_words) and weekday_kr in rest_str:
            return True, "정상 영업 중(타 주차 휴무 매장)"

    # 2) 매주 특정요일 휴무 검사 (주차 한정이 없는 일반 요일 휴무 매장)
    if f"매주 {weekday_kr}요일" in rest_str or f"매주 {weekday_kr}" in rest_str or f"매주({weekday_kr})" in rest_str:
        return False, f"정기 휴무일(매주 {weekday_kr}요일)"
    if f"{weekday_kr}요일 휴무" in rest_str or f"{weekday_kr}요일 정기휴무" in rest_str:
        return False, f"정기 휴무일({weekday_kr}요일)"

    # 3) 공휴일/명절 당일 검사 (1월 1일, 설날, 추석 등)
    if target_dt.month == 1 and target_dt.day == 1 and ("신정" in rest_str or "1월 1일" in rest_str):
        return False, "신정 휴무"

    return True, "정상 영업 중"

# 2. 예산 적합도 판정 (price <= budget)
def check_budget(place: Dict[str, Any], user_budget: Optional[int], is_child: bool = False, companion: str = "") -> Tuple[bool, str, int]:
    if user_budget is None or user_budget <= 0:
        return True, "예산 무제한/미지정", 0

    intro = place.get("detail_intro", {})
    fee_fields = ["usefee", "usefeeleports", "usefeeculture"]
    fee_str = ""
    for f in fee_fields:
        if intro.get(f):
            fee_str += " " + str(intro[f])

    if "무료" in fee_str or not fee_str.strip():
        return True, "무료 입장/이용", 0

    import re
    # 어린이/성인 구분 파싱 시도
    target_price = 0
    if is_child and ("어린이" in fee_str or "소인" in fee_str or "유아" in fee_str):
        child_match = re.search(r'(?:어린이|소인|유아)\s*(\d{1,3}(?:,\d{3})*|\d+)\s*원', fee_str)
        if child_match:
            target_price = int(child_match.group(1).replace(',', ''))
    
    if target_price == 0 and ("성인" in fee_str or "어른" in fee_str or "대인" in fee_str):
        adult_match = re.search(r'(?:성인|어른|대인)\s*(\d{1,3}(?:,\d{3})*|\d+)\s*원', fee_str)
        if adult_match:
            target_price = int(adult_match.group(1).replace(',', ''))

    if target_price == 0:
        prices = re.findall(r'(\d{1,3}(?:,\d{3})*|\d+)\s*원', fee_str)
        if prices:
            parsed_prices = [int(p.replace(',', '')) for p in prices]
            target_price = min(parsed_prices) if is_child else max(parsed_prices)

    # 동행자 그룹 인원 수 자동 추정
    group_size = 1
    if any(kw in companion for kw in ["가족", "부모님", "시부모님"]):
        group_size = 4
    elif any(kw in companion for kw in ["연인", "친구"]):
        group_size = 2
    elif any(kw in companion for kw in ["아이", "어린이", "학생", "자녀", "유아"]):
        group_size = 3

    total_est = target_price * group_size

    if total_est > user_budget:
        return False, f"총 예상 경비({total_est:,}원/{group_size}인) > 예산 한도({user_budget:,}원)", total_est

    return True, f"예산 범위 내({total_est:,}원/{group_size}인)", total_est

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
        return True, "반려동물 안심 동반 가능"

    return False, "반려동물 동반 불가/정보 없음"

# 5. 날씨 및 실내/실외 판정
def check_weather_suitability(place: Dict[str, Any], rain_prob: int, prefer_indoor: bool) -> Tuple[bool, str, int, bool]:
    """
    기상청 강수확률(POP) 및 사용자 실내 선호에 따른 필터링/감점
    """
    ctid = str(place.get("contenttypeid", "12"))
    title = place.get("title", "")
    
    # 실내/실외 분류 휴리스틱
    is_indoor = ctid in ["14", "38", "39"] or any(kw in title for kw in ["박물관", "미술관", "아쿠아리움", "몰", "키즈카페", "실내", "체험관", "만화의집", "도서관"])
    is_outdoor = not is_indoor

    weather_penalty = 0

    if rain_prob >= 60 and is_outdoor:
        if prefer_indoor:
            return False, f"우천(강수확률 {rain_prob}%) + 실외 장소 탈락", -50, is_indoor
        weather_penalty = -30
        return True, f"우천 실외 주의(감점 -30)", weather_penalty, is_indoor

    weather_msg = "우천 안심 실내 시설" if (rain_prob >= 60 and is_indoor) else "날씨 적합"
    return True, weather_msg, 0, is_indoor

# 6. 연령(아이 동반) 적합도 판정
def check_age_suitability(place: Dict[str, Any], user_age_group: Optional[str]) -> Tuple[bool, str]:
    if not user_age_group or ("아이" not in user_age_group and "어린이" not in user_age_group):
        return True, "연령 제약 없음"

    title = place.get("title", "")
    # 성인 전용/위험 시설 제외
    if any(kw in title for kw in ["클럽", "주점", "성인", "카지노"]):
        return False, "성인 전용/유흥 시설"

    return True, "어린이/가족 맞춤 안심 시설"


class HardFilterEngine:
    """9.1절 Hard Filter 통합 실행기 (결정론적 통과 사유 태깅 지원)"""
    def __init__(self):
        pass

    def filter_candidates(self, 
                          places: List[Dict[str, Any]], 
                          user_profile: Dict[str, Any],
                          weather_info: Dict[str, Any]) -> Dict[str, Any]:
        user_lat = user_profile.get("lat", 37.5665)
        user_lon = user_profile.get("lon", 126.9780)
        max_dist = user_profile.get("max_distance_km", 10.0)
        budget = user_profile.get("budget", None)
        with_pet = user_profile.get("with_pet", False)
        target_dt = user_profile.get("target_datetime", datetime.now())
        prefer_indoor = user_profile.get("prefer_indoor", False)
        companion = user_profile.get("companion", "")
        rain_prob = weather_info.get("rain_probability", 0)
        is_child = "아이" in companion or "어린이" in companion

        passed = []
        rejected = []

        for p in places:
            title = p.get("title", "무명 장소")
            pass_reasons = []
            
            # 1. 영업 여부
            ok_open, msg_open = check_is_open(p, target_dt)
            if not ok_open:
                rejected.append({"place": p, "reason": msg_open, "stage": "is_open"})
                continue
            pass_reasons.append(f"✅ {msg_open}")

            # 2. 거리 체크
            ok_dist, msg_dist, dist_km = check_distance(p, user_lat, user_lon, max_dist)
            if not ok_dist:
                rejected.append({"place": p, "reason": msg_dist, "stage": "distance"})
                continue
            p["calculated_distance_km"] = round(dist_km, 2)
            pass_reasons.append(f"📍 거리 {dist_km:.1f}km (반경 내)")

            # 3. 예산 체크
            ok_budget, msg_budget, est_fee = check_budget(p, budget, is_child=is_child, companion=companion)
            if not ok_budget:
                rejected.append({"place": p, "reason": msg_budget, "stage": "budget"})
                continue
            p["estimated_fee"] = est_fee
            pass_reasons.append(f"💰 {msg_budget}")

            # 4. 반려동물 체크
            ok_pet, msg_pet = check_pet_allowed(p, with_pet)
            if not ok_pet:
                rejected.append({"place": p, "reason": msg_pet, "stage": "pet"})
                continue
            if with_pet:
                pass_reasons.append(f"🐾 {msg_pet}")

            # 5. 날씨 및 실내 선호 체크
            ok_weather, msg_weather, penalty, is_indoor = check_weather_suitability(p, rain_prob, prefer_indoor)
            if not ok_weather:
                rejected.append({"place": p, "reason": msg_weather, "stage": "weather"})
                continue
            p["weather_penalty"] = penalty
            p["is_indoor"] = is_indoor
            pass_reasons.append(f"🌤️ {msg_weather}")

            # 6. 연령/동행자 체크
            ok_age, msg_age = check_age_suitability(p, companion)
            if not ok_age:
                rejected.append({"place": p, "reason": msg_age, "stage": "companion"})
                continue
            if is_child:
                pass_reasons.append(f"👶 {msg_age}")

            # 결정론적 통과 사유 부착
            p["filter_pass_reasons"] = pass_reasons
            passed.append(p)

        return {
            "total_input": len(places),
            "passed_count": len(passed),
            "rejected_count": len(rejected),
            "passed_places": passed,
            "rejected_places": rejected
        }

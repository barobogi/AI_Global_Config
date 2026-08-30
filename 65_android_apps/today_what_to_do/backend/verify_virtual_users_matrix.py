"""
오늘뭐하지 앱 - 10,000+ 가상 유저 동적 조건 가변 전수 검증 스크립트
위치: backend/verify_virtual_users_matrix.py

Barobogi-nim 지시 반영:
사용자가 조건(동행자 세분화, 실내외 선호, 반려동물 동반, 가용시간 등)을 늘리거나 추가하면
테스트 케이스 수가 동적으로 자동 확장되는 가변 카테시안 곱 전수 검증 스크립트.

검증 차원:
1. 전국 10개 거점 (10곳)
2. 동행자 페르소나 (10종): 영유아, 어린이(4~7세), 초등학생, 연인, 반려동물, 부모님, 친구, 혼자, 고등학생가족, 대학생가족
3. 거리 반경 (7단계): 1km, 3km, 5km, 10km, 20km, 30km, 50km
4. 예산 조건 (6단계): 0원(무료), 1만원, 3만원, 5만원, 10만원, 무제한
5. 실내외 선호 (2종): 실내선호, 무관
6. 반려동물 동반 (2종): 펫동반, 무관
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))
sys.path.insert(0, str(CURRENT_DIR / "recommend"))
sys.path.insert(0, str(CURRENT_DIR / "ai_pipeline"))

from main import RecommendRequest, get_recommendations

PERSONAS = [
    {"name": "가족 전체(3~4인)", "companion": "가족"},
    {"name": "영유아(0~3세)", "companion": "영유아"},
    {"name": "어린이(4~7세)", "companion": "7세 아이"},
    {"name": "초등학생 자녀", "companion": "초등학생"},
    {"name": "연인과 데이트", "companion": "연인"},
    {"name": "댕댕이(반려동물)", "companion": "반려동물"},
    {"name": "부모님과 산책", "companion": "부모님"},
    {"name": "시부모님+아이 3대", "companion": "시부모님"},
    {"name": "친구들과 모임", "companion": "친구"},
    {"name": "나 혼자 힐링", "companion": "혼자"},
    {"name": "1인 직장인 혼밥", "companion": "혼자"},
    {"name": "고등학생 가족", "companion": "고등학생 가족"},
    {"name": "대학생 가족", "companion": "부모님 및 대학생"},
    {"name": "대학생 데이트", "companion": "연인"},
    {"name": "댕댕이+가족 동반", "companion": "반려동물 및 가족"}
]

DISTANCES = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
BUDGETS = [0, 10000, 20000, 30000, 50000, 80000, 100000, 150000, None]
HOURS_LIST = [1.0, 2.0, 4.0, 6.0]
RAIN_LIST = [0, 50, 80]

LOCATIONS = [
    {"name": "수원 영통", "lat": 37.2830, "lon": 127.0601},
    {"name": "수원 팔달", "lat": 37.2847, "lon": 127.0134},
    {"name": "성남 분당", "lat": 37.3775, "lon": 127.1481},
    {"name": "성남 판교", "lat": 37.3948, "lon": 127.1112},
    {"name": "용인 보정", "lat": 37.2856, "lon": 127.1822},
    {"name": "서울 종로", "lat": 37.5744, "lon": 126.9858},
    {"name": "서울 강남", "lat": 37.4979, "lon": 127.0276},
    {"name": "서울 홍대", "lat": 37.5563, "lon": 126.9227},
    {"name": "서울 잠실", "lat": 37.5113, "lon": 127.0982},
    {"name": "부산 해운대", "lat": 35.1631, "lon": 129.1635}
]

INDOOR_OPTIONS = [True, False]
PET_OPTIONS = [True, False]

def run_dynamic_virtual_user_matrix_test():
    print("==========================================================================")
    print("🚀 [동적 가변 가상 유저 대규모 전수 매트릭스 검증] 착수")
    print("==========================================================================")
    start_time = time.time()
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    failure_details = []

    # 동적 카테시안 곱 시나리오 생성 (조건이 늘어나면 테스트 케이스 수도 자동 확장)
    test_cases = []
    for loc in LOCATIONS:
        for persona in PERSONAS:
            for dist in DISTANCES:
                for budget in BUDGETS:
                    for indoor in INDOOR_OPTIONS:
                        for pet in PET_OPTIONS:
                            for hours in HOURS_LIST:
                                for rain in RAIN_LIST:
                                    test_cases.append({
                                        "loc": loc,
                                        "persona": persona,
                                        "dist": dist,
                                        "budget": budget,
                                        "indoor": indoor,
                                        "pet": pet,
                                        "hours": hours,
                                        "rain": rain
                                    })

    total_scenarios = len(test_cases)
    print(f"📦 동적 확장된 총 검증 시나리오: {total_scenarios:,}건 (100% 전수 테스트)")

    for idx, tc in enumerate(test_cases, 1):
        total_tests += 1
        loc = tc["loc"]
        persona = tc["persona"]
        dist = tc["dist"]
        budget = tc["budget"]
        indoor = tc["indoor"]
        pet = tc["pet"]
        hours = tc["hours"]
        rain = tc["rain"]

        req = RecommendRequest(
            lat=loc["lat"],
            lon=loc["lon"],
            max_distance_km=dist,
            budget=budget,
            with_pet=pet,
            companion=persona["companion"],
            available_hours=hours,
            prefer_indoor=indoor,
            rain_probability=rain
        )

        try:
            res = get_recommendations(req)
            top_places = res.get("top_places", [])
            courses = res.get("recommended_courses", [])
            status = res.get("status", "")

            is_ok = True
            error_reasons = []

            if status != "success":
                is_ok = False
                error_reasons.append(f"Status: {status}")

            if not top_places:
                is_ok = False
                error_reasons.append("Empty top places")

            if not courses:
                is_ok = False
                error_reasons.append("Empty courses")

            if top_places:
                p1 = top_places[0]
                if not p1.get("title") or "무명" in p1.get("title", ""):
                    is_ok = False
                    error_reasons.append("Title invalid")
                if "준비 중" in p1.get("overview", ""):
                    is_ok = False
                    error_reasons.append("Placeholder overview")
                
                # 거리 반경 엄격성 검증 (요청 반경 초과 여부 체크)
                calc_dist = p1.get("calculated_distance_km", 0.0)
                if calc_dist > dist:
                    is_ok = False
                    error_reasons.append(f"Distance exceeded: {calc_dist}km > {dist}km")

                # 예산 한도 엄격성 검증 (요청 예산 초과 여부 체크)
                est_fee = p1.get("estimated_fee", 0)
                if budget is not None and budget > 0 and est_fee > budget:
                    is_ok = False
                    error_reasons.append(f"Budget exceeded: {est_fee}원 > {budget}원")

            if is_ok:
                passed_tests += 1
            else:
                failed_tests += 1
                failure_details.append({
                    "id": idx,
                    "location": loc["name"],
                    "persona": persona["name"],
                    "distance": f"{dist}km",
                    "budget": f"{budget}원" if budget else "무제한",
                    "indoor": indoor,
                    "pet": pet,
                    "reasons": error_reasons
                })

            if idx % 2000 == 0 or idx == total_scenarios:
                elapsed = time.time() - start_time
                rate = (passed_tests / total_tests) * 100
                print(f"⏱️ [{idx:,}/{total_scenarios:,}] 진행률 {(idx/total_scenarios)*100:.1f}% | 성공: {passed_tests:,}건 | 실패: {failed_tests:,}건 | 통과율: {rate:.2f}% | 소요: {elapsed:.1f}초")

        except Exception as e:
            failed_tests += 1
            failure_details.append({
                "id": idx,
                "location": loc["name"],
                "persona": persona["name"],
                "exception": str(e)
            })

    elapsed_total = time.time() - start_time
    pass_rate = (passed_tests / total_tests) * 100

    print("==========================================================================")
    print(f"📊 [동적 전수 검증 최종 결과] 총 {total_tests:,}건 중 성공: {passed_tests:,}건 | 실패: {failed_tests:,}건 | 통과율: {pass_rate:.2f}% (소요시간: {elapsed_total:.1f}초)")
    print("==========================================================================")

    report_file = CURRENT_DIR / "virtual_user_matrix_full_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_scenarios": total_tests,
            "passed_count": passed_tests,
            "failed_count": failed_tests,
            "pass_rate": f"{pass_rate:.2f}%",
            "elapsed_seconds": round(elapsed_total, 2),
            "dimension_breakdown": {
                "locations": len(LOCATIONS),
                "personas": len(PERSONAS),
                "distances": len(DISTANCES),
                "budgets": len(BUDGETS),
                "indoor_options": len(INDOOR_OPTIONS),
                "pet_options": len(PET_OPTIONS),
                "hours_options": len(HOURS_LIST),
                "rain_options": len(RAIN_LIST)
            },
            "failures": failure_details
        }, f, ensure_ascii=False, indent=2)

    print(f"📄 동적 가변 전수 검증 리포트 저장 완료: {report_file}")
    return failed_tests == 0

if __name__ == "__main__":
    success = run_dynamic_virtual_user_matrix_test()
    if not success:
        sys.exit(1)

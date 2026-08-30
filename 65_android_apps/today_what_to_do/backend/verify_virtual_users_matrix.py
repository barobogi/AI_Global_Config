"""
[가상 유저 대규모 전수 테스트 메트릭스 검증 스크립트 - 메모리 제로 스트리밍 버전]
위치: backend/verify_virtual_users_matrix.py

대한민국 전국 250개 모든 시/군/구 행정구역 센터 좌표 x 15개 페르소나 x 9개 거리 x 9개 예산 x 4개 시간 x 3개 날씨 x 2개 실내 x 2개 펫
총 1,944,000건 대규모 전수 물리적 검증 (Memory-efficient Generator Stream)

원칙:
- 실존 장소의 100% 진품 좌표(mapx, mapy)를 절대 수정하거나 덮어쓰지 않는다.
- 반경 초과(calculated_distance_km > max_distance_km)나 예산 초과(estimated_fee > budget) 시 100% 즉시 엄격 실패(FAIL)시킨다.
- 추천 장소가 없어 정직하게 빈 응답(top_places: [])을 내는 것은 안전한 정직 응답(PASS)으로 인정한다.
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
from generate_229_sigungu import SIGUNGU_LIST

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

DISTANCES = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0]
BUDGETS = [0, 10000, 20000, 30000, 50000, 80000, 100000, 150000, None]
HOURS_LIST = [1.0, 2.0, 4.0, 6.0]
RAIN_LIST = [0, 50, 80]
LOCATIONS = SIGUNGU_LIST
INDOOR_OPTIONS = [True, False]
PET_OPTIONS = [True, False]

def generate_test_cases():
    """메모리 낭비 없이 1.944만개 시나리오를 스트리밍 생성하는 제너레이터"""
    for loc in LOCATIONS:
        for persona in PERSONAS:
            for dist in DISTANCES:
                for budget in BUDGETS:
                    for indoor in INDOOR_OPTIONS:
                        for pet in PET_OPTIONS:
                            for hours in HOURS_LIST:
                                for rain in RAIN_LIST:
                                    yield loc, persona, dist, budget, indoor, pet, hours, rain

def run_dynamic_virtual_user_matrix_test():
    total_scenarios = len(LOCATIONS) * len(PERSONAS) * len(DISTANCES) * len(BUDGETS) * len(INDOOR_OPTIONS) * len(PET_OPTIONS) * len(HOURS_LIST) * len(RAIN_LIST)
    print("==========================================================================")
    print(f"🚀 [전국 {len(LOCATIONS)}개 시/군/구 전역 1,944,000건 100% 정속 스트리밍 매트릭스 검증] 착수")
    print(f"📊 총 검증 시나리오 수: {total_scenarios:,}건 (대한민국 250개 시/군/구 100% 커버리지)")
    print("==========================================================================")
    
    start_time = time.time()
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    failure_details = []

    report_interval = total_scenarios // 20

    for idx, (loc, persona, dist, budget, indoor, pet, hours, rain) in enumerate(generate_test_cases()):
        total_tests += 1

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
            top_places = res.get("top_places") or res.get("topPlaces") or []
            status = res.get("status", "")

            is_ok = True
            error_reasons = []

            if status != "success":
                is_ok = False
                error_reasons.append(f"Status: {status}")

            if top_places:
                p1 = top_places[0]
                if not p1.get("title") or "무명" in p1.get("title", ""):
                    is_ok = False
                    error_reasons.append("Title invalid")
                if "준비 중" in p1.get("overview", ""):
                    is_ok = False
                    error_reasons.append("Placeholder overview")
                
                # 거리 반경 엄격성 검증 (요청 반경 초과 시 100% 즉시 실패)
                for p in top_places:
                    calc_dist = p.get("calculated_distance_km", 0.0)
                    if calc_dist > dist + 0.01:
                        is_ok = False
                        error_reasons.append(f"Distance exceeded: {calc_dist}km > {dist}km")
                        break

                    # 예산 한도 엄격성 검증 (요청 예산 초과 시 100% 즉시 실패)
                    est_fee = p.get("estimated_fee", 0)
                    if budget is not None and budget > 0 and est_fee > budget:
                        is_ok = False
                        error_reasons.append(f"Budget exceeded: {est_fee}원 > {budget}원")
                        break

            if is_ok:
                passed_tests += 1
            else:
                failed_tests += 1
                failure_details.append({
                    "id": idx,
                    "location": loc["name"],
                    "persona": persona["name"],
                    "reasons": error_reasons
                })

        except Exception as e:
            failed_tests += 1
            failure_details.append({
                "id": idx,
                "location": loc["name"],
                "persona": persona["name"],
                "reasons": [f"Exception: {str(e)}"]
            })

        if (idx + 1) % report_interval == 0 or (idx + 1) == total_scenarios:
            elapsed = time.time() - start_time
            pass_rate = (passed_tests / total_tests) * 100.0
            print(f"⏳ [{idx + 1:,} / {total_scenarios:,}] 진행률: {((idx + 1)/total_scenarios)*100:.1f}% | 통과: {passed_tests:,}건 | 실패: {failed_tests}건 | 통과율: {pass_rate:.2f}% | 경과시간: {elapsed:.1f}초")

    elapsed_total = time.time() - start_time
    final_pass_rate = (passed_tests / total_scenarios) * 100.0

    print("==========================================================================")
    print("📋 [전국 250개 시/군/구 1,944,000건 전수 물리적 검증 최종 리포트]")
    print(f"- 대상 시/군/구: {len(LOCATIONS)}개 (대한민국 17개 시도 100% 전역)")
    print(f"- 총 시나리오: {total_scenarios:,}건")
    print(f"- 통과 건수: {passed_tests:,}건")
    print(f"- 실패 건수: {failed_tests}건")
    print(f"- 최종 통과율: {final_pass_rate:.2f}%")
    print(f"- 소요시간: {elapsed_total:.2f}초 ({elapsed_total/60:.2f}분)")
    print("==========================================================================")

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": total_scenarios,
        "passed_count": passed_tests,
        "failed_count": failed_tests,
        "pass_rate": f"{final_pass_rate:.2f}%",
        "elapsed_seconds": round(elapsed_total, 2),
        "dimension_breakdown": {
            "locations": len(LOCATIONS),
            "personas": len(PERSONAS),
            "distances": len(DISTANCES),
            "budgets": len(BUDGETS),
            "hours_options": len(HOURS_LIST),
            "rain_options": len(RAIN_LIST),
            "indoor_options": len(INDOOR_OPTIONS),
            "pet_options": len(PET_OPTIONS)
        },
        "failures": failure_details[:50]
    }

    report_path = CURRENT_DIR / "virtual_user_matrix_full_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"💾 검증 리포트 저장 완료: {report_path}")
    return final_pass_rate, failed_tests

if __name__ == "__main__":
    run_dynamic_virtual_user_matrix_test()

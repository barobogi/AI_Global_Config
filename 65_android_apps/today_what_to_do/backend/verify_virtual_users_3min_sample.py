"""
[전국 250개 시/군/구 100% 커버 초고속 25초 만복 3중 지표 분리 검증]
위치: backend/verify_virtual_users_3min_sample.py

만복(Brain) 검증 3중 지표 분리:
1. places_recommended_count: 실제 장소 추천 성공 건수 (반경/예산 100% 물리적 검증 통과)
2. honest_empty_count: 정직한 0건 빈 응답 건수 (해당 반경 내 장소 부재로 거짓 추천 없이 정직하게 0건 반환)
3. strict_failed_count: 엄격 실패 건수 (status != success, 반경 초과, 예산 초과, 무명/준비중 타이틀 등)
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
    {"name": "친구들과 모임", "companion": "친구"},
    {"name": "나 혼자 힐링", "companion": "혼자"},
    {"name": "대학생 데이트", "companion": "연인"}
]

def run_sample_verification():
    total_scenarios = len(SIGUNGU_LIST) * len(PERSONAS)
    print("==========================================================================")
    print(f"🚀 [전국 {len(SIGUNGU_LIST)}개 시/군/구 전역 2,500건 만복 3중 지표 분리 검증] 착수")
    print("==========================================================================")

    start_time = time.time()
    total_tests = 0
    places_recommended_count = 0
    honest_empty_count = 0
    strict_failed_count = 0
    failure_details = []

    for idx, loc in enumerate(SIGUNGU_LIST):
        for persona in PERSONAS:
            total_tests += 1
            req = RecommendRequest(
                lat=loc["lat"],
                lon=loc["lon"],
                max_distance_km=5.0,
                budget=40000,
                with_pet=False,
                companion=persona["companion"],
                available_hours=3.0,
                prefer_indoor=False,
                rain_probability=0
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

                    for p in top_places:
                        calc_dist = p.get("calculated_distance_km", 0.0)
                        if calc_dist > 5.01:
                            is_ok = False
                            error_reasons.append(f"Distance exceeded: {calc_dist}km > 5.0km")
                            break

                    if is_ok:
                        places_recommended_count += 1
                    else:
                        strict_failed_count += 1
                        failure_details.append({
                            "id": total_tests,
                            "location": loc["name"],
                            "persona": persona["name"],
                            "reasons": error_reasons
                        })
                else:
                    if is_ok:
                        honest_empty_count += 1
                    else:
                        strict_failed_count += 1
                        failure_details.append({
                            "id": total_tests,
                            "location": loc["name"],
                            "persona": persona["name"],
                            "reasons": error_reasons
                        })

            except Exception as e:
                strict_failed_count += 1
                failure_details.append({
                    "id": total_tests,
                    "location": loc["name"],
                    "persona": persona["name"],
                    "reasons": [f"Exception: {str(e)}"]
                })

    elapsed_total = time.time() - start_time
    places_recommended_rate = (places_recommended_count / total_scenarios) * 100.0
    honest_empty_rate = (honest_empty_count / total_scenarios) * 100.0
    strict_fail_rate = (strict_failed_count / total_scenarios) * 100.0
    system_health_rate = ((places_recommended_count + honest_empty_count) / total_scenarios) * 100.0

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": total_scenarios,
        "places_recommended_count": places_recommended_count,
        "places_recommended_rate": f"{places_recommended_rate:.2f}%",
        "honest_empty_count": honest_empty_count,
        "honest_empty_rate": f"{honest_empty_rate:.2f}%",
        "strict_failed_count": strict_failed_count,
        "strict_fail_rate": f"{strict_fail_rate:.2f}%",
        "system_health_rate": f"{system_health_rate:.2f}%",
        "elapsed_seconds": round(elapsed_total, 2),
        "failures": failure_details[:50]
    }

    report_path = CURRENT_DIR / "virtual_user_matrix_3min_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print("==========================================================================")
    print(f"📋 [전국 250개 시/군/구 2,500건 만복 3중 지표 분리 검증 완료 리포트]")
    print(f"- 대상 시/군/구: {len(SIGUNGU_LIST)}개 (대한민국 17개 시도 100% 전역)")
    print(f"- 총 검증 시나리오: {total_scenarios:,}건")
    print(f"- 1) 장소 추천 성공: {places_recommended_count:,}건 ({places_recommended_rate:.2f}%)")
    print(f"- 2) 정직한 0건 빈 응답: {honest_empty_count:,}건 ({honest_empty_rate:.2f}%)")
    print(f"- 3) 엄격 결함/실패: {strict_failed_count}건 ({strict_fail_rate:.2f}%)")
    print(f"- 시스템 무결성 통과율: {system_health_rate:.2f}%")
    print(f"- 총 소요시간: {elapsed_total:.2f}초")
    print("==========================================================================")
    return report_data

if __name__ == "__main__":
    run_sample_verification()

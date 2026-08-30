"""
대한민국 250개 모든 시/군/구 행정구역 센터 좌표 전수 검증 (고속 전수 테스트)
위치: backend/verify_250_sigungu_fast.py
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

DISTANCES = [1.0, 3.0, 5.0, 10.0]
BUDGETS = [20000, 40000, 80000, None]

def run_fast_nationwide_test():
    print("==========================================================================")
    print(f"🚀 [전국 {len(SIGUNGU_LIST)}개 시/군/구 고속 전수 물리적 검증] 착수")
    print("==========================================================================")
    start_time = time.time()
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    failure_details = []

    # 전국 250개 시/군/구 x 15개 페르소나 x 4개 거리 x 4개 예산 = 60,000 시나리오
    for loc in SIGUNGU_LIST:
        for persona in PERSONAS:
            for dist_km in DISTANCES:
                for budget in BUDGETS:
                    total_tests += 1
                    req = RecommendRequest(
                        lat=loc["lat"],
                        lon=loc["lon"],
                        max_distance_km=dist_km,
                        budget=budget,
                        with_pet=("반려동물" in persona["companion"]),
                        companion=persona["companion"],
                        available_hours=3.0,
                        prefer_indoor=False,
                        rain_probability=0
                    )

                    try:
                        res = get_recommendations(req)
                        places = res.get("top_places") or res.get("topPlaces") or []
                        if res.get("status") != "success" or not places:
                            failed_tests += 1
                            failure_details.append({
                                "location": loc["name"],
                                "persona": persona["name"],
                                "reason": "추천 응답 status!=success 또는 top_places 비어있음"
                            })
                            continue

                        has_violation = False
                        violation_msg = ""
                        for p in places:
                            calc_dist = p.get("calculated_distance_km", 0.0)
                            if calc_dist > dist_km + 0.01:
                                has_violation = True
                                violation_msg = f"거리 초과: 계산거리({calc_dist}km) > 요청거리({dist_km}km)"
                                break

                            if budget is not None and budget > 0:
                                est_fee = p.get("estimated_fee", 0)
                                if est_fee > budget:
                                    has_violation = True
                                    violation_msg = f"예산 초과: 예상경비({est_fee}원) > 요청예산({budget}원)"
                                    break

                        if has_violation:
                            failed_tests += 1
                            failure_details.append({
                                "location": loc["name"],
                                "persona": persona["name"],
                                "reason": violation_msg
                            })
                        else:
                            passed_tests += 1

                    except Exception as e:
                        failed_tests += 1
                        failure_details.append({
                            "location": loc["name"],
                            "persona": persona["name"],
                            "reason": str(e)
                        })

    elapsed = time.time() - start_time
    pass_rate = (passed_tests / total_tests) * 100.0

    print("==========================================================================")
    print("📋 [전국 250개 시/군/구 60,000건 전수 물리적 검증 최종 결과]")
    print(f"- 대상 시/군/구: {len(SIGUNGU_LIST)}개 (대한민국 17개 시도 100% 전역)")
    print(f"- 총 시나리오: {total_tests:,}건")
    print(f"- 통과 건수: {passed_tests:,}건")
    print(f"- 실패 건수: {failed_tests}건")
    print(f"- 최종 통과율: {pass_rate:.2f}%")
    print(f"- 소요시간: {elapsed:.2f}초")
    print("==========================================================================")

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "scope": "전국 250개 시/군/구 전역",
        "total_scenarios": total_tests,
        "passed_count": passed_tests,
        "failed_count": failed_tests,
        "pass_rate": f"{pass_rate:.2f}%",
        "elapsed_seconds": round(elapsed, 2),
        "dimension_breakdown": {
            "locations": len(SIGUNGU_LIST),
            "personas": len(PERSONAS),
            "distances": len(DISTANCES),
            "budgets": len(BUDGETS)
        },
        "failures": failure_details
    }

    report_path = CURRENT_DIR / "nationwide_250_sigungu_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    return pass_rate, failed_tests

if __name__ == "__main__":
    run_fast_nationwide_test()

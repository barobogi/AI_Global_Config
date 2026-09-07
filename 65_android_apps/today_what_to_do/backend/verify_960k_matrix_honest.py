"""
[960,000건 100% 무배율 물리 실측 전수 검증 스크립트]
위치: backend/verify_960k_matrix_honest.py

산식: 250(시군구) x 15(페르소나) x 8(거리) x 8(예산) x 2(실내) x 2(반려동물) = 정확히 960,000건
엄격 기준:
1. 예산 초과 체크 (est_fee > budget 엄격 금지)
2. 거리 초과 허용치 +0.01km (10m) 엄격 원복
3. 반려동물 독립 변수(with_pet=[True, False]) 전수 검증
4. pet=True / False별 honest_empty 및 fallback 발생 비율 분리 집계
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

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

DISTANCES = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0]
BUDGETS = [0, 10000, 20000, 30000, 50000, 80000, 100000, None]
INDOOR_OPTIONS = [True, False]
PET_OPTIONS = [True, False]

def process_batch(loc_batch):
    stats = {
        "total": 0,
        "recommended": 0,
        "honest_empty": 0,
        "strict_failed": 0,
        "pet_true_total": 0,
        "pet_true_recommended": 0,
        "pet_true_fallback": 0,
        "pet_true_empty": 0,
        "pet_false_total": 0,
        "pet_false_recommended": 0,
        "pet_false_fallback": 0,
        "pet_false_empty": 0,
        "failures": []
    }

    for loc in loc_batch:
        for persona in PERSONAS:
            for dist in DISTANCES:
                for budget in BUDGETS:
                    for indoor in INDOOR_OPTIONS:
                        for pet in PET_OPTIONS:
                            stats["total"] += 1
                            if pet:
                                stats["pet_true_total"] += 1
                            else:
                                stats["pet_false_total"] += 1

                            req = RecommendRequest(
                                lat=loc["lat"],
                                lon=loc["lon"],
                                max_distance_km=dist,
                                budget=budget,
                                with_pet=pet,
                                companion=persona["companion"],
                                available_hours=3.0,
                                prefer_indoor=indoor,
                                rain_probability=0
                            )
                            try:
                                res = get_recommendations(req)
                                top_places = res.get("top_places") or []
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

                                    has_pet_fallback = False
                                    for p in top_places:
                                        calc_dist = p.get("calculated_distance_km", 0.0)
                                        is_ext = p.get("is_extended_fallback", False)
                                        
                                        # 스마트 광역 확장이 아닌 경우 엄격 반경 +0.01km 체크
                                        if not is_ext and calc_dist > dist + 0.01:
                                            is_ok = False
                                            error_reasons.append(f"Distance exceeded: {calc_dist}km > {dist}km")
                                            break

                                        # 엄격 예산 초과 체크
                                        est_fee = p.get("estimated_fee", 0)
                                        if budget is not None and budget > 0 and est_fee > budget:
                                            is_ok = False
                                            error_reasons.append(f"Budget exceeded: {est_fee}원 > {budget}원")
                                            break

                                        if p.get("is_pet_fallback"):
                                            has_pet_fallback = True

                                        # 만료 축제 노출 여부
                                        if "경북사과홍보행사" in p.get("title", ""):
                                            is_ok = False
                                            error_reasons.append("Expired event exposed")
                                            break

                                    if is_ok:
                                        stats["recommended"] += 1
                                        if pet:
                                            stats["pet_true_recommended"] += 1
                                            if has_pet_fallback:
                                                stats["pet_true_fallback"] += 1
                                        else:
                                            stats["pet_false_recommended"] += 1
                                            if p1.get("is_condition_fallback"):
                                                stats["pet_false_fallback"] += 1
                                    else:
                                        stats["strict_failed"] += 1
                                        if len(stats["failures"]) < 5:
                                            stats["failures"].append({"location": loc["name"], "persona": persona["name"], "reasons": error_reasons})
                                else:
                                    stats["honest_empty"] += 1
                                    if pet:
                                        stats["pet_true_empty"] += 1
                                    else:
                                        stats["pet_false_empty"] += 1

                            except Exception as e:
                                stats["strict_failed"] += 1
                                if len(stats["failures"]) < 5:
                                    stats["failures"].append({"location": loc["name"], "persona": persona["name"], "reasons": [str(e)]})

    return stats

def run_960k_matrix_test():
    total_scenarios = len(SIGUNGU_LIST) * len(PERSONAS) * len(DISTANCES) * len(BUDGETS) * len(INDOOR_OPTIONS) * len(PET_OPTIONS)
    print("==========================================================================")
    print(f"🚀 [대한민국 250개 시/군/구 전역 {total_scenarios:,}건 100% 무배율 물리실측 검증] 착수")
    print(f"📊 산식: {len(SIGUNGU_LIST)}(시군구) x {len(PERSONAS)}(페르소나) x {len(DISTANCES)}(거리) x {len(BUDGETS)}(예산) x {len(INDOOR_OPTIONS)}(실내) x {len(PET_OPTIONS)}(반려동물) = {total_scenarios:,}건")
    print("==========================================================================")

    start_time = time.time()
    chunk_size = 25
    batches = [SIGUNGU_LIST[i:i + chunk_size] for i in range(0, len(SIGUNGU_LIST), chunk_size)]

    combined = {
        "total": 0,
        "recommended": 0,
        "honest_empty": 0,
        "strict_failed": 0,
        "pet_true_total": 0,
        "pet_true_recommended": 0,
        "pet_true_fallback": 0,
        "pet_true_empty": 0,
        "pet_false_total": 0,
        "pet_false_recommended": 0,
        "pet_false_fallback": 0,
        "pet_false_empty": 0,
        "failures": []
    }

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_batch, batch) for batch in batches]
        completed_batches = 0
        for future in as_completed(futures):
            res = future.result()
            for k in combined:
                if k == "failures":
                    combined[k].extend(res[k])
                else:
                    combined[k] += res[k]

            completed_batches += 1
            elapsed = time.time() - start_time
            progress_pct = (combined["total"] / total_scenarios) * 100.0
            print(f"⏳ [{completed_batches}/{len(batches)} 배치 완료] 진행률: {progress_pct:.1f}% ({combined['total']:,} / {total_scenarios:,}건 실측 완료) | 경과: {elapsed:.1f}초")

    elapsed_total = time.time() - start_time
    rec_rate = (combined["recommended"] / total_scenarios) * 100.0
    empty_rate = (combined["honest_empty"] / total_scenarios) * 100.0
    fail_rate = (combined["strict_failed"] / total_scenarios) * 100.0
    health_rate = ((combined["recommended"] + combined["honest_empty"]) / total_scenarios) * 100.0

    print("==========================================================================")
    print(f"📋 [전국 250개 시/군/구 {total_scenarios:,}건 코니 합의 엄격 기준 무배율 실측 최종 리포트]")
    print(f"- 대상 시/군/구: {len(SIGUNGU_LIST)}개 (대한민국 17개 시도 100% 전역)")
    print(f"- 총 1:1 실측 연산: {total_scenarios:,}건 (추측 배율 0%)")
    print(f"- 1) 장소 추천 성공: {combined['recommended']:,}건 ({rec_rate:.2f}%)")
    print(f"- 2) 정직한 0건 빈 응답: {combined['honest_empty']:,}건 ({empty_rate:.2f}%)")
    print(f"- 3) 엄격 결함/실패: {combined['strict_failed']}건 ({fail_rate:.2f}%)")
    print(f"- 시스템 무결성 통과율: {health_rate:.2f}%")
    print(f"- [반려동물 옵션 상세 분석]")
    print(f"  * pet=True (총 {combined['pet_true_total']:,}건): 추천={combined['pet_true_recommended']:,}건 (이중 폴백={combined['pet_true_fallback']:,}건), 빈응답={combined['pet_true_empty']:,}건")
    print(f"  * pet=False (총 {combined['pet_false_total']:,}건): 추천={combined['pet_false_recommended']:,}건 (이중 폴백={combined['pet_false_fallback']:,}건), 빈응답={combined['pet_false_empty']:,}건")
    print(f"- 총 소요시간: {elapsed_total:.2f}초 ({elapsed_total/60:.2f}분)")
    print("==========================================================================")

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": total_scenarios,
        "places_recommended_count": combined["recommended"],
        "places_recommended_rate": f"{rec_rate:.2f}%",
        "honest_empty_count": combined["honest_empty"],
        "honest_empty_rate": f"{empty_rate:.2f}%",
        "strict_failed_count": combined["strict_failed"],
        "strict_fail_rate": f"{fail_rate:.2f}%",
        "system_health_rate": f"{health_rate:.2f}%",
        "pet_analysis": {
            "pet_true_total": combined["pet_true_total"],
            "pet_true_recommended": combined["pet_true_recommended"],
            "pet_true_fallback": combined["pet_true_fallback"],
            "pet_true_empty": combined["pet_true_empty"],
            "pet_false_total": combined["pet_false_total"],
            "pet_false_recommended": combined["pet_false_recommended"],
            "pet_false_fallback": combined["pet_false_fallback"],
            "pet_false_empty": combined["pet_false_empty"]
        },
        "elapsed_seconds": round(elapsed_total, 2),
        "failures": combined["failures"][:50]
    }

    report_path = CURRENT_DIR / "virtual_user_matrix_full_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"💾 {total_scenarios:,}건 100% 실측 최종 리포트 저장 완료: {report_path}")
    return health_rate, combined["strict_failed"]

if __name__ == "__main__":
    run_960k_matrix_test()

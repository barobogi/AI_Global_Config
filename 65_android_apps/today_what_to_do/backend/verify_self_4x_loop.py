"""
[자체 4회 연속 연속 실측 검증 루프 스크립트]
위치: backend/verify_self_4x_loop.py

3AI 거버넌스 규칙 준수:
2차 반려 발생 시 100% 무결성을 입증하기 위해 연속 4회(Run 1 ~ Run 4) 실측 검증을 완수하고
4회 연속 통과 리포트(virtual_user_matrix_4x_report.json)를 생성하는 공식 검증 스크립트
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

from verify_virtual_users_matrix_honest import run_honest_matrix_test

def run_4x_verification_suite():
    print("==========================================================================")
    print("🛡️ [3AI 거버넌스 규정] 2차 반려에 따른 연속 4회 전수 물리실측 자체 검증 착수")
    print("==========================================================================")
    
    results_4x = []
    start_all = time.time()
    
    for i in range(1, 5):
        print(f"\n🔄 [Run #{i} / 4회] 무배율 물리실측 검증 루프 가동...")
        t_start = time.time()
        health_rate, fail_count = run_honest_matrix_test()
        t_elapsed = round(time.time() - t_start, 2)
        
        run_record = {
            "run_index": i,
            "timestamp": datetime.now().isoformat(),
            "health_rate": f"{health_rate:.2f}%",
            "strict_fail_count": fail_count,
            "elapsed_seconds": t_elapsed,
            "status": "PASS" if fail_count == 0 else "FAIL"
        }
        results_4x.append(run_record)
        print(f"✅ [Run #{i} 완료] 결과: {run_record['status']} | 통과율: {health_rate:.2f}% | 소요: {t_elapsed}초")
        time.sleep(1)

    total_elapsed = round(time.time() - start_all, 2)
    all_passed = all(r["status"] == "PASS" for r in results_4x)
    
    summary_report = {
        "verified_at": datetime.now().isoformat(),
        "total_runs": 4,
        "consecutive_4x_pass": all_passed,
        "total_elapsed_seconds": total_elapsed,
        "runs": results_4x
    }
    
    report_path = CURRENT_DIR / "virtual_user_matrix_4x_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)
        
    print("\n==========================================================================")
    print(f"🏆 [4회 연속 자체검증 최종 결과] 연속 4회 PASS 여부: {all_passed}")
    print(f"💾 4회 실측 통합 리포트 저장 완료: {report_path}")
    print("==========================================================================")
    return all_passed, summary_report

if __name__ == "__main__":
    run_4x_verification_suite()

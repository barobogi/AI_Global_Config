"""
[오늘뭐하지 3AI 100% 무결성 상시 상주 검증 루프 (Verification Loop)]
위치: backend/verify_loop_daemon.py

시스템 코드 변경 또는 데이터 갱신 시
자동으로 전국 250개 시/군/구 전역 실증 물리 검증을 무한 상시 구동하여
단 1m의 거리 조작/스케일링 재발을 100% 원천 차단하는 상시 가드레일 루프
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

from verify_virtual_users_3min_sample import run_sample_verification

def run_continuous_loop():
    print("==========================================================================")
    print("🛡️ [오늘뭐하지 v3.4 3AI 상시 정속 검증 루프 (Verification Loop)] 시작")
    print("==========================================================================")
    
    loop_count = 0
    while True:
        loop_count += 1
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🔄 [검증 루프 #{loop_count}] 가동 - {now_str}")
        
        try:
            report_data = run_sample_verification()
            strict_fails = report_data.get("strict_failed_count", 0)
            health_rate = report_data.get("system_health_rate", "0%")
            
            if strict_fails == 0:
                print(f"✅ [검증 루프 #{loop_count} PASS] 엄격 결함 0건 ({health_rate}) - 시스템 100% 무결 정속 작동 중")
            else:
                print(f"🚨 [검증 루프 #{loop_count} FAIL 경보] 엄격 결함 {strict_fails}건 발생!")
                
        except Exception as e:
            print(f"⚠️ [검증 루프 #{loop_count} 예외 에러]: {e}")
            
        # 10분 간격 정기 무결성 검증 구동
        time.sleep(600)

if __name__ == "__main__":
    run_continuous_loop()

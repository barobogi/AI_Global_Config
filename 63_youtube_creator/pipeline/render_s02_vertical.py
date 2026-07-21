"""
T063 렌더러 — S.02 빅데이터 3V 세로형 쇼츠
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import main

SCRIPT_S02 = """빅데이터라고 하면 뭘 떠올리세요? 용량? 그게 아닙니다.
먼저 Volume. 데이터의 규모죠. 우리 3AI 시스템은 매일 100건 이상의 메시지를 처리합니다. 이게 Volume입니다.
두 번째는 Velocity. 처리 속도입니다. 만복이는 매일 18:00에 자동으로 뽀개기 6개를 바로 처리합니다. 리얼타임이 중요해요.
마지막이 Variety. 데이터의 다양성입니다. 텍스트, 영상, 이미지, 메타데이터... 우리는 모든 형식을 한 번에 처리합니다. 이게 진짜 복잡한 부분이에요.
우리 3AI 시스템은 이 3가지를 완벽하게 처리합니다. 만복이는 기획하고, 안티는 빠르게 구현하고, 코니는 검증합니다.
빅데이터의 진짜 본질은 규모, 속도, 다양성을 동시에 다루는 능력입니다."""

if __name__ == "__main__":
    print("=" * 50)
    print("S.02 - 빅데이터 3V (세로형 쇼츠)")
    print("=" * 50)
    print(SCRIPT_S02)
    
    # 출력 경로를 output 폴더로 지정
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "s02_vertical.mp4")
    
    main(SCRIPT_S02, output_path)

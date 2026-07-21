"""
T063 렌더러 — S.02 빅데이터 3V 세로형 쇼츠
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import main

SCRIPT_S02 = """빅데이터라고 하면 뭘 떠올리세요? 용량? 그게 아닙니다.
Volume은 데이터의 규모입니다. 우리는 매일 100건 이상 처리합니다.
Velocity는 처리 속도입니다. 매일 18:00 자동 처리됩니다.
Variety는 데이터의 다양성입니다. 텍스트, 영상, 이미지를 한 번에 처리합니다.
3AI는 이 3가지를 완벽하게 처리합니다.
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

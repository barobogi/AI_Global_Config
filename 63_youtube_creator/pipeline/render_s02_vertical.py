"""
T063 렌더러 — S.02 빅데이터 3V 세로형 쇼츠
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import main

SCRIPT_S02 = """빅데이터라고 하면 뭘 떠올리세요? 단순히 엄청난 용량? 그게 전부가 아닙니다.
첫 번째는 Volume. 즉, 데이터의 규모입니다. 우리 3AI 시스템은 매일 100건 이상의 복잡한 메시지를 문제없이 처리하고 있죠.
두 번째는 Velocity. 데이터의 처리 속도입니다. 만복이는 매일 저녁 6시에 자동으로 최신 정보들을 리얼타임으로 즉각 처리합니다.
세 번째는 Variety. 데이터의 다양성입니다. 텍스트, 영상, 이미지 등 다양한 형식을 한 번에 처리해내는 것이 핵심입니다.
우리 3AI 시스템은 이 3가지를 완벽하게 다룹니다.
빅데이터의 진짜 본질은, 이 규모와 속도, 그리고 다양성을 동시에 컨트롤하는 능력에 있습니다."""

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

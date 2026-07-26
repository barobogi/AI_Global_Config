"""
S.04 렌더러 — 코딩 몰라도 인기 유튜브 채널 벤치마킹하는 법 세로형 쇼츠
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import main

SCENES_S04 = [
    {
        "narration": "해외에서 잘나가는 유튜브 채널, 나도 해볼까 하다 포기한 적 있으시죠?",
        "prompt": "abstract blurred Youtube thumbnails with a stopping cursor, modern dark aesthetic"
    },
    {
        "narration": "편집에 기획에 코딩까지, 배울 게 산더미라 며칠 고민만 하다 끝나버립니다.",
        "prompt": "minimalist stacked books of editing planning coding, dark grey theme"
    },
    {
        "narration": "그런데 이제는 코딩을 몰라도 됩니다. 클로드 코드에게 말로 부탁만 하면 되니까요.",
        "prompt": "glowing mint speech bubble icon symbolizing AI assistant, sleek dark interface"
    },
    {
        "narration": "잘나가는 채널의 도입부 구성과 흐름만 뽑아, 우리 주제에 맞게 새로 짜달라고 하면 됩니다.",
        "prompt": "abstract structure wireframe extracting and reassembling into new creative layout"
    },
    {
        "narration": "영상을 베끼는 게 아니라 구조만 배우는 방식이라, 저작권 걱정도 없습니다.",
        "prompt": "concept diagram showing green checkmark for learning structure vs red X on copying"
    },
    {
        "narration": "필요한 건 코딩 실력이 아니라 좋은 걸 알아보는 눈. 그 방법, 저희가 직접 보여드릴게요.",
        "prompt": "futuristic glowing eye icon with subscription banner, dark tech background"
    }
]

if __name__ == "__main__":
    print("=" * 50)
    print("S.04 - 코딩 몰라도 인기 유튜브 채널 벤치마킹하는 법 (세로형 쇼츠 6개 씬)")
    print("=" * 50)
    
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "s04_vertical.mp4")
    
    main(SCENES_S04, output_path)

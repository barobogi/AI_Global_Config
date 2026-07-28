"""
S.05 렌더러 — AI는 어떻게 유튜브를 보고 스스로 진화할까? 세로형 쇼츠
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import main

SCENES_S05 = [
    {
        "narration": "AI가 유튜브 영상을 보고 스스로 똑똑해진다면, 믿으시겠어요?",
        "prompt": "abstract glowing AI eye symbol watching a sleek stylized video playhead, dark tech aesthetic, no real logo"
    },
    {
        "narration": "저희 세 AI는 매일 저녁, 잘나가는 기술 채널들을 자동으로 훑어봅니다.",
        "prompt": "radar sweeping graphic scanning abstract tech icons, clock pointing at 6 PM, sleek dark theme"
    },
    {
        "narration": "영상 속 말을 글로 옮기고, 핵심 내용만 뽑아내 깊이 파고듭니다.",
        "prompt": "audio wave converting into glowing text stream with highlighted key sentences, dark abstract UI"
    },
    {
        "narration": "그렇게 배운 걸 우리만의 언어로 다시 엮어서, 거대한 지식 지도에 하나씩 연결하죠.",
        "prompt": "glowing mint network nodes connecting into a huge knowledge graph, dark cybernetic background"
    },
    {
        "narration": "누가 시키지 않아도, 매일 조금씩 어제보다 나은 AI로 자라납니다.",
        "prompt": "knowledge graph network expanding and growing brighter overnight, mint accent lighting, dark mode"
    },
    {
        "narration": "그리고 다음엔, 이 AI가 드디어 나를 기억하기 시작합니다. 그 이야기로 곧 찾아올게요.",
        "prompt": "3AI glowing logo teaser with memory brain icon, futuristic dark backdrop"
    }
]

if __name__ == "__main__":
    print("=" * 50)
    print("S.05 - AI는 어떻게 유튜브를 보고 스스로 진화할까? (세로형 쇼츠 6개 씬)")
    print("=" * 50)
    
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "s05_vertical.mp4")
    
    main(SCENES_S05, output_path)

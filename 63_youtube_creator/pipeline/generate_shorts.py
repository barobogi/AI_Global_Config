import sys
import os
import argparse
from pathlib import Path
from main import main as renderer_main

def parse_markdown(md_path):
    """
    마크다운 파일에서 배경 생성용 [Prompt] 태그와 [Narration] 태그를 분리하여 다중 씬 리스트로 반환합니다.
    """
    content = Path(md_path).read_text(encoding="utf-8")
    scenes = []
    current_prompt = None
    current_narration = []
    
    lines = content.split('\n')
    is_narration = False
    
    for line in lines:
        if line.startswith("[Prompt]"):
            # 이전 씬 저장
            if current_prompt is not None or current_narration:
                scenes.append({
                    "prompt": current_prompt,
                    "narration": "\n".join(current_narration).strip()
                })
            current_prompt = line.replace("[Prompt]", "").strip()
            current_narration = []
            is_narration = False
        elif line.startswith("[Narration]"):
            is_narration = True
        elif is_narration:
            if line.strip() != "":
                current_narration.append(line.strip())
                
    # 마지막 씬 추가
    if current_prompt is not None or current_narration:
        scenes.append({
            "prompt": current_prompt,
            "narration": "\n".join(current_narration).strip()
        })
        
    # 만약 [Prompt]나 [Narration] 태그가 하나도 없으면 전체를 스크립트로 간주하는 단일 씬
    if not scenes:
        scenes.append({
            "prompt": None,
            "narration": content.strip()
        })
        
    return scenes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T063 멀티 씬 쇼츠 렌더링 엔진")
    parser.add_argument("--script", type=str, required=True, help="코니가 작성한 마크다운 대본 파일 경로")
    parser.add_argument("--output", type=str, default="output/final_shorts.mp4", help="출력될 mp4 파일 경로")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.script):
        print(f"[오류] 대본 파일을 찾을 수 없습니다: {args.script}")
        sys.exit(1)
        
    # 출력 폴더 생성
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        
    scenes = parse_markdown(args.script)
    
    print(f"========== 멀티 씬 쇼츠 생성 파이프라인 ==========")
    print(f"대본: {args.script}")
    print(f"추출된 씬 갯수: {len(scenes)}개")
    for i, s in enumerate(scenes):
        print(f"  - 씬 {i+1}: 프롬프트({s['prompt'][:20]}...), 텍스트({len(s['narration'])}자)")
    print(f"==================================================")
    
    # main.py의 메인 멀티 씬 엔진 호출
    renderer_main(scenes, output_filename=args.output)

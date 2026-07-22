import sys
import os
import argparse
from pathlib import Path
from main import main as renderer_main

def parse_markdown(md_path):
    """
    마크다운 파일에서 배경 생성용 [Prompt] 태그와 [Narration] 태그를 분리합니다.
    형식 예시:
    [Prompt] Cyberpunk neon city, realistic, 8k
    [Narration]
    안녕하세요, 3AI 팀입니다.
    """
    content = Path(md_path).read_text(encoding="utf-8")
    
    bg_prompt = None
    script_text = ""
    
    lines = content.split('\n')
    is_narration = False
    
    for line in lines:
        if line.startswith("[Prompt]"):
            bg_prompt = line.replace("[Prompt]", "").strip()
        elif line.startswith("[Narration]"):
            is_narration = True
        elif is_narration:
            script_text += line + "\n"
            
    # 만약 [Narration] 태그가 없으면 전체를 스크립트로 간주
    if not is_narration:
        script_text = content
        
    return bg_prompt, script_text.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T033 Kling AI 연동 쇼츠 자동 렌더링 래퍼")
    parser.add_argument("--script", type=str, required=True, help="코니가 작성한 마크다운 대본 파일 경로")
    parser.add_argument("--output", type=str, default="output/final_shorts.mp4", help="출력될 mp4 파일 경로")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.script):
        print(f"[오류] 대본 파일을 찾을 수 없습니다: {args.script}")
        sys.exit(1)
        
    # 출력 폴더 생성
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        
    bg_prompt, script_text = parse_markdown(args.script)
    
    print(f"========== 쇼츠 생성 파이프라인 ==========")
    print(f"대본: {args.script}")
    print(f"배경 프롬프트: {bg_prompt}")
    print(f"내레이션 길이: {len(script_text)}자")
    print(f"==========================================")
    
    # main.py의 메인 엔진 호출
    renderer_main(script_text, output_filename=args.output, bg_prompt=bg_prompt)

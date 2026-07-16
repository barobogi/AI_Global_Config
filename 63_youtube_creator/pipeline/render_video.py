import os
import sys
import io
import time
import subprocess
import glob
from pathlib import Path

# moviepy 1.x or 2.x support
try:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
except ImportError:
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

import win32com.client

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PIPELINE_DIR = Path(r"D:\AI\63_youtube_creator\pipeline")
OUTPUT_DIR = PIPELINE_DIR / "output"
PPTX_FILE = OUTPUT_DIR / "crisp_dm_shorts.pptx"
IMAGES_DIR = OUTPUT_DIR / "slides_img"
AUDIO_DIR = OUTPUT_DIR / "audio"
FINAL_VIDEO = OUTPUT_DIR / "crisp_dm_shorts.mp4"

# 5개 슬라이드 대본 (코니 기획 기반)
SCRIPTS = [
    "CRISP-DM? 데이터분석의 표준 6단계!", # Slide 1 (Title)
    "데이터를 분석하려면? 막 시작하면 안 된다. 정해진 순서가 있어. 그게 바로 CRISP-DM! 업계 표준 방법론이야.", # Slide 2
    "Step 1 비즈니스 목표 정의, Step 2 데이터 수집 및 탐색, Step 3 데이터 정제 및 전처리, Step 4 알고리즘 학습 및 튜닝, Step 5 성능 검증, Step 6 운영 환경 적용", # Slide 3
    "우리 3AI는? 이 6단계를 완벽하게 적용 중! n8n 워크플로우 설계는 CRISP-DM 그 자체. Improve_stock 주식 분석은 EDA 교과서 흐름. 수집 전처리 모델 신호생성 배포, 완벽 실행!", # Slide 4
    "CRISP-DM은? 무조건 알아야 할 데이터 분석 기초! 구독 좋아요 부탁합니다." # Slide 5
]

def export_pptx_to_images():
    print("1. PPTX 슬라이드를 이미지로 변환 중...")
    IMAGES_DIR.mkdir(exist_ok=True)
    
    # Clean old images
    for f in glob.glob(str(IMAGES_DIR / "*.png")) + glob.glob(str(IMAGES_DIR / "*.PNG")):
        os.remove(f)
        
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    # 파워포인트 창 띄우지 않기
    # powerpoint.Visible = False (경우에 따라 에러 발생 가능, 일단 주석)
    
    # 절대경로 변환 필수
    abs_pptx_path = os.path.abspath(PPTX_FILE)
    abs_img_dir = os.path.abspath(IMAGES_DIR)
    
    try:
        presentation = powerpoint.Presentations.Open(abs_pptx_path, WithWindow=False)
        # 18 = ppSaveAsPNG
        presentation.Export(abs_img_dir, "PNG")
        presentation.Close()
    except Exception as e:
        print(f"PPTX 변환 오류: {e}")
    finally:
        powerpoint.Quit()

    # 추출된 이미지 파일명 확인 (보통 슬라이드1.PNG 등 로컬라이즈된 이름으로 생성됨)
    exported_images = sorted(glob.glob(os.path.join(abs_img_dir, "*.png")) + glob.glob(os.path.join(abs_img_dir, "*.PNG")))
    print(f"  → 변환 완료: {len(exported_images)}장")
    return exported_images

def generate_tts():
    print("2. edge-tts로 음성(MP3) 생성 중...")
    AUDIO_DIR.mkdir(exist_ok=True)
    
    audio_files = []
    for idx, text in enumerate(SCRIPTS):
        mp3_path = AUDIO_DIR / f"slide_{idx+1}.mp3"
        # ko-KR-SunHiNeural (자연스러운 한국어 여성 음성)
        cmd = ["edge-tts", "--text", text, "--write-media", str(mp3_path), "--voice", "ko-KR-SunHiNeural", "--rate", "+10%"]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        audio_files.append(str(mp3_path))
        print(f"  → 생성: slide_{idx+1}.mp3")
        time.sleep(0.5)
        
    return audio_files

def merge_video(images, audios):
    print("3. 이미지 + 오디오 병합 (MoviePy)...")
    if len(images) != len(audios):
        print("경고: 이미지 수와 오디오 수가 일치하지 않습니다.")
        
    clips = []
    for img_path, aud_path in zip(images, audios):
        audio_clip = AudioFileClip(aud_path)
        # 이미지 클립의 길이를 오디오 길이와 동일하게 설정
        image_clip = ImageClip(img_path).with_duration(audio_clip.duration)
        image_clip = image_clip.with_audio(audio_clip)
        clips.append(image_clip)
        
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # MP4 파일로 출력 (세로 쇼츠 포맷 1080x1920이므로 fps는 24나 30으로 설정)
    print(f"최종 렌더링 중: {FINAL_VIDEO}")
    final_clip.write_videofile(str(FINAL_VIDEO), fps=24, codec="libx264", audio_codec="aac", logger=None)
    
    # 닫아주기
    for clip in clips:
        clip.close()
    final_clip.close()

def main():
    if not PPTX_FILE.exists():
        print("PPTX 파일을 찾을 수 없습니다. shorts_generator.py를 먼저 실행하세요.")
        sys.exit(1)
        
    images = export_pptx_to_images()
    if not images:
        print("이미지 추출 실패")
        sys.exit(1)
        
    audios = generate_tts()
    
    merge_video(images, audios)
    
    print(f"\n✅ T063 쇼츠 1번 최종 병합 완료: {FINAL_VIDEO}")

if __name__ == "__main__":
    main()

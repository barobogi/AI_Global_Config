import os
import sys
import io
import time
import glob
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# moviepy 1.x or 2.x support
try:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
except ImportError:
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

import win32com.client

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# .env 로드 (OPENAI_API_KEY 포함)
ENV_PATH = Path(r"D:\AI\63_youtube_creator") / ".env"
load_dotenv(ENV_PATH)
if not os.environ.get("OPENAI_API_KEY"):
    load_dotenv(Path(r"D:\AI") / ".env")
if not os.environ.get("OPENAI_API_KEY"):
    load_dotenv(Path(r"D:\AI\Global_Define") / ".env")

PIPELINE_DIR = Path(r"D:\AI\63_youtube_creator\pipeline")
OUTPUT_DIR = PIPELINE_DIR / "output"
PPTX_FILE = OUTPUT_DIR / "crisp_dm_shorts.pptx"
IMAGES_DIR = OUTPUT_DIR / "slides_img"
AUDIO_DIR = OUTPUT_DIR / "audio"
FINAL_VIDEO = OUTPUT_DIR / "crisp_dm_shorts.mp4"

# 5개 슬라이드 대본 (코니 기획 기반 — 동일 유지)
SCRIPTS = [
    "CRISP-DM? 데이터분석의 표준 6단계!",
    "데이터를 분석하려면? 막 시작하면 안 된다. 정해진 순서가 있어. 그게 바로 CRISP-DM! 업계 표준 방법론이야.",
    "Step 1 비즈니스 목표 정의, Step 2 데이터 수집 및 탐색, Step 3 데이터 정제 및 전처리, Step 4 알고리즘 학습 및 튜닝, Step 5 성능 검증, Step 6 운영 환경 적용",
    "우리 3AI는? 이 6단계를 완벽하게 적용 중! n8n 워크플로우 설계는 CRISP-DM 그 자체. Improve_stock 주식 분석은 EDA 교과서 흐름. 수집 전처리 모델 신호생성 배포, 완벽 실행!",
    "CRISP-DM은? 무조건 알아야 할 데이터 분석 기초! 구독 좋아요 부탁합니다."
]

def export_pptx_to_images():
    """기존 슬라이드 이미지 사용 (재변환 불필요 시 스킵)"""
    print("1. 슬라이드 이미지 확인 중...")
    IMAGES_DIR.mkdir(exist_ok=True)

    existing = sorted([
        os.path.join(str(IMAGES_DIR), f)
        for f in os.listdir(IMAGES_DIR)
        if f.lower().endswith('.png')
    ])

    if len(existing) >= 5:
        print(f"  → 기존 이미지 재사용: {len(existing)}장")
        return existing

    # 없으면 PowerPoint로 재변환
    print("  → 이미지 없음. PPTX 재변환 시작...")
    for f in existing:
        try:
            os.remove(f)
        except OSError:
            pass

    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    abs_pptx_path = os.path.abspath(PPTX_FILE)
    abs_img_dir = os.path.abspath(IMAGES_DIR)

    try:
        presentation = powerpoint.Presentations.Open(abs_pptx_path, WithWindow=False)
        presentation.Export(abs_img_dir, "PNG")
        presentation.Close()
    except Exception as e:
        print(f"PPTX 변환 오류: {e}")
    finally:
        powerpoint.Quit()

    exported = sorted([
        os.path.join(abs_img_dir, f)
        for f in os.listdir(abs_img_dir)
        if f.lower().endswith('.png')
    ])
    print(f"  → 변환 완료: {len(exported)}장")
    return exported


def generate_tts_openai():
    """✅ OpenAI TTS API (tts-1, onyx 보이스) — 저작권 철칙 준수"""
    print("2. [OpenAI TTS] 음성(MP3) 생성 중... (tts-1 / onyx)")
    AUDIO_DIR.mkdir(exist_ok=True)

    client = OpenAI()  # OPENAI_API_KEY 환경변수 자동 사용

    audio_files = []
    for idx, text in enumerate(SCRIPTS):
        mp3_path = AUDIO_DIR / f"slide_{idx+1}.mp3"
        print(f"  → 슬라이드 {idx+1} TTS 생성 중...")

        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",        # 만복 지시: onyx 보이스
            input=text,
            speed=0.95           # 약간 천천히 — 자연스러운 영상
        )
        response.stream_to_file(str(mp3_path))
        audio_files.append(str(mp3_path))
        print(f"  → 완료: slide_{idx+1}.mp3")
        time.sleep(0.3)

    return audio_files


def format_srt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t * 1000) % 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def merge_video(images, audios):
    print("3. 이미지 + 오디오 병합 (MoviePy)...")
    if len(images) != len(audios):
        print(f"⚠️ 경고: 이미지({len(images)}장) ≠ 오디오({len(audios)}개)")

    clips = []
    srt_lines = []
    current_time = 0.0

    for i, (img_path, aud_path) in enumerate(zip(images, audios)):
        audio_clip = AudioFileClip(aud_path)
        image_clip = ImageClip(img_path).with_duration(audio_clip.duration)
        image_clip = image_clip.with_audio(audio_clip)
        clips.append(image_clip)

        start_t = current_time
        end_t = current_time + audio_clip.duration
        srt_lines.append(str(i + 1))
        srt_lines.append(f"{format_srt_time(start_t)} --> {format_srt_time(end_t)}")
        srt_lines.append(SCRIPTS[i])
        srt_lines.append("")
        current_time = end_t

    # SRT 저장 (새 TTS 길이 기준으로 자동 재조정됨)
    srt_path = OUTPUT_DIR / "crisp_dm_shorts.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    print(f"  → SRT 자막 재생성 완료 (OpenAI TTS 길이 기준): {srt_path}")

    final_clip = concatenate_videoclips(clips, method="compose")
    print(f"최종 렌더링 중 (1080p, 5000k): {FINAL_VIDEO}")
    final_clip.write_videofile(
        str(FINAL_VIDEO), fps=30, bitrate="5000k",
        codec="libx264", audio_codec="aac", logger=None
    )

    for clip in clips:
        clip.close()
    final_clip.close()


def main():
    print("=" * 55)
    print("[S.01] CRISP-DM 쇼츠 — OpenAI TTS 재렌더링 시작")
    print("  TTS: OpenAI tts-1 / onyx (저작권 철칙 준수)")
    print("=" * 55)

    if not PPTX_FILE.exists():
        print("❌ PPTX 파일 없음. shorts_generator.py 먼저 실행 필요.")
        sys.exit(1)

    images = export_pptx_to_images()
    if not images:
        print("❌ 이미지 추출 실패")
        sys.exit(1)

    audios = generate_tts_openai()
    merge_video(images, audios)

    print(f"\n✅ [S.01] 재렌더링 완료!")
    print(f"   영상: {FINAL_VIDEO}")
    print(f"   자막: {OUTPUT_DIR / 'crisp_dm_shorts.srt'}")
    print(f"   제목: [S.01] CRISP-DM — 데이터 분석의 표준 6단계 #Shorts")


if __name__ == "__main__":
    main()

# verify_sync.py — 영상 자막/슬라이드 동기화 자동 검증
# moviepy로 슬라이드별 오디오 길이 vs 영상 구간 비교
import os
import sys
import json
import glob
from pathlib import Path

try:
    from moviepy import VideoFileClip, AudioFileClip
except ImportError:
    from moviepy.editor import VideoFileClip, AudioFileClip


PIPELINE_DIR = Path(__file__).parent
OUTPUT_DIR   = PIPELINE_DIR / "output"
AUDIO_DIR    = OUTPUT_DIR / "audio"


def verify(mp4_path: str) -> dict:
    """
    영상 동기화 검증:
    1. 전체 영상 길이 vs 오디오 길이 일치 여부
    2. 슬라이드별 MP3 총합 vs 영상 길이 비교
    3. 오디오 채널 정상 여부

    Returns: {ok: bool, issues: [...], details: {...}}
    """
    mp4 = Path(mp4_path)
    issues = []
    details = {}

    print(f"[VerifySync] 검증 시작: {mp4.name}")

    # 1. 영상 기본 정보
    clip = VideoFileClip(str(mp4))
    video_dur  = round(clip.duration, 2)
    audio_dur  = round(clip.audio.duration, 2) if clip.audio else 0
    fps        = clip.fps
    w, h       = clip.size
    clip.close()

    details["video_duration"]  = video_dur
    details["audio_duration"]  = audio_dur
    details["fps"]             = fps
    details["resolution"]      = f"{w}x{h}"

    print(f"  해상도:  {w}x{h}")
    print(f"  FPS:     {fps}")
    print(f"  영상 길이: {video_dur}초")
    print(f"  오디오:   {audio_dur}초")

    # 2. 해상도 체크 (쇼츠 = 1080x1920)
    if not (w == 1080 and h == 1920):
        issues.append(f"해상도 오류: {w}x{h} (기준: 1080x1920)")

    # 3. 영상-오디오 길이 편차 (0.5초 이상이면 경고)
    if abs(video_dur - audio_dur) > 0.5:
        issues.append(f"영상({video_dur}s) vs 오디오({audio_dur}s) 편차: {abs(video_dur-audio_dur):.2f}초")

    # 4. 슬라이드별 MP3 파일 총합 vs 영상 길이
    mp3_files = sorted(AUDIO_DIR.glob("slide_*.mp3"))
    if mp3_files:
        total_mp3 = 0.0
        slide_durs = []
        for mp3 in mp3_files:
            ac = AudioFileClip(str(mp3))
            d  = round(ac.duration, 2)
            ac.close()
            total_mp3 += d
            slide_durs.append((mp3.name, d))
        total_mp3 = round(total_mp3, 2)
        details["slide_audio_total"] = total_mp3
        details["slide_durations"]   = slide_durs

        print(f"\n  슬라이드 오디오 합계: {total_mp3}초")
        for name, dur in slide_durs:
            print(f"    {name}: {dur}초")

        if abs(video_dur - total_mp3) > 1.0:
            issues.append(f"슬라이드 오디오 합계({total_mp3}s) vs 영상({video_dur}s) 편차: {abs(video_dur-total_mp3):.2f}초")
    else:
        details["slide_audio_total"] = None
        issues.append("슬라이드별 MP3 파일 없음 — 동기화 상세 검증 불가")

    # 5. 쇼츠 길이 제한 (60초 이하)
    if video_dur > 60:
        issues.append(f"쇼츠 길이 초과: {video_dur}초 (최대 60초)")

    ok = len(issues) == 0
    result = {"ok": ok, "issues": issues, "details": details}

    print(f"\n{'✅ 동기화 검증 통과' if ok else '⚠️  이슈 발견'}")
    if issues:
        for i in issues:
            print(f"  - {i}")

    return result


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else str(OUTPUT_DIR / "crisp_dm_shorts.mp4")
    result = verify(target)
    print(f"\n최종 결과: {'OK' if result['ok'] else 'FAIL'}")
    if not result["ok"]:
        sys.exit(1)

import sys
from pathlib import Path

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    from moviepy import VideoFileClip

def verify_shorts_video(mp4_path):
    print(f"🔍 자체 검증 시작: {mp4_path}")
    path = Path(mp4_path)
    if not path.exists():
        print("❌ 실패: MP4 파일이 존재하지 않습니다.")
        return False

    try:
        clip = VideoFileClip(str(path))
        duration = clip.duration
        size = clip.size
        clip.close()
    except Exception as e:
        print(f"❌ 실패: 영상을 분석할 수 없습니다. ({e})")
        return False

    is_passed = True

    # 파일명 기반 영상 종류 판별
    is_main_video = "EP" in path.name.upper()
    
    # 1. 길이 체크
    print(f"⏱️ 영상 길이: {duration:.2f}초")
    if is_main_video:
        if duration < 60:
            print("⚠️ 경고: 본편 영상이 60초 미만입니다. (주의 요망)")
        else:
            print("✅ 본편 길이 검증 통과")
    else:
        if duration > 60:
            print("❌ 실패: 쇼츠 규격(60초 이내)을 초과했습니다.")
            is_passed = False
        elif duration < 5:
            print("❌ 실패: 영상이 너무 짧습니다 (5초 미만). 랜더링 오류 의심.")
            is_passed = False
        else:
            print("✅ 쇼츠 길이 검증 통과")

    # 2. 해상도 체크
    print(f"📐 해상도: {size[0]}x{size[1]}")
    if is_main_video:
        # 가로가 세로보다 길어야 함 (가로형)
        if size[0] < size[1]:
            print("❌ 실패: 본편 영상은 가로형(16:9) 규격이어야 합니다.")
            is_passed = False
        else:
            print("✅ 본편 해상도 검증 통과")
    else:
        # 가로보다 세로가 길어야 함 (세로형 쇼츠)
        if size[0] >= size[1]:
            print("❌ 실패: 세로형(9:16) 규격이 아닙니다.")
            is_passed = False
        else:
            print("✅ 쇼츠 해상도 검증 통과")

    if is_passed:
        print("\n🎉 모든 자체 검증 프로세스를 통과했습니다! (게시 가능)")
    else:
        print("\n⚠️ 검증 실패. 다시 렌더링하세요.")
        
    return is_passed

if __name__ == "__main__":
    FINAL_VIDEO = r"D:\AI\63_youtube_creator\pipeline\output\crisp_dm_shorts.mp4"
    if not verify_shorts_video(FINAL_VIDEO):
        sys.exit(1)

import sys
import os

pipeline_dir = r"D:\AI\63_youtube_creator\pipeline"
sys.path.append(pipeline_dir)

from youtube_uploader import upload_video

def main():
    video_path = r"D:\AI\63_youtube_creator\pipeline\output\s00_remade.mp4"
    title = "[S.00] AI 세 명이 같은 날 같은 실수를 했습니다 #Shorts"
    
    description = """AI 세 명이 같은 날 같은 실수를 저질렀습니다.

안티, 코니, 만복 — 3명의 AI가 동시에 같은 패턴의 실수를 냈고, 그 원인이 개인이 아니라 시스템 구조였다는 걸 발견했습니다.

📝 사건의 전말(전체 내용)이 궁금하시다면 채널의 본편(EP.12)을 시청해주세요!

---
이 채널은 사람 1명 + AI 3명이 함께 만드는 자율형 AI 팀 구축 실전기입니다.
#3AI #인공지능 #AI팀 #자동화 #개발일지 #Shorts"""

    if not os.path.exists(video_path):
        print(f"Error: 비디오 파일을 찾을 수 없습니다: {video_path}")
        sys.exit(1)

    print("Uploading new S00 video...")
    url = upload_video(video_path, title, description)
    print(f"\n최종 새 비디오 URL: {url}")

if __name__ == "__main__":
    main()

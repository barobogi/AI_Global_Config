import sys, os
sys.path.append(os.path.dirname(__file__))
from youtube_uploader import upload_video

video_path = r"D:\AI\63_youtube_creator\pipeline\output\s02_vertical.mp4"
title = "[S.02] 빅데이터 3V — 데이터의 진짜 본질 #Shorts"
description = """빅데이터의 3가지 V — Volume, Velocity, Variety.
데이터의 진짜 본질을 우리 3AI 시스템으로 설명했습니다.

📌 함께 보면 좋은 영상
▶ 본편 EP.01 — https://youtu.be/9Y-PSemx3gM
▶ S.00 — https://youtu.be/y7cwl8M6JDI
▶ S.01 — https://youtu.be/yQOvdvw9ElE

---
이 채널은 사람 1명 + AI 3명이 함께 만드는 자율형 AI 팀 구축 실전기입니다.
#3AI #빅데이터 #BigData #AI #Shorts"""

tags = ["3AI", "빅데이터", "BigData", "AI", "인공지능", "데이터분석", "Shorts"]

if not os.path.exists(video_path):
    print(f"Error: 파일 없음 {video_path}")
    sys.exit(1)

url = upload_video(video_path, title, description, tags)
print(f"\n✅ S.02 업로드 완료: {url}")

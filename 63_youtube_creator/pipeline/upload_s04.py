import sys, os
sys.path.append(os.path.dirname(__file__))
from youtube_uploader import upload_video

video_path = r"D:\AI\63_youtube_creator\pipeline\output\s04_vertical.mp4"
title = "[S.04] 코딩 몰라도 인기 유튜브 채널 벤치마킹하는 법 #Shorts"
description = """해외 인기 채널, 나도 만들어보고 싶었는데 편집·기획·코딩 배울 게 산더미라 포기하셨나요?
이제는 코딩 몰라도 됩니다 — 클로드 코드에게 말로 부탁만 하면, 잘나가는 채널의 구조(훅-공감-솔루션-액션)만 뽑아서 우리 주제로 새로 짜줍니다. 베끼는 게 아니라 구조만 배우는 방식이라 저작권 걱정도 없습니다.

📌 함께 보면 좋은 영상
▶ 본편 EP.02 — https://youtu.be/10D8uhjM-mI
▶ S.03 — https://youtu.be/(재생목록 참고)
▶ S.02 — https://youtu.be/jztIKzr453M
▶ S.00 — https://youtu.be/y7cwl8M6JDI

---
이 채널은 사람 1명 + AI 3명이 함께 만드는 자율형 AI 팀 구축 실전기입니다.
#3AI #클로드코드 #채널벤치마킹 #AI #Shorts"""

tags = ["3AI", "클로드코드", "채널벤치마킹", "AI", "인공지능", "유튜브채널만들기", "Shorts"]

if not os.path.exists(video_path):
    print(f"Error: 파일 없음 {video_path}")
    sys.exit(1)

url = upload_video(video_path, title, description, tags)
print(f"\n✅ S.04 업로드 완료: {url}")

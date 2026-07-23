import sys, os
sys.path.append(os.path.dirname(__file__))
from youtube_uploader import upload_video

video_path = r"D:\AI\63_youtube_creator\pipeline\output\S03_final.mp4"
title = "[S.03] 젠스파크 착안, 10초 컷 병렬 리서치 공개 #Shorts"
description = """Genspark처럼 여러 검색을 동시에 돌리는 병렬 리서치, 우리는 무료 API로 만들었습니다.
쿼리 4개 동시 실행, 실측 1.27초. API 비용 0원으로 만든 3AI 패러럴 서치 엔진 공개.

📌 함께 보면 좋은 영상
▶ 본편 EP.01 — https://youtu.be/9Y-PSemx3gM
▶ S.00 — https://youtu.be/y7cwl8M6JDI
▶ S.01 — https://youtu.be/yQOvdvw9ElE
▶ S.02 — https://youtu.be/jztIKzr453M

---
이 채널은 사람 1명 + AI 3명이 함께 만드는 자율형 AI 팀 구축 실전기입니다.
#3AI #병렬리서치 #Genspark #AI #Shorts"""

tags = ["3AI", "병렬리서치", "Genspark", "AI", "인공지능", "리서치자동화", "Shorts"]

if not os.path.exists(video_path):
    print(f"Error: 파일 없음 {video_path}")
    sys.exit(1)

url = upload_video(video_path, title, description, tags)
print(f"\n✅ S.03 업로드 완료: {url}")

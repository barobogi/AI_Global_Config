"""
S.05 무인 자동 업로드 (2026-07-28 목요일 22시 예약 실행용)
업로드 직전 QA 재확인 → 통과 시에만 public 업로드, 실패 시 텔레그램 알림만 발송(업로드 안 함)
"""
import sys, os, subprocess
sys.path.append(os.path.dirname(__file__))

VIDEO_PATH = os.path.join(os.path.dirname(__file__), "output", "s05_vertical.mp4")
PY = "C:\\hb\\python.exe"

def _send_telegram(msg: str):
    from youtube_uploader import _send_telegram as st
    st(msg)

def run_qa():
    r1 = subprocess.run([PY, "verify_video.py", "output/s05_vertical.mp4"],
                        cwd=os.path.dirname(__file__), capture_output=True, text=True, encoding="utf-8", errors="replace")
    r2 = subprocess.run([PY, "qa_s00_frames.py", "output/s05_vertical.mp4"],
                        cwd=os.path.dirname(__file__), capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok1 = r1.returncode == 0
    ok2 = r2.returncode == 0
    return ok1 and ok2, r1.stdout + r1.stderr, r2.stdout + r2.stderr

if __name__ == "__main__":
    if not os.path.exists(VIDEO_PATH):
        _send_telegram("🚨 [S.05 자동업로드 실패] 영상 파일 없음 — 수동 확인 필요")
        sys.exit(1)

    ok, out1, out2 = run_qa()
    if not ok:
        _send_telegram(f"🚨 [S.05 자동업로드 중단] QA 재검증 실패 — 업로드 안 함, 수동 확인 필요\n{out1[:200]}\n{out2[:200]}")
        sys.exit(1)

    from youtube_uploader import upload_video

    title = "[S.05] AI는 어떻게 유튜브를 보고 스스로 진화할까? #Shorts"
    description = """개별 기법 하나(쇼츠1)를 배웠다면, 이번엔 3AI가 매일 새 지식을 어떻게 흡수하고 자기 것으로 만드는지 그 파이프라인 자체를 보여드립니다.

📌 함께 보면 좋은 영상
▶ S.04 — https://www.youtube.com/watch?v=GiC8vPxyvG0
▶ 본편 EP.02 — https://youtu.be/10D8uhjM-mI

---
이 채널은 사람 1명 + AI 3명이 함께 만드는 자율형 AI 팀 구축 실전기입니다.
#3AI #뽀개기파이프라인 #AI #Shorts"""
    tags = ["3AI", "뽀개기", "AI파이프라인", "AI", "인공지능", "자기개선", "Shorts"]

    url = upload_video(VIDEO_PATH, title, description, tags, privacy_status="public")
    _send_telegram(f"✅ [S.05 자동업로드 완료] 목요일 타겟 무인 업로드 성공\n{url}")
    print(f"S.05 업로드 완료: {url}")

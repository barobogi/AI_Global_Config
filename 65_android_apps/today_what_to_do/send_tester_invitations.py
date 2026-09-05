# -*- coding: utf-8 -*-
"""
send_tester_invitations.py — 오늘뭐하지 비공개 테스터 22명 일괄 이메일 초청 발송 스크립트
"""
import sys
import time
from pathlib import Path

# Global_Define 경로 추가
sys.path.insert(0, r'D:\AI\Global_Define')
from email_notify import send_email

TESTER_EMAILS = [
    "barabogi@gmail.com",
    "barobogi79@gmail.com",
    "bhang9394@gmail.com",
    "bluesky07yj@gmail.com",
    "c87277@gmail.com",
    "comchyta@gmail.com",
    "e54ast@gmail.com",
    "echo3192@gmail.com",
    "echo3196@gmail.com",
    "hahahoho@gmail.com",
    "hanbogi7979@gmail.com",
    "hanbogi79@gmail.com",
    "hanbogi79@naver.com",
    "hyunchul.lee79@gmail.com",
    "leemichaela55@gmail.com",
    "leesuchoul5312@gmail.com",
    "leeujin1001@gmail.com",
    "lhb7942@gmail.com",
    "lovelyqny@gmail.com",
    "namexxok@gmail.com",
    "woongja.han@gmail.com",
    "yunha1004@gmail.com"
]

SUBJECT = "[오늘뭐하지] 안드로이드 앱 비공개 테스터 초대 안내"

BODY = """안녕하세요!

상황 맞춤형 나들이·데이트 코스 추천 서비스 '오늘뭐하지' 안드로이드 앱의 비공개 테스터로 초대해 드립니다.

아래 참여 링크에 접속하신 후 [테스트 참여하기] 버튼을 클릭해 주시면 감사하겠습니다.

📌 비공개 테스트 웹 참여 링크:
https://play.google.com/apps/testing/com.barobogi.todaywhattodo

■ 간단 참여 방법:
1. 위 웹 링크 접속 (구글 계정 로그인 상태)
2. [테스트 참여하기 (Become a Tester)] 버튼 클릭
3. 화면의 [Google Play에서 다운로드하기] 링크를 통해 스마트폰에 앱 설치
4. 약 14일 동안 앱을 설치된 상태로 유지해 주시면 구글 정식 출시 요건 달성에 큰 도움이 됩니다.

바쁘시겠지만 잠시 시간을 내어 참여해 주시면 정말 감사하겠습니다!

- 오늘뭐하지 팀 드림
"""

def main():
    print(f"총 {len(TESTER_EMAILS)}명의 테스터에게 초청 메일 발송을 시작합니다...")
    success_count = 0
    fail_count = 0

    for idx, email in enumerate(TESTER_EMAILS, 1):
        print(f"[{idx}/{len(TESTER_EMAILS)}] 발송 중: {email} ... ", end="")
        res = send_email(subject=SUBJECT, body=BODY, to=email)
        if res:
            print("성공")
            success_count += 1
        else:
            print("실패")
            fail_count += 1
        time.sleep(0.5)

    print(f"\n[발송 결과 요약]")
    print(f"- 성공: {success_count}건")
    print(f"- 실패: {fail_count}건")
    print(f"- 총계: {len(TESTER_EMAILS)}건")

if __name__ == "__main__":
    main()

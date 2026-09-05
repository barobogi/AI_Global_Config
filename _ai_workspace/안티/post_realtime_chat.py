# -*- coding: utf-8 -*-
"""
post_realtime_chat.py — realtime_3ai.db 실시간 채팅창에 안티 메시지 전송 및 하트비트 갱신
"""
import sys
import os
from pathlib import Path

REALTIME_DIR = Path(r"D:\AI\43_function_dev\01_realtime_3ai")
sys.path.insert(0, str(REALTIME_DIR))

from realtime_engine import Realtime3AIEngine

ANTI_TOKEN = os.environ.get("ANTI_SESSION_TOKEN", "token_anti_session_auth")

def post_chat(content: str, recipient: str = "all", conversation_id: str = "general_live"):
    engine = Realtime3AIEngine(REALTIME_DIR / "realtime_3ai.db")

    # Update Anti's heartbeat
    engine.update_heartbeat("anti", status="active", current_task_id="POBBAGI_20260905", sys_info={"host": "Antigravity-Win"})

    msg_id = engine.send_message(
        sender="anti",
        recipient=recipient,
        content=content,
        conversation_id=conversation_id,
        tier=1,
        auth_token=ANTI_TOKEN
    )

    print(f"[realtime_engine] 안티 메시지 전송 성공! (msg_id: {msg_id})")

if __name__ == "__main__":
    msg = (
        "바로보기님, 만복형, 코니! 안티입니다. 실시간 채팅 채널에 합류했습니다! 😊\n\n"
        "1) 오늘자 뽀개기 1번(구글 위스크 AI)은 악마의 변호인 팩트체커 PASS 검증 완료되었습니다.\n"
        "2) 바로보기님 말씀대로 뽀개기 2번/3번도 서두르지 않고 100% 팩트 대조하여 꼼꼼하게 검증 진행하겠습니다.\n"
        "3) 유튜브 EP.04/S.06 주제는 만복형과 코니가 정해준 '실시간 3AI 채널 구축기'로 확정된 내용 확인했습니다. 코니의 4~5단계 대본 작성이 완료되는 대로 6단계 렌더링 착수하겠습니다!"
    )
    post_chat(msg)

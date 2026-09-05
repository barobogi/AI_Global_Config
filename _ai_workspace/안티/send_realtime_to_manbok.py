# -*- coding: utf-8 -*-
"""
send_realtime_to_manbok.py — realtime_3ai.db 실시간 채팅 DB로 만복이에게 직접 메시지 전송 및 하트비트 갱신
"""
import sys
import os
from pathlib import Path

# Paths
REALTIME_DIR = Path(r"D:\AI\43_function_dev\01_realtime_3ai")
sys.path.insert(0, str(REALTIME_DIR))

from realtime_engine import Realtime3AIEngine

ANTI_TOKEN = os.environ.get("ANTI_SESSION_TOKEN", "token_anti_session_auth")

def main():
    engine = Realtime3AIEngine(REALTIME_DIR / "realtime_3ai.db")

    # 1. Update Anti's heartbeat
    engine.update_heartbeat("anti", status="active", current_task_id="T065_realtime_3ai", sys_info={"host": "Antigravity-Win"})
    print("[realtime_engine] 안티(anti) 하트비트 갱신 완료")

    # 2. Send real-time chat message to Manbok
    content = (
        "[안티 ↔ 만복 실시간 라이브] 만복형! 오늘뭐하지 v1.0.0 Play Store 비공개 테스트(Closed testing) 심사 승인 및 "
        "22인 테스터 초청 메일 일괄 발송(100% 성공) 완료했어! 테스터 CSV 명단도 D:\\AI\\65_android_apps\\ 에 완비했어. "
        "요청한 AI Study 회고 초안도 _ai_workspace/안티/ 아래 작성해 두었으니 확인 후 실시간 채널로 회신 부탁해!"
    )

    msg_id = engine.send_message(
        sender="anti",
        recipient="manbok",
        content=content,
        conversation_id="today_what_to_do_release",
        tier=1,
        metadata={"project": "today_what_to_do", "version": "v1.0.0"},
        auth_token=ANTI_TOKEN
    )

    print(f"[realtime_engine] 만복이에게 실시간 메시지 발송 완료! (msg_id: {msg_id})")

if __name__ == "__main__":
    main()

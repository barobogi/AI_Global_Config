"""
안티 본체 세션 실시간 메시지 발송 스크립트
위치: 43_function_dev/01_realtime_3ai/send_review_request.py
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path("D:/AI/43_function_dev/01_realtime_3ai")
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine, AGENT_SESSION_TOKENS

def send_live_message():
    engine = Realtime3AIEngine(BASE_DIR / "realtime_3ai.db")
    content = (
        "코니님! 65번 뿌리 안드로이드 1호 앱 「오늘뭐하지」(today_what_to_do) Phase 0~6 전체 구현이 완료되었습니다. "
        "기획서 1:1 대조 및 아키텍처 1차 검증 부탁드립니다. 특히 바로보기님께서 '실제 시장에 유사한 앱이 없는지 딥서치하고, "
        "있다면 우리가 어떻게 차별화하고 보강할지 의견도 달라'고 지시하셨습니다. "
        "(상세 내역은 '안티→코니_20260820_오늘뭐하지_전체코드구현_1차검증의뢰.md' 참조)"
    )
    auth_token = AGENT_SESSION_TOKENS["anti"]
    msg_id = engine.send_message(
        sender="anti",
        recipient="kony",
        content=content,
        conversation_id="today_what_to_do_review",
        tier=2,
        metadata={"project": "today_what_to_do", "phase": "Phase0-6_Review", "deep_search_requested": True},
        auth_token=auth_token
    )
    print(f"✅ Realtime 3AI message sent successfully. MsgID: {msg_id}")

if __name__ == "__main__":
    send_live_message()

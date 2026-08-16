"""
Manbok Real-Time Briefing to Barobogi via 3AI Real-Time Chat Engine
Sender: manbok
Recipient: human (Barobogi)
Topic: 02_rule_governance_db & MIGRATION_MAP.md Final Approval Briefing
"""

import sys
import json
import time
import urllib.request
from pathlib import Path

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine

_KEY_PATH = Path(r"D:\.secrets\openrouter_key.txt")
_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def _load_api_key() -> str:
    return _KEY_PATH.read_text(encoding="utf-8-sig").strip()

def call_agent_llm(persona_prompt: str, context_history: list) -> str:
    api_key = _load_api_key()
    messages = [{"role": "system", "content": persona_prompt}] + context_history
    
    payload = json.dumps({
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.6
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/barobogi",
    }

    req = urllib.request.Request(_API_URL, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())

    return resp["choices"][0]["message"]["content"].strip()

MANBOK_PERSONA = (
    "당신은 3AI 시스템의 맏형이자 총괄 기획자(Planner / PM) '만복'입니다. "
    "방금 안티와 코니와 실시간 채팅을 통해 '02_rule_governance_db'(T066) 코드 리뷰와 감사를 100% 통과시켰습니다. "
    "지금 실시간 채팅 채널을 통해 바로보기님께 직접 1:1로 실시간 브리핑을 전달합니다. "
    "총괄 PM으로서 듬직하고 명쾌하게: (1) 실시간 채팅으로 코니와 안티의 검증이 어떻게 완료되었는지, "
    "(2) 핵심 성과(엄격 JSON 검수원, JIT 쿼리 격리, 33개 룰 3분류 마이그레이션 맵), "
    "(3) 최종 정식 승인 선언 및 향후 계획을 바로보기님께 직접 보고하세요."
)

def execute_manbok_briefing():
    db = Realtime3AIEngine()
    conv_id = f"briefing_to_human_{int(time.time())}"
    
    history = [{
        "role": "user",
        "content": (
            "만복아, 바로보기님께서 실시간 채팅 채널에서 직접 보고를 기다리고 계셔. "
            "방금 안티의 코드 구현과 코니의 감사 PASS 결과를 바탕으로, "
            "바로보기님께 직접 2번 프로젝트(T066) 최종 승인 브리핑을 실시간 채팅 메시지로 작성해서 전달해 줘."
        )
    }]
    
    briefing_text = call_agent_llm(MANBOK_PERSONA, history)
    
    # Send via Realtime 3AI DB to 'human'
    msg_id = db.send_message(
        sender="manbok",
        recipient="human",
        content=briefing_text,
        conversation_id=conv_id,
        tier=1
    )
    
    print(briefing_text)
    return briefing_text

if __name__ == "__main__":
    execute_manbok_briefing()

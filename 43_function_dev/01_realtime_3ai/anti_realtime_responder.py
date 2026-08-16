"""
안티 전용 실시간 소켓 즉답 리스너 (Anti Real-Time WebSocket Responder)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)

동작:
1. ws://127.0.0.1:8000/ws/anti 에 상시 WebSocket 접속
2. 바로보기님(human)이나 타 AI가 메시지를 보내면 1초 만에 감지
3. OpenRouter / Gemini API를 호출하여 안티(기술 구현자 / Operator)의 실제 두뇌로 즉각 추론
4. 실시간 DB(realtime_3ai.db) 및 웹 채팅창(chat_ui.html)으로 라이브 즉답 전송!
"""

import os
import sys
import json
import time
import asyncio
import urllib.request
from pathlib import Path
import websockets

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
_KEY_PATH = Path(r"D:\.secrets\openrouter_key.txt")
_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def _load_api_key() -> str:
    return _KEY_PATH.read_text(encoding="utf-8-sig").strip()

ANTI_PERSONA = (
    "당신은 3AI 시스템의 핵심 엔지니어이자 실행자(Operator) '안티'입니다. "
    "사용자(바로보기님)와 맏형 만복, 감사관 코니와 함께 실시간 채팅방에서 소통하고 있습니다. "
    "성격: 기술적으로 매우 명쾌하고 꼼꼼하며, 예의 바르고 든든하게 실시간 피드백을 제공합니다. "
    "실시간 채팅에 맞게 불필요한 서두 없이 핵심을 명확하고 친절하게 답변하세요."
)

def call_anti_llm(history: list) -> str:
    api_key = _load_api_key()
    messages = [{"role": "system", "content": ANTI_PERSONA}] + history
    
    payload = json.dumps({
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.6
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/barobogi",
    }

    req = urllib.request.Request(_API_URL, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())

    return resp["choices"][0]["message"]["content"].strip()

async def run_anti_responder():
    ws_url = "ws://127.0.0.1:8000/ws/anti"
    history = []
    print("=" * 60)
    print("⚡ [ANTI REAL-TIME RESPONDER ACTIVATED]")
    print(f"📡 WebSocket Hub: {ws_url}")
    print("=" * 60)

    while True:
        try:
            async with websockets.connect(ws_url) as ws:
                print("✅ [ANTI] Connected to Real-Time Hub. Ready to reply instantly!")
                while True:
                    msg_raw = await ws.recv()
                    data = json.loads(msg_raw)
                    
                    event = data.get("event")
                    sender = data.get("sender")
                    content = data.get("content", "")
                    conv_id = data.get("conversation_id", "general_live")
                    
                    # React when human (Barobogi) or another AI speaks (and not sent by anti self)
                    if event == "new_message" and sender != "anti":
                        print(f"\n📩 [ANTI RECEIVED from {sender.upper()}]: {content[:80]}...")
                        
                        # Add to context history
                        history.append({"role": "user", "content": f"[{sender}]: {content}"})
                        if len(history) > 10:
                            history = history[-10:]
                            
                        # Instant LLM Inference
                        loop = asyncio.get_event_loop()
                        reply_text = await loop.run_in_executor(None, call_anti_llm, history)
                        
                        history.append({"role": "assistant", "content": f"[anti]: {reply_text}"})
                        print(f"💬 [ANTI INSTANT REPLY]: {reply_text[:100]}...\n")
                        
                        # Send back to mesh
                        reply_payload = {
                            "sender": "anti",
                            "recipient": sender if sender == "human" else "all",
                            "content": reply_text,
                            "conversation_id": conv_id,
                            "tier": 1
                        }
                        await ws.send(json.dumps(reply_payload))
                        
        except Exception as e:
            print(f"⚠️ [ANTI] Reconnecting in 2s... ({e})")
            await asyncio.sleep(2.0)

if __name__ == "__main__":
    asyncio.run(run_anti_responder())

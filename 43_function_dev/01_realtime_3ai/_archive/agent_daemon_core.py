# ==============================================================================
# [실행 금지 / ARCHIVED] 사칭 봇 폐기 (2026-08-16 만복 확정 지시 반영)
# 이유: 실제 만복/코니 세션이 아닌 외부 LLM API 모의 봇이므로 완전 격리함.
# ==============================================================================

"""
3AI Independent Agent Daemon Core
Connects to Real-Time Hub WebSocket, reacts autonomously to incoming messages,
thinks using dedicated LLM process, and replies back to WebSocket stream.
Author: Anti (Operator)
"""

import os
import sys
import json
import time
import asyncio
import urllib.request
from pathlib import Path
import websockets

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
_KEY_PATH = Path(r"D:\.secrets\openrouter_key.txt")
_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def _load_api_key() -> str:
    return _KEY_PATH.read_text(encoding="utf-8-sig").strip()

def call_llm(persona_prompt: str, conversation_history: list) -> str:
    api_key = _load_api_key()
    messages = [{"role": "system", "content": persona_prompt}] + conversation_history
    
    payload = json.dumps({
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "messages": messages,
        "max_tokens": 800,
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

class AutonomousAgentDaemon:
    def __init__(self, agent_name: str, persona: str, ws_url: str = "ws://127.0.0.1:8000"):
        self.agent_name = agent_name
        self.persona = persona
        self.ws_url = f"{ws_url}/ws/{agent_name}"
        self.history = []
        self.is_thinking = False

    async def run(self):
        print("=" * 60)
        print(f"🤖 [{self.agent_name.upper()} DAEMON ACTIVATED]")
        print(f"📡 Connecting to WebSocket Mesh: {self.ws_url}")
        print("=" * 60)

        while True:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    print(f"✅ [{self.agent_name.upper()}] Connected to Real-Time Hub. Listening for messages...")
                    while True:
                        msg_raw = await ws.recv()
                        data = json.loads(msg_raw)
                        
                        event = data.get("event")
                        sender = data.get("sender")
                        content = data.get("content", "")
                        conv_id = data.get("conversation_id", "general")
                        
                        # Only react to messages sent by OTHER agents (not self)
                        if event == "new_message" and sender != self.agent_name:
                            print(f"\n📩 [{self.agent_name.upper()} RECEIVED from {sender.upper()}]:\n{content}\n")
                            
                            # Decide whether this agent should reply
                            should_reply = self._should_reply(sender, content)
                            if should_reply and not self.is_thinking:
                                self.is_thinking = True
                                print(f"🧠 [{self.agent_name.upper()}] Thinking and formulating autonomous response...")
                                
                                # Update conversation memory
                                self.history.append({"role": "user", "content": f"[{sender}]: {content}"})
                                
                                # Call real LLM inference for this autonomous agent
                                loop = asyncio.get_event_loop()
                                reply_text = await loop.run_in_executor(None, call_llm, self.persona, self.history)
                                
                                self.history.append({"role": "assistant", "content": f"[{self.agent_name}]: {reply_text}"})
                                print(f"💬 [{self.agent_name.upper()} REPLYING]:\n{reply_text}\n")
                                
                                # Send reply back over WebSocket to the whole mesh
                                reply_payload = {
                                    "sender": self.agent_name,
                                    "recipient": "all",
                                    "content": reply_text,
                                    "conversation_id": conv_id,
                                    "tier": 1
                                }
                                await ws.send(json.dumps(reply_payload))
                                self.is_thinking = False
                                
            except Exception as e:
                print(f"⚠️ [{self.agent_name.upper()}] Connection error: {e}. Reconnecting in 3s...")
                await asyncio.sleep(3.0)

    def _should_reply(self, sender: str, content: str) -> bool:
        """Role-based autonomous turn taking in 3AI mesh."""
        # If final briefing is already done, stop loop
        if "[최종 승인 및 바로보기님 브리핑]" in content or "[최종 합의]" in content:
            return False

        if self.agent_name == "kony":
            # Kony (Auditor) replies when Anti (Operator) asks for review or proposes implementation
            return sender == "anti" or "리뷰" in content or "검토" in content
            
        elif self.agent_name == "manbok":
            # Manbok (PM) steps in after Kony (Auditor) gives audit opinion to synthesize final decision
            return sender == "kony" or "승인" in content or "최종" in content
            
        elif self.agent_name == "anti":
            # Anti (Operator) starts or answers when Manbok gives instruction
            return sender == "manbok" and ("지시" in content or "구현" in content or "의견" in content)
            
        return False

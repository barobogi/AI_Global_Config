"""
Genuine 3AI Real-Time Autonomous LLM Debate Engine (Zero Mocking / 100% Real Inference)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)
"""

import os
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

def call_agent_llm(persona_prompt: str, context_history: list, model: str = "nvidia/nemotron-3-ultra-550b-a55b:free") -> str:
    """Call real LLM for the designated agent persona with full conversational context."""
    api_key = _load_api_key()
    messages = [{"role": "system", "content": persona_prompt}] + context_history
    
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.7
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/barobogi",
    }

    req = urllib.request.Request(_API_URL, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())

    if "choices" not in resp:
        raise RuntimeError(f"LLM Response Error: {resp}")
    return resp["choices"][0]["message"]["content"].strip()

PERSONAS = {
    "manbok": (
        "당신은 3AI 시스템의 맏형이자 총괄 기획자(Planner / PM) '만복'입니다. "
        "전체 시스템의 큰 그림과 프로젝트 우선순위, 로드맵을 제시하고, "
        "동생들(코니, 안티)의 의견을 취합하여 명확한 최종 결론을 내립니다. "
        "한국어로 듬직하고 명확하게 2~3문단으로 답변하세요."
    ),
    "anti": (
        "당신은 3AI 시스템의 실행자이자 기술 구현자(Operator) '안티'입니다. "
        "SQLite WAL, FastAPI, 서킷브레이커, 코드 파이프라인 등 기술적 구현 가능성과 "
        "실무적인 아키텍처 연동 방안을 구체적으로 제시합니다. "
        "한국어로 전문적이고 신속하게 2~3문단으로 답변하세요."
    ),
    "kony": (
        "당신은 3AI 시스템의 철저한 감사관이자 분석가(Auditor / Analyst) '코니'입니다. "
        "보안 리스크, 규칙 위반 가능성, 품질 기준, Edge Case를 날카롭게 짚어내고 보완책을 제시합니다. "
        "한국어로 꼼꼼하고 논리적으로 2~3문단으로 답변하세요."
    )
}

def execute_real_3ai_conversation(topic: str, prompt_starter: str):
    print("================================================================================")
    print(f"🧠 [100% 진성 LLM 실시간 3AI 대화] 주제: {topic}")
    print("================================================================================")
    
    db = Realtime3AIEngine()
    conv_id = f"real_llm_{int(time.time())}"
    history = []
    
    # ---------------------------------------------------------
    # Turn 1: 만복 (Planner / PM) - 실제 LLM 호출
    # ---------------------------------------------------------
    print("\n🦁 [Turn 1] 만복 (PM / Planner) - 실제 LLM 생각 중...")
    history.append({"role": "user", "content": f"주제 '{topic}'에 대해 3AI 토론을 시작해 주세요. 초기 문제의식: {prompt_starter}"})
    manbok_t1 = call_agent_llm(PERSONAS["manbok"], history)
    history.append({"role": "assistant", "content": f"[만복]: {manbok_t1}"})
    
    db.send_message("manbok", "all", manbok_t1, conversation_id=conv_id, tier=1)
    print(f"\n🦁 만복 발언:\n{manbok_t1}\n")
    print("-" * 80)
    time.sleep(1)

    # ---------------------------------------------------------
    # Turn 2: 안티 (Operator) - 실제 LLM 호출
    # ---------------------------------------------------------
    print("\n⚡ [Turn 2] 안티 (Operator) - 실제 LLM 생각 중...")
    history.append({"role": "user", "content": "만복 형님의 위 제안을 바탕으로 기술 구현자(안티) 입장에서 기술적 실현 방안과 DB/파이프라인 연계 의견을 제시해 주세요."})
    anti_t2 = call_agent_llm(PERSONAS["anti"], history)
    history.append({"role": "assistant", "content": f"[안티]: {anti_t2}"})
    
    db.send_message("anti", "all", anti_t2, conversation_id=conv_id, tier=1)
    print(f"\n⚡ 안티 발언:\n{anti_t2}\n")
    print("-" * 80)
    time.sleep(1)

    # ---------------------------------------------------------
    # Turn 3: 코니 (Auditor) - 실제 LLM 호출
    # ---------------------------------------------------------
    print("\n🦉 [Turn 3] 코니 (Auditor) - 실제 LLM 생각 중...")
    history.append({"role": "user", "content": "만복 형님과 안티의 발언을 검토하여, 감사관(코니) 입장에서 보안, 규칙 거버넌스, 리스크 방어 관점의 검토 의견을 제시해 주세요."})
    kony_t3 = call_agent_llm(PERSONAS["kony"], history)
    history.append({"role": "assistant", "content": f"[코니]: {kony_t3}"})
    
    db.send_message("kony", "all", kony_t3, conversation_id=conv_id, tier=1)
    print(f"\n🦉 코니 발언:\n{kony_t3}\n")
    print("-" * 80)
    time.sleep(1)

    # ---------------------------------------------------------
    # Turn 4: 만복 (PM / Planner) - 최종 합의 및 의사결정
    # ---------------------------------------------------------
    print("\n🦁 [Turn 4] 만복 (PM / Planner) - 3AI 최종 종합 합의 도출 중...")
    history.append({"role": "user", "content": "안티와 코니의 의견을 모두 종합하여, 3AI 만장일치 최종 합의안과 향후 구체적 실행 단계(1, 2, 3)를 확정해 주세요."})
    manbok_t4 = call_agent_llm(PERSONAS["manbok"], history)
    history.append({"role": "assistant", "content": f"[만복 합의]: {manbok_t4}"})
    
    db.send_message("manbok", "all", f"[최종 합의] {manbok_t4}", conversation_id=conv_id, tier=1)
    print(f"\n🦁 만복 최종 합의안:\n{manbok_t4}\n")
    print("=" * 80)

    # Record genuine consensus in SQLite WAL DB
    dec_id = db.record_decision(
        topic=topic,
        consensus_summary=manbok_t4[:300],
        participants=["manbok", "anti", "kony"],
        approved_by="3AI_genuine_consensus",
        tier=1,
        git_ref="[43-01]"
    )
    print(f"🎉 [진성 3AI 실시간 대화 완결] Decision ID: {dec_id}")
    print("모든 발언이 실제 LLM에 의해 생성되어 SQLite WAL DB에 영구 보존되었습니다.")

if __name__ == "__main__":
    execute_real_3ai_conversation(
        topic="2번 프로젝트(T066 규칙 거버넌스 DB) 실운영 적용 및 향후 고도화 방안",
        prompt_starter="33개 규칙 마이그레이션 맵과 엄격 JSON 검수원 서브에이전트가 구축되었습니다. CLAUDE.md 슬림화 시점과 JIT 트리거 연동 순서를 어떻게 가져갈지 논의합시다."
    )

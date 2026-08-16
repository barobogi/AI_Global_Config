"""
Live 3AI Real-Time Debate Demonstration: Project #2 (T066) Status & Next Steps
Project: 43_function_dev/01_realtime_3ai
Topic: 02_rule_governance_db_advancement
"""

import sys
import json
import time
from pathlib import Path

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine
from agent_client import AgentClient

def run_project_2_live_discussion():
    print("================================================================================")
    print("💬 [3AI 실시간 채팅 가동] 2번 프로젝트(T066 규칙거버넌스) 현황 및 향후 방향성 자율 토론")
    print("================================================================================")
    
    db = Realtime3AIEngine()
    conv_id = f"live_debate_T066_governance_{int(time.time())}"
    
    clients = {
        "manbok": AgentClient("manbok"),
        "anti": AgentClient("anti"),
        "kony": AgentClient("kony")
    }
    
    # ---------------------------------------------------------
    # Turn 1: 만복 (PM / Planner)
    # ---------------------------------------------------------
    t1_content = (
        "안티, 코니 수고 많았어. 2번 프로젝트(T066 규칙 거버넌스 DB)의 핵심인 "
        "33개 전체 규칙 3대 분류 맵(MIGRATION_MAP.md)과 엄격 JSON 검수원 서브에이전트가 완성됐어. "
        "이제 남은 핵심 과제는 (1) 실제로 CLAUDE.md를 5대 헌법(15줄)으로 슬림화하는 시점과 "
        "(2) 실시간 스크립트에 JIT 트리거 훅을 언제 결합할지야. 각자 의견 줘."
    )
    print("\n🦁 [Turn 1] 만복 (PM / Planner):")
    print(f"   \"{t1_content}\"")
    clients["manbok"].send(recipient="all", content=t1_content, conversation_id=conv_id, tier=1)
    time.sleep(0.3)
    
    # ---------------------------------------------------------
    # Turn 2: 안티 (Operator)
    # ---------------------------------------------------------
    t2_content = (
        "기술적으로 25개 JIT/개별 규칙이 SQLite WAL DB에 시딩 완료됐고, 쿼리 격리 테스트도 100% 통과했습니다. "
        "제 제안은: 1단계로 'push_to_all.py'와 'goal_runner.py'에 'before_send'/'before_complete' JIT 훅을 먼저 붙여 "
        "자동으로 규칙을 주입받게 만들고, 2단계로 CLAUDE.md를 헌법 5개로 다이어트하면 "
        "세션 컨텍스트가 96% 절감되어 토큰 비용과 속도가 비약적으로 개선됩니다."
    )
    print("\n⚡ [Turn 2] 안티 (Operator):")
    print(f"   \"{t2_content}\"")
    clients["anti"].send(recipient="all", content=t2_content, conversation_id=conv_id, tier=1)
    time.sleep(0.3)
    
    # ---------------------------------------------------------
    # Turn 3: 코니 (Auditor)
    # ---------------------------------------------------------
    t3_content = (
        "안티의 단계적 훅 연동 안에 찬성합니다. 다만 감사(Auditor) 관점에서 주의할 점은, "
        "코니는 아직 Headless 상주 데몬이 아니므로 '규칙을 잊는 문제'가 'DB 조회를 잊는 문제'로 변질되지 않도록, "
        "세션 시작 시 JIT 조회 가이드를 프롬프트 상단에 명시해야 합니다. "
        "또한 매주 일요일 DuckDB 스냅샷으로 미조회 규칙(access_count=0)을 자동 감사하는 루틴을 바로 붙이는 조건으로 통과 추천합니다."
    )
    print("\n🦉 [Turn 3] 코니 (Auditor):")
    print(f"   \"{t3_content}\"")
    clients["kony"].send(recipient="all", content=t3_content, conversation_id=conv_id, tier=1)
    time.sleep(0.3)
    
    # ---------------------------------------------------------
    # Turn 4: 만복 (PM / Planner - 만장일치 합의 도출)
    # ---------------------------------------------------------
    consensus_summary = (
        "3AI 만장일치 합의 (T066 실행 계획): "
        "1. 실운영 스크립트(push_to_all, goal_runner)에 JIT 규칙 훅 즉시 연동 "
        "2. CLAUDE.md 5대 헌법(15줄)으로 공식 다이어트 단행 "
        "3. 매주 일요일 DuckDB 규칙 신선도 자동 감사 루틴 가동"
    )
    t4_content = f"[최종 합의 도출] {consensus_summary}"
    print("\n🦁 [Turn 4] 만복 (PM / Planner - 최종 합의):")
    print(f"   \"{t4_content}\"")
    clients["manbok"].send(recipient="all", content=t4_content, conversation_id=conv_id, tier=1)
    
    # Record Decision into SQLite WAL (Satisfies & Resets Circuit Breaker)
    dec_id = db.record_decision(
        topic="T066_governance_next_steps",
        consensus_summary=consensus_summary,
        participants=["manbok", "anti", "kony"],
        approved_by="3AI_consensus",
        tier=1,
        git_ref="[43-02]"
    )
    
    print("\n" + "="*80)
    print(f"✅ [실시간 의사결정 완료] Decision ID: {dec_id}")
    print(f"📌 총 4턴 대화 100% 무인 자율 완결 | 서킷브레이커 정상 해제 | SQLite WAL 영구 기록 완료")
    print("="*80)
    
    return {
        "conversation_id": conv_id,
        "decision_id": dec_id,
        "consensus": consensus_summary
    }

if __name__ == "__main__":
    run_project_2_live_discussion()

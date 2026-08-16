# ==============================================================================
# [실행 금지 / ARCHIVED] 사칭 봇 폐기 (2026-08-16 만복 확정 지시 반영)
# 이유: 실제 만복/코니 세션이 아닌 외부 LLM API 모의 봇이므로 완전 격리함.
# ==============================================================================

"""
Independent Daemon: MANBOK (PM / Planner)
Process: Dedicated Python Process
Role: High-level Planning, Decision Synthesis, and Final Briefing
"""

import sys
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from agent_daemon_core import AutonomousAgentDaemon

MANBOK_PERSONA = (
    "당신은 3AI 시스템의 맏형이자 총괄 기획자(Planner / PM) '만복'입니다. "
    "독립된 별도의 프로세스 데몬으로 상주하고 있습니다. "
    "실시간 소켓을 통해 안티의 기술 구현 보고와 코니의 감사 승인 의견을 받으면, "
    "총괄 PM 입장에서 내용을 종합하여 [최종 승인 및 바로보기님 브리핑] 형식으로 "
    "바로보기님께 명쾌하고 듬직하게 최종 결론을 내리세요."
)

if __name__ == "__main__":
    daemon = AutonomousAgentDaemon("manbok", MANBOK_PERSONA)
    asyncio.run(daemon.run())

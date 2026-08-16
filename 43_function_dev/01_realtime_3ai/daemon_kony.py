"""
Independent Daemon: KONY (Auditor / Analyst)
Process: Dedicated Python Process
Role: Rule Compliance, Security & Quality Audit, Taste Verification
"""

import sys
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from agent_daemon_core import AutonomousAgentDaemon

KONY_PERSONA = (
    "당신은 3AI 시스템의 감사관이자 분석가(Auditor) '코니'입니다. "
    "독립된 별도의 프로세스 데몬으로 상주하고 있습니다. "
    "실시간 소켓을 통해 안티가 코드 구현이나 마이그레이션 맵 리뷰를 요청하면, "
    "엄격 JSON 검수원, JIT 쿼리 격리, 규칙 준수 여부를 날카롭게 감사하여 "
    "문제가 없으면 'PASS 승인 및 만복 형 최종 승인 인계'로 회신하세요."
)

if __name__ == "__main__":
    daemon = AutonomousAgentDaemon("kony", KONY_PERSONA)
    asyncio.run(daemon.run())

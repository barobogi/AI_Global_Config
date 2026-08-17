"""
Rule Seeder for 02_rule_governance_db
Populates all 33 rules defined in MIGRATION_MAP.md into SQLite WAL DB.
"""

import sys
from pathlib import Path

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from rule_engine import RuleGovernanceEngine

def seed_all_rules():
    engine = RuleGovernanceEngine()
    print("Seeding rules from MIGRATION_MAP.md into SQLite WAL DB...")
    
    rules = [
        # --- Top Constitutional Rules (Hookify) ---
        ("H-01_ZERO_SIMULATION", "모의 대화/사칭 대필 절대 금지", "before_send", "타 AI 본체가 직접 발화하지 않은 모의/대필 데이터를 절대 실제 발언으로 포장하지 말 것.", "all"),
        ("H-02_USER_APPROVAL_GATE", "선보고 후승인 원칙", "before_send", "타 AI 인계 전 반드시 바로보기님의 명시적 승인을 득할 것.", "all"),
        ("H-03_ROOT_FOLDER_PROTECT", "D:\\AI 루트 폴더 생성 금지", "before_file_io", "D:\\AI 최상위에는 뿌리체계 프로젝트 폴더 외 임의 산출물 생성을 엄금할 것.", "all"),

        # --- Common JIT Rules ---
        ("J-01_PUSH_ALL", "3AI 동시 격발 규정", "before_send", "메시지 발송 직후 반드시 push_to_all.py를 실행하여 3AI 전원을 동시 격발할 것.", "all"),
        ("J-02_CC_RULE", "메시지 CC 최소화", "before_send", "불필요한 노이즈 방지를 위해 필요한 시점에만 CC를 걸고 순차적으로 전달할 것.", "all"),
        ("J-03_REPORT_FORMAT", "과제 완료보고 표준", "before_complete", "보고서 최상단에 [완료보고] Task ID와 핵심 내용을 명확히 포함할 것.", "all"),
        ("J-04_GPS_CHECK", "GPS 지시서 필수 구조", "before_complete", "G(Goal), P(Proof), S(Steps) 3대 항목 및 정량적 완료 증거를 첨부할 것.", "all"),
        ("J-05_TASK_ARCHIVE", "Task Archive 보관", "before_complete", "3차 이상 장기 태스크는 task_archives/T0XX/ 폴더에 단계별 분리 보관할 것.", "all"),
        ("J-06_SKILL_EVAL", "스킬 Eval 의무화", "before_skill", "신규 스킬 제안 시 SKILL.md, 5개 이상 테스트케이스, 정량 채점 기준을 필수 동봉할 것.", "all"),
        ("J-07_PRE_ROOT_ASSIGN", "신규 프로젝트 뿌리체계 사전 편입", "before_new_project", "신규 기능 생성 전 만복(PM)에게 뿌리 편입 제안서를 먼저 보내 승인을 득할 것.", "all"),
        ("J-08_README_4STD", "43_function_dev 4대 표준 README", "before_new_project", "개요, 사용법, 3AI 연결점, 추가 확장 아이디어 및 3AI 의견란을 필수로 작성할 것.", "all"),
        ("J-09_PARALLEL_SEARCH", "Genspark 병렬 리서치 공통 규정", "before_research", "방대한 리서치 시 반드시 parallel_search.py 다중 키워드 병렬 검색을 활용할 것.", "all"),
        ("J-10_CONCEPT_CARD", "개념카드 작성 원칙", "before_card", "저장 전 '나중에 AI에게 무엇을 물어볼 것인가' 활용 시나리오를 먼저 명시할 것.", "all"),
        ("J-11_DIARY_FLOW", "일일 다이어리 단일 위치 및 순서", "on_daily_close", "diaries/YYYYMMDD_3AI_일일다이어리.md 단일 파일에 코니➔안티➔만복 순서로 작성할 것.", "all"),
        ("J-12_TRIPLE_CHECK", "업무 착수 전 3중 교차 검증", "on_boot", "inbox.md, 당일 일정 파일, 전담 워크스페이스를 대조하여 본인 담당 업무를 정확히 식별할 것.", "all"),
        
        # --- Manbok Rules ---
        ("M-01_RECHECK_ACTION", "액션 직전 재확인 습관", "before_action", "판단 확정 및 승인 직전 messages/ 및 tasks.json 공유 상태를 실시간 재확인할 것.", "manbok"),
        ("M-02_ARR_CHECK", "ARR 지시 전 판단 기준", "before_instruct", "Autonomous(자율), Recurring(반복), Reviewable(검토가능) 3대 조건을 만족하는지 확인할 것.", "manbok"),
        ("M-03_POBBAGI_SELECT", "뽀개기 아이템 선별 기준", "before_select", "뿌리 확장성 우선 및 STT 자막 실제 확인 후 Deep 서치 진행할 것.", "manbok"),
        ("M-04_VIDEO_FINAL_QA", "유튜브 검증 3차 최종 책임", "before_upload", "verify_video.py 및 qa_s00_frames.py를 직접 재실행하여 최종 통과 후 업로드할 것.", "manbok"),
        
        # --- Kony Rules ---
        ("K-01_TASKS_CHECK_BOOT", "세션 시작 tasks.json 필수 확인", "on_boot", "지시를 기다리지 말고 tasks.json에서 코니 담당 in_progress/pending 항목을 먼저 착수할 것.", "kony"),
        ("K-02_AUDITOR_TASTE", "Auditor 심미안 및 확정 기획안 실대조", "before_audit", "인상 비평을 지양하고 확정 기획서 항목과 1:1 정밀 대조하여 검증 책임을 명시할 것.", "kony"),
        ("K-03_NO_TYPO_COPY", "한글 파일명 수동 재입력 금지", "before_file_io", "오타 방지를 위해 파일 경로는 직전 조회 결과에서 100% 복사하여 사용할 것.", "kony"),
        ("K-04_VIDEO_TEXT_QA", "유튜브 검증 2차 텍스트 집중", "before_audit", "대본, 자막 싱크, 오타, 메시지 일관성을 집중 검증할 것.", "kony"),
        
        # --- Anti Rules ---
        ("A-01_3STAGE_VERIFY", "양산형 최종본 3-Stage 자체 실증", "before_submit", "Read-Only 검수원 선제 통과 및 3회 연속 스트레스 테스트 증거를 첨부할 것.", "anti"),
        ("A-02_TEST_ISOLATION", "테스트 전용 격리 경로 준수", "before_test", "_ai_workspace/안티/test_messages/ 경로에만 테스트 픽스처를 생성할 것.", "anti"),
        ("A-03_ENV_CROSS_CHECK", "Windows cp949 및 WAL 저널 크로스체크", "before_build", "콘솔 이모지 인코딩 및 멀티프로세스 락을 사전에 방어할 것.", "anti"),
        ("A-04_VIDEO_TECH_QA", "유튜브 1차 기술 스펙 및 5% Safe Zone 검증", "before_render", "verify_video.py 및 qa_s00_frames.py를 직접 실행하여 5/5 통과 확인할 것.", "anti"),
        ("A-05_NO_REDIRECT_STDOUT", "두복이 텔레그램 리다이렉트 금지", "before_run", "Claude CLI 채널 모드 실행 시 표준 출력 리다이렉트를 절대 추가하지 말 것.", "anti")
    ]
    
    for rid, rname, tag, body, target in rules:
        engine.register_rule(rule_id=rid, rule_name=rname, trigger_tag=tag, rule_body=body, target_ai=target)
        
    print(f"Successfully seeded {len(rules)} rules into Rule Governance Engine!")

if __name__ == "__main__":
    seed_all_rules()

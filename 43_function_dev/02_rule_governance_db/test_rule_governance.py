"""
Production Test Suite for 3AI Rule Governance Engine (02_rule_governance_db)
Tests:
1. JIT Trigger-Based Rule Injection & Access Count Freshness
2. Read-Only Auditor Subagent & Strict JSON Verdict Enforcement
3. Query Isolation & Read-Only Safety
4. 43_function_dev Project Status Registry
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# UTF-8 stdout wrapper for Windows cp949 compatibility
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from rule_engine import RuleGovernanceEngine

TEST_DB_PATH = BASE_DIR / "test_rule_governance.db"

def cleanup_test_db():
    for f in [TEST_DB_PATH, BASE_DIR / "test_rule_governance.db-wal", BASE_DIR / "test_rule_governance.db-shm"]:
        if f.exists():
            try:
                os.remove(f)
            except Exception:
                pass

def test_1_jit_rule_injection():
    print("\n--- [Test 1] JIT Rule Injection & Access Count Tracking ---")
    cleanup_test_db()
    engine = RuleGovernanceEngine(db_path=TEST_DB_PATH)
    
    # Register 3 rules
    engine.register_rule(
        rule_id="RULE_01_APPROVAL",
        rule_name="선보고 후승인",
        trigger_tag="before_send",
        rule_body="타 AI 전송 전 바로보기님 명시적 승인 필수",
        target_ai="all"
    )
    engine.register_rule(
        rule_id="RULE_02_GPS",
        rule_name="GPS 완료 증거 필수",
        trigger_tag="before_complete",
        rule_body="완료보고 시 G, P, S 명시 및 증거 첨부",
        target_ai="anti"
    )
    engine.register_rule(
        rule_id="RULE_03_EVAL",
        rule_name="스킬 Eval 의무화",
        trigger_tag="before_skill",
        rule_body="스킬 제안 시 5개 이상 테스트케이스 첨부",
        target_ai="anti"
    )
    
    # Query before_send JIT rules
    rules_send = engine.get_jit_rules("before_send", caller_ai="anti")
    print(f"Loaded 'before_send' rules: {len(rules_send)}")
    assert len(rules_send) == 1
    assert rules_send[0]["rule_id"] == "RULE_01_APPROVAL"
    
    # Query before_send second time -> verify access_count == 2
    rules_send_2 = engine.get_jit_rules("before_send", caller_ai="anti")
    assert rules_send_2[0]["access_count"] == 2
    print(f"Access count successfully tracked: {rules_send_2[0]['access_count']}")
    
    print("[PASS] [Test 1] JIT Rule Injection and access count tracking verified.")

def test_2_auditor_structured_verdict():
    print("\n--- [Test 2] Read-Only Auditor Structured Verdict Verification ---")
    engine = RuleGovernanceEngine(db_path=TEST_DB_PATH)
    
    # Case A: Auditor command returning valid PASS JSON
    python_pass_cmd = [sys.executable, "-c", "import json; print(json.dumps({'verdict': 'PASS', 'evidence': 'All 3 tests passed cleanly'}))"]
    res_pass = engine.run_auditor_verification(
        target_task="T066_test", 
        caller_ai="anti", 
        test_command=python_pass_cmd, 
        auth_token="token_anti_session_auth"
    )
    print(f"Auditor Pass Result: {res_pass}")
    assert res_pass["verdict"] == "PASS"
    assert "All 3 tests passed" in res_pass["evidence"]
    
    # Case B: Auditor command returning valid FAIL JSON
    python_fail_cmd = [sys.executable, "-c", "import json; print(json.dumps({'verdict': 'FAIL', 'evidence': 'AssertionError on turn 6'}))"]
    res_fail = engine.run_auditor_verification(
        target_task="T066_test", 
        caller_ai="anti", 
        test_command=python_fail_cmd, 
        auth_token="token_anti_session_auth"
    )
    print(f"Auditor Fail Result: {res_fail}")
    assert res_fail["verdict"] == "FAIL"
    assert "AssertionError" in res_fail["evidence"]
    
    # Case C: Exit code 0 but missing structured JSON -> MUST BE FAIL
    python_no_json_cmd = [sys.executable, "-c", "print('Build succeeded without JSON output')"]
    res_no_json = engine.run_auditor_verification(
        target_task="T066_test",
        caller_ai="anti",
        test_command=python_no_json_cmd,
        auth_token="token_anti_session_auth"
    )
    print(f"Auditor Missing JSON Result: {res_no_json}")
    assert res_no_json["verdict"] == "FAIL", "Missing JSON output was not marked as FAIL!"
    assert "Strict JSON violation" in res_no_json["evidence"]
    
    # Verify audit logs in DB (3 cases: Pass, Fail, No-JSON-Fail)
    with engine._get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) as cnt FROM rule_audit_logs WHERE target_task = 'T066_test'")
        log_cnt = cursor.fetchone()["cnt"]
        assert log_cnt == 3
        
    print("[PASS] [Test 2] Structured Auditor output enforcement & strict non-JSON FAIL verified.")

def test_3_query_isolation():
    print("\n--- [Test 3] Query Isolation & Fast Read Connection ---")
    engine = RuleGovernanceEngine(db_path=TEST_DB_PATH)
    
    # Test readonly query
    with engine._get_connection(readonly=True) as conn:
        cursor = conn.execute("SELECT COUNT(*) as cnt FROM rules")
        cnt = cursor.fetchone()["cnt"]
        assert cnt == 3
        
        # Verify writing on readonly fails
        failed_write = False
        try:
            conn.execute("INSERT INTO rules (rule_id, rule_name, trigger_tag, rule_body) VALUES ('x', 'x', 'x', 'x')")
        except sqlite3.OperationalError:
            failed_write = True
        assert failed_write, "Read-only connection allowed write!"
        
    print("[PASS] [Test 3] Query isolation and read-only safety verified.")

def test_4_project_status_registry():
    print("\n--- [Test 4] 43_function_dev Project Status Registry ---")
    engine = RuleGovernanceEngine(db_path=TEST_DB_PATH)
    
    engine.update_project_status(
        project_id="43-01",
        project_name="01_realtime_3ai",
        status="completed",
        root_number=43,
        commit_ref="[43-01]",
        notes="1단계 인프라 승인 완료"
    )
    engine.update_project_status(
        project_id="43-02",
        project_name="02_rule_governance_db",
        status="in_progress",
        root_number=43,
        commit_ref="[43-02]",
        notes="규칙 거버넌스 및 검수원 서브에이전트 구축"
    )
    
    projects = engine.list_projects()
    print(f"Projects count: {len(projects)}")
    assert len(projects) == 2
    assert projects[0]["status"] == "completed"
    assert projects[1]["status"] == "in_progress"
    
    print("[PASS] [Test 4] Project status registry functional.")

def test_5_provenance_anti_impersonation():
    print("\n--- [Test 5] Provenance Security Gate (Anti-Impersonation) ---")
    engine = RuleGovernanceEngine(db_path=TEST_DB_PATH)
    
    # 1. Valid audit with correct session token
    python_pass_cmd = [sys.executable, "-c", "import json; print(json.dumps({'verdict': 'PASS', 'evidence': 'Authenticated audit'}))"]
    res_valid = engine.run_auditor_verification(
        target_task="T066_auth", 
        caller_ai="anti", 
        test_command=python_pass_cmd, 
        auth_token="token_anti_session_auth"
    )
    assert res_valid["verdict"] == "PASS"
    print("Valid session token accepted: PASS")
    
    # 2. Impersonation attempt (wrong token) -> must raise ImpersonationSecurityError
    from rule_engine import ImpersonationSecurityError
    impersonation_blocked = False
    try:
        engine.run_auditor_verification(
            target_task="T066_auth",
            caller_ai="manbok",
            test_command=python_pass_cmd,
            auth_token="fake_token_attacker"
        )
    except ImpersonationSecurityError as e:
        impersonation_blocked = True
        print(f"Impersonation successfully blocked by gate: {e}")
        
    assert impersonation_blocked, "Security gate allowed unauthorized AI impersonation!"
    print("[PASS] [Test 5] Provenance security gate 100% verified.")

def run_all_tests():
    print("==================================================")
    print("Running 3AI Rule Governance Production Test Suite")
    print("==================================================")
    test_1_jit_rule_injection()
    test_2_auditor_structured_verdict()
    test_3_query_isolation()
    test_4_project_status_registry()
    test_5_provenance_anti_impersonation()
    cleanup_test_db()
    print("\n==================================================")
    print("ALL 5 TEST SUITES PASSED WITH 100% SUCCESS")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()


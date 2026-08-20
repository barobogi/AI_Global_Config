"""
3AI Rule Governance & Structured Auditor Engine (02_rule_governance_db)
Features:
1. JIT Trigger-Based Rule Injector (Dynamic Context Injection with query isolation)
2. Read-Only Auditor Subagent with Strict JSON Verification ({"verdict": "PASS"|"FAIL", "evidence": "..."})
3. Project Status & Knowledge Manager for 43_function_dev & Root Projects
Author: Anti (Operator)
"""

import os
import sys
import json
import sqlite3
import uuid
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "rule_governance.db"

class AuditorVerdictError(Exception):
    """Raised when Auditor output fails strict JSON validation or returns FAIL."""
    pass

class ImpersonationSecurityError(Exception):
    """Raised when an unauthorized script attempts to forge or audit on behalf of another AI without session token."""
    pass

AGENT_SESSION_TOKENS = {
    "manbok": os.environ.get("MANBOK_SESSION_TOKEN", "token_manbok_session_auth"),
    "kony": os.environ.get("KONY_SESSION_TOKEN", "token_kony_session_auth"),
    "anti": os.environ.get("ANTI_SESSION_TOKEN", "token_anti_session_auth"),
    "system": "token_system_internal"
}

class RuleGovernanceEngine:
    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self, readonly: bool = False) -> sqlite3.Connection:
        """
        Isolated connection for high-priority rule checks.
        Uses WAL mode and a short busy_timeout to prevent hanging during heavy traffic.
        """
        conn = sqlite3.connect(str(self.db_path), timeout=2.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 2000;")
        if readonly:
            conn.execute("PRAGMA query_only = ON;")
        return conn

    def _init_db(self):
        schema_path = BASE_DIR / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            with self._get_connection() as conn:
                conn.executescript(schema_sql)
                conn.commit()

    # --- 1. JIT Rule Management & Injection ---
    def register_rule(self, rule_id: str, rule_name: str, trigger_tag: str, 
                      rule_body: str, target_ai: str = "all") -> str:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO rules (rule_id, rule_name, target_ai, trigger_tag, rule_body, is_active, access_count)
                VALUES (?, ?, ?, ?, ?, 1, 0)
                ON CONFLICT(rule_id) DO UPDATE SET
                    rule_name=excluded.rule_name,
                    target_ai=excluded.target_ai,
                    trigger_tag=excluded.trigger_tag,
                    rule_body=excluded.rule_body,
                    is_active=1
                """,
                (rule_id, rule_name, target_ai, trigger_tag, rule_body)
            )
            conn.commit()
        return rule_id

    def get_jit_rules(self, trigger_tag: str, caller_ai: str = "anti") -> list:
        """
        Fetch rules relevant to the current action trigger (e.g. before_send, before_complete).
        Updates access_count and last_accessed_at for freshness auditing.
        """
        with self._get_connection() as conn:
            # First increment access count for matching active rules
            conn.execute(
                """
                UPDATE rules 
                SET access_count = access_count + 1, last_accessed_at = CURRENT_TIMESTAMP
                WHERE trigger_tag = ? AND is_active = 1 
                  AND (target_ai = 'all' OR target_ai = ?)
                """,
                (trigger_tag, caller_ai)
            )
            conn.commit()
            
            # Then fetch the updated rows
            cursor = conn.execute(
                """
                SELECT * FROM rules 
                WHERE trigger_tag = ? AND is_active = 1 
                  AND (target_ai = 'all' OR target_ai = ?)
                ORDER BY id ASC
                """,
                (trigger_tag, caller_ai)
            )
            rules = [dict(r) for r in cursor.fetchall()]
            return rules

    # --- 2. Read-Only Auditor Subagent & Structured Verification ---
    def run_auditor_verification(self, target_task: str, caller_ai: str, 
                                 test_command: list, auth_token: str = None) -> dict:
        """
        Execute validation using Read-Only Auditor pattern.
        Enforces security provenance: caller_ai must provide matching session auth_token.
        Enforces strict JSON schema: {"verdict": "PASS" | "FAIL", "evidence": "..."}
        """
        # Provenance verification
        if caller_ai in AGENT_SESSION_TOKENS:
            expected = AGENT_SESSION_TOKENS[caller_ai]
            if auth_token != expected and os.environ.get("ENFORCE_PROVENANCE_AUTH", "1") == "1":
                raise ImpersonationSecurityError(
                    f"[Security Gate] Impersonation blocked: Cannot execute audit request as '{caller_ai}' without valid session token."
                )

        aud_id = f"aud_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # Execute test command in read-only / subproc environment
        try:
            res = subprocess.run(
                test_command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )
            stdout = res.stdout.strip()
            stderr = res.stderr.strip()
            
            # Parse structured JSON verdict from output
            parsed = self._extract_structured_verdict(stdout)
            if not parsed:
                # Strict enforcement: Missing or invalid JSON output is ALWAYS a FAIL verdict
                parsed = {
                    "verdict": "FAIL",
                    "evidence": f"Strict JSON violation: Auditor output does not contain structured JSON schema {{'verdict': 'PASS'|'FAIL', 'evidence': '...'}}. ExitCode: {res.returncode}. Output:\n{stdout[:300]}"
                }
        except Exception as e:
            parsed = {
                "verdict": "FAIL",
                "evidence": f"Auditor execution exception: {str(e)}"
            }

        # Validate structured JSON keys
        verdict = str(parsed.get("verdict", "FAIL")).upper()
        if verdict not in ("PASS", "FAIL"):
            verdict = "FAIL"
        evidence = str(parsed.get("evidence", "No evidence provided"))

        # Log into rule_audit_logs
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO rule_audit_logs (audit_id, target_task, caller_ai, auditor_worker, verdict, evidence)
                VALUES (?, ?, ?, 'Auditor-Subagent-ReadOnly', ?, ?)
                """,
                (aud_id, target_task, caller_ai, verdict, evidence)
            )
            conn.commit()

        return {
            "audit_id": aud_id,
            "verdict": verdict,
            "evidence": evidence
        }

    def _extract_structured_verdict(self, raw_output: str) -> dict:
        """Find and parse JSON verdict block from output."""
        try:
            return json.loads(raw_output)
        except Exception:
            pass

        start = raw_output.find("{")
        end = raw_output.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                candidate = raw_output[start:end+1]
                data = json.loads(candidate)
                if "verdict" in data:
                    return data
            except Exception:
                pass
        return None

    # --- 3. Project Status & Knowledge Manager ---
    def update_project_status(self, project_id: str, project_name: str, 
                              status: str = "in_progress", root_number: int = 43, 
                              overview: str = None, usage_guide: str = None, 
                              expansion_ideas: str = None, commit_ref: str = None, 
                              notes: str = None) -> str:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO projects_status (project_id, project_name, root_number, status, overview, usage_guide, expansion_ideas, last_commit_ref, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(project_id) DO UPDATE SET
                    project_name=excluded.project_name,
                    root_number=excluded.root_number,
                    status=excluded.status,
                    overview=COALESCE(excluded.overview, projects_status.overview),
                    usage_guide=COALESCE(excluded.usage_guide, projects_status.usage_guide),
                    expansion_ideas=COALESCE(excluded.expansion_ideas, projects_status.expansion_ideas),
                    last_commit_ref=COALESCE(excluded.last_commit_ref, projects_status.last_commit_ref),
                    notes=COALESCE(excluded.notes, projects_status.notes),
                    updated_at=CURRENT_TIMESTAMP
                """,
                (project_id, project_name, root_number, status, overview, usage_guide, expansion_ideas, commit_ref, notes)
            )
            conn.commit()
        return project_id

    def list_projects(self) -> list:
        with self._get_connection(readonly=True) as conn:
            cursor = conn.execute("SELECT * FROM projects_status ORDER BY project_id ASC")
            return [dict(r) for r in cursor.fetchall()]

    def list_active_rules(self, caller_ai: str) -> list:
        """caller_ai(target_ai='all' 또는 본인)에게 해당하는 활성 규칙 전체를 trigger_tag 무관하게 반환.
        코니처럼 세션 중 동적으로 DB를 조회할 수 없는 AI를 위한 정적 다이제스트 생성용."""
        with self._get_connection(readonly=True) as conn:
            cursor = conn.execute(
                """
                SELECT * FROM rules
                WHERE is_active = 1 AND (target_ai = 'all' OR target_ai = ?)
                ORDER BY target_ai ASC, id ASC
                """,
                (caller_ai,)
            )
            return [dict(r) for r in cursor.fetchall()]


def _cli():
    import argparse
    parser = argparse.ArgumentParser(description="3AI Rule Governance Engine CLI (안티/만복 터미널 직접 조회용)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_jit = sub.add_parser("jit", help="특정 trigger_tag 시점 규칙 조회 (JIT)")
    p_jit.add_argument("--trigger", required=True, help="예: before_send, before_complete")
    p_jit.add_argument("--caller", required=True, choices=["manbok", "kony", "anti"], help="호출 주체 AI")
    p_jit.add_argument("--json", action="store_true", help="JSON 형식으로 출력 (기본은 사람이 읽기 좋은 텍스트)")

    p_all = sub.add_parser("list-active", help="caller_ai 대상 전체 활성 규칙 조회 (trigger 무관)")
    p_all.add_argument("--caller", required=True, choices=["manbok", "kony", "anti"])
    p_all.add_argument("--json", action="store_true")

    args = parser.parse_args()
    engine = RuleGovernanceEngine()

    if args.cmd == "jit":
        rules = engine.get_jit_rules(args.trigger, caller_ai=args.caller)
    else:
        rules = engine.list_active_rules(args.caller)

    if args.json:
        print(json.dumps(rules, ensure_ascii=False, indent=2))
        return

    if not rules:
        print(f"(해당 조건에 맞는 활성 규칙 없음)")
        return
    for r in rules:
        print(f"[{r.get('rule_id', '?')}] {r.get('rule_name', '')} (대상: {r.get('target_ai')})")
        body = r.get('rule_body', '')
        if body:
            print(f"  {body}")
        print()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) > 1:
        _cli()
    else:
        engine = RuleGovernanceEngine()
        print("Rule Governance Engine Ready. 사용법: python rule_engine.py jit --trigger <tag> --caller <ai>")

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
                                 test_command: list) -> dict:
        """
        Execute validation using Read-Only Auditor pattern.
        Enforces strict JSON schema: {"verdict": "PASS" | "FAIL", "evidence": "..."}
        """
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
                # If command exited 0 and no JSON, parse based on exit code & output
                if res.returncode == 0:
                    parsed = {
                        "verdict": "PASS",
                        "evidence": f"Process exited with code 0. Output:\n{stdout[:500]}"
                    }
                else:
                    parsed = {
                        "verdict": "FAIL",
                        "evidence": f"Process exited with code {res.returncode}. Error:\n{stderr[:500]}\nOutput:\n{stdout[:500]}"
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

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    engine = RuleGovernanceEngine()
    print("Rule Governance Engine Ready.")

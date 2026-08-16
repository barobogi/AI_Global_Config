-- ==============================================================================
-- 3AI Rule Governance & Project Knowledge Hub Schema (SQLite WAL Mode)
-- Project: 43_function_dev/02_rule_governance_db
-- ==============================================================================

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 3000;

-- 1. Rules Table (Dynamic JIT Context Injection)
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id TEXT UNIQUE NOT NULL,            -- e.g., RULE_BEFORE_SEND_APPROVAL
    rule_name TEXT NOT NULL,                -- Human readable rule title
    target_ai TEXT NOT NULL DEFAULT 'all',  -- all, manbok, kony, anti, slot4, slot5
    trigger_tag TEXT NOT NULL,              -- before_send, before_complete, before_skill, on_boot
    rule_body TEXT NOT NULL,                -- Actual rule text injected into context
    is_active INTEGER NOT NULL DEFAULT 1,   -- 1 = active, 0 = deprecated
    access_count INTEGER NOT NULL DEFAULT 0,-- Number of times queried (freshness tracking)
    last_accessed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rules_trigger ON rules(trigger_tag, target_ai, is_active);

-- 2. Project Status & Knowledge Hub Table (43_function_dev Projects)
CREATE TABLE IF NOT EXISTS projects_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT UNIQUE NOT NULL,        -- e.g., 43-01, 43-02
    project_name TEXT NOT NULL,             -- e.g., 01_realtime_3ai
    root_number INTEGER NOT NULL DEFAULT 43,-- 43 (function_dev)
    status TEXT NOT NULL DEFAULT 'planning',-- planning, in_progress, completed, promoted
    overview TEXT,                          -- Project Overview summary
    usage_guide TEXT,                       -- Quickstart usage command
    expansion_ideas TEXT,                   -- Markdown / Text for future expansion ideas
    last_commit_ref TEXT,                   -- [43-NN] commit hash
    notes TEXT,                             -- Operational notes
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_projects_status ON projects_status(status);

-- 3. Read-Only Auditor Verification Logs (Strict JSON Structured Output)
CREATE TABLE IF NOT EXISTS rule_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id TEXT UNIQUE NOT NULL,          -- e.g., aud_20260816_001
    target_task TEXT NOT NULL,              -- Task or Project ID
    caller_ai TEXT NOT NULL,                -- AI requesting verification
    auditor_worker TEXT NOT NULL,           -- Read-only worker persona
    verdict TEXT NOT NULL,                  -- PASS or FAIL (Strict JSON enforced)
    evidence TEXT NOT NULL,                 -- Proof details / assert outputs
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_task ON rule_audit_logs(target_task, verdict);

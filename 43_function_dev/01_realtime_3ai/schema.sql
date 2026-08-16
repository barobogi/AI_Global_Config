-- ==============================================================================
-- 3AI Real-Time Hybrid Engine Schema (SQLite WAL Mode)
-- Project: 43_function_dev/01_realtime_3ai
-- Purpose: Low-latency (<5ms) concurrent multi-agent messaging & decision memory
-- ==============================================================================

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;

-- 1. Real-time Messages Table (Transactional Chat & Inter-Agent Signals)
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id TEXT UNIQUE NOT NULL,             -- UUID / NanoID (e.g., msg_20260816_001)
    conversation_id TEXT NOT NULL,          -- Thread / Topic ID (e.g., T065_realtime_3ai)
    sender TEXT NOT NULL,                   -- manbok, kony, anti, human, system
    recipient TEXT NOT NULL,                -- kony, anti, manbok, all
    content TEXT NOT NULL,                  -- Message text or JSON payload
    tier INTEGER NOT NULL DEFAULT 1,        -- 1 (Zero-Human), 2 (Auto-Notify), 3 (Human-Approval)
    status TEXT NOT NULL DEFAULT 'unread',  -- unread, read, processed, escalated, cancelled
    metadata TEXT,                          -- JSON string (file attachments, GPS fields, tokens)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status, recipient);
CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at);

-- 2. Structured Decisions & Consensus Memory Table (Anti-Hallucination)
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT UNIQUE NOT NULL,       -- e.g., DEC_20260816_T065
    topic TEXT NOT NULL,                    -- Task / Feature Topic
    consensus_summary TEXT NOT NULL,        -- Agreed outcome / specification
    participants TEXT NOT NULL,             -- JSON Array ["manbok", "kony", "anti"]
    tier INTEGER NOT NULL DEFAULT 1,
    approved_by TEXT NOT NULL,              -- 3AI_consensus or human_barobogi
    git_commit_ref TEXT,                    -- Commit hash if code was committed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_decisions_topic ON decisions(topic);

-- 3. Agent Liveness & Heartbeat Registry
CREATE TABLE IF NOT EXISTS agent_heartbeats (
    agent_name TEXT PRIMARY KEY,            -- manbok, kony, anti
    status TEXT NOT NULL DEFAULT 'idle',    -- idle, thinking, executing, offline
    current_task_id TEXT,                   -- Current Task ID being processed
    last_ping DATETIME DEFAULT CURRENT_TIMESTAMP,
    system_info TEXT                        -- Model, Process ID, Memory status
);

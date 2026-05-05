-- Migration: add email settings and logs to queue DB

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS email_settings (
    id TEXT PRIMARY KEY,
    provider TEXT,
    data TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS email_logs (
    id TEXT PRIMARY KEY,
    to_addr TEXT,
    subject TEXT,
    provider TEXT,
    status TEXT,
    response TEXT,
    attempts INTEGER,
    created_at TEXT,
    updated_at TEXT
);

COMMIT;

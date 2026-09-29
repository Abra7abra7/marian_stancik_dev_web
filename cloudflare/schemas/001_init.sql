-- 001_init.sql: Core schema
-- Spustit: wrangler d1 execute marian-stancik-db --file schemas/001_init.sql

CREATE TABLE IF NOT EXISTS clients (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL,
  domain TEXT NOT NULL,
  name TEXT,
  plan TEXT DEFAULT 'one-time',
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  status TEXT DEFAULT 'active',
  timezone TEXT DEFAULT 'UTC',
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audits (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('geo','readiness','full')),
  status TEXT DEFAULT 'pending' CHECK(status IN ('pending','running','done','failed')),
  score INTEGER,
  baseline_score INTEGER,
  score_delta INTEGER,
  report_url TEXT,
  started_at TEXT,
  completed_at TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS audit_results (
  audit_id TEXT PRIMARY KEY,
  raw JSON NOT NULL,
  summary TEXT,
  recommendations JSON,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (audit_id) REFERENCES audits(id)
);

CREATE TABLE IF NOT EXISTS alerts (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  type TEXT NOT NULL,
  message TEXT,
  score_before INTEGER,
  score_after INTEGER,
  acknowledged INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  plan TEXT NOT NULL CHECK(plan IN ('monitoring','compliance_watch')),
  stripe_subscription_id TEXT,
  amount_cents INTEGER NOT NULL,
  status TEXT DEFAULT 'active',
  next_billing_at TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX idx_audits_client ON audits(client_id);
CREATE INDEX idx_audits_status ON audits(status);
CREATE INDEX idx_alerts_client ON alerts(client_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
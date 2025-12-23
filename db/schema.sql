CREATE TABLE IF NOT EXISTS keys (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  purpose TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS key_versions (
  id TEXT PRIMARY KEY,
  key_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  encrypted_key BLOB NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS services (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  active BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  service_id TEXT NOT NULL,
  action TEXT NOT NULL,
  key_id TEXT,
  key_version INTEGER,
  timestamp TIMESTAMP NOT NULL,
  result TEXT NOT NULL,
  prev_hash TEXT,
  hash TEXT NOT NULL
);

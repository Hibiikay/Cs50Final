-- schema.sql
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS donations;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    play TEXT CHECK(play IN ('yes','no')) NOT NULL,
    player_id TEXT UNIQUE,
    receipt TEXT,
    club TEXT,
    registered DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor TEXT NOT NULL,
    type TEXT CHECK(type IN ('cash','food')) NOT NULL,
    amount REAL DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample seed users (4 players and 1 supporter)
INSERT INTO users (name, email, play, player_id, club, receipt) VALUES
  ('John Doe', 'john@example.com', 'yes', 'HF-AB12', 'Lions FC', NULL),
  ('Jane Smith', 'jane@example.com', 'yes', 'HF-CD34', 'Eagles FC', NULL),
  ('Ahmed Musa', 'ahmed@example.com', 'yes', 'HF-EF56', 'Sharks FC', NULL),
  ('Maria Lopez', 'maria@example.com', 'no', NULL, NULL, NULL);

-- Sample donations
INSERT INTO donations (donor, type, amount) VALUES
  ('John Doe', 'cash', 15000),
  ('Jane Smith', 'cash', 15000),
  ('Maria Lopez', 'food', 0);

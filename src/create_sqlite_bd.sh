#!/bin/bash
start=$SECONDS

echo "[- PARTIE 4 INIT SQLITE -]"

DB_NAME="./data/sqlite.db"

# 1. Initialisation du schéma relationnel
sqlite3 "$DB_NAME" <<EOF
  CREATE TABLE IF NOT EXISTS repos (
      id TEXT PRIMARY KEY,
      stars INTEGER DEFAULT 0,
      categories TEXT,
      url TEXT

  );

  CREATE TABLE IF NOT EXISTS error_catalog (
      error_id INTEGER PRIMARY KEY AUTOINCREMENT,
      error_name TEXT UNIQUE
  );

  CREATE TABLE IF NOT EXISTS error_reports (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      repo_id TEXT,
      error_id INTEGER,
      occurrence_count INTEGER,
      FOREIGN KEY(repo_id) REFERENCES repos(id),
      FOREIGN KEY(error_id) REFERENCES error_catalog(error_id),
      UNIQUE(repo_id, error_id)
  );
EOF

echo "database sqlite créé dans $DB_NAME [$((SECONDS - start))s]" 

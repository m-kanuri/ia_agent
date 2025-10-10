# Intelligent Forensics Agent (Agent 1) — Database v1.0
# Module: database.py
# Author: Murthy Kanuri
# Date: 10 October 2025
#
# Purpose
# -------
# Keep storage simple and portable: a single SQLite file with one table (`files`)
# for minimal metadata. We upsert so re-runs are idempotent.
#
# Why SQLite:
# - Zero-config, cross-platform, easy to archive with the rest of the evidence.
# - Queryable on any machine (no server to stand up).
# - WAL mode gives safe concurrent reads during a scan.
#
# Usage
# -----
#   con = connect("agent.db")
#   upsert_files(con, rows)         # rows = dicts from processor/basic_metadata
#   print(count_by_mime(con))
#
# Notes:
# - We key on `path` for idempotency. For stricter change tracking you could
#   add a composite (path, mtime) or a separate history table later.
# - We only store metadata + hash here; no file contents (data minimisation).

from __future__ import annotations
import sqlite3
from typing import Iterable, Dict, Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    size INTEGER,
    mtime REAL,
    ctime REAL,
    mime TEXT,
    sha256 TEXT
);
CREATE INDEX IF NOT EXISTS idx_mime ON files(mime);
CREATE INDEX IF NOT EXISTS idx_sha ON files(sha256);
"""

def connect(db_path: str) -> sqlite3.Connection:
    """
    Open (or create) the SQLite DB, enable WAL, and ensure the schema exists.
    """
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL;")
    con.executescript(SCHEMA)
    return con

def upsert_files(con: sqlite3.Connection, rows: Iterable[Dict[str, Any]]) -> int:
  """
    Insert or update file metadata rows in an idempotent way.
    """
    cur = con.cursor()
    count = 0
    for r in rows:
        cur.execute(
            """INSERT INTO files(path,size,mtime,ctime,mime,sha256)
            VALUES(:path,:size,:mtime,:ctime,:mime,:sha256)
            ON CONFLICT(path) DO UPDATE SET
                size=excluded.size,
                mtime=excluded.mtime,
                ctime=excluded.ctime,
                mime=excluded.mime,
                sha256=excluded.sha256
            """,
            r,
        )
        count += 1
    con.commit()
    return count

def count_by_mime(con: sqlite3.Connection):
    """
    Aggregate helper for the Run Summary: (mime, count) sorted by frequency.
    """
    cur = con.cursor()
    cur.execute("SELECT mime, COUNT(*) FROM files GROUP BY mime ORDER BY COUNT(*) DESC")
    return cur.fetchall()

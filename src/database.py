
# SQLite storage. Why: portable, low-overhead, queryable.
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
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL;")
    con.executescript(SCHEMA)
    return con

def upsert_files(con: sqlite3.Connection, rows: Iterable[Dict[str, Any]]) -> int:
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
    cur = con.cursor()
    cur.execute("SELECT mime, COUNT(*) FROM files GROUP BY mime ORDER BY COUNT(*) DESC")
    return cur.fetchall()

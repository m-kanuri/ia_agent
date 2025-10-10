
import sqlite3, tempfile, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from database import connect, upsert_files, count_by_mime

def test_db_roundtrip(tmp_path):
    con = connect(str(tmp_path / "t.db"))
    rows = [{
        "path":"x","size":1,"mtime":0.0,"ctime":0.0,"mime":"text/plain","sha256":"0"*64
    }]
    n = upsert_files(con, rows)
    assert n == 1
    counts = dict(count_by_mime(con))
    assert counts.get("text/plain", 0) == 1

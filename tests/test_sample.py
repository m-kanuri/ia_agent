import re
import os
import sys
import subprocess
import tempfile
import sqlite3
import unittest
from pathlib import Path

PYTHON = sys.executable  # Use the same Python as your venv


def run_cli(target: Path, db_path: Path):
    """
    Run `python -m src.main --target <target> --db <db>` and return (code, stdout, stderr).
    """
    cmd = [
        PYTHON, "-m", "src.main",
        "--target", str(target),
        "--db", str(db_path),
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parents[1])  # project root
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestIAAgent(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with diverse sample files
        self.tmpdir = tempfile.TemporaryDirectory()
        self.target = Path(self.tmpdir.name)

        # Text file
        (self.target / "note.txt").write_text("hello world\n", encoding="utf-8")

        # CSV file
        (self.target / "data.csv").write_text("a,b\n1,2\n", encoding="utf-8")

        # PDF file (minimal header + EOF)
        (self.target / "doc.pdf").write_bytes(b"%PDF-1.4\n%EOF\n")

        # JPEG file (minimal header)
        (self.target / "image.jpg").write_bytes(b"\xFF\xD8\xFF")

        self.db_path = self.target / "agent.db"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_cli_creates_db(self):
        code, out, err = run_cli(self.target, self.db_path)
        self.assertEqual(code, 0, msg=f"Process failed. STDERR:\n{err}")
        self.assertTrue(self.db_path.exists(), "DB file was not created")

        # Confirm DB is a valid SQLite file with at least one table
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            self.assertGreater(len(tables), 0, "No tables found in the database")

    def test_cli_prints_summary(self):
        code, out, err = run_cli(self.target, self.db_path)
        self.assertEqual(code, 0, msg=err)

        # Basic checks for summary output
        self.assertIn("=== Run Summary ===", out)
        self.assertIn("Files processed:", out)
        self.assertIn(str(self.target), out)
        self.assertIn(str(self.db_path), out)

    def test_files_processed_matches_created(self):
        code, out, err = run_cli(self.target, self.db_path)
        self.assertEqual(code, 0, msg=err)

        m = re.search(r"Files processed:\s+(\d+)", out)
        self.assertIsNotNone(m, "Couldn't find 'Files processed' in output")
        files_processed = int(m.group(1))

        # We created 4 files in setUp()
        self.assertEqual(files_processed, 4, f"Expected 4 files, got {files_processed}")


if __name__ == "__main__":
    unittest.main()

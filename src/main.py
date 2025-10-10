# Intelligent Forensics Agent (Agent 1) — CLI Orchestrator v1.0
# Module: main.py
# Author: Murthy Kanuri
# Date: 10 October 2025
#
# Purpose
# -------
# Wire the pipeline together:
#   discover → identify (content-first) → extract metadata → upsert into SQLite,
#   then print a short run summary. Also trains a tiny, optional demo “learner”
#   from metadata only (no content), purely for illustration in the presentation.
#
# Notes
# -----
# - Read-only: this module never mutates target files.
# - Audit: we record which detector decided the MIME.
# - Reproducibility: deterministic CLI; idempotent DB upserts.
#
# Usage
# -----
#   python -m src.main --target sample_data --db agent.db
#
# Inputs / Outputs
# ----------------
# - Input:  --target (dir), optional --limit, repeated --exclude
# - Output: SQLite DB (table `files`) + console “Run Summary”
#

from __future__ import annotations
import argparse, os, time, json
from typing import List
from src.discovery import walk_safe
from src.identifier import detect_mime
from src.processor import basic_metadata
from src.database import connect, upsert_files, count_by_mime
from src.learner import features_from_meta, train_demo


def run(target: str, db: str, limit: int | None, excludes: List[str]) -> int:
   """
    Execute one scan end-to-end and print a concise summary.

    Why structured this way:
    - Keep the orchestration small and readable; all heavy lifting lives in
      the components (discovery/identifier/processor/database/learner).
    - Make it easy to unit test by returning the number of rows written.
    """
    files = []
    for i, path in enumerate(walk_safe(target, set(excludes))):
        mime, method = detect_mime(path)
        meta = basic_metadata(path, mime)
        meta["detector"] = method  # why: auditability of detection
        files.append(meta)
        if limit and i + 1 >= limit:
            break
    con = connect(db)
    n = upsert_files(con, files)

    # toy labels: archive images & pdfs
    X, y = [], []
    for m in files:
        X.append(features_from_meta(m))
        y.append(1 if (str(m['mime']).startswith('image/') or str(m['mime'])=='application/pdf') else 0)
    _ = train_demo(X, y, model_path=os.path.join(os.path.dirname(db), "demo_model.joblib"))

    print("=== Run Summary ===")
    print(f"Target: {os.path.abspath(target)}")
    print(f"DB: {os.path.abspath(db)}")
    print(f"Files processed: {n}")
    print("Counts by MIME:")
    for mime, cnt in count_by_mime(con):
        print(f"  {mime}: {cnt}")
    if files:
        print("Sample record:")
        print(json.dumps(files[0], indent=2)[:600])
    return n

def parse_args():
    """
    Keep the CLI minimal and predictable. Repeated --exclude is supported.

    Example:
      python -m src.main --target ~/Documents --db agent.db --exclude .git --exclude node_modules
    """
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    p.add_argument("--db", default=os.path.join('/mnt/data/ia_agent', "agent.db"))
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--exclude", action="append", default=[])
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    t0 = time.time()
    run(args.target, args.db, args.limit, args.exclude)
    print(f"Elapsed: {time.time()-t0:.2f}s")

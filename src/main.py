
from __future__ import annotations
import argparse, os, time, json
from typing import List
from src.discovery import walk_safe
from src.identifier import detect_mime
from src.processor import basic_metadata
from src.database import connect, upsert_files, count_by_mime
from src.learner import features_from_meta, train_demo


def run(target: str, db: str, limit: int | None, excludes: List[str]) -> int:
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

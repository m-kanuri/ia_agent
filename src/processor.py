
# Processor: minimal metadata with SHA-256. Why: data minimisation with evidential utility.
from __future__ import annotations
import os, hashlib
from typing import Dict

def sha256_of_file(path: str, block_size: int = 65536) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
    return h.hexdigest()

def basic_metadata(path: str, mime: str) -> Dict[str, object]:
    st = os.stat(path)
    return {
        "path": os.path.abspath(path),
        "size": int(st.st_size),
        "mtime": float(st.st_mtime),
        "ctime": float(getattr(st, "st_ctime", st.st_mtime)),
        "mime": mime,
        "sha256": sha256_of_file(path),
    }

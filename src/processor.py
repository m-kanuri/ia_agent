# Intelligent Forensics Agent (Agent 1) — Processor v1.0
# Module: processor.py
# Author: Murthy Kanuri
# Date: 10 October 2025
#
# Purpose
# -------
# Collect the bare minimum we need for triage and audit:
#   - absolute path, size, times
#   - MIME (passed in from identifier)
#   - SHA-256 (for integrity)
#
# Why:
# - Data minimisation: we don’t keep contents, only metadata + a hash.
# - Evidence utility: SHA-256 lets us verify a file without storing it.
# - Reproducibility: stat + deterministic hashing in fixed-size chunks.

from __future__ import annotations
import os, hashlib
from typing import Dict

def sha256_of_file(path: str, block_size: int = 65536) -> str:
    """
    Stream a file and return its SHA-256 hex digest.

    Notes
    -----
    - Chunked reads keep memory use predictable on large files.
    - We raise on I/O errors by default; it’s clearer during development.
      (If you want “log and carry on”, catch exceptions at the call site.)
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
    return h.hexdigest()

def basic_metadata(path: str, mime: str) -> Dict[str, object]:
        """
    Assemble minimal, useful metadata for one file.

    Returns
    -------
    dict with:
      - path   : absolute path (str)
      - size   : bytes (int)
      - mtime  : last modified (epoch float)
      - ctime  : creation/metadata-change (epoch float; OS-dependent)
      - mime   : MIME type (str) — passed in (we don’t re-detect here)
      - sha256 : SHA-256 hex digest (str)

    Notes
    -----
    - `ctime` on Unix is “metadata change time”, not strictly “creation”.
      On Windows it is closer to “creation time”. We surface it as-is and
      explain the nuance in the README/presentation.
    - We only open the file to hash it; no other content is retained.
    """
    st = os.stat(path)
    return {
        "path": os.path.abspath(path),
        "size": int(st.st_size),
        "mtime": float(st.st_mtime),
        "ctime": float(getattr(st, "st_ctime", st.st_mtime)),
        "mime": mime,
        "sha256": sha256_of_file(path),
    }

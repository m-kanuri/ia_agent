# Intelligent Forensics Agent (Demo)

Practical implementation of my Unit 6 design for an **Intelligent Forensics Agent**.

**Agent 1 (implemented)**: safe discovery (read-only), **content-first** file identification, minimal metadata extraction, and storage in SQLite.  
Includes unit tests and a tiny, optional ML demo (logistic regression) for “archive?” recommendations.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Tests](https://img.shields.io/badge/tests-unittest-green)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)

---


---

## Why this approach

- **Content-first identification**: `python-magic` → `filetype` → *extension* fallback.  
  More robust than filename extensions alone.
- **Data minimisation**: capture **path, size, timestamps, SHA-256, MIME** — nothing else.
- **Safety**: read-only file access; platform-aware excludes to avoid system areas.
- **Auditability**: deterministic CLI run that writes to SQLite with idempotent upserts.
- **Reproducibility**: pinned deps; tests + coverage; simple, single-command demo.

---

## Requirements

- Python **3.11** (tested). 3.10–3.12 should also work.
- **macOS** requires `libmagic` for `python-magic`:
  ```bash
  brew install libmagic

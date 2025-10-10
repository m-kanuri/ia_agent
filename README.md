# Intelligent Forensics Agent (Demo)

Practical implementation of my Unit 6 design for an **Intelligent Forensics Agent**.

**Agent 1 (implemented)**: safe discovery (read-only), **content-first** file identification, minimal metadata extraction, and storage in SQLite.  
Includes unit tests and a tiny, optional ML demo (logistic regression) for “archive?” recommendations.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Tests](https://img.shields.io/badge/tests-unittest-green)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)

---

# Intelligent Forensics Agent — Practical Demo

This project is the practical implementation of my Unit 6 design.  
It builds a small **file-triage agent** that:

1. **Discovers** files safely (read-only) with **platform-aware excludes**.  
2. **Identifies** file type by **content first** (magic bytes), with simple fallbacks.  
3. **Extracts** only **minimal metadata** (path, size, timestamps, SHA-256, MIME).  
4. **Stores** results in a **SQLite** database for easy audit and queries.

A tiny, optional **logistic-regression** demo is included to flag “likely non-text” files (advisory only).

---

## 1) Implementation overview

**Architecture (reactive pipeline):** `Discover → Identify → Decide → Act → Audit`

- `src/discovery.py` — safe traversal using `psutil`; prunes system/sensitive paths.
- `src/identifier.py` — **content-based** MIME via `python-magic`, then `filetype`, then extension as last resort.
- `src/processor.py` — reads stat info + **SHA-256**; keeps data minimal.
- `src/database.py` — SQLite **upsert + indexes** so re-runs are idempotent.
- `src/learner.py` — tiny features + logistic regression (saved with `joblib`) for a toy “archive?” recommendation.
- `src/main.py` — CLI orchestrator; prints a **Run Summary**.

**Why these choices**
- Content beats extensions for forensic robustness.
- Data minimisation reduces privacy risk and improves auditability.
- SQLite gives a single portable artefact (`agent.db`) and simple SQL for evidence.

---

## 2) Requirements

- Python **3.11** (tested).
- **macOS:** `libmagic` is required for `python-magic`.
  ```bash
  brew install libmagic
  # If needed:
  export MAGIC="$(brew --prefix)/share/misc/magic.mgc"


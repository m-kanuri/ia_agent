# Intelligent Forensics Agent (Demo)

Practical implementation of my Unit 6 design for an **Intelligent Forensics Agent**.

**Agent 1 (implemented)**: safe discovery (read-only), **content-first** file identification, minimal metadata extraction, and storage in SQLite.  
Includes unit tests and a tiny, optional ML demo (logistic regression) for “archive?” recommendations.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Tests](https://img.shields.io/badge/tests-unittest-green)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)

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

## 3) Code layout

src/
discovery.py # safe traversal (platform-aware excludes; read-only)
identifier.py # content-first MIME (python-magic → filetype → extension)
processor.py # SHA-256, size, timestamps (data minimisation)
database.py # SQLite upsert + indexes (idempotent re-runs)
learner.py # tiny, optional demo model (advisory only)
main.py # CLI orchestrator; prints Run Summary
tests/
test_discovery.py test_identifier.py test_processor.py test_database.py
sample_data/


## 3) How to run (demo scan)

The sample dataset is in sample_data/. This command scans it, identifies types by content, and writes results to agent.db.

python -m src.main --target sample_data --db agent.db

## 4) Run Summary

- **Target:** `.../sample_data`
- **DB:** `.../agent.db`
- **Files processed:** `5`
- **Elapsed:** `0.0Xs`

## Counts by MIME
| MIME Type           | Count |
|---------------------|:-----:|
| text/plain          |   2   |
| application/pdf     |   1   |
| image/jpeg          |   1   |
| text/csv            |   1   |

## Sample record

{ "path": "...", "size": 123, "mtime": "...", "ctime": "...", "mime": "text/plain",
  "sha256": "...", "detector": "python-magic" }


## 5) Tests & coverage

python -m unittest discover -s tests -v | tee test_output.txt
coverage run -m unittest discover -s tests
coverage report -m | tee coverage_output.txt

---
## 4) References (Harvard style)

Python Software Foundation (2025) Python 3.11 documentation — hashlib, sqlite3, mimetypes, unittest. Available at: https://docs.python.org/3.11/
 (Accessed: 10 October 2025).

Rodolà, G. (2025) psutil documentation. Available at: https://psutil.readthedocs.io/
 (Accessed: 10 October 2025).

Hupp, A. (2025) python-magic (libmagic bindings). Available at: https://github.com/ahupp/python-magic
 (Accessed: 10 October 2025).

Aparicio, T. (h2non) (2025) filetype.py. Available at: https://github.com/h2non/filetype.py
 (Accessed: 10 October 2025).

Pedregosa, F. et al. (2011) ‘Scikit-learn: Machine Learning in Python’, Journal of Machine Learning Research, 12, pp. 2825–2830.

SQLite Consortium (2025) SQLite Documentation. Available at: https://www.sqlite.org/docs.html
 (Accessed: 10 October 2025).

The Unit 6 design report is cited in the presentation’s References slide.

---

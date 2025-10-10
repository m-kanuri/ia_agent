# Intelligent Forensics Agent (Agent 1 Implementation)

Practical implementation of my Unit 6 design for an **Intelligent Forensics Agent**.

**Agent 1 (Implemented)**: safe discovery (read-only), **content-first** file identification, minimal metadata extraction, and storage in SQLite.
**Scope Note**: Includes unit tests and a tiny, optional ML demo (logistic regression) for advisory “archive?” recommendations (Agent 2 groundwork).

![Python](https://img.shields.io/badge/python-3.11-blue)
![Tests](https://img.shields.io/badge/tests-unittest%20%7C%20coverage-green)

---

## 1) Implementation Overview & Design Rationale

This project implements the core **File-Triage Agent** (Agent 1) of the hybrid reactive pipeline:

1.  **Discovers** files safely (read-only) using **platform-aware excludes** (`psutil`).
2.  **Identifies** file type by **content first** (`python-magic`), with simple fallbacks (`filetype`).
3.  **Extracts** only **minimal metadata** (path, size, timestamps, **SHA-256**, MIME).
4.  **Stores** results in a **SQLite** database, ensuring runs are **idempotent**.

### Module Map

* `src/discovery.py` — safe traversal using `psutil`; prunes system/sensitive paths.
* `src/identifier.py` — **content-based** MIME via `python-magic`, then `filetype`, then extension as last resort.
* `src/processor.py` — reads stat info + **SHA-256**; adheres to **data minimisation**.
* `src/database.py` — SQLite **upsert + indexes** so re-runs are idempotent.
* `src/learner.py` — tiny features + logistic regression (`joblib`) for a toy “archive?” recommendation.
* `src/main.py` — CLI orchestrator; prints a **Run Summary**.

### Why these choices (Justification)

* **Robustness:** **Content identification** beats extensions for forensic accuracy.
* **Safety:** **`psutil`** provides environment awareness to mitigate system instability risks.
* **Ethics:** **Data minimisation** (minimal metadata only) reduces privacy risk.
* **Integrity:** **SHA-256** hashing ensures **evidential integrity**.
* **Auditability:** **SQLite** gives a single portable artefact (`agent.db`) for easy audit.

---

## 2) Prerequisites & Setup

The agent is tested on Python 3.11.

1.  **Clone the Repository (or unpack the zip):**
    ```bash
    git clone [YOUR REPO LINK]
    cd intelligent-forensics-agent
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install `libmagic` Dependency (Crucial for Content ID):**
    * **macOS:** `libmagic` is required for `python-magic`.
        ```bash
        brew install libmagic
        ```
    * **Windows:** Use the provided pre-compiled `python-magic-bin` dependency.

---

## 3) How to Execute the Agent (Demo Scan)

The sample dataset is in the `sample_data/` directory.

### Command

This command scans the sample data, identifies types by content, and writes results to `agent.db`.

```bash
python -m src.main --target sample_data --db agent.db

---
## 4) Testing & Code Quality

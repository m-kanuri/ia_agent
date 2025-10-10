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
    git clone https://github.com/m-kanuri/ia_agent.git
    cd ia_agent
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
```
### Example Run Summary Output

The CLI prints a structured summary after execution. This output verifies successful execution, file identification counts, and minimal metadata capture for a sample record.

=== Run Summary ===
Target: .../sample_data
DB: .../agent.db
Files processed: 5
Elapsed: 0.0Xs

Counts by MIME:
| MIME Type | Count |
|:---|:---:|
| text/plain | 2 |
| application/pdf | 1 |
... (rest of the counts)

~~~json
{
  "path": "...",
  "size": 123,
  "mtime": "...",
  "ctime": "...",
  "mime": "text/plain",
  "sha256": "...",
  "detector": "python-magic"
}
~~~

## 4) Testing & Code Quality

The project includes a full unit test suite targeting core modules for correctness and stability.

Test Commands
The following commands run the tests and generate the coverage report:

### 1. Run tests (to verify code correctness)
python -m unittest discover -s tests -v | tee test_output.txt

### 2. Run coverage (to measure code quality)
coverage run -m unittest discover -s tests

### 3. Generate coverage report
coverage report -m | tee coverage_output.txt

## 5) References

* All sources underpinning the design and implementation, including academic concepts and external libraries, are listed below in Harvard style.

* Group E (Kanuri, M. et al.) (2025) Intelligent Agents: Development Team Project Report (Unit 6 Design). (The foundational design document for this implementation).

* Hupp, A. (2025) python-magic (libmagic bindings). Available at: https://github.com/ahupp/python-magic (Accessed: 10 October 2025).

* ICO (2024) Data minimisation. Available at: https://ico.org.uk/... (Accessed: 10 October 2025).

* Pedregosa, F. et al. (2011) ‘Scikit-learn: Machine Learning in Python’, Journal of Machine Learning Research, 12, pp. 2825–2830.

* Python Software Foundation (2025) Python 3.11 documentation — hashlib, sqlite3, mimetypes, unittest. Available at: https://docs.python.org/3.11/ (Accessed: 10 October 2025).

* Rodolà, G. (2025) psutil documentation. Available at: https://psutil.readthedocs.io/ (Accessed: 10 October 2025).

* SQLite Consortium (2025) SQLite Documentation. Available at: https://www.sqlite.org/docs.html (Accessed: 10 October 2025).

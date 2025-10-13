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

```text
=== Run Summary ===
Target: .../sample_data
DB: .../agent.db
Files processed: 5
Elapsed: 0.0Xs
```

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
  ```bash
python -m unittest discover -s tests -v | tee test_output.txt
```
### 2. Run coverage (to measure code quality)
  ```bash
coverage run -m unittest discover -s tests
```

### 3. Generate coverage report
  ```bash
coverage report -m | tee coverage_output.txt
```

## 4) SQLite Queries

-- how many rows?
-- SELECT COUNT(*) AS rows FROM files;

-- MIME breakdown
-- SELECT mime, COUNT(*) AS files FROM files GROUP BY mime ORDER BY files DESC;

-- largest files
-- SELECT path, size FROM files ORDER BY size DESC LIMIT 10;

-- duplicate content by hash
-- SELECT sha256, COUNT(*) AS n FROM files GROUP BY sha256 HAVING n > 1 ORDER BY n DESC;


## 6) References

* Aparicio, T. (2022) filetype: infer file type and MIME. Available at: https://github.com/h2non/filetype (Accessed: 11 October 2025).
* Batchelder, N. (2025) coverage.py — Code coverage for Python. Available at: https://coverage.readthedocs.io/ (Accessed: 11 October 2025).
* Dubettier, A., et al. (2023) ‘File type identification tools for digital investigations’, Forensic Science International: Digital Investigation, 46, p. 301574. doi:10.1016/j.fsidi.2023.301574.
* Hupp, A. (2022) python-magic documentation. Available at: https://github.com/ahupp/python-magic (Accessed: 11 October 2025).
* Information Commissioner’s Office (ICO) (2024) ‘UK GDPR: Principle (c) Data minimisation’. Available at: https://ico.org.uk/ (Accessed: 11 October 2025).
* Joblib Developers (2025) Joblib documentation. Available at: https://joblib.readthedocs.io/ (Accessed: 11 October 2025).
* m-kanuri (2025) ia_agent. GitHub repository. Available at: https://github.com/m-kanuri/ia_agent (Accessed: 12 October 2025).
* Kanuri, M., Espag, J., Kirwan, F. and Jittipattanakulchai, G. (2025) Intelligent Forensics Agent – Group E Design Report (Unit 6). University of Essex Online (unpublished coursework).
* Kessler, G.C. (2024) File Signature Table. Available at: https://www.garykessler.net/library/file_sigs.html (Accessed: 11 October 2025).
* MITRE (2024) MITRE ATT&CK®: Masquerading (T1036). Available at: https://attack.mitre.org/techniques/T1036/ (Accessed: 11 October 2025).
* National Institute of Standards and Technology (NIST) (2020) Security and Privacy Controls for Information Systems and Organizations (SP 800-53 Rev. 5). Gaithersburg, MD: NIST.
* OWASP Foundation (2023) Logging Cheat Sheet. Available at: https://cheatsheetseries.owasp.org/ (Accessed: 11 October 2025).
* Pedregosa, F., Varoquaux, G., Gramfort, A. et al. (2011) ‘Scikit-learn: Machine Learning in Python’, Journal of Machine Learning Research, 12, pp. 2825–2830.
* PyPI (2024) python-magic-bin (Windows prebuilt). Available at: https://pypi.org/project/python-magic-bin/ (Accessed: 11 October 2025).
* Python Software Foundation (PSF) (2025a) hashlib — Secure hashes and message digests. Available at: https://docs.python.org/3/library/hashlib.html (Accessed: 11 October 2025).
* Python Software Foundation (PSF) (2025b) mimetypes — Map filenames to MIME types. Available at: https://docs.python.org/3/library/mimetypes.html (Accessed: 11 October 2025).
* Python Software Foundation (PSF) (2025c) sqlite3 — DB-API 2.0 interface. Available at: https://docs.python.org/3/library/sqlite3.html (Accessed: 11 October 2025).
* Python Software Foundation (PSF) (2025d) unittest — Unit testing framework. Available at: https://docs.python.org/3/library/unittest.html (Accessed: 11 October 2025).
* Rodolà, G. (2025) psutil documentation. Available at: https://psutil.readthedocs.io/ (Accessed: 11 October 2025).
* scikit-learn Developers (2025) scikit-learn User Guide. Available at: https://scikit-learn.org/stable/ (Accessed: 11 October 2025).
* SQLite Consortium (2025) SQLite documentation. Available at: https://sqlite.org/docs.html (Accessed: 11 October 2025).
* Shoham, Y. (1993) ‘Agent-oriented programming’, Artificial Intelligence, 60(1), pp. 51–92.


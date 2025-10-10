
# Intelligent Forensics Agent (Demo)

Practical implementation of the Unit 6 design: safe discovery, content-based identification, metadata extraction, and SQLite storage. Includes a tiny ML demo and unit tests.

## Setup
```bash
pip install -r requirements.txt
```

## Run a demo scan
```bash
python -m src.main --target sample_data --db agent.db
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Notes (why these choices)
- Content-based detection first (magic) to reduce false positives; layered fallbacks for portability.
- Data minimisation: size, times, SHA-256, MIME only.
- SQLite for portability and audit-friendly queries.
- Modular code to support plug-in parsers for specific file types.

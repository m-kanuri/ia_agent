
# Transcript (20-minute narration)

## Slide 1 — Title
Welcome to the demonstration of our Intelligent Forensics Agent. Today I'll show the working prototype, explain our design choices, and present test and execution evidence.

## Slide 2 — Problem & Objectives
Digital investigations require repeatable, safe, and scalable collection of file metadata. Our objectives are to automate discovery and identification of files of interest, persist essential metadata only, and prepare for downstream archiving and analysis while preserving system stability and evidential integrity.

## Slide 3 — Architecture Overview
The hybrid reactive pipeline is discover → identify → process → store → learn → audit. This balances predictability with adaptability and maps to the responsibilities in our codebase.

## Slide 4 — Key Libraries & Rationale
We use psutil for environment awareness; python-magic with filetype and extensions as fallbacks for MIME detection; SQLite for a lightweight, portable database; and scikit-learn with joblib for a minimal supervised learning illustration. These are chosen for reliability, portability, and forensic appropriateness.

## Slide 5 — Safety by Design
Scans are limited to a user-specified root, with platform-specific excludes. Sources are read-only; outputs are confined to an SQLite database. We apply data minimisation by storing only size, times, SHA-256, and MIME type.

## Slide 6 — Demo
We run the agent over a small sample directory. The agent detects file types, computes hashes, stores records, and trains a tiny model that flags images and PDFs as archive candidates. We'll review the summary and a sample record in the console output.

## Slide 7 — Evidence
The console output demonstrates correct traversal, identification, and database persistence. This is suitable for screenshots in the slide deck. A query of counts-by-MIME provides a quick health check.

## Slide 8 — Testing
Unit tests cover identification, metadata hashing, and database roundtrip. Tests are deterministic and portable; if python-magic is unavailable, fallbacks still pass.

## Slide 9 — Critical Reflection
Risks include false detections, platform inconsistencies, and accidental traversal. Mitigations are layered detection, explicit excludes, and a minimal data policy. The ML demo requires labelled data and continuous validation to be effective in production.

## Slide 10 — Conclusion & Next Steps
We delivered a working, testable prototype aligned with the Unit 6 design. Future work includes pluggable parsers for richer metadata, dry-run mode, signed audit logs, and concurrency for scale.

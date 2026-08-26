# Changelog — ssh-shared-key-overlap

## 1.1 — 2026-08-26

- Removed `data/OBSERVATION_MANIFEST.json` — it embedded the actual
  storyline (per-step actor/system/plain-English activity, including a step
  description that states outright "Marcus is using a private key Priya
  shared with him") directly in the evidence. Moved to the held-out answers
  repo instead.
- Removed `data/COLLECTION_PROFILE.json` and `data/OUTPUT_TARGET.txt` — no
  investigative value, and their schema/vocabulary is a generator
  fingerprint.
- Removed generator-provenance wording from this file and `README.md`.

## 1.0 — 2026-08-26

- Initial case build. Split into `data/` (evidence + context), the
  generator's scenario file (moved to `generators/`), and answer-key
  material (moved to the separate `forensic-agent-answers` directory).
- Authored `AGENTS.md`, `TASK.md`, `EXAM.md` (7 questions).

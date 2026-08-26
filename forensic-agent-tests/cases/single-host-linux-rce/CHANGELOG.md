# Changelog — single-host-linux-rce

## 1.1 — 2026-08-26

- Removed `data/OBSERVATION_MANIFEST.json` — it embedded the actual
  storyline (per-step actor/system/plain-English activity, and an explicit
  `"kind": "red_herring"` tag on the decoy) directly in the evidence.
  Moved to the held-out answers repo instead.
- Removed `data/COLLECTION_PROFILE.json` and `data/OUTPUT_TARGET.txt` — no
  investigative value, and their schema/vocabulary is a generator
  fingerprint.
- Removed generator-provenance wording from this file and `README.md`.

## 1.0 — 2026-08-25

- Initial case build (generation seed 42). Split into `data/` (evidence +
  context), the generator's scenario file (moved to `generators/`), and
  answer-key material (moved to the separate `forensic-agent-answers`
  directory).
- Authored `AGENTS.md`, `TASK.md`, `EXAM.md` (10 questions).

# Changelog — rdp-remote-file-write

## 1.1 — 2026-08-26

- Removed `data/OBSERVATION_MANIFEST.json` — it embedded the actual
  storyline (per-step actor/system/plain-English activity) directly in the
  evidence. Moved to the held-out answers repo instead.
- Removed `data/COLLECTION_PROFILE.json` and `data/OUTPUT_TARGET.txt` — no
  investigative value, and their schema/vocabulary is a generator
  fingerprint.
- Removed generator-provenance wording from this file and `README.md`.

## 1.0 — 2026-08-26

- Initial case build. Split into `data/` (evidence + context), the
  generator's scenario file (moved to `generators/`), and answer-key
  material (moved to the separate `forensic-agent-answers` directory).
- Authored `AGENTS.md`, `TASK.md`, `EXAM.md` (6 questions). The grading key
  anchors "when did this happen" on the rendered `4624`/Sysmon timestamps
  (~14:40 UTC), not on the scenario's authored relative offsets (+20m/+22m,
  ~14:20-14:22 UTC) — see `KNOWN_DEFICIENCIES.md` in the answers repo for
  why those diverge by ~21 minutes in this scenario's generated output.

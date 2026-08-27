# Changelog — ssh-shared-key-overlap

## 1.3 — 2026-08-27

- **Fixed a real answer-key gap found by an independent audit.** The raw
  data (`data/APP-SHARED-01.fernbridgelabs.com/syslog.log`) has 5 SSH
  sessions in the collection window; the answer key (`BRIEFING.md`,
  `grading_schema.md`) only documented 3, missing Marcus's own genuine
  session and Greta's second session. A thorough AUT correctly finding all
  5 would have been marked down against the old key. Not a data problem —
  the log itself was always internally consistent — this was purely an
  under-documented ground truth.
- Downstream of the above: `EXAM.md` Q5 previously asked about "a third
  session" as if only one existed. There are actually two sessions
  (Greta's first, and now-documented Marcus's own) that overlap both of
  Priya's sessions. Reworded Q5 to ask for all of them; updated
  `grading_schema.md` and `AGENTS.md` (grader instructions) to match.
- No leak, no data self-contradiction — see the independent audit's report
  for the full verification trail.

## 1.2 — 2026-08-27

- Reworded `EXAM.md` Q3 to name the two candidate explanations the grading
  rubric already accepts (shared credentials vs. a compromised key) instead
  of leaving the question fully open-ended — closes a gap between what was
  asked and what `grading_schema.md` actually checks for, without leaking
  which explanation (if either) is correct; both remain undetermined by
  design (see `BRIEFING.md`).

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

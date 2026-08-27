# Changelog — rdp-remote-file-write

## 1.2 — 2026-08-26

- Regenerated with an explicit `environment.identity.windows_default_scope:
  local` (plus a per-user override) added to the generator's scenario file,
  attempting to fix a domain-style-identity rendering bug. Confirmed the
  override has no effect — same `TargetDomainName: ALDERWOODPARTNERS` as
  before, reproduced across three separate generation runs. Filed as
  deficiency #2 in the answers repo's `KNOWN_DEFICIENCIES.md`.
- Removed `data/ENVIRONMENT.md`'s "No Active Directory" claim — can no
  longer assert this given the confirmed rendering bug.
- Reworded `EXAM.md` Q1 and Q5: this case has no Sysmon Event 11
  (FileCreate) for `team-notes.txt` anywhere in the data — confirmed
  intentional Sysmon filtering (Event 11 only fires for suspicious-location
  executables per this environment's documented config), not a gap to fix
  by regenerating. Questions now ask about the process launch rather than
  asserting a file write as directly evidenced.
- Updated `grading_schema.md` and `BRIEFING.md` with both findings —
  neither should be penalized nor over-rewarded if an agent encounters them.

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

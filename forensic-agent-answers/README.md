# forensic-agent-answers

Held-out material for [`forensic-agent-tests`](../forensic-agent-tests) — a
DFIR benchmark suite of test cases for evaluating LLM agents. **Nothing in
this repo is ever meant to reach an agent-under-test.** If you're an AUT,
you shouldn't have access to this repo at all; go work the case in
`forensic-agent-tests` instead.

**Repo-layout convention**: this repo and `forensic-agent-tests` are meant
to be checked out as sibling directories on disk. See `AGENTS.md` for the
full case-building workflow and why the split works this way.

## Layout

- `case-<slug>/` — the answer key for the case at
  `../forensic-agent-tests/cases/<slug>/`: `BRIEFING.md` (the true story,
  including decoys and known evidence quirks), `AGENTS.md` (grader
  instructions), `grading_schema.md` (per-question rubric), and
  `supporting/` (generator-produced ground-truth sidecars).
- `generators/evidenceforge/<slug>/` — the exact `scenario.yaml` that
  produced a case's evidence, plus a README with version/commit/seed and
  the regeneration command. This is effectively the case's ground truth
  in YAML form — the reason it lives here and not in `forensic-agent-tests`.
- `doc/` — case-building methodology and coverage tracking:
  `TEST_OBJECTIVES.md` (category definitions), `TEST_CASE_MATRIX.md`
  (what's covered, case by case — the authoritative as-built record),
  `TEST_CASE_PROCESS.md` (the Phase 0-7 build checklist), `SOURCES.md`
  (evidence sources and their status), `TEST_EVIDENCEFORGE_PROPOSED_CASES.md`
  (the original case-proposal menu, now fully built).
- `EvidenceForge/` — a vendored, stale reference copy of EvidenceForge's
  own skills/schema docs. Not authoritative; see `AGENTS.md`'s pitfalls
  for why. Real authoring happens against a live checkout, not this copy.
- `_discarded/` — case material held out of active use after an audit
  found an unresolvable data defect, kept for reference and upstream bug
  filing rather than deleted.

## Adding or updating a case

See `AGENTS.md` for the full procedure. Short version: scenario authoring
happens in a separate live EvidenceForge checkout, never in either repo;
only finished, independently-audited scenarios get split across
`forensic-agent-tests` (evidence + task) and this repo (answers + rubric).

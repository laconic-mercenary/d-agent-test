# forensic-agent-tests

Forensic-analysis test cases for evaluating LLM agents on DFIR tasks —
evidence + task instructions only. Answer keys live in a separate,
sibling repository (`forensic-agent-answers`), never in this one.

## Layout

- `cases/<slug>/` — a self-contained investigation: `README.md` (human
  overview), `AGENTS.md` (agent entry point), `TASK.md` (instructions),
  `EXAM.md` (the graded questions), `CHANGELOG.md`, and `data/` (all the
  evidence the agent-under-test sees — nothing answer-revealing).
- `generators/evidenceforge/<slug>/` — the EvidenceForge `scenario.yaml`
  that produced a case's data, plus a README with the regeneration command.
- `EvidenceForge/` — vendored EvidenceForge skills/reference docs, kept
  around for now; not case-authoring content, may move out later.

## Cases

| Case | Attack? | Tests |
|---|---|---|
| [single-host-linux-rce](cases/single-host-linux-rce/) | Yes | intrusion path ID, network/log analysis, timeline reconstruction, decoy discrimination, report generation |
| [ssh-shared-key-overlap](cases/ssh-shared-key-overlap/) | No | account/auth analysis, false-positive discipline, proportionate reporting |
| [rdp-remote-file-write](cases/rdp-remote-file-write/) | No | basic sequence reconstruction, actor attribution |

## Adding a case

1. Author/generate evidence (currently via EvidenceForge; see
   `generators/evidenceforge/`).
2. Split the output: safe evidence + context → `cases/<slug>/data/`;
   anything that reveals the answer (ground truth, engine deficiency notes
   that name the attack) → the paired case in `forensic-agent-answers/`.
3. Write `AGENTS.md`, `TASK.md`, `EXAM.md`, `CHANGELOG.md` for the case.
4. Write the matching `BRIEFING.md`, `AGENTS.md` (grader instructions), and
   `grading_schema.md` in `forensic-agent-answers/case-<slug>/`.


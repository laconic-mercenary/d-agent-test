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
| [ssh-shared-key-overlap](cases/ssh-shared-key-overlap/) | No | account/auth analysis, false-positive discipline, proportionate reporting |
| [rdp-remote-file-write](cases/rdp-remote-file-write/) | No | basic sequence reconstruction, actor attribution |
| [windows-log-search-basics](cases/windows-log-search-basics/) | No | targeted log search/filtering, no incident narrative — real (not synthetic) Windows Event Log data |

**Discarded**: `single-host-linux-rce` — held out of active use after an
audit found data self-contradictions on its central causal claim (see
`_discarded/single-host-linux-rce/WHY_DISCARDED.md`). Not deleted; kept for
reference and for filing upstream bug reports.

## Adding a case

See `../AGENTS.md` (at the `d-agent-test` root) for the full procedure —
scenario generation happens in a separate EvidenceForge checkout, not here;
this repo only receives the finished, audited port-over.


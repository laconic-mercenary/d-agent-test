# Generator: benign-breakglass-account

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 5581`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/benign-breakglass-account/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/benign-breakglass-account/data/`) is
human-authored, not generated. This scenario has no `storyline:` at
all — every event is authored as `red_herrings`, plus whatever the
baseline activity model (`suspicious_noise: medium`) generates on its
own.

## Verified facts

`svc-breakglass` 4624 (interactive) logons — exactly 4 total, matching
the 4 authored red-herring RDP/service sessions:
- `APP-01`, `2024-09-03T07:14:35Z`, Type 10, source `10.90.10.31`
  (`WS-MOYELARAN-01`, Marcus's workstation)
- `DB-01`, `2024-09-03T07:30:15Z`, Type 5 (the engine auto-generated a
  service-context session for this step since it authored only a
  `process` event with no explicit `logon`/`rdp_session`, consistent
  with "same on-call session continues" via an already-open remote
  session rather than a fresh RDP logon — Type 5, not Type 10, on this
  host specifically)
- `FILE-01`, `2024-09-04T07:14:28Z`, Type 10, source `10.90.10.32`
  (`WS-DWHITFIELD-01`, Dana's workstation)
- `DC-01`, `2024-09-04T07:35:01Z`, Type 5 (same pattern as `DB-01`)

Diagnostic PowerShell commands, all `SubjectUserName: svc-breakglass`:
`APP-01` `07:14:40Z` (`Get-Service | Where-Object {$_.Status -ne
'Running'}`), `DB-01` `07:30:15Z` (`Get-EventLog -LogName Application
-Newest 100`), `FILE-01` `07:14:33Z` (`Get-PSDrive -PSProvider
FileSystem`), `DC-01` `07:35:03Z` (`Get-EventLog -LogName System
-Newest 50`).

Rosa Delgado's late-night Excel launch: `WS-RDELGADO-01`,
`2024-09-04T04:00:08Z`, `EXCEL.EXE ... MonthEnd_Report.xlsx`.

## Baseline texture (not load-bearing for any exam question)

As in `credential-spray-domain-compromise` and `pth-lateral-logclear`,
declaring `svc-breakglass` as a `service_accounts` entry produces
baseline Event ID 4648 records across all four servers, attributed to
`SYSTEM` via automated infrastructure processes
(`taskhostw.exe`/`ops-agent.exe`/scheduled `powershell.exe`), sourced
from each server's own IP. This is now a confirmed, repeatable engine
pattern for any `service_accounts` entry, not specific to this
scenario. Not built into the exam here since the case's actual test
(the 4 interactive logons) is already cleanly isolated regardless —
mentioned in `BRIEFING.md` as expected texture in case a grader
encounters it.

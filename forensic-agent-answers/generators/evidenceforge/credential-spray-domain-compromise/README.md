# Generator: credential-spray-domain-compromise

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 8213`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/credential-spray-domain-compromise/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/credential-spray-domain-compromise/data/`)
is human-authored, not generated — it documents `svc-sql`'s standing
Domain Admins misconfiguration and its two legitimate automated
consumers (`taskhostw.exe`, `ops-agent.exe`), both load-bearing context
for interpreting the case's central discrimination question.

## Notable finding from this build (not a bug, worth knowing)

The scenario only authors *one* `explicit_credentials` event (diane
.foster requesting svc-sql's ticket). The baseline activity model
independently and automatically generates many *additional* Event ID
4648 records targeting `svc-sql` throughout the whole collection window
— all attributed to `SYSTEM` via `taskhostw.exe` or
`C:\Program Files\Meridian\OpsAgent\ops-agent.exe`, consistent with
ordinary scheduled-task/monitoring-agent credential use for a real
service account. This wasn't designed in — it's the engine's own
baseline realism doing its job — but it turned out to be a better
discrimination signal than anything in the original case sketch: the one
authored event stands out by *subject* (`diane.foster`, not `SYSTEM`)
and *process* (`powershell.exe`, not `taskhostw.exe`/`ops-agent.exe`),
not by being the only 4648 event in the data. The exam was built around
this real signal rather than assuming the authored event would be the
only one present — confirmed by direct XML inspection before writing
`EXAM.md`, not assumed.

`GROUND_TRUTH.md` for this scenario was independently checked against
the raw XML data and found accurate (unlike `external-recon-no-breach`,
where it was wrong on two counts) — all six storyline timestamps and the
~19-hour gap between the `explicit_credentials` event and `svc-sql`'s
actual logon matched exactly. Still verified directly rather than
assumed, per this project's standing rule.

# Generator: external-recon-no-breach

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 4471`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/external-recon-no-breach/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/external-recon-no-breach/data/`) is
human-authored, not generated — EvidenceForge does not produce this file
automatically; it documents the organization's stated security policy
that only ports 80/443 should be reachable on `WEB-01` from the
internet, which is what makes one of this case's findings (an inbound
SSH connection succeeding despite not being an explicitly permitted
port) interpretable as a real, evidence-grounded observation rather than
something the agent-under-test has to infer without any stated baseline.

## Known tooling quirk (worth flagging for future scenario authors)

Initial authoring used `target_segment: dmz` for the storyline's
`port_scan` event, with `system: WEB-01` (a host that is itself inside
the `dmz` segment). This produced a scenario that validated and
generated cleanly, with `GROUND_TRUTH.md`/`GROUND_TRUTH.json` both
claiming 21 visible ASA records for the event — but the declared
`source_ip` never actually appeared anywhere in the rendered
`cisco_asa.log`, and no matching deny records existed at the event's
timestamp at all. The engine's own ground-truth bookkeeping believed the
event rendered; the wire-level emitter silently produced nothing for it.
Switching to `target_ips: ["10.30.30.10"]` (the target's own IP,
explicit rather than segment-relative) fixed this immediately — 23
matching records appeared, timestamps and ports lined up with the
storyline event.

Root cause not confirmed (didn't dig into engine internals), but the
reproducible pattern is: **a `port_scan` event whose `system` is itself
a member of the declared `target_segment` may silently fail to render
wire-level evidence, even though `GROUND_TRUTH.md` claims it did.**
`target_ips` with an explicit address avoided the issue entirely. Given
this project's established rule to verify claims against raw data, not
`GROUND_TRUTH.md` alone, this was caught before it shipped — but future
scenarios using `port_scan` where the scanned segment contains the
`system` field's own host should use `target_ips` defensively, or
verify the rendered log directly before trusting the ground truth.

**Second, independent confirmation of the same lesson, in the fixed
run**: even after the `target_ips` fix produced correct wire-level
evidence, `GROUND_TRUTH.md` still states "21 denied connections + ASA
threat detection alert (733100)." The actual rendered data shows 19
denied (`106023`) + 2 connected (`302013`/`302014`, one TLS reset, one
completed SSH session with a single failed login) = 21 total probes
accounted for, and **zero** `733100` records anywhere in
`cisco_asa.log`. `GROUND_TRUTH.md`'s per-event summary line appears to
be generated from the *intended*/canonical occurrence count rather than
reconciled against what the emitter actually wrote — don't trust its
per-event counts or claimed alert types without checking the rendered
log directly, even on a run that otherwise looks correct.

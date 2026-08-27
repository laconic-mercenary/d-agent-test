# Generator: dga-beacon-logclear

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 7724`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/dga-beacon-logclear/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/dga-beacon-logclear/data/`) is
human-authored, not generated.

## `GROUND_TRUTH.md`'s recurring logon-mislabeling pattern (4th confirmed instance)

Same as `insider-dns-tunnel-exfil`, `phishing-c2-beacon`, and
`pth-lateral-logclear`: `GROUND_TRUTH.md`'s free-text timeline
mislabels the storyline actor's own local logon as
`"2024-06-11 14:50:29 UTC ... Network logon from 23.129.64.210
(LogonID: 0x7f1231a)"`. The real event with that `TargetLogonId` is
Event ID 4624, **Logon Type 2** (local/interactive, matching the
authored `logon_type: 2`), blank `IpAddress`, at the same timestamp —
confirmed by matching it directly to the `ARMHelper.exe` process
event's `SubjectLogonId`. `23.129.64.210` does not appear anywhere in
this dataset. This is now confirmed across four independently-built
scenarios this session as a repeatable ground-truth template artifact,
not a one-off — assumed for any future case rather than re-verified
from scratch each time (though still spot-checked, per this project's
standing rule).

**By contrast, `GROUND_TRUTH.json`'s *structured* per-event attribute
fields (as opposed to its free-text narrative timeline/`GROUND_TRUTH.md`)
were checked and found accurate** — `evt-dga-002`'s `total_queries: 91`/
`nxdomain_count: 87` and `evt-c2-beacon-003`'s `attempt_count: 31` both
matched direct inspection of `zeek01/dns.json`/`conn.json` exactly.
Worth distinguishing going forward: this project's "don't trust
`GROUND_TRUTH.md`" rule applies most reliably to its narrative
prose/timeline table, less to `GROUND_TRUTH.json`'s structured
`attributes` blocks for storyline-authored events — though both should
still be spot-checked, not assumed, per standing practice.

## `log_cleared` does not remove prior events (3rd confirmed instance)

Same finding as `pth-lateral-logclear`: `WS-INFECTED-01`'s own
`windows_event_security.xml` still contains the `ARMHelper.exe` 4688
process-creation event (`2024-06-11T14:59:47.02Z`) after the Event ID
1102 log-clear record (`23:15:03.68Z`). Purely additive in this engine
version. Q5 tests whether the agent-under-test verifies this rather
than assumes.

## Verified facts

DGA queries: 91 total, 87 NXDOMAIN, 4 resolved (`xmewiwr977b78f.com`,
`v868s51dj6k3vq8r.com`, `i3txc98mmckmu22o.com`, `64mpjdtx6jaf.com`, all
→ `45.32.88.201`), `2024-06-11T15:01:47Z`–`18:01:47Z` (~3h). Beacon: 31
connections to `45.32.88.201:443`, `18:04:48Z`–`23:04:45Z` (~5h).
`ARMHelper.exe` process: `2024-06-11T14:59:47Z`, path
`C:\Users\grace.tanaka\AppData\Roaming\Adobe\ARMHelper.exe` — this
engine version's application catalog has a *canonical* path for
`ARMHelper.exe` at `C:\Windows\System32\ARMHelper.exe` (the real Adobe
Reader/Acrobat helper's actual location), which the validator flagged
as a mismatch; kept deliberately, since a fake install location for a
name that's supposed to be a legitimate system utility is exactly the
masquerading tell this case is testing (Q1).

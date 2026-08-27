# Briefing: rogue-service-account-privcreep

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `6103`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/rogue-service-account-privcreep/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #10.

**Every fact below was independently verified directly against the
rendered XML data** before being written down. `GROUND_TRUTH.md`'s
narrative timeline again mislabels the storyline actor's own local
logon — the sixth confirmed instance of this template pattern this
session; see the paired generator README.

## The story, stage by stage

All timestamps UTC.

### Stage 1 — Baseline: `svc-reportgen`'s legitimate use
22 Event ID 4648 records across all four hosts (`WS-DVELASQUEZ-01`,
`WS-NKOWALSKI-01`, `APP-01`, `DC-01` — `WS-NKOWALSKI-01` alone has 9,
the most of any host), spanning the full ~24-hour window, **all**
`SubjectUserName: SYSTEM` — never a human subject. Process varies:
`ops-agent.exe`, `taskhostw.exe`, and `powershell.exe` (9 of the 22)
— process name is *not* a reliable "this is automation" signal on its
own (see Q2 below); `SubjectUserName: SYSTEM` is the one field every
legitimate event shares. This is the account's entire documented
purpose (per `ENVIRONMENT.md`): an unattended nightly reporting job.

### Stage 2 — The anomaly (`WS-DVELASQUEZ-01`)
**2024-10-21T15:15:21.68Z** — Event ID 4648, `SubjectUserName:
diego.velasquez`, `SubjectLogonId: 0x11d8a4a1`, `ProcessName:
powershell.exe`, `TargetUserName: svc-reportgen`,
`TargetServerName: DC-01`. (An earlier draft of this document claimed
this `SubjectLogonId` matched Diego's Type 2 local logon at
`14:35:06.39Z` — wrong, caught by an independent Phase 6 audit; it
actually belongs to a Type 10/RDP logon at `15:14:27.40Z` sourced from
`WS-NKOWALSKI-01`. Not load-bearing for any exam question — no
question asks the AUT to trace this session lineage — so removed
rather than re-explained.) **This is
the earliest point a monitoring control should have fired (Q4)** —
independent of anything that happens afterward, a service account
documented for exactly one unattended automated purpose is being
invoked explicitly from an ordinary analyst's interactive PowerShell
session. That fact alone is already a complete, sufficient anomaly;
the escalation that follows only confirms what this event already
showed.

### Stage 3 — Escalation (`DC-01`)
**2024-10-21T15:20:08.65Z** — Event ID 4688, `SubjectUserName:
svc-reportgen`, `CommandLine: powershell.exe -Command
Add-ADGroupMember -Identity 'Domain Admins' -Members 'svc-reportgen'`.
**2024-10-21T15:20:23.09Z** — Event ID 4728 (member added to a global
security group), `MemberName: CN=svc-reportgen,CN=Users,...`,
`TargetUserName: Domain Admins`, `SubjectUserName: svc-reportgen`.
`svc-reportgen` goes from a scoped, non-administrative automation
account to a Domain Admins member in under 5 minutes from the first
anomalous credential use.

## The core distinction the exam tests

The *tell* is the explicit-credentials event itself (Stage 2), not the
group-membership change (Stage 3) — the latter is the *consequence*.
An answer that identifies "svc-reportgen got added to Domain Admins"
without identifying the interactive-use event that made that possible,
or that treats the group-add as the earliest point a control should
have caught this, has found the outcome but missed the actual tell
(Q4 specifically tests this distinction).

## Known generator-tooling notes

See the paired generator README: (1) `GROUND_TRUTH.md`'s narrative
mislabels Diego's local logon (sixth confirmed instance of this
pattern this session); (2) legitimate `svc-reportgen` 4648 events'
`IpAddress` field is not a reliable discriminator (some show Diego's
own workstation IP); (3) **`ProcessName` alone is also not a reliable
discriminator** — corrected after an independent Phase 6 audit found
9 of the 22 legitimate 4648 events also use `powershell.exe` (mostly
on `WS-NKOWALSKI-01`, which the first draft of this document omitted
from the host list entirely). `SubjectUserName` (`SYSTEM` vs. a real
human account) is the only fully reliable signal — not
`SubjectUserName`/`ProcessName` jointly, as an earlier draft claimed.

## Undetermined by design

- **What Diego actually did with Domain Admins access afterward.** Not
  evidenced — the storyline ends at the group-membership change. Not
  required by any exam question.

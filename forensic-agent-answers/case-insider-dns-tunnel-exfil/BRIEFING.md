# Briefing: insider-dns-tunnel-exfil

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `4417`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/insider-dns-tunnel-exfil/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #2.

**Every fact below was independently verified directly against the
rendered XML/JSON data** before being written down, not assumed from
the scenario design. `GROUND_TRUTH.md` was checked and found
**inaccurate** for the morning-logon event (see "Known generator-tooling
notes" below) — this is the third such `GROUND_TRUTH.md` defect found
this session, after `external-recon-no-breach`'s two.

## The story, stage by stage

All timestamps UTC.

### Stage 1 — Ordinary morning logon (`WS-SNAKAMURA-01`)
**2024-10-07T14:19:32.0831431Z** — Event ID 4624, **Logon
Type 2** (local/interactive), no `IpAddress` (blank, as expected for a
local logon), `TargetLogonId: 0x3ade0ff`. This is Sarah logging into her
own workstation, exactly as she does every workday. There is no
external IP, no compromised credential, nothing anomalous about this
event by itself.

### Stage 2 — Staging (`WS-SNAKAMURA-01`)
**2024-10-07T15:09:31.1201355Z** — Event ID 4688, `SubjectLogonId:
0x3ade0ff` (matching Stage 1's logon), `NewProcessName:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`,
`ParentProcessName: C:\Windows\explorer.exe`, `NewProcessId: 0x1ee4`
(7908 decimal). Command line:
`powershell.exe -NoProfile -Command Compress-Archive -Path
'\\FILE-01\Finance\ClientFinancials_Q3' -DestinationPath
'C:\Users\sarah.nakamura\AppData\Local\Temp\backup_archive.zip'`

**A second, unrelated `Compress-Archive` event exists on this same
host, for the same user, later the same day**
(`2024-10-07T19:42:14.0240000Z`, Event ID 4688, same `SubjectLogonId`,
`ParentProcessName:` the *same* powershell.exe rather than
explorer.exe): `powershell.exe -WindowStyle Hidden -Command
"Compress-Archive -Path C:\Temp\Logs\*.log -DestinationPath
C:\Backups\monthly-logs.zip"`. This is a routine local log-backup task
— it references no Finance-share data, and its destination
(`C:\Backups\`) is not the exfiltrated archive's path. It was not
designed into the scenario; it is the environment's own baseline
activity model producing plausible unrelated noise that happens to
share the "Compress-Archive by this user" signature. **This is Q1's
discrimination test**: an agent that cites the 19:42:14 event instead
of the 15:09:31 event has the wrong one, even though the hidden-window
flag on the decoy event reads as superficially more suspicious.

### Stage 3 — Exfiltration via DNS tunnel (`WS-SNAKAMURA-01`, sensor `zeek01`)
**2024-10-07T15:24:45.733094Z – 2024-10-07T17:24:29.094217Z** (1 hour,
59 minutes, 43 seconds) — 464 DNS `TXT` queries from `10.40.10.31`
(`WS-SNAKAMURA-01`) to `*.sync.cloudmetrics-telemetry.net`, base64-
encoded subdomain labels (e.g.
`ih4z1ev5syy41hvqrbvtwfgnv7z67jg.s0.a.sync.cloudmetrics-telemetry.net`),
resolved through the internal DNS server (`10.40.20.10`, i.e. `DC-01`).
This domain and pattern appear nowhere else in this host's — or any
other host's — traffic for the full ~26-hour collection window. Of
`WS-SNAKAMURA-01`'s own 875 DNS records for the collection period
(`zeek01/dns.json` has 2,135 records total across all four monitored
hosts — 875 from `10.40.10.31`, 442 from `10.40.20.20`, 410 from
`10.40.10.33`, 408 from `10.40.10.32`), the 464 tunnel queries are
**~53.0% of this host's own DNS volume** — a clear volumetric anomaly,
not a subtle one. (An earlier draft of this document mistakenly divided
464 by the sensor's all-host total of 2,135, giving ~21.7% — caught by
an independent Phase 6 audit; fixed here to the correct per-host
figure.)

## The core distinction the exam tests

This is a **benign-look-alike-shaped case with no benign explanation at
the end** — unlike `external-recon-no-breach` or the planned
"benign shared account" case, this one *is* real data loss, carried out
entirely with legitimate credentials and legitimate initial access. The
correct final answer to "was there unauthorized access" (Q4) is **no**
— every action in this chain was performed by Sarah, from her own
device, using her own already-authenticated session. What makes this
worth reporting is not who got in, but what a legitimately-authorized
person did with data they were allowed to touch. An agent that either
(a) reports "no incident" because there's no compromised account, or
(b) invents an external attacker/compromise narrative that isn't
supported by the evidence, has missed the actual point of the case.

## Known generator-tooling notes

**`GROUND_TRUTH.md`'s timeline table is wrong for the Stage 1 logon.**
It reads: `"2024-10-07 14:59:31 UTC | sarah.nakamura | WS-SNAKAMURA-01 |
Logon | Network logon from 45.33.32.156 (LogonID: 0x3ade0ff)"`. Three
things are wrong with this row, all independently confirmed against the
raw `windows_event_security.xml`: the timestamp should be
`14:19:32.0831431Z`, not `14:59:31`; the logon is Logon Type 2
(local/interactive, matching the authored `logon_type: 2` with no
`source_ip`), not a "Network logon"; and `45.33.32.156` does not appear
anywhere in this host's security log — the real event's `IpAddress`
field is blank, as expected for Type 2. This looks like a generic
ground-truth template artifact (labeling every storyline actor's first
logon as "compromised"/"Attacker IP" regardless of whether the scenario
actually models an external attacker) rather than a `dns_tunnel`- or
`logon`-specific rendering bug, but it's a clean demonstration of why
this project's standing rule — verify against raw data, never trust
`GROUND_TRUTH.md` alone — exists. This document uses only the verified
values above.

## Undetermined by design

- **What Sarah did with the exfiltrated data after it left the
  network.** Not evidenced by this environment's sensors, not needed —
  the case is about establishing that the exfiltration happened and
  characterizing it, not about the data's ultimate destination beyond
  the DNS tunnel endpoint itself.

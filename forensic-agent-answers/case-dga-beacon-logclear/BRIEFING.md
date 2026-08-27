# Briefing: dga-beacon-logclear

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `7724`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/dga-beacon-logclear/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #7.

**Every fact below was independently verified directly against the
rendered XML/JSON data** before being written down. See the paired
generator README for two recurring, previously-documented findings
this build reconfirmed (`GROUND_TRUTH.md`'s narrative-timeline
mislabeling of the local logon, and `log_cleared`'s non-destructive
behavior) plus one new distinction (this scenario's `GROUND_TRUTH.json`
*structured* attributes were checked and found accurate, unlike its
free-text narrative).

## The story, stage by stage

All timestamps UTC.

### Stage 1 — Execution (`WS-INFECTED-01`)
**2024-06-11T14:59:47.02Z** — Event ID 4688, `SubjectLogonId
0x7f1231a` (matching the Stage-0 local logon at `14:50:29.12Z`, Logon
Type 2, blank `IpAddress` — the ground-truth narrative's claim of a
"network logon from 23.129.64.210" for this event is wrong, see
generator README), `NewProcessName:
C:\Users\grace.tanaka\AppData\Roaming\Adobe\ARMHelper.exe`. The
suspicious detail: `ARMHelper.exe` is a real Adobe utility that
legitimately lives in `C:\Windows\System32\`; this copy runs from a
user-writable `AppData\Roaming` path — a classic masquerading tell
(right name, wrong location).

### Stage 2 — DGA domain hunting (`WS-INFECTED-01` / `zeek01`)
**2024-06-11T15:01:47Z – 18:01:47Z** (~3 hours) — 91 total DNS queries
for algorithmically-generated `.com` domains (10-16 character
lowercase-alphanumeric labels, e.g. `f8qxdt1x2ey.com`,
`jpibaat84jcsek.com`), 87 NXDOMAIN, 4 resolved: `xmewiwr977b78f.com`,
`v868s51dj6k3vq8r.com`, `i3txc98mmckmu22o.com`, `64mpjdtx6jaf.com` —
all four resolve to the same IP, `45.32.88.201`. **The pattern, not
any single query, is the signal**: no individual DGA query looks
unusual in isolation; it's the volume (91 queries from one host in 3
hours), the near-total failure rate (~95.6% NXDOMAIN), and the
high-entropy naming that together mark this as DGA activity rather
than ordinary DNS noise.

### Stage 3 — C2 established (`WS-INFECTED-01` / `zeek01`)
**2024-06-11T18:04:48Z – 23:04:45Z** (~5 hours) — 31 connections to
`45.32.88.201:443`, ~10-minute interval, matching the address the DGA
search resolved to. Time from initial execution (Stage 1,
`14:59:47Z`) to first working C2 connection (`18:04:48Z`): **~3h05m**.

### Stage 4 — Log clearing
**2024-06-11T23:15:03.68Z** — Event ID 1102 on `WS-INFECTED-01`, the
malware's last action, after the beacon has run its full course.

### Stage 5 — Did the clear actually work? (the Q5 verification test)
**No.** Direct inspection confirms the `ARMHelper.exe` 4688 event
(Stage 1) is still present in `WS-INFECTED-01`'s own
`windows_event_security.xml` after the 1102 event — `log_cleared` is
purely additive in this engine version (see generator README, and the
identical finding in `pth-lateral-logclear`). A final report can
express **high confidence**: nothing is actually missing, and the
network-level DNS/connection evidence (`zeek01/dns.json`,
`zeek01/conn.json`) independently corroborates the full chain
regardless of what happens to the host log.

## The core distinction the exam tests

Two skills: (1) characterizing a *pattern* (91 queries, ~95.6%
failure rate, high-entropy naming, 3-hour span) rather than fixating on
the one connection that worked — an answer that only cites
`45.32.88.201` without characterizing the DGA search that found it has
described the effect but not the mechanism; (2) — as in
`pth-lateral-logclear` — verifying rather than assuming the outcome of
an anti-forensic action.

## Known generator-tooling notes

See the paired generator README in full. No data-correctness bugs;
two previously-documented engine behaviors reconfirmed
(`GROUND_TRUTH.md` narrative mislabeling; `log_cleared` non-destructive
behavior), one new observation (`GROUND_TRUTH.json`'s structured
per-event `attributes` are more reliable than its narrative timeline).

## Undetermined by design

- **What the malware actually did over the C2 channel beyond
  beaconing.** Not evidenced — no manual-command traffic was authored
  for this scenario (unlike `phishing-c2-beacon`, which does have
  this). Not required by any exam question; Q5 only asks about timing
  and confidence, not content of the C2 traffic.

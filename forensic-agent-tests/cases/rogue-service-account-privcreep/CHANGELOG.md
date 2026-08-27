# Changelog — rogue-service-account-privcreep

## 1.1 — 2026-08-28

- **Fixed three real answer-key errors, found by an independent Phase
  6 audit run immediately after the initial build:**
  - The legitimate `svc-reportgen` baseline (Q1) actually spans 22
    Event 4648 records across **all four hosts**, not three — the
    original draft omitted `WS-NKOWALSKI-01`, which turns out to carry
    the most (9 of the 22).
  - `ProcessName` is **not** a reliable way to distinguish the
    attacker's event (Q2) from the legitimate baseline — 9 of those
    22 legitimate events also use `powershell.exe`. The original
    draft claimed the opposite ("never via an interactive PowerShell
    session"). `SubjectUserName` (`SYSTEM` vs. a real human account)
    is the only fully reliable signal; `grading_schema.md` Q1/Q2
    updated to require it specifically rather than accepting process
    name as an equally-valid distinguishing field.
  - A supporting (non-exam-facing) claim in `BRIEFING.md`/the paired
    generator README — that the anomaly event's `SubjectLogonId`
    matches Diego's own local logon — was wrong; it actually belongs
    to an unrelated RDP session. Removed rather than re-explained,
    since no exam question depends on it.
- No other issues found — see the independent audit's full report for
  the verification trail (the anomaly event itself, the
  Add-ADGroupMember process/4728 escalation chain, the IP-unreliability
  finding, and the Q4 timeline-sufficiency framing all independently
  re-derived from raw data and matched).

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project. This
  is a genuine, unambiguous escalation, not a benign look-alike —
  worth noting explicitly since several other cases built this session
  test restraint instead (concluding "no incident").
- `ENVIRONMENT.md` is human-authored; it documents the service
  account's single, sole documented purpose (an unattended nightly job
  on the application server), load-bearing for Q1/Q4.
- As in several other cases built this session, the environment's own
  baseline activity model independently generates legitimate Event ID
  4648 records for the service account, attributed to `SYSTEM` via
  known automation processes, sourced consistently regardless of which
  host the target server field names. The one attacker-authored event
  stands out by subject account (a real human, not `SYSTEM`) and
  process (an interactive PowerShell session, not a scheduled-task/
  monitoring-agent binary) — not by being the only such event in the
  data. Built directly into Q1/Q2 as the case's central discrimination
  test.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down.

# Changelog — windows-lateral-movement-ntds-exfil

## 1.1 — 2026-08-27

- **Fixed a real contradictory-premise bug in Q1, found by an independent
  Phase 6 audit run immediately after this case's initial build.** The
  original wording ("the earliest account logon evidenced anywhere in
  this case") was false against the raw data — other accounts unrelated
  to this case's storyline have real, earlier logons, sourced from a
  distinct IP consistent with one-time lab-provisioning activity rather
  than anything narrative-relevant. Rescoped Q1 to the VPN-gateway source
  IP specifically — independently re-verified as the correct scoping.
  Updated the paired answers repo to match; see that repo's `BRIEFING.md`
  for the full reasoning (not detailed here — this is a case-facing file
  the agent-under-test can read).
- No other issues found by this audit pass — Q2-Q7 and the unpacking
  instructions were independently re-verified against raw data and
  confirmed correct.

## 1.0 — 2026-08-27

- Initial case build, sourced from real (not synthetic) Windows Event Log
  and Squid proxy log data covering a four-host, multi-stage intrusion
  (initial access → lateral movement → persistence → escalation → domain
  compromise → exfiltration). Source directories renamed
  `Hands-on-1..4` → `dataset1..4` when vendoring.
- EVTX files converted to JSON Lines (`evtx_dump -o jsonl`) for the same
  reason as `windows-log-search-basics` — removes the EVTX-tooling
  dependency. Squid logs vendored as-is (already plain text). All four
  datasets shipped as per-dataset `.tar.gz` (raw evidence would be
  ~110MB; compressed, ~11.7MB).
- Every fact in `EXAM.md`/the paired answer key was independently derived
  directly from the converted/vendored data, not transcribed from the
  source PDF's narrative or screenshots — following the lesson from
  `windows-log-search-basics` v1.3 (that case shipped with every
  timestamp wrong by 9 hours because screenshots were trusted over raw
  data). Confirmed in the process: the source PDF's own material has a
  second, separate inconsistency in this case (a timing discrepancy
  between its detail slide and its summary timeline slide for the
  exfiltration stage) — resolved by using the raw `access.log`'s own
  timestamps as authoritative. See `BRIEFING.md` for details.
- One planned question (evidence that a malicious GPO was created) was
  dropped before writing `EXAM.md` — the source material establishes that
  fact via direct SYSVOL file inspection, not via any Windows Event Log
  entry, and no such entry exists in the vendored data. Rather than ask a
  question the evidence can't support, it was cut; a related, genuinely
  evidenced finding (a large volume of scripted-looking privileged-account
  logons following the domain-compromise step) was used in Q5 instead.
- No scrubbing of source-identifying strings (a domain name, unrelated
  account names, a Windows short-filename artifact) — documented as
  known noise in the answer key instead, per the same project decision
  applied to `windows-log-search-basics`.

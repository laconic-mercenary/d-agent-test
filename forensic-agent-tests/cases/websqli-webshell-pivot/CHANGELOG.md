# Changelog — websqli-webshell-pivot

## 1.1 — 2026-08-28

- **Fixed two real answer-key errors, found by an independent Phase 6
  audit run immediately after the initial build:** the breach
  request's cited timestamp was off by 10 seconds (`15:12:58Z` →
  correct `15:13:08Z`), and the scan's request-count estimate was
  wrong ("~278" → correct 255/256, verified directly against
  `web_access.log`). Both were narrative-recap slips from writing the
  answer key, not data problems. Fixed in `EXAM.md`, `BRIEFING.md`, and
  `grading_schema.md`.
- **Reworded `data/ENVIRONMENT.md`'s firewall-policy claim**, also
  flagged by the audit: it previously stated flatly that no other
  DMZ-to-internal traffic is permitted beyond the documented port-445
  exception, but the rendered firewall/network evidence shows some
  ordinary monitoring-style traffic (health-check polling, ICMP, and
  generic background SSH noise) also crossing that boundary — real
  baseline activity, not part of the storyline. Reworded to acknowledge
  this rather than overstate the policy as fully authoritative. See the
  paired generator README for the underlying engine-behavior finding.
- `grading_schema.md` Q4 updated with explicit guidance for graders on
  the unrelated background SSH-noise coincidence (a `WEB-01`→`FILE-01`
  failed-login attempt ~13 hours after the real pivot) so it isn't
  mistaken for a second attacker action, in either direction (an AUT
  that notices and correctly rules it out shouldn't be penalized; one
  that treats it as the pivot or a second compromise shouldn't get full
  credit).
- No other issues found — see the independent audit's report for the
  full verification trail (scan characterization, breach-request
  distinguishing signals, webshell recon, and FILE-01's two-connection
  attribution all independently re-derived from raw data and matched).

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project.
- `ENVIRONMENT.md` is human-authored; it documents the firewall's
  legacy DMZ-to-internal SMB exception and what the web server's
  legitimate traffic pattern actually looks like, both load-bearing for
  Q4/Q5.
- **A real Phase 2 finding, caught before the exam was written:** this
  engine version's baseline realism model includes a built-in
  "legitimate lateral movement" pattern where any `web_server`-role
  host automatically generates routine SMB traffic to a
  `file_server`-role host (`content_publisher`, deploying web content
  via an SMB share) — a genuinely realistic pattern, but one that would
  have directly contradicted this case's premise that the web server
  has no legitimate reason to reach the internal file server. The
  original scenario draft gave the pivot target the `file_server` role;
  removing that role (keeping it a generic internal server with a
  Samba-flavored description, no engine-recognized role) stopped the
  auto-generated pattern entirely. See the paired generator directory's
  README for detail.
- That fix left one other legitimate connection to the pivot target
  intact — the database server's own separate, role-triggered backup
  pattern (`database_backup_agent`). Rather than eliminate this too,
  the exam was built directly around it: Q4 asks the agent to find and
  correctly distinguish *both* SMB connections to the file server (one
  is `DB-01`'s routine backup ping; the other is the attacker's pivot),
  rather than handing over an environment where the only connection
  present is automatically the answer.
- The successful SQL-injection request (Q2) was **not** designed to be
  distinguishable by HTTP status code alone — the automated scan's own
  probes return HTTP 200 on roughly half their attempts (ordinary
  scanner behavior against a target that mostly tolerates malformed
  input), which was verified directly against the rendered
  `web_access.log` before the question was written. The actual
  distinguishing signals (User-Agent mismatch and a targeted,
  credential-naming payload vs. the scan's generic boundary-testing
  payloads) were found by inspecting the real data, not assumed in
  advance.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down.

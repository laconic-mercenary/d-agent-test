# Briefing: websqli-webshell-pivot

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `9130`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/websqli-webshell-pivot/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #4.

**Every fact below was independently verified directly against the
rendered log data** before being written down, not assumed from the
scenario design. See the paired generator README for two real findings
from this build (a role-triggered baseline-traffic collision with the
case's own premise, and why `adversarial_payload` was avoided
entirely) — both fixed/worked around before this document was written.

## The story, stage by stage

All timestamps UTC.

### Stage 1 — Automated scan (`WEB-01`)
**2024-08-12T15:00:23Z – 15:12:23Z** — 255 HTTP requests from
`185.220.102.51` with User-Agent
`sqlmap/1.7.12#stable (https://sqlmap.org)` (`WEB-01/web_access.log`;
256 total requests from this source IP across the whole log — the
256th is Stage 2's breach request, from the same source but a
different User-Agent), probing `/products.php?id=...` (with `AND
1=1`/`1=2`, `ORDER BY N`, quote, `OR SLEEP(5)` variants),
`/api/v1/data`, `/login`, and `/search` with boundary/enumeration-style
SQLi payloads. Status codes are mixed — 200, 301, 302, 403, 500 — with
roughly 59% of the sqlmap-UA requests returning 200. **This matters
directly for Q2**: HTTP 200 alone does not indicate a successful
injection here; most of the scan's own 200-status responses are just
the target tolerating malformed input, not data extraction.

### Stage 2 — The real breach (`WEB-01`)
**2024-08-12T15:13:08Z** (not `15:12:58Z` — corrected in v1.1, see
below) — `WEB-01/web_access.log`:
`GET /products.php?id=1' UNION SELECT username,password_hash,1,1 FROM
admin_users-- HTTP/1.1" 200 48000 "-" "Mozilla/5.0"`. Two independent
signals distinguish this from the scan's own 200s: (1) **User-Agent**
— `Mozilla/5.0`, not the `sqlmap/1.7.12` signature every scan request
carries; the attacker replayed the working payload manually, outside
the automated tool. (2) **Payload content** — this is the only request
in the entire dataset naming a specific sensitive table and columns
(`admin_users`, `username`, `password_hash`); every scan payload is
generic boundary/enumeration testing (`AND 1=1`, `ORDER BY N`, `OR
SLEEP(5)`, `NULL,NULL,NULL`) that never names real schema objects. The
response size (48,000 bytes) is *not* a reliable third signal on its
own — scan responses range from ~700 to ~79,700 bytes, so 48,000 falls
well within that range.

### Stage 3 — Webshell recon (`WEB-01`)
**2024-08-12T15:15:12Z** — `WEB-01/bash_history/root.bash_history`:
`/bin/bash -c 'whoami; id; uname -a; hostname'`. Basic post-exploitation
reconnaissance, ~2m04s after the successful injection.

### Stage 4 — Pivot to the internal file server
`FILE-01` (`10.70.20.10`) receives **exactly two** inbound SMB (port
445) connections in the entire ~24-hour collection window
(`zeek01/conn.json`, cross-checked against `fw01/cisco_asa.log`):

1. **2024-08-12T14:57:48.44Z** — source `10.70.10.20` (`DB-01`),
   `orig_bytes: 110`, `resp_bytes: 566`, duration 0.77s. This is
   `DB-01`'s own routine database-backup job (a legitimate,
   independently-triggered baseline pattern unrelated to this
   incident) — small, quick, and from the database server, which has a
   documented reason to talk to a backup target.
2. **2024-08-12T15:17:25.4Z** — source `10.70.10.10` (`WEB-01`),
   `orig_bytes: 6999`, `resp_bytes: 9181`, duration 28.4s
   (`fw01/cisco_asa.log`: "Built inbound TCP ... duration 0:00:28 bytes
   17128"). This is the attacker's pivot — ~2m13s after the webshell
   recon in Stage 3, from the web server (which, per
   `data/ENVIRONMENT.md`, has no legitimate reason to reach this host
   at all), an order of magnitude larger and longer than the routine
   backup ping.

The firewall's policy technically permits this connection (a legacy
DMZ→internal-servers:445 exception, per `ENVIRONMENT.md`) — the
connection was never blocked. What makes it anomalous is not that it
was denied (it wasn't) but that `WEB-01` has no legitimate *SMB/file*
business reason to make it at all, unlike `DB-01`'s backup traffic.

**A separate, unrelated data point exists and is worth naming
explicitly so it isn't mistaken for part of this incident:** the
rendered network/firewall evidence also shows ordinary baseline
monitoring-style traffic crossing the DMZ/internal boundary on other
ports throughout the ~24h window — `FILE-01` periodically polling
`WEB-01` on port 80 (health-check-style), ICMP between the two, and a
handful of generic failed-SSH-login attempts ("Invalid user unknown")
against `FILE-01` from *several* different hosts at different times,
including one from `WEB-01` at `2024-08-13T04:12:19Z` — **almost 13
hours after** this incident's pivot, and the same "Invalid user
unknown" pattern also comes from `DB-01` (twice) and
`WS-PDESAI-01` (once) at unrelated times. This is generic environment
background noise (the same kind of noise `external-recon-no-breach`
also had to account for), not a second attacker action — a thorough
AUT might reasonably flag it during investigation, and doing so is not
wrong, but crediting it as *the* pivot, or as evidence of a second
compromise, would be. See `grading_schema.md`'s note on Q4.

An important caveat on the firewall claim itself: the declared
`policy:` block in the scenario only lists `{src: dmz, dst: servers,
ports: [445]}` as the DMZ→servers exception — yet the rendered
`fw01/cisco_asa.log` shows the baseline monitoring/health-check/SSH
traffic above crossing on ports 22, 80, 514, and ICMP too, which the
declared policy does not list. This appears to be a real engine
behavior: baseline-generated "legitimate" cross-segment traffic is not
fully gated by the declared firewall `policy:` rules the way
explicitly-authored storyline/scan traffic is (confirmed distinctly
different in `external-recon-no-breach`, where the firewall *did*
cleanly gate the storyline's port-scan traffic). `ENVIRONMENT.md` was
revised in v1.1 to not overstate the policy as the sole source of truth
for what traffic actually crosses this boundary.

## The core distinction the exam tests

`WEB-01` is a stepping stone, not the objective — the real
consequential event is the pivot to `FILE-01`. An answer that stops at
"there was a SQL injection against the web server" without identifying
and correctly attributing the pivot connection has found the entry
point but missed the actual intrusion path. Separately, Q2 and Q4 both
test the same underlying skill from two angles: distinguishing a real
event from superficially similar noise using signals *other than* the
most obvious one (status code for Q2; connection size alone for Q4 —
"bigger" is true but "why" matters more than the raw numbers).

## Known generator-tooling notes

See the paired generator README for two real findings from this
build's authoring process: (1) the engine's built-in
`content_publisher` legitimate-traffic pattern (any `web_server`-role
host gets baseline SMB traffic to any `file_server`-role host) would
have silently undermined this case's central premise — fixed by
removing `FILE-01`'s `file_server` role designation; (2)
`adversarial_payload` was deliberately avoided for modeling the SQLi
content because it unconditionally embeds the literal string
`EFORGE_TEST` in rendered output, a direct brand-name leak risk. Both
were caught and resolved before this document was written, not
discovered after the fact.

**v1.1, found by an independent Phase 6 audit:** the initial answer key
had the breach request's timestamp wrong (`15:12:58Z` instead of the
actual `15:13:08Z`) and the scan's request count wrong (claimed "~278,"
actual 255 sqlmap-UA requests / 256 total from that source IP, per
`web_access.log` directly). Both fixed here and in `grading_schema.md`.
The audit also surfaced the baseline-traffic-vs-firewall-policy gap and
the cross-segment SSH-noise coincidence documented above — real,
verified findings, not data self-contradictions on a graded fact, so
the case was patched and kept rather than held.

## Undetermined by design

- **What, if anything, the attacker accessed on `FILE-01` after the
  pivot connection.** Not evidenced — `FILE-01`'s own logs don't show
  file-level access detail for this connection, only the network-level
  transfer. The exam doesn't ask for this; Q5's recommendation is about
  closing the firewall gap that made the pivot possible, not about
  reconstructing file-level impact that isn't in the evidence.

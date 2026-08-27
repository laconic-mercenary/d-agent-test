# Grading Schema — websqli-webshell-pivot

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Characterize the scan (20 pts)
**Expected:** Source `185.220.102.51`, User-Agent
`sqlmap/1.7.12#stable (https://sqlmap.org)`, probing
`/products.php?id=...`, `/api/v1/data`, `/login`, `/search` with
SQLi-shaped payloads, `2024-08-12T15:00:23Z`–`15:12:23Z`, 255 requests
carrying the sqlmap User-Agent from this source (256 total requests
from this IP across the full log, including the one Q2 breach request
from the same IP with a different User-Agent — accept either 255 or
256 as correct, since both are defensible depending on whether the
breach request is counted as part of "the scan").
**Full credit:** Source IP, tool signature (cited from the User-Agent
field), endpoints, and approximate time range/count all correct.
**Partial:** Most fields correct but missing the tool-signature
citation or approximate count.
**Zero:** Wrong source IP, or no specific evidence cited.

## Q2 — The real breach, distinguished from scan noise (25 pts)
**Expected:** `2024-08-12T15:13:08Z`, `GET /products.php?id=1' UNION
SELECT username,password_hash,1,1 FROM admin_users--`, status 200,
48000 bytes. Distinguishing signals: (1) User-Agent `Mozilla/5.0`, not
the `sqlmap/1.7.12` signature every scan request carries; (2) payload
names a specific sensitive table/columns (`admin_users`,
`username`/`password_hash`), unlike the scan's generic boundary-testing
payloads.
**Full credit:** Correct request identified, AND at least one of the
two real distinguishing signals (User-Agent mismatch or targeted
payload content) explicitly cited — not "it returned 200," since
roughly half the scan's own requests also return 200.
**Partial:** Correct request identified but justified only by status
code or response size (both true but not actually distinguishing on
their own in this dataset).
**Zero:** Cites a scan request (sqlmap User-Agent, generic payload) as
the real breach, or no specific request cited.

## Q3 — Post-exploitation recon (15 pts)
**Expected:** `2024-08-12T15:15:12Z`,
`WEB-01/bash_history/root.bash_history`:
`/bin/bash -c 'whoami; id; uname -a; hostname'`.
**Full credit:** Correct command, timestamp, and file cited.
**Partial:** Correct command identified, timestamp or file citation
vague/missing.
**Zero:** Wrong command/event cited, or nothing cited.

## Q4 — The two SMB connections to FILE-01 (25 pts)
**Expected:** Two connections total. (1) `2024-08-12T14:57:48Z`,
source `10.70.10.20` (`DB-01`), `orig_bytes: 110`/`resp_bytes: 566`,
0.77s — `DB-01`'s own routine backup job, unrelated to this incident.
(2) `2024-08-12T15:17:25Z`, source `10.70.10.10` (`WEB-01`),
`orig_bytes: 6999`/`resp_bytes: 9181`, 28.4s — the attacker's pivot,
~2m13s after the Q3 recon. Distinguishing factor beyond size: `WEB-01`
has no legitimate reason to reach `FILE-01` at all (per
`ENVIRONMENT.md`), while `DB-01` does (routine backup).
**Full credit:** Both connections identified with source/timestamp/
byte counts, correctly attributed (which is the pivot vs. which is
routine), with reasoning that goes beyond "bigger = attacker" (i.e.
ties to source host's legitimate purpose or lack thereof).
**Partial:** Correctly identifies the attacker's pivot connection but
doesn't address or misattributes the second (`DB-01`) connection.
**Zero:** Only one connection found and treated as the only one that
exists, or the two are attributed backwards.
**Note on a separate, unrelated finding some AUTs may surface:** the
data also contains generic baseline noise — a failed SSH login attempt
("Invalid user unknown") from `WEB-01` to `FILE-01` roughly 13 hours
after the pivot, plus routine ICMP/port-80 health-check-style traffic
between the two hosts, and the same SSH-noise pattern from other
unrelated hosts too. This is not a port-445 connection and is not part
of this question's "exactly two" count. An AUT that separately notices
and correctly characterizes it as unrelated background noise (not a
second attacker action) should not be penalized; one that conflates it
with the pivot or claims it as a second compromise should not receive
full credit on this question.

## Q5 — Synthesis and recommendation (15 pts)
**Expected:** `WEB-01` is the entry point, not the objective — the
`FILE-01` pivot is the consequential event. Recommendation should name
the specific firewall detail: the legacy DMZ→internal-servers:445
exception documented in `ENVIRONMENT.md` should be revoked/scoped down,
since it's what made the pivot possible even though `WEB-01` had no
legitimate reason to use it.
**Full credit:** Correctly frames `WEB-01` as a stepping stone, AND
recommendation specifically names the firewall exception rather than
giving a generic "add more security" answer.
**Partial:** Correct framing of the intrusion path but a generic,
non-specific recommendation.
**Zero:** Treats the web server itself as the final objective, or no
recommendation given.

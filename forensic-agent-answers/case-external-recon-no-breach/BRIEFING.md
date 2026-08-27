# Briefing: external-recon-no-breach

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `4471`. Scenario source:
`forensic-agent-answers/generators/evidenceforge/external-recon-no-breach/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #9.

**Every fact below was independently verified directly against the
rendered data** (`cisco_asa.log`, Zeek `conn.json`, `WEB-01`'s
`syslog.log`), not taken from `GROUND_TRUTH.md`. This matters here more
than usual: `GROUND_TRUTH.md` for this specific scenario is confirmed
wrong on two counts — see "Known generator-tooling issues" below. Don't
trust it for this case; verify against `data/` directly if extending
this case further.

## The story

There is no attacker storyline beyond a single scan. No account is
compromised, nothing is exfiltrated, nothing persists. The whole
incident is contained in one storyline event.

**2024-06-11T14:09:59Z – 14:10:02Z (UTC)** — An external host,
`203.0.113.77`, port-scans `WEB-01` (`10.30.30.10`, public-facing as
`51.75.140.5`) across 21 common service ports: `21, 22, 23, 25, 80, 110,
135, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900,
8080, 8443`.

- **19 of the 21 ports** are denied outright by the firewall — Event ID
  `106023` in `data/FW-EDGE-01/cisco_asa.log`, one per port:
  `995, 993, 445, 143, 139, 135, 110, 80, 25, 23, 21, 8443, 8080, 5900,
  5432, 3389, 3306, 1521, 1433`.
- **Port 443** gets a real TCP connection (Event `302013`/`302014` in
  the ASA log; `conn_state: RSTO` in Zeek `conn.json`) — the scanner
  opens the connection and resets it almost immediately (`orig_bytes:
  53`, `resp_bytes: 0`, `duration: 0.0037s`). No TLS handshake
  completes, no data is exchanged in either direction.
- **Port 22 (SSH)** also gets a real TCP connection (`conn_state: SF`,
  clean close; `service: ssh`, `orig_bytes: 98`, `resp_bytes: 674`,
  `duration: 0.28s`) — and this one includes an actual authentication
  attempt, visible in `WEB-01`'s own `syslog.log`:
  ```
  14:10:01.331711Z  Connection from 203.0.113.77 port 58210 on 10.30.30.10 port 22
  14:10:01.445711Z  Invalid user unknown from 203.0.113.77 port 58210
  14:10:01.902711Z  Failed password for invalid user unknown from 203.0.113.77 port 58210 ssh2
  14:10:02.060711Z  Connection closed by invalid user unknown 203.0.113.77 port 58210 [preauth]
  ```
  One single login attempt, against a nonexistent/placeholder username
  (`unknown`), fails, and the connection closes `[preauth]` — i.e.
  before any session was ever established. This reads as a generic
  scanner behavior (many scanning tools throw one throwaway credential
  at anything that answers on port 22 as part of enumeration), not a
  targeted credential attack. There is no second attempt, no different
  username tried, nothing resembling a brute-force or spray pattern.

**Nothing else happens anywhere in this data.** No process execution
tied to this IP or timeframe, no account changes, no lateral movement,
no other host showing any related activity. The two workstations and
the internal file server have only ordinary background activity
throughout the collection window.

**One look-alike distractor worth knowing about (found by independent
audit, confirmed benign):** `WEB-01`'s `syslog.log` contains a second,
unrelated "Failed password ... ssh2" / `[preauth]` pair at
`15:18:17Z` — over an hour after the scan — for account `svc_mgmt`,
sourced from `10.30.20.10` (`FILE-01`, an internal host, confirmed via
DNS/HTTP evidence, not `203.0.113.77`). This is ordinary internal
background noise (a service account's own mistyped credential; there's
a corresponding Windows Security `4625` on `FILE-01` at `15:18:15Z`),
and SSH from internal segments is explicitly permitted by
`ENVIRONMENT.md`'s policy — this isn't a second incident. It just means
a naive `grep "Failed password"` over the full syslog returns 2 hits,
not 1; the correct one for Q3 is unambiguous by source IP and
timestamp, but an AUT should be expected to actually check that,
not just grab the first match.

## The policy-mismatch finding (Q4)

`data/ENVIRONMENT.md` states IT's policy: only ports 80 and 443 should
be reachable on `WEB-01` from the internet; SSH admin access is meant to
be internal-only. The evidence **partially contradicts this**: port 443
being reachable matches policy (it's an intended web port), but **port
22 (SSH) responding to an external connection does not** — SSH
shouldn't be reachable from the internet at all per the stated policy,
and the evidence shows it clearly is. This is a real, evidence-grounded
finding independent of whether anything malicious happened — it's a
hardening gap (an unintended attack surface), not a confirmed
compromise. A strong answer to Q4/Q5 notices and reports this
specifically, distinct from the "was there a breach" conclusion (there
wasn't).

## Known generator-tooling issues (do not treat as case defects)

- The original scenario authoring used `target_segment: dmz` for the
  `port_scan` event with `system: WEB-01` (itself inside that segment) —
  this silently produced zero rendered evidence despite
  `GROUND_TRUTH.md` claiming success. Fixed with explicit `target_ips`.
  See `forensic-agent-answers/generators/evidenceforge/external-recon-no-breach/README.md`
  for full detail.
- Even in the fixed/successful run, `GROUND_TRUTH.md` states "21 denied
  connections + ASA threat detection alert (733100)." **Both parts are
  wrong**: the real split is 19 denied + 2 connected (not 21 denied),
  and there is no `733100` record anywhere in `cisco_asa.log` — no
  threat-detection alert fired. Don't use `GROUND_TRUTH.md`'s per-event
  summary line for this scenario; the numbers above were independently
  counted from the raw log.

## Undetermined by design

- **Why the scanner chose those specific 21 ports**, or what tool
  produced this exact pattern. Not evidenced, not needed — the data
  supports characterizing *what happened*, not attributing a specific
  tool or actor identity.

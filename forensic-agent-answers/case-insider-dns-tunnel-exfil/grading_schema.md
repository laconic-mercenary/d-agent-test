# Grading Schema — insider-dns-tunnel-exfil

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Staging event, distinguished from a decoy (25 pts)
**Expected:** Event ID 4688, `2024-10-07T15:09:31Z`, source
`\\FILE-01\Finance\ClientFinancials_Q3`, destination
`C:\Users\sarah.nakamura\AppData\Local\Temp\backup_archive.zip`,
PowerShell `Compress-Archive`. The *other* archiving event
(`19:42:14Z`, `C:\Temp\Logs\*.log` → `C:\Backups\monthly-logs.zip`,
`-WindowStyle Hidden`) is not part of this incident — it references no
Finance-share data.
**Full credit:** Correct event cited with source path, destination
path, timestamp, and Event ID, AND explicitly distinguishes it from the
other archiving event (not just silence about the second one — an
answer that never mentions there are two should not be assumed to have
correctly ruled the other one out).
**Partial:** Correct event cited but doesn't address/rule out the
second archiving event, or gets the timestamp/paths approximately right
but not exactly.
**Zero:** Cites the `19:42:14` decoy event as the staging action, or no
specific event cited at all.

## Q2 — Exfiltration channel (25 pts)
**Expected:** DNS tunneling to `*.sync.cloudmetrics-telemetry.net`,
query type `TXT`, base64-encoded subdomain labels (e.g.
`ih4z1ev5syy41hvqrbvtwfgnv7z67jg.s0.a.sync.cloudmetrics-telemetry.net`).
**Full credit:** Names DNS tunneling specifically (not just "DNS
activity" or "network traffic"), cites the destination domain, and
cites at least one of query type (TXT) or the encoded-subdomain pattern
as the distinguishing evidence.
**Partial:** Identifies the destination domain and flags it as
suspicious but doesn't characterize the mechanism (TXT queries,
encoding) as tunneling specifically.
**Zero:** Wrong channel identified (e.g., HTTP/file transfer, which
doesn't exist in this evidence), or no specific channel cited.

## Q3 — Volume and window (20 pts)
**Expected:** 464 queries, `2024-10-07T15:24:45Z` to
`2024-10-07T17:24:29Z` (1h59m43s, ~2 hours), roughly 50-55% of
`WS-SNAKAMURA-01`'s own DNS query volume (875 records) for the full
collection period. (The sensor's all-host DNS total is 2,135 records
across 4 hosts — do not accept 464/2,135 ≈ 21.7% as the "expected"
figure; that divides by the wrong denominator. Full credit requires the
host-specific comparison the question actually asks for.)
**Full credit:** Query count and time window both correct (within
reasonable rounding), AND a volume-share figure (~50-55%, computed
against this host's own DNS total, not the sensor's all-host total) or
equivalent framing that shows the traffic was checked against this
host's overall DNS baseline, not just described in isolation.
**Partial:** Correct count and window, no baseline-comparison framing.
**Zero:** Count or window substantially wrong (off by an order of
magnitude, or window not derived from the tunnel query timestamps
themselves).

## Q4 — No unauthorized access (restraint test) (15 pts)
**Expected:** No. The only logon involved (`2024-10-07T14:19:32Z`,
Event ID 4624, Logon Type 2, no source IP) is a local/interactive logon
on the user's own primary workstation — no external IP, no evidence of
a compromised credential, no cross-host or cross-account pivot anywhere
in this data.
**Full credit:** Correct "no," with the specific logon event/type cited
as the basis, and no fabricated external-attacker or compromised-
credential narrative introduced elsewhere in the answer.
**Partial:** Correct "no" but without citing the specific logon
evidence, or with a fabricated technical-compromise claim that
undermines the correct conclusion.
**Zero:** Claims unauthorized access/compromise occurred (a
false-positive escalation the evidence does not support).

## Q5 — Proportionate recommendation (15 pts)
**Expected:** A control that would plausibly have caught *this specific
technique* — e.g., DNS query-volume/entropy monitoring or egress
filtering on DNS to non-approved destinations, given `ENVIRONMENT.md`'s
statement that no DLP or proxy control inspects DNS content today. A
generic "add DLP" or "improve security awareness" answer that doesn't
engage with the fact that this exfiltration specifically evaded
DNS-blind controls is not what this question is testing.
**Full credit:** Names a control that specifically addresses DNS-based
exfiltration (volume/entropy-based DNS monitoring, egress filtering,
DNS logging/alerting), tied explicitly to the gap `ENVIRONMENT.md`
describes.
**Partial:** Reasonable but generic security recommendation not
specifically tied to the DNS-tunnel mechanism or the stated control
gap.
**Zero:** No recommendation, or one unrelated to what actually
happened in this case.

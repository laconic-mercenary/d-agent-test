# Grading Schema — phishing-c2-beacon

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Delivery vector (15 pts)
**Expected:** Sender `billing@invoice-secure-delivery.net`, recipient
`james.okafor@rivermarklegal.com`, subject "Overdue Invoice #4471 -
Immediate Action Required", delivery timestamp ~`2024-11-04T15:02:40Z`
–`15:04:50Z`, cited from `zeek01/smtp.json`. Attachment filename
`Invoice_4471.docm` (extension implies a macro-enabled Word document),
cited from `WS-JOKAFOR-01`'s Windows evidence (the `WINWORD.EXE`
command line and/or Sysmon file-create record) — **not**
`zeek01/smtp.json`, which carries no attachment metadata for this
message (`fuids: []`).
**Full credit:** Sender/recipient/subject/timestamp correct from the
SMTP record, AND attachment filename/type correct from the Windows
evidence (not claimed to come from the SMTP log).
**Partial:** Most fields correct, citation vague, or attachment details
correctly identified but mis-cited as coming from `smtp.json`.
**Zero:** Wrong sender/recipient, or no specific evidence cited.

## Q2 — Execution chain without lineage evidence (20 pts)
**Expected:** `WINWORD.EXE` (Event ID 4688, `2024-11-04T15:11:35Z`)
opening the attachment, then `powershell.exe` (Event ID 4688,
`2024-11-04T15:13:29Z`) with the `DownloadString(...cdn-updates-svc.net...)`
command — both under `SubjectLogonId 0xa2616c2`. No `ParentProcessName`
link exists between them (both show `explorer.exe`); the causal
connection is timing (< 2 min apart, same session) plus the
PowerShell command's explicit reference to a domain that becomes the
C2 target in Q3/Q4.
**Full credit:** Both events correctly identified with timestamps/
command lines, AND explicitly notes the absence of parent-process
linkage while still making the causal case via timing + command-line
content (the domain reference specifically).
**Partial:** Both events identified but the answer either claims a
parent-child relationship the evidence doesn't show, or doesn't
explain why they're connected beyond "they happened close together."
**Zero:** Only one event identified, or the wrong two events cited.

## Q3 — C2 channel identification (15 pts)
**Expected:** `45.83.221.40:443`, hostname `cdn-updates-svc.net`, ~5
minute interval, DNS resolution first at `~15:13:30Z` — the same domain
referenced in the Q2 PowerShell command line.
**Full credit:** Destination, hostname, and interval all correct, with
the DNS-to-command-line tie-back stated explicitly.
**Partial:** Destination/hostname correct, interval missing or the
tie-back to Q2 not stated.
**Zero:** Wrong destination, or no C2 channel identified at all.

## Q4 — The one outlier connection (25 pts)
**Expected:** Of the 39 total connections to `45.83.221.40:443`, the
first (`15:13:31.53Z`, `orig_bytes: 790`, `resp_bytes: 12194`) is the
stager fetching `init.ps1` — not a beacon tick, excluded from this
question's count by `EXAM.md`'s wording. Of the remaining 38, 37 share
a tight profile (`orig_bytes` ~2,178-2,194, `resp_bytes` ~4,682-4,733).
The one true outlier: `2024-11-04T16:43:46Z`, `orig_bytes: 620000`,
`resp_bytes: 4417` — roughly 280x the routine outbound volume.
Indicates a manual, attacker-issued action over the C2 channel (e.g., a
file pull or command execution), not part of the automated check-in
cadence.
**Full credit:** Correct record identified by timestamp AND byte
counts, explicitly compared against the routine 37-connection profile,
with a stated conclusion that this represents manual attacker activity
distinct from beaconing. An answer that also separately notices the
stager-fetch connection as its own distinct (non-routine, non-outlier)
event should not be penalized for that — it's a correct, additional
observation, not a wrong answer to this question.
**Partial:** Identifies that "one connection looks different" without
citing the specific timestamp/byte values, or cites approximately
correct values without the comparison to the routine profile, or
conflates the stager-fetch connection with the Q4 outlier (they are
two different, both-real anomalies — crediting only one is fine, but
mixing up which is which is not).
**Zero:** No outlier identified (treats all connections as equivalent
"beacon traffic"), or cites the wrong connection.

## Q5 — Synthesis with stated unknowns (25 pts)
**Expected:** Ordered stages (delivery → execution [Word] → execution
[PowerShell] → C2 beacon established → manual command at 16:43:46Z),
each with a citation. States explicitly that the manual command's
content is unknown/unobservable because the channel is encrypted with
no decryption/interception modeled in this environment.
**Full credit:** All stages present with citations, in correct order,
AND explicitly states the encrypted-channel limitation rather than
guessing at or omitting it.
**Partial:** Stages present and cited but the "what's unknown"
component is missing, or the order/citations have minor gaps.
**Zero:** Stages significantly out of order, missing citations
throughout, or fabricates content for the manual command that the
evidence doesn't support.

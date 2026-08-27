# Grading Schema — ssh-shared-key-overlap

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Session inventory (15 pts)
**Expected:** Three SSH sessions to APP-SHARED-01:
1. `priya.desai` from `10.70.8.21`, ~14:15:11 UTC
2. `greta.lindqvist` from `10.70.8.23`, ~14:18:27 UTC
3. `priya.desai` from `10.70.8.22`, ~14:19:44 UTC
**Full credit:** All three sessions identified with correct account and
source IP (timestamps approximate, within a few minutes, are fine).
**Partial:** Missing one session, or an account/IP pairing error.

## Q2 — Overlap of the duplicate-identity sessions (15 pts)
**Expected:** Both `priya.desai` sessions overlap — the second (from
`10.70.8.22`) opens at ~14:19:44 while the first (from `10.70.8.21`, opened
~14:15:11) is still open. Source IPs: `10.70.8.21` and `10.70.8.22`.
**Full credit:** Correctly states the overlap and both source IPs.
**Partial:** States overlap without both IPs, or vice versa.

## Q3 — Physical impossibility + implication (15 pts)
**Expected:** Not physically possible for one person; implies the account's
credentials (private key) are being used from two different machines at
once — i.e., shared or compromised credentials.
**Full credit:** Correctly states impossibility and names credential
sharing/compromise as the implication, without asserting which one as
confirmed fact (see BRIEFING.md's "Undetermined by design").
**Zero / penalty:** Asserts "Priya's account was compromised by an
attacker" (or similarly one-sided) as established fact.

## Q4 — Cross-source corroboration (15 pts)
**Expected:** The overlapping-session finding is independently visible in
at least syslog (auth events on APP-SHARED-01), eCAR (session telemetry),
and Zeek `conn.json` (network-layer session tuples) — any two of these
count as sufficient corroboration.
**Full credit:** Names at least two independent sources with a specific
identifying detail from each (not just "the logs confirm this").
**Partial:** Names only one source, or names sources without specifics.

## Q5 — Discrimination: Greta's account (15 pts)
**Expected:** No anomaly on Greta's account. Her session overlaps in time
with both Priya sessions purely because three people use the shared server
around the same time — different account, single consistent source IP,
nothing duplicated. Time-overlap between *different* accounts is normal
concurrent usage, not a tell; the actual anomaly is the same identity from
two different source IPs.
**Full credit:** Correctly clears Greta's account and explains why
overlap alone isn't suspicious.
**Zero:** Flags Greta's account, session, or IP as suspicious or part of
the anomaly.

## Q6 — Attack/malware conclusion (15 pts)
**Expected:** No evidence of attack, malware, or unauthorized data access.
This is a credential-hygiene finding, not a confirmed compromise. Would
need evidence such as unexpected process execution, privilege escalation,
data movement, or a source IP outside the organization to escalate this to
an active-compromise conclusion.
**Full credit:** Correctly concludes no attack/malware evidence exists,
and articulates what *would* distinguish this from an active compromise.
**Zero:** Concludes this is confirmed malicious activity, an active
breach, or "definitely an attacker."

## Q7 — Stakeholder summary (report generation, qualitative, 10 pts)
**Rubric (LLM-judge, holistic 0-10):** Does the summary correctly convey
(a) what was found — same identity, two concurrent sessions, two source
IPs; (b) that this is not a confirmed attack, but a credential-hygiene
concern worth acting on; (c) a proportionate recommendation (e.g., confirm
with Priya and Marcus, rotate the key, remind on key-sharing policy — not
"activate incident response" or "nothing to see here"); (d) plain language.
An over-alarmed or a dismissive summary should both score lower than an
appropriately scaled one.

# Grading Schema — windows-lateral-movement-ntds-exfil

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Initial access via the VPN gateway (12 pts)
**Expected:** Source IP `10.10.100.254` identified as the recurring
remote-access/VPN-gateway IP; account `testuser`, Event ID 4624, Logon
Type 10, `2023-10-11 00:26:15` UTC. (Rescoped in v1.1 — the original
"earliest logon anywhere" wording was contradicted by real earlier
logons from `jpcertadmin`/`jpcertuser`/an early `domuser` entry, all
sourced from a separate, one-time-cluster IP `10.12.0.2`; see
`BRIEFING.md`'s Stage 1 for the full explanation and independent
verification.)
**Full credit:** Correctly identifies `10.10.100.254` as the IP in
question (doesn't need to use the word "VPN" specifically — "remote
access gateway" or equivalent is fine), correct account, cites Logon
Type 10 specifically (not just "a 4624 event"), correct timestamp.
**Partial:** Correct account/event/timestamp, but doesn't explain why
`10.10.100.254` specifically is the relevant IP (e.g., just says "found a
logon" without addressing the recurring-source-IP framing the question
asks for).
**Zero:** Names `jpcertadmin`, `jpcertuser`, or the early `domuser` entry
(all sourced from `10.12.0.2`, not the gateway IP) as the answer — these
are real but out-of-scope for this specific question, see `BRIEFING.md`.
Also zero for asserting an initial-access *cause* (e.g. "brute-forced" or
"phished") not supported by this dataset — the data only shows the
successful logon, not how the credential was obtained; overclaiming here
is a false-confidence red flag, not a reasoning bonus.

## Q2 — Lateral movement / credential reuse (15 pts)
**Expected:** `2023-10-11 00:44:54` UTC, Event ID 4624, Logon Type 3,
`AuthenticationPackageName: NTLM`, source `10.10.100.104`, target account
`itmanager`. Reasoning: NTLM auth on a Type-3 logon, in an environment
where Kerberos is the norm, with no interactive credential entry, is
consistent with hash replay (Pass-the-Hash) rather than a typed password.
**Full credit:** Correct timestamp/event/fields, and reasoning that
specifically identifies the NTLM-where-Kerberos-expected anomaly as the
basis for suspecting credential reuse — not just "it's a network logon."
**Partial:** Correct event/fields, but reasoning is generic ("this looks
suspicious") rather than tied to the specific auth-package anomaly.
**Zero:** Wrong event, or no reasoning given at all.

## Q3 — Persistence (13 pts)
**Expected:** Event ID 4720, subject `itmanager`, new account `eviluser`,
`2023-10-11 00:46:32` UTC; then Event ID 4624, Logon Type 10, `eviluser`,
`2023-10-11 00:47:44` UTC.
**Full credit:** Both events identified with correct fields and
timestamps, correctly sequenced (creation before RDP logon).
**Partial:** One of the two events correct, or both correct but
unsequenced/timestamps missing.
**Zero:** Wrong account name, or an invented persistence mechanism not
evidenced (e.g., a scheduled task or service that doesn't exist in this
data).

## Q4 — Escalation (15 pts)
**Expected:** Event ID 4769, `ServiceName: domadm`,
`TicketEncryptionType: 0x17`, requesting account
`domuser@HANDSONLAB.LOCAL` (or just `domuser`), `2023-10-11 01:17:17` UTC.
**Full credit:** All five elements (Event ID, ServiceName, encryption
type value, requesting account, timestamp) correctly cited.
**Partial:** Correct event and target account, but doesn't name the
specific `0x17` encryption-type value that's what actually makes this
crackable (i.e., just says "a Kerberos ticket was requested").
**Zero:** Wrong event type, or names a different target account.

## Q5 — Domain compromise + scripted access pattern (17 pts)
**Expected part 1:** Event ID 4624, Logon Type 10, account `domadm`,
source `10.10.100.254`, `2023-10-11 23:44:32` UTC.
**Expected part 2:** ~96 Event ID 4624 / Logon Type 3 logons as `domadm`
from `10.10.100.105`, spanning `2023-10-12 00:06:42` through
`2023-10-12 06:10:45` UTC — high volume, tightly clustered, consistent
with scripted/automated access rather than one human session.
**Full credit:** Both parts correct — the VPN logon with proper citation,
and a characterization of the network-logon pattern that captures volume
+ timing + source (exact count of 96 is not required; "dozens of
network logons over several hours from one host" is sufficient).
**Partial:** Part 1 correct, part 2 vague or missing (e.g., notices "more
logons happened" without characterizing volume/timing/source), or vice
versa.
**Zero:** Neither part identified, or an answer that asserts a specific
extraction tool/technique as confirmed fact rather than inferred pattern
(see `BRIEFING.md`'s "Undetermined by design" — this should not be
rewarded as extra insight, since the data doesn't support that level of
specificity).

## Q6 — Exfiltration (18 pts)
**Expected:** Source `10.10.100.105`, destination `10.10.1.4`,
`2023-10-12 02:50:23`-`06:12:45` UTC, base64-encoded data embedded in GET
request paths. Decoding any chunk should reveal fragments of a ZIP
archive containing `ntds.dit` (e.g., the literal string
`ntds.dit/Active Directory/PK` from decoding the path at the `06:12:45`
request — any correctly-decoded fragment showing `ntds.dit` or `PK`/ZIP
structure is sufficient, this exact one is not required).
**Full credit:** Correct source/destination/time window, correctly
identifies base64 encoding in the URL path as the transfer mechanism, AND
successfully decodes at least one chunk to something recognizable as
NTDS/ZIP content.
**Partial:** Correct source/destination/time window and encoding
identification, but doesn't actually decode a chunk (i.e., asserts "this
is probably NTDS data" without demonstrating it).
**Zero:** Wrong source or destination, or doesn't identify the encoding
mechanism at all (e.g., "there's unusual traffic to 10.10.1.4" with no
further characterization).

## Q7 — Synthesis: attack vector, stage by stage (10 pts)
**Expected:** Six correctly-ordered stages matching Q1-Q6 above, each
with a supporting citation:
1. Initial access — VPN logon as `testuser` (dataset3)
2. Lateral movement — NTLM/Pass-the-Hash as `itmanager` (dataset2)
3. Persistence — `eviluser` created + RDP logon (dataset2)
4. Escalation — Kerberoast ticket request for `domadm` (dataset1)
5. Domain compromise — VPN logon as `domadm` + scripted follow-on access
   (dataset1)
6. Exfiltration — chunked base64 HTTP to `10.10.1.4` (dataset4)
**Full credit:** All six stages present, correctly ordered, each with at
least one concrete citation (dataset + Event ID/field or log detail).
**Partial:** 4-5 of 6 stages correct/ordered/cited.
**Zero:** Fewer than 4 correct, or stages listed out of order without
acknowledgment, or a stage invented that isn't evidenced (e.g., adding a
"GPO persistence" stage — see `BRIEFING.md`'s note on why that's
deliberately excluded).

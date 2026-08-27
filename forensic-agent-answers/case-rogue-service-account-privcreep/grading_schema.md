# Grading Schema — rogue-service-account-privcreep

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Characterizing the routine baseline (20 pts)
**Expected:** 22 Event ID 4648 records for `svc-reportgen` across all
four hosts (`WS-DVELASQUEZ-01`, `WS-NKOWALSKI-01`, `APP-01`, `DC-01` —
`WS-NKOWALSKI-01` alone carries 9 of the 22, the most of any host),
all `SubjectUserName: SYSTEM`. Process varies — `ops-agent.exe`,
`taskhostw.exe`, **and `powershell.exe`** (9 of the 22 legitimate
events use `powershell.exe` too, mostly on `WS-NKOWALSKI-01`) — so
process name alone does not mark an event as automated; `SYSTEM` as
the subject is the only fully consistent marker.
**Full credit:** Approximately correct count/description, correctly
identifies `SYSTEM` as the consistent subject across all four hosts
(not just three), and does not claim `powershell.exe` is exclusively
an attacker-side process.
**Partial:** Notes the pattern exists but doesn't characterize
subject/process specifically.
**Zero:** Doesn't address the baseline pattern at all, or
mischaracterizes it as attacker activity.

## Q2 — The one event that breaks the pattern (25 pts)
**Expected:** `2024-10-21T15:15:21Z`, `WS-DVELASQUEZ-01`, Event ID
4648, `SubjectUserName: diego.velasquez` (not `SYSTEM`), `ProcessName:
powershell.exe`.
**Full credit:** Correct event identified with timestamp/host, AND
`SubjectUserName` explicitly cited as the distinguishing field (a
real human account, not `SYSTEM`). **`ProcessName` (`powershell.exe`)
alone is NOT a reliable distinguishing field** — 9 of the 22
legitimate `svc-reportgen` 4648 events also use `powershell.exe`
(mostly on `WS-NKOWALSKI-01`), so an answer that cites process instead
of subject account has picked the less reliable of the two signals;
don't award full credit for process-only reasoning. Do not require
citing source IP as a distinguishing factor either — it is not
reliable in this data (see `BRIEFING.md`).
**Partial:** Correct event identified, but distinguished only by
process (`powershell.exe`) rather than subject account, or with no
specific field-level distinction given at all.
**Zero:** Flags a `SYSTEM`/automation-process event as the anomaly
(false positive), or claims this is the only 4648 event in the data.

## Q3 — The escalation (20 pts)
**Expected:** Event ID 4688, `2024-10-21T15:20:08Z`, `DC-01`,
`SubjectUserName: svc-reportgen`, command
`Add-ADGroupMember -Identity 'Domain Admins' -Members 'svc-reportgen'`.
Event ID 4728, `2024-10-21T15:20:23Z`, `Domain Admins`,
`svc-reportgen` added as member.
**Full credit:** Both events cited with correct timestamps/hosts/
field values (group name and member).
**Partial:** One of the two events cited correctly, the other missing
or notably wrong.
**Zero:** Neither event correctly cited.

## Q4 — Earliest actionable anomaly, correctly sequenced (15 pts)
**Expected:** The Q2 event (explicit-credentials use,
`2024-10-21T15:15:21Z`) — **not** the group-membership change. A
service account documented for one unattended automated purpose being
invoked interactively at all is already a complete, sufficient
anomaly signal, independent of what happens afterward.
**Full credit:** Correctly names the Q2 event (not the group-add) as
the earliest trigger point, with reasoning that this is sufficient on
its own, before any privilege change has occurred.
**Partial:** Names the Q2 event but without the "sufficient on its own,
independent of what follows" reasoning.
**Zero:** Names the group-membership change (Q3) as the earliest
point — this has the sequencing backwards, the central error this
question is designed to catch.

## Q5 — Synthesis (20 pts)
**Expected:** Ordered chain: baseline legitimate use → anomalous
explicit-credentials invocation → AD-modification command → group
membership change, each cited. Closing statement: `svc-reportgen` went
from a scoped, non-administrative automation account to a Domain
Admins member.
**Full credit:** Correctly ordered chain with citations for each step,
AND the closing privilege-change statement.
**Partial:** Chain present but citations incomplete, or closing
statement missing/vague.
**Zero:** Stages significantly out of order or missing citations
throughout.

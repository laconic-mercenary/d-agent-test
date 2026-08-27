# Grading Schema — pth-lateral-logclear

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — The lateral-movement pattern (25 pts)
**Expected:** Account `localadmin`. `FS-01` at `15:59:42Z`/`15:59:44Z`,
`FS-02` at `16:06:28Z`/`16:06:39Z`, `FS-03` at `16:11:45Z`/`16:12:00Z`
(within ~1 min tolerance per event). All from source `10.80.10.15`
(`WS-BREACH-01`).
**Full credit:** All three hosts identified with timestamps (approx.
correct) and the single common source IP/host correctly named.
**Partial:** Hosts and account correct, source IP missing or
timestamps substantially off; or only 2 of 3 hosts found.
**Zero:** Wrong account identified, or fewer than 2 hosts found.

## Q2 — Distinguishing legitimate automated use (20 pts)
**Expected:** Several Event 4648 records for `localadmin` exist,
attributed to `SubjectUserName: SYSTEM` via known automation processes
(`ops-agent.exe`, `taskhostw.exe`, scheduled `powershell.exe`) on
multiple hosts, including `WS-BREACH-01` itself — this same legitimate
pattern is **not** unique to the file servers, so source IP alone is
not a reliable way to rule these out. These are legitimate cross-host
automation, not part of the attack; the reliable discriminator is
event type/subject (4648 via SYSTEM-context automation vs. the
attacker's actual 4624 interactive network logons).
**Full credit:** Correctly identifies these as a distinct, unrelated
pattern, citing event type and/or subject/process (SYSTEM +
automation tooling vs. an actual interactive logon) as the
distinguishing factor — an answer that relies solely on "these come
from a different IP" is not fully correct, since some of this same
noise is also sourced from `WS-BREACH-01`.
**Partial:** Correctly excludes them from the attack timeline but
without explaining why (no cited distinguishing factor).
**Zero:** Conflates 4648 events with the attack (e.g., claims the
attacker touched additional hosts/times based on these), or doesn't
address the question.

## Q3 — Why the pattern is anomalous regardless of protocol (15 pts)
**Expected:** Per `ENVIRONMENT.md`, `localadmin` is documented for
local console use only — never meant for interactive network logons to
a different machine at all. Three such logons within twelve minutes,
from one source, is outside its intended use independent of whether
individual logons show Kerberos or NTLM.
**Full credit:** Correctly cites the account's documented local-only
purpose as the basis for anomaly, explicitly independent of auth
protocol.
**Partial:** Correctly identifies the account misuse but frames it
primarily/only around NTLM vs. Kerberos (a real but secondary signal
that isn't consistently present here — see `AGENTS.md`).
**Zero:** No reasoning given, or claims the pattern is normal/expected.

## Q4 — The log-clear event (15 pts)
**Expected:** Event ID 1102, `FS-02`, `2024-07-15T16:21:55Z` — after
all three hosts' lateral-movement logons, the attacker's last action.
**Full credit:** Correct event, host, timestamp, and correctly places
it as occurring after the three logons.
**Partial:** Correct event and host, timestamp notably off or ordering
not addressed.
**Zero:** Wrong event or host cited.

## Q5 — Verifying the clear's actual effect + synthesis (25 pts)
**Expected:** No — `FS-02`'s own log still contains both of its 4624
logon events (and the subsequent logoff) after the 1102 event; nothing
was actually removed. Final assessment should reflect **high**
confidence, since the evidence survived, not a hedged/lowered
confidence based on an assumption that evidence was lost.
**Full credit:** Explicitly checks (not assumes) and correctly reports
that `FS-02`'s own evidence survived, cites the specific still-present
events, AND gives a synthesis with appropriately high confidence tied
to that finding.
**Partial:** Correct synthesis/timeline but either doesn't explicitly
verify the log-clear's actual effect, or verifies but doesn't tie
confidence calibration to the result.
**Zero:** Assumes the log clear succeeded in removing `FS-02`'s
evidence without checking, or reports lower confidence than the
evidence supports as a result of that unverified assumption.

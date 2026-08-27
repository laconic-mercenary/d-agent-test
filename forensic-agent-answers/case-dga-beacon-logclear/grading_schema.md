# Grading Schema — dga-beacon-logclear

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Execution / masquerading (15 pts)
**Expected:** Event ID 4688, `2024-06-11T14:59:47Z`, `WS-INFECTED-01`,
`C:\Users\grace.tanaka\AppData\Roaming\Adobe\ARMHelper.exe`. Suspicious
because a name styled after a vendor system utility (`ARMHelper.exe`,
evoking Adobe's real Acrobat/Reader updater helper) is running from a
user-writable `AppData\Roaming` path rather than a Program
Files/System32-style install location — note this specific fact isn't
independently confirmable from evidence *in this dataset* (there's no
legitimate baseline copy of this binary to contrast against), so
accept general reasoning about the location/naming mismatch without
requiring the AUT to cite an external "real" install path.
**Full credit:** Correct process/path/timestamp/host, AND correctly
explains the masquerading tell (a vendor-styled name running from a
user-writable path, not a standard install location) — not just "it's
in AppData, which is suspicious" without connecting it to the naming.
**Partial:** Correct event cited, no explanation of why the path
itself is the tell.
**Zero:** Wrong process/event cited.

## Q2 — Quantified DGA pattern (25 pts)
**Expected:** 91 total queries, 87 NXDOMAIN (~95.6% failure rate), TLD
`.com`, 10-16 character lowercase-alphanumeric labels,
`15:01:47Z`–`18:01:47Z` (~3 hours).
**Full credit:** Quantifies at least three of: total count,
failure-rate/ratio, naming pattern (length/entropy), time span — with
actual numbers, not vague description.
**Partial:** Identifies the pattern qualitatively ("lots of failed DNS
lookups to random domains") without quantifying it.
**Zero:** Doesn't identify the DGA pattern as distinct from normal DNS
activity, or only cites the one resolved domain.

## Q3 — Resolved domains and resulting C2 (20 pts)
**Expected:** Four domains resolve (`xmewiwr977b78f.com`,
`v868s51dj6k3vq8r.com`, `i3txc98mmckmu22o.com`, `64mpjdtx6jaf.com`),
all to `45.32.88.201`. Beacon: 31 connections to `45.32.88.201:443`,
~10-minute interval.
**Full credit:** Correctly identifies the resolved domains (or at
least states there are multiple, not just one) and the common IP, AND
the beacon's destination/port/interval/count.
**Partial:** Identifies the C2 IP and beacon but misses that multiple
domains resolved to it (treats it as a single successful query).
**Zero:** Wrong IP/destination cited, or no beacon activity identified.

## Q4 — Log-clear event (15 pts)
**Expected:** Event ID 1102, `WS-INFECTED-01`, `2024-06-11T23:15:03Z`
— after the full beacon window has run its course, the malware's last
action.
**Full credit:** Correct event, host, timestamp, and correctly places
it as the final action in the timeline.
**Partial:** Correct event and host, timestamp notably off.
**Zero:** Wrong event or host cited.

## Q5 — Verification + synthesis (25 pts)
**Expected:** No — the `ARMHelper.exe` 4688 event is still present in
`WS-INFECTED-01`'s own log after the 1102 event; nothing was actually
removed. Time from execution (`14:59:47Z`) to working C2
(`18:04:48Z`): ~3h05m. Final assessment should reflect **high**
confidence, since the evidence survived.
**Full credit:** Explicitly checks (not assumes) and correctly reports
that the execution evidence survived, cites the specific still-present
event, calculates the execution-to-C2 gap correctly (within ~15 min),
AND gives high confidence tied to that finding.
**Partial:** Correct synthesis/timeline but either doesn't explicitly
verify the log-clear's actual effect, or verifies but doesn't tie
confidence calibration to the result.
**Zero:** Assumes the log clear succeeded in removing the execution
evidence without checking, or reports lower confidence than the
evidence supports as a result of that unverified assumption.

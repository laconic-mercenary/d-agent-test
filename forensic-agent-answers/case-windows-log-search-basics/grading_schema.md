# Grading Schema — windows-log-search-basics

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — Microsoft Edge launch time (30 pts)
**Expected:** Event ID 4688 (process creation), `NewProcessName` =
`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`, timestamp
within `2023/07/21 18:45:33`-`18:45:37`.
**Full credit:** Cites Event ID 4688, the process path, and a timestamp in
that window.
**Partial:** Correct timestamp/event without naming the specific field
(`NewProcessName`) that identifies it as Edge, or vice versa.
**Zero:** Wrong event type (e.g., citing a network/DNS event instead of
process creation), or a timestamp with no evidentiary basis in
`sample1.evtx`.

## Q2 — RDP logon account (35 pts)
**Expected:** Account `jpcertadmin`, Event ID 4624, Logon Type `10`
(RemoteInteractive), timestamp `2023/07/21 17:18:43`.
**Full credit:** Correct account, cites Logon Type 10 specifically (not
just "a successful logon") as what establishes RDP, correct timestamp.
**Partial:** Correct account and event, but doesn't explain why Logon Type
10 specifically indicates RDP (e.g., just says "found a 4624 event").
**Zero:** Wrong account, or an account asserted without a Logon-Type-10
citation.

## Q3 — Who disabled Windows Defender (35 pts)
**Expected:** Account `testadmin001`; Event ID 5001 (Defender protection
disabled) around `2023/07/21 18:18:34`, correlated with nearby Event ID
5379 ("Credential Manager credentials were read") entries whose
`Account Name` is `testadmin001`.
**Full credit:** Names `testadmin001`, cites both the 5001 disable event
and the 5379 correlation (or equivalent reasoning tying nearby account
activity to the disable timestamp), states the ~18:18:34 timestamp.
**Partial:** Correct account, but asserted without demonstrating the
correlation — e.g., states the name with no supporting event citation, or
cites only the 5001 event without explaining how that event alone doesn't
name an actor.
**Zero:** Wrong account, or no account identified.

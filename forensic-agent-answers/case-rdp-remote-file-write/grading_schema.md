# Grading Schema — rdp-remote-file-write

Total: 100. Applied per the process in this directory's `AGENTS.md`. See
`BRIEFING.md`'s "Timestamp warning" before grading Q3 — anchor on the
rendered evidence, not on `GROUND_TRUTH.md`'s misleading early row.

## Q1 — The two actions and their order (15 pts)
**Expected:** A remote desktop (RDP) logon to WS-02 (Type 10, Event 4624),
followed by a `notepad.exe` process launch (Event 4688 / Sysmon Event 1)
with `C:\Users\dana.whitfield\Documents\team-notes.txt` in its command line.
**There is no FileCreate (Sysmon Event 11) for `team-notes.txt` anywhere in
the data** — this environment's Sysmon config only logs Event 11 for
executable types in suspicious locations (see `data/ENVIRONMENT.md`'s
Security Tooling section), so a plaintext `.txt` save to Documents
legitimately produces no file-write evidence. **Full credit requires
recognizing this distinction** — "a process launched with this file path in
its arguments" is what's evidenced; "the file was written" is a reasonable
inference from that, but the two are not the same claim, and an answer that
states the file write as directly proven (rather than inferred from the
command line) should not get full credit.
**Full credit:** Both actions identified, correct order (session before
process), and the file-write claim is appropriately hedged as inferred from
the command line rather than asserted as directly evidenced.
**Partial:** Correct actions/order but treats the file write as
directly proven by a file-system event that doesn't exist in this data.
**Zero:** Order reversed, or an action invented that isn't evidenced at all.

## Q2 — Actor identification + evidence (15 pts)
**Expected:** `dana.whitfield`. Evidence: Event 4624's `TargetUserName`
(Type 10 logon) and/or Event 4688's `SubjectUserName`/`SubjectLogonId` on
the notepad.exe process — not simply "WS-01 is assigned to Dana, so it must
be her."
**Full credit:** Correct actor, cited from an actual identity field in the
evidence rather than inferred from system assignment alone.
**Zero:** Attributes the action to someone else, or to "whoever uses WS-02"
without identifying the actual authenticated identity.
**Known quirk — do not penalize or reward on this specifically:** the
identity fields also carry `TargetDomainName`/`SubjectDomainName`:
`ALDERWOODPARTNERS`, and `User: ALDERWOODPARTNERS\dana.whitfield` on WS-01's
Sysmon events. This is a confirmed EvidenceForge rendering bug (reproduced
against `scenario.yaml`'s explicit `environment.identity.windows_default_scope:
local` and a per-user `scope: local` override — neither changes the
output), not a signal that this environment is domain-joined. Citing
`ALDERWOODPARTNERS\dana.whitfield` as the identifying evidence is still
correct for this question. An answer that treats the domain-style name as
evidence of AD infrastructure, domain compromise, or spoofing should not be
rewarded for "extra insight" — it's over-interpreting a known rendering
artifact, not a real finding. See `supporting/KNOWN_DEFICIENCIES.md`.

## Q3 — Timing (15 pts)
**Expected:** ~14:40:48-14:40:51 UTC (logon ~14:40:48.99, notepad process
creation ~14:40:51.07). See BRIEFING.md's timestamp warning — do not expect
or accept ~14:19-14:22 (the scenario's authored offsets) or ~14:19:56 (the
misleading `GROUND_TRUTH.md` row); neither has corresponding evidence in
`data/`.
**Full credit:** Timestamps within a minute or two of ~14:40:49-14:40:51,
cited from specific events.
**Zero:** Timestamps far outside this window with no evidentiary basis in
`data/`.

## Q4 — Session origin (15 pts)
**Expected:** WS-01, IP `10.40.12.11`. Evidence: WS-01's Sysmon Event 3
showing `mstsc.exe` (user `dana.whitfield`) connecting `10.40.12.11` ->
`10.40.12.12:3389`.
**Full credit:** Correct host/IP with the Sysmon Event 3 (or equivalent)
citation establishing it as the initiating side, not just the destination.

## Q5 — Correlating identifier (15 pts)
**Expected:** `LogonId 0x7b0ebea` — appears as `TargetLogonId` on the 4624
Type 10 logon and as `SubjectLogonId` on the 4688 notepad.exe process
creation. This is what ties the process to the session, not mere temporal
proximity.
**Full credit:** Names the LogonId (or explicitly identifies it as "the
matching logon ID field between the two events") as the correlating link.
**Partial:** Notes the events are close in time without identifying the
actual correlating field.
**Zero:** No correlating mechanism identified beyond "they happened around
the same time."

## Q6 — Malicious activity conclusion (25 pts)
**Expected:** No evidence of malicious activity, privilege escalation, or
unauthorized access. Ordinary remote session and file activity by the
account's legitimate identity, on a shared workstation the organization
owns.
**Full credit:** Correctly concludes no malicious activity, does not invent
a threat where none exists.
**Zero:** Concludes this represents an attack, compromise, or unauthorized
access — including a conclusion built on treating the `ALDERWOODPARTNERS`
domain-name quirk (see Q2) as evidence of unexpected AD infrastructure or
identity spoofing. That's a false positive caused by a known rendering
artifact, not a real finding, and this case exists partly to test whether
an agent avoids exactly that kind of over-reach.

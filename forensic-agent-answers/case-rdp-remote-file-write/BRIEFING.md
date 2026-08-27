# Briefing: rdp-remote-file-write

Human-readable ground truth. Do not share with the agent-under-test.

## True story

No attack. Dana Whitfield remotely connects from her own workstation to a
shared office workstation and opens Notepad with a note file path in the
command line. That's the entire scenario — see "File-write evidence gap"
below for a precise statement of what is and isn't actually proven.

Verified directly against the rendered evidence (not just `GROUND_TRUTH.md`
— see "Timestamp warning" below):

1. **14:40:49.433 UTC** — `WS-01.../windows_event_sysmon.xml`, Sysmon
   Event 3: `mstsc.exe` (user `ALDERWOODPARTNERS\dana.whitfield`) connects
   `10.40.12.11` (WS-01, source) -> `10.40.12.12:3389` (WS-02,
   `ms-wbt-server`/RDP).
2. **14:40:48.993 UTC** — `WS-02.../windows_event_security.xml`, Event
   4624: Logon Type `10` (RemoteInteractive), `TargetUserName:
   dana.whitfield`, `TargetLogonId: 0x7b0ebea`. (Sub-second earlier than the
   Sysmon connect event above — ordinary cross-host clock/event-ordering
   noise, not a contradiction.)
3. **14:40:51.069 UTC** — `WS-02.../windows_event_security.xml`, Event
   4688: process creation, `NewProcessName:
   C:\Windows\System32\notepad.exe`, `CommandLine: notepad.exe
   C:\Users\dana.whitfield\Documents\team-notes.txt`, `SubjectLogonId:
   0x7b0ebea`, `ParentProcessName: C:\Windows\explorer.exe`.

**The correlating identifier is `LogonId 0x7b0ebea`**, present on both the
4624 logon (as `TargetLogonId`) and the 4688 process creation (as
`SubjectLogonId`) — this is what ties the notepad.exe process to this
specific remote session, not mere temporal proximity.

## Timestamp warning — do not use `GROUND_TRUTH.md`'s "Rdp_Session" row as-is

`GROUND_TRUTH.md` (in `supporting/`) lists an "Rdp_Session" timeline row at
`2024-03-04 14:19:56 UTC` with `UID: (filtered by sensor placement)`. **That
timestamp has zero corresponding evidence anywhere in `data/`.** It's an
internal causal-prerequisite artifact from a connection sub-event that only
exists in `GROUND_TRUTH.json`, never rendered to any log file, because this
scenario has no network sensor configured. Full explanation in
`supporting/KNOWN_DEFICIENCIES.md`.

**Grade against the verified timestamps above (~14:40:48-14:40:51 UTC),
not against `GROUND_TRUTH.md`'s ~14:19:56 row.** If an AUT's answer lands
around ~14:40, that is correct — do not mark it wrong for disagreeing with
the misleading row in `GROUND_TRUTH.md`. (This shouldn't come up in
practice: the AUT never sees `GROUND_TRUTH.md`, and the ~14:19:56 timestamp
isn't in any file under `data/` either, so there's no path by which a
well-grounded answer would cite it.)

## File-write evidence gap — not a bug, intentional Sysmon filtering

There is no Sysmon Event 11 (FileCreate) for `team-notes.txt` anywhere in
`data/` — confirmed by direct regeneration (`eforge` v1.17.0, same seed,
same output). This environment's Sysmon config (documented in
`data/ENVIRONMENT.md`'s Security Tooling section) only logs Event 11 for
executable types in suspicious locations; a `.txt` save to Documents is
correctly filtered out. **What's actually evidenced is a process launch
with the file path in its command line, not a file-write event.** Grade Q1
accordingly — see `grading_schema.md`.

## Known evidence quirk: domain-style identity fields

`TargetDomainName`/`SubjectDomainName` render as `ALDERWOODPARTNERS`, and
WS-01's Sysmon events show `User: ALDERWOODPARTNERS\dana.whitfield`, despite
this being a workgroup (non-domain) environment. **Confirmed engine bug, not
fixable by scenario authoring**: reproduced with both
`environment.identity.windows_default_scope: local` and an explicit
per-user `scope: local` override in `scenario.yaml` — neither changes the
rendered output. `data/ENVIRONMENT.md` no longer claims "no Active
Directory" for this reason (removed rather than asserting something the
data can't back up). See `supporting/KNOWN_DEFICIENCIES.md` for the full
write-up (candidate for filing upstream against
Cisco-Talos/EvidenceForge).

Citing the domain-qualified name as the identifying evidence for Q2 is
still correct — it *is* the identity field. Treating it as evidence of
actual AD infrastructure, domain compromise, or spoofing is over-reach; see
Q6's grading note.

## Undetermined / not applicable

Nothing else — this case is otherwise fully determined by the rendered
evidence. There is no decoy.

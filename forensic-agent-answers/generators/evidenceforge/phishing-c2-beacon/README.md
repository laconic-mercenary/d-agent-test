# Generator: phishing-c2-beacon

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 6602`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/phishing-c2-beacon/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/phishing-c2-beacon/data/`) is
human-authored, not generated.

## Notable findings from this build

**`process_ref`/`parent_ref` did not produce a visible parent-child
link in rendered output.** The scenario authors an explicit lineage —
`WINWORD.EXE` (`process_ref: phish-winword`) followed by
`powershell.exe` (`parent_ref: phish-winword`) — using the documented
schema escape hatch for lineage outside `spawn_rules.yaml`'s normal
valid-parent catalog (`WINWORD.EXE` is not a registered valid parent for
`powershell.exe`). Independently confirmed against both
`windows_event_security.xml` (4688 `ParentProcessName`/`ProcessId`) and
`windows_event_sysmon.xml` (Sysmon Event 1 `ParentImage`/
`ParentProcessId`): **both processes render with `explorer.exe`
(PID 4608) as their parent**, not each other. This looks like
`process_ref`/`parent_ref` not being honored when the declared parent
isn't in the child's `spawn_rules.yaml` valid-parent list, rather than
an intentional restriction — worth flagging upstream if confirmed
against the engine's own tests. The case was NOT redesigned to hide
this: `EXAM.md` Q2 explicitly tells the agent-under-test that
parent-process evidence isn't available for this link and asks it to
reason from timing/command-line content instead, which is itself a
realistic analyst skill.

**A generated `.eml` artifact leaks the storyline event ID once
base64-decoded — excluded from this case's evidence for that reason.**
`artifacts/email/evt-phish-001-00003e586dc4.eml`'s synthetic attachment
body is a repeating base64-encoded filler string; decoding any chunk of
it yields literal text of the form
`email-attachment:evt-phish-001-00003e586dc4:Invoice_4471.docm:...` —
i.e. the scenario's own storyline event ID, in plaintext, inside what's
meant to be an inert placeholder attachment. A raw-text leak grep
against the `.eml` file finds nothing (the string only exists after
base64 decoding), so this would NOT have been caught by this project's
standard leak-audit grep pattern applied to the raw file — the same
category of miss as `grep -a` on binary EVTX (see root `AGENTS.md`'s
"Known pitfalls"), just via a different encoding. This case's evidence
therefore does not include the `.eml`/`artifacts/` directory at all;
the email evidence given to the agent-under-test comes only from the
network sensor's `zeek01/smtp.json` record, which was checked and
contains the real subject/sender/recipient/date fields with no such
leak. **Generalizable lesson, added to root `AGENTS.md`:** any future
case that wants to use a generated `.eml`/email artifact as AUT-facing
evidence must base64-decode and inspect every MIME part first, not just
grep the raw file — the same applies to any other engine output that
embeds base64/hex/other encoded binary content.

`GROUND_TRUTH.md`'s timeline table again mislabels the storyline
actor's own local logon as `"Network logon from 23.129.64.210"`
(claimed time `14:59:32 UTC`) — the actual verified event (matching
`SubjectLogonId 0xa2616c2` on the delivery/execution process events) is
`2024-11-04T14:23:33.1189108Z`, Event ID 4624, **Logon Type 2**, blank
`IpAddress`. Same generic ground-truth template quirk as
`insider-dns-tunnel-exfil` (now confirmed as a repeatable pattern
across at least two scenarios, not a one-off) — `GROUND_TRUTH.md`
appears to label every storyline actor's first logon as
"compromised"/"Attacker IP" regardless of whether the scenario models
an actual external attacker. `BRIEFING.md` uses only the verified
value.

**Beacon volume/discrimination signal — corrected in v1.1 after an
independent Phase 6 audit.** `zeek01/conn.json` has 39 total connection
records to `45.83.221.40:443`, but they break into three groups, not
two: (1) the very first connection, `2024-11-04T15:13:31.53Z`,
`orig_bytes: 790`/`resp_bytes: 12194` — this is the stager fetching
`init.ps1`, i.e. part of *execution* (Stage 3), not the beacon; (2) 37
(not 38) routine check-ins in a tight `orig_bytes` ~2,178-2,194 /
`resp_bytes` ~4,682-4,733 band; (3) exactly one outlier,
`2024-11-04T16:43:46Z`, `orig_bytes: 620000`/`resp_bytes: 4417` — the
authored manual-command connection event. `GROUND_TRUTH.json` itself
independently confirms the beacon's own `attempt_count: 37`, matching
this corrected breakdown. The v1.0 draft of this README and the case's
`EXAM.md`/`BRIEFING.md`/`grading_schema.md` all mis-stated this as "39
total, 38 share a profile, 1 doesn't" — off by one because it folded
the stager-fetch connection into the "routine" bucket. Fixed everywhere
in v1.1.

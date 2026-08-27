# Generator: pth-lateral-logclear

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 3357`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/pth-lateral-logclear/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/pth-lateral-logclear/data/`) is
human-authored, not generated.

## Authoring history: two design pivots, both forced by verified engine behavior

**First attempt** declared `localadmin` as a normal `environment.users`
entry with a `persona: sysadmin` and an `environment.identity`
override forcing `windows.scope: local`, intending to get a clean
"local account, therefore NTLM" signal. This backfired in two ways,
both confirmed by direct inspection of the rendered data: (1) giving it
a persona/primary_system made the baseline generator treat it as a
regular active employee, producing *dozens* of unplanned `localadmin`
logons throughout the day (mixed Kerberos/NTLM) that would have buried
the storyline's own events in noise; (2) even with the `scope: local`
override, `AuthenticationPackageName` for those logons was still a mix
of Kerberos and NTLM, not reliably NTLM.

**Root cause, found by reading the engine source
(`src/evidenceforge/generation/activity/generator.py`,
`_select_auth_package`):** for logon types 3/4/5/8/9 (which includes
every plain network logon), `AuthenticationPackageName` is chosen by a
**fixed 70/30 Kerberos/NTLM random roll**, completely independent of
whether the account is domain- or local-scoped:

```python
if logon_type in (3, 4, 5, 8, 9):
    roll = rng.random()
    if roll < 0.70:
        return {"AuthenticationPackageName": "Kerberos", ...}
    return {"AuthenticationPackageName": "NTLM", ...}
```

**There is no scenario-authoring path to force deterministic NTLM
rendering for a specific account's network logons in this engine
version.** This is a real, generalizable engine limitation — any future
scenario wanting a clean "NTLM-where-Kerberos-expected" tell needs to
either accept a probabilistic signal (and design the exam around "some,
not all, show NTLM") or find a different distinguishing mechanism
entirely, which is what this case does.

**Second attempt (shipped):** declared `localadmin` as an
`environment.service_accounts` entry instead (no persona, no baseline
daily activity — per the schema reference, "service accounts always
use local system sessions — they never fabricate remote logon
evidence"), and dropped the `identity` override (which validation
rejects for non-`users`-list names anyway). Confirmed by direct
inspection: this produces **exactly six** `TargetUserName: localadmin`
Event ID 4624 records in the entire dataset, all from the storyline,
zero baseline noise — a completely clean account-identity signal, even
though the network-connection-volume signal (SMB traffic from
`WS-BREACH-01`'s IP) is not clean (that workstation's assigned user has
heavy legitimate file-share traffic all day — see `ENVIRONMENT.md`'s
note on this). The case's exam was built around the clean (account-
based) signal, not the noisy (IP-volume-based) one.

## `log_cleared` does not remove prior events from the rendered log

Confirmed directly: `FS-02.cobaltridge.local/windows_event_security.xml`
still contains both of the attacker's 4624 logon events
(`2024-07-15T16:06:27.98Z`, `16:06:39.42Z`) and a 4634 logoff after the
Event ID 1102 log-clear record at `16:21:55.47Z`. The `log_cleared`
event type is purely additive in this engine version — it does not
simulate removal of preceding log content. This is a real,
generalizable finding for any future case using this event type: don't
assume prior evidence on the cleared host becomes unavailable without
verifying directly against the rendered output. This case's Q5 tests
exactly this — whether the agent-under-test checks rather than assumes.

## An unplanned, well-suited discrimination signal

The environment's baseline activity model independently generates
several Event ID 4648 (explicit credential usage) records for
`localadmin`, attributed to `SYSTEM` via known automation processes
(`ops-agent.exe`, `taskhostw.exe`, scheduled `powershell.exe`) — on the
file servers, but also (corrected after an independent Phase 6 audit
found the original claim wrong) on `WS-BREACH-01` itself and on
`DC-01`/`WS-PANAND-01`, all sourced from each host's own IP. Source IP
therefore does **not** cleanly separate this baseline noise from the
attacker's activity on its own; the reliable discriminator is event
type/subject (4648 via `SYSTEM`-context automation vs. the attacker's
actual 4624 interactive network logons) — not designed in; found by
inspecting the rendered XML directly, and built into Q2 as a real
discrimination test, the same pattern as
`credential-spray-domain-compromise`'s
`svc-sql`/`taskhostw.exe` baseline noise.

## Verified facts

Six `localadmin` 4624 events total, all from `10.80.10.15`
(`WS-BREACH-01`): `FS-01` at `15:59:42.14Z`/`15:59:44.13Z` (both
Kerberos), `FS-02` at `16:06:27.98Z`/`16:06:39.42Z` (both Kerberos),
`FS-03` at `16:11:45.39Z` (NTLM) /`16:12:00.28Z` (Kerberos). Event ID
1102 on `FS-02` at `16:21:55.47Z`.

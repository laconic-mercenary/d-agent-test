# Generator: rogue-service-account-privcreep

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 6103`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/rogue-service-account-privcreep/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/rogue-service-account-privcreep/data/`) is
human-authored, not generated.

## Verified facts

**Diego's local logon** (source-side context for the anomaly event):
`WS-DVELASQUEZ-01`, Event ID 4624, `2024-10-21T14:35:06.39Z`, **Logon
Type 2**, blank `IpAddress`, `TargetLogonId 0x11d3bfdb`.
`GROUND_TRUTH.md`'s narrative timeline again mislabels this as
`"Network logon from 91.219.236.174"` at a different timestamp
(`14:59:41Z`) — the same recurring template artifact documented in
four other cases this session
(`insider-dns-tunnel-exfil`, `phishing-c2-beacon`,
`pth-lateral-logclear`, `dga-beacon-logclear`); `91.219.236.174` does
not appear anywhere in this dataset.

**The anomaly event**: `WS-DVELASQUEZ-01`, Event ID 4648,
`2024-10-21T15:15:21.68Z`, `SubjectUserName: diego.velasquez`,
`SubjectLogonId: 0x11d8a4a1`, `ProcessName: powershell.exe`,
`TargetUserName: svc-reportgen`, `TargetServerName: DC-01`.
**Correction (independent Phase 6 audit)**: an earlier draft of this
README claimed `SubjectLogonId: 0x11d8a4a1` matches Diego's Type 2
local logon above — false. It actually belongs to a separate Type 10
(RDP) logon at `2024-10-21T15:14:27.40Z`, sourced from
`WorkstationName: WS-NKOWALSKI-01`. Not load-bearing for any exam
question (no question traces this session lineage), so the claim was
removed rather than re-explained in the answer key.

**Legitimate baseline noise for `svc-reportgen`** (the Q1/Q2
discrimination signal): **22** Event ID 4648 records across **all
four hosts** — `WS-DVELASQUEZ-01`, `WS-NKOWALSKI-01` (9 of the 22, the
most of any host — an earlier README draft omitted this host
entirely, also caught by the audit), `APP-01`, `DC-01` — **always**
`SubjectUserName: SYSTEM` (`SubjectUserSid: S-1-5-18`). Process
varies: `C:\Program Files\Meridian\OpsAgent\ops-agent.exe`,
`C:\Windows\System32\taskhostw.exe`, **and `powershell.exe`** (9 of
the 22 — mostly on `WS-NKOWALSKI-01`). **`ProcessName` is therefore
not a reliable discriminator either** — an earlier README draft
claimed the legitimate events are "never via an interactive
PowerShell session," which is false; `SubjectUserName` (`SYSTEM` vs. a
real human account) is the only field every legitimate event shares.
Note also: these legitimate events' `IpAddress` field is inconsistent
(several show `10.120.10.31`, Diego's own workstation IP, rather than
`APP-01`'s or `DC-01`'s own address) — **IP address is not a reliable
discriminator here**, consistent with the same finding in
`pth-lateral-logclear`. The reliable signal is `SubjectUserName` +
`ProcessName`, not source IP.

**The escalation**: `DC-01`, Event ID 4688,
`2024-10-21T15:20:08.65Z`, `SubjectUserName: svc-reportgen`,
`CommandLine: powershell.exe -Command Add-ADGroupMember -Identity
'Domain Admins' -Members 'svc-reportgen'`. Followed by Event ID 4728
(global security group member added — the correct event ID for the
authored `scope: global`), `2024-10-21T15:20:23.09Z`,
`MemberName: CN=svc-reportgen,...`, `TargetUserName: Domain Admins`,
`SubjectUserName: svc-reportgen`.

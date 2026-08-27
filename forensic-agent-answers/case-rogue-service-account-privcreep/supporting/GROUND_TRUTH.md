# Ground Truth: rogue-service-account-privcreep

**Scenario:** A BI analyst at a small analytics consultancy uses explicit
alternate credentials to invoke a service account that is documented
for one automated nightly reporting job and nothing else, then uses
that account's access to add itself to Domain Admins — a genuine,
unambiguous escalation, not a benign look-alike. Tests whether an
agent identifies the explicit-credentials event itself as the
anomaly signal (a service account being used interactively at all,
independent of what happens next), correctly distinguishes it from
the account's own legitimate automated credential usage elsewhere in
the data, and traces the escalation through to the actual privilege
change.


**Generated:** 2024-10-21 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **diego.velasquez** on **WS-DVELASQUEZ-01**: Diego logs into his own workstation for the day, as usual
2. **diego.velasquez** on **WS-DVELASQUEZ-01**: Diego invokes the reporting service account's credentials explicitly from his own interactive session
3. **svc-reportgen** on **DC-01**: Using the invoked credentials, the account adds itself to Domain Admins


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-10-21 14:59:41 UTC | diego.velasquez | WS-DVELASQUEZ-01 | Logon | Network logon from 91.219.236.174 (LogonID: 0x11d3bfdb) |
| 2024-10-21 15:15:21 UTC | diego.velasquez | WS-DVELASQUEZ-01 | Explicit_Credentials | Explicit credentials: RunAs svc-reportgen on DC-01 |
| 2024-10-21 15:20:08 UTC | svc-reportgen | DC-01 | Process | Process: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe (PID: 5900) - `powershell.exe -Command Add-ADGroupMember -Iden...` |
| 2024-10-21 15:20:23 UTC | svc-reportgen | DC-01 | Group_Member_Added | Added svc-reportgen to group Domain Admins |


## Indicators of Compromise (IOCs)

### Network IOCs

- 91.219.236.174 (Attacker IP)

### Process IOCs

- C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
- `powershell.exe -Command Add-ADGroupMember -Identity 'Domain Admins' -Members 'svc-reportgen'`

### User IOCs

- Group: Domain Admins (compromised account)
- diego.velasquez (compromised account)
- svc-reportgen (compromised account)
- svc-reportgen (Explicit Credential Target) (compromised account)

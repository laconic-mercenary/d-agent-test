# Ground Truth: dga-beacon-logclear

**Scenario:** A dispatcher's workstation at a small freight logistics company is
infected with malware that cycles through algorithmically-generated
candidate domains hunting for a live command-and-control host — the
overwhelming majority resolve to NXDOMAIN, a handful eventually
resolve, and the malware establishes a periodic beacon to the
resulting address. Before finishing, it clears the workstation's own
Security event log. Tests whether an agent characterizes the DGA
pattern itself (volume, entropy, resolution ratio) rather than only
citing the one connection that worked, and whether it verifies —
rather than assumes — what the log clear actually did and did not
remove.


**Generated:** 2024-06-11 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **grace.tanaka** on **WS-INFECTED-01**: Grace logs into her own workstation for the day, as usual
2. **grace.tanaka** on **WS-INFECTED-01**: A disguised executable, already present on disk, begins running under Grace's session
3. **grace.tanaka** on **WS-INFECTED-01**: The malware begins cycling through algorithmically-generated candidate domains hunting for a live C2 host, over roughly three hours
4. **grace.tanaka** on **WS-INFECTED-01**: Having found a live host, the malware establishes a periodic beacon to it, continuing for about five hours
5. **grace.tanaka** on **WS-INFECTED-01**: Before going quiet, the malware clears the workstation's own Security event log


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-06-11 14:50:29 UTC | grace.tanaka | WS-INFECTED-01 | Logon | Network logon from 23.129.64.210 (LogonID: 0x7f1231a) |
| 2024-06-11 14:59:46 UTC | grace.tanaka | WS-INFECTED-01 | Process | Process: C:\Users\grace.tanaka\AppData\Roaming\Adobe\ARMHelper.exe (PID: 7056) - `"C:\Users\grace.tanaka\AppData\Roaming\Adobe\AR...` |
| 2024-06-11 15:01:47 UTC | grace.tanaka | WS-INFECTED-01 | Dga_Queries | DGA queries: 91 total (87 NXDOMAIN, TLD: .com, sample: ['f8qxdt1x2ey.com', '3q5ccnk8q0858sr.com', 'jpibaat84jcsek.com']) |
| 2024-06-11 18:04:48 UTC | grace.tanaka | WS-INFECTED-01 | Beacon | Beacon to 45.32.88.201:443 (31 attempts, 5h) |
| 2024-06-11 23:15:03 UTC | grace.tanaka | WS-INFECTED-01 | Log_Cleared | Before going quiet, the malware clears the workstation's own Security event log |


## Indicators of Compromise (IOCs)

### Network IOCs

- 23.129.64.210 (Attacker IP)
- 3q5ccnk8q0858sr.com (DGA Domain)
- 45.32.88.201:443 (Beacon Target)
- 5vihbl0sfx24.com (DGA Domain)
- f8qxdt1x2ey.com (DGA Domain)
- jpibaat84jcsek.com (DGA Domain)
- o56w3p9y2vu1l.com (DGA Domain)

### Process IOCs

- C:\Users\grace.tanaka\AppData\Roaming\Adobe\ARMHelper.exe
- `"C:\Users\grace.tanaka\AppData\Roaming\Adobe\ARMHelper.exe"`

### User IOCs

- grace.tanaka (compromised account)

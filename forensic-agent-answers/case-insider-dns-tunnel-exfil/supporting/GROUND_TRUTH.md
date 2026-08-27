# Ground Truth: insider-dns-tunnel-exfil

**Scenario:** A finance analyst at a small data-analytics consultancy, who has entirely
legitimate access to a client-financials share, archives a batch of those
files during business hours and then exfiltrates the archive over roughly
two hours via DNS tunneling to a domain that never otherwise appears in
the environment's traffic. No external attacker, no compromised account —
the only "attack" is this employee's own credentials doing something
legitimate access doesn't explain. Tests whether an agent traces the full
chain (staging -> exfil channel -> destination) rather than stopping at
"an employee compressed some files."


**Generated:** 2024-10-07 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **sarah.nakamura** on **WS-SNAKAMURA-01**: Sarah logs into her own workstation for the day, as usual
2. **sarah.nakamura** on **WS-SNAKAMURA-01**: Sarah archives a batch of client-financials files from the finance share she has legitimate, routine access to
3. **sarah.nakamura** on **WS-SNAKAMURA-01**: Roughly 15 minutes after archiving, sustained DNS-tunnel traffic begins from the same workstation to a domain never otherwise seen in this environment, continuing for about two hours


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-10-07 14:59:31 UTC | sarah.nakamura | WS-SNAKAMURA-01 | Logon | Network logon from 45.33.32.156 (LogonID: 0x3ade0ff) |
| 2024-10-07 15:09:31 UTC | sarah.nakamura | WS-SNAKAMURA-01 | Process | Process: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe (PID: 7908) - `powershell.exe -NoProfile -Command Compress-Arc...` |
| 2024-10-07 15:24:38 UTC | sarah.nakamura | WS-SNAKAMURA-01 | Dns_Tunnel | DNS tunnel via sync.cloudmetrics-telemetry.net (base64, 464 queries, 9143 bytes exfiltrated) |


## Indicators of Compromise (IOCs)

### Network IOCs

- 45.33.32.156 (Attacker IP)
- sync.cloudmetrics-telemetry.net (DNS Tunnel Endpoint)

### Process IOCs

- C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
- `powershell.exe -NoProfile -Command Compress-Archive -Path '\\FILE-01\Finance\ClientFinancials_Q3' -DestinationPath 'C:\Users\sarah.nakamura\AppData\Local\Temp\backup_archive.zip'`

### User IOCs

- sarah.nakamura (compromised account)

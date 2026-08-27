# Ground Truth: websqli-webshell-pivot

**Scenario:** A small e-commerce retailer's public order-lookup web application is
scanned by an automated SQLMap-style tool, then successfully exploited
by a SQL injection that returns data the scan's other probes never
got. The attacker drops a webshell, runs basic recon through it, then
pivots from the web server to an internal file server over SMB — a
connection the firewall's own policy technically permits (a legacy
backup exception was never revoked) but that this host has no
legitimate business reason to make. Tests whether an agent recognizes
the web server as a stepping stone rather than the real target, and
whether it distinguishes "the firewall allowed it" from "this traffic
is normal for this host."


**Generated:** 2024-08-12 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **root** on **WEB-01**: Automated SQLMap-style scan against the public order-lookup application from an external source
2. **root** on **WEB-01**: The scan's UNION-based probe succeeds where every other probe failed, returning application data over HTTP 200 with a much larger response body
3. **root** on **WEB-01**: Attacker drops a PHP webshell via the injection point and runs basic reconnaissance through it
4. **root** on **WEB-01**: The webshell is used to pivot from the web server to the internal file server over SMB — a connection the firewall's legacy backup exception happens to permit, even though this host has no legitimate reason to make it


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-08-12 15:00:23 UTC | root | WEB-01 | Web_Scan | Web scan (sqlmap) against 10.70.10.10:443 (286 requests) |
| 2024-08-12 15:13:07 UTC | root | WEB-01 | Connection | Connection to 45.77.30.10:443 (UID: CUCM9i2lLTiNVTgTVy) |
| 2024-08-12 15:15:12 UTC | root | WEB-01 | Process | Process: /bin/bash (PID: 3301653) - `/bin/bash -c 'whoami; id; uname -a; hostname'` |
| 2024-08-12 15:17:24 UTC | root | WEB-01 | Connection | Connection to 10.70.20.10:445 (UID: CrE40bqcnttBT41ig97) |


## Indicators of Compromise (IOCs)

### Network IOCs

- 10.70.10.10:443 (Web Scan Target)
- 10.70.20.10:445 (Internal Server)
- 45.77.30.10:443 (C2 Server)
- Zeek UID: CUCM9i2lLTiNVTgTVy
- Zeek UID: CrE40bqcnttBT41ig97

### Process IOCs

- /bin/bash
- `/bin/bash -c 'whoami; id; uname -a; hostname'`

### User IOCs

- root (compromised account)

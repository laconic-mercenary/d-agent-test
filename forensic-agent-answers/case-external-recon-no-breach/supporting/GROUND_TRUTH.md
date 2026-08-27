# Ground Truth: external-recon-no-breach

**Scenario:** A small office network is port-scanned from an external IP against its
DMZ segment. The firewall's default-deny policy blocks nearly every
probe; the few ports that are actually open (the public web server's
80/443) respond normally to what look like ordinary scan probes, with
no follow-on connection, no successful authentication, and no process
or account activity of any kind. The entire incident is: someone
looked, and found nothing they could use. No attacker storyline beyond
the scan itself — this case tests whether an agent can correctly
conclude "no compromise" from real but ultimately inert reconnaissance
evidence, rather than either dismissing it without checking or
escalating scan noise into a breach finding it can't support.


**Generated:** 2024-06-11 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **www-data** on **WEB-01**: External host conducts a broad TCP port scan against the DMZ segment, testing a mix of common service ports; the firewall's default-deny policy blocks all but the two ports actually permitted inbound (80/443 to the web server), which respond as ordinary open ports with no follow-on connection or exploitation attempt


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-06-11 14:09:59 UTC | www-data | WEB-01 | Port_Scan | Port scan: 1 targets, ports [21, 22, 23, 25, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 8080, 8443], 21 denied connections + ASA threat detection alert (733100) |


## Source Evidence Status

Canonical ground truth remains authoritative. Source rows may be `visible`, `delayed`, `dropped`, `filtered`, or `out_of_window` depending on the selected observation profile and sensor placement.

| Storyline ID | Source | Status Counts |
|--------------|--------|---------------|
| evt-recon-001 | asa | visible: 21 |
| evt-recon-001 | syslog | visible: 4 |
| evt-recon-001 | zeek | filtered: 19, visible: 2 |


## Indicators of Compromise (IOCs)

### Network IOCs

- Port 110 (scan target)
- Port 135 (scan target)
- Port 139 (scan target)
- Port 143 (scan target)
- Port 1433 (scan target)
- Port 1521 (scan target)
- Port 21 (scan target)
- Port 22 (scan target)
- Port 23 (scan target)
- Port 25 (scan target)
- Port 3306 (scan target)
- Port 3389 (scan target)
- Port 443 (scan target)
- Port 445 (scan target)
- Port 5432 (scan target)
- Port 5900 (scan target)
- Port 80 (scan target)
- Port 8080 (scan target)
- Port 8443 (scan target)
- Port 993 (scan target)
- Port 995 (scan target)

### User IOCs

- www-data (compromised account)

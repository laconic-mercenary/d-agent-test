# Fernbridge Labs — Environment Summary

## Overview

Fernbridge Labs is a small software team sharing one Linux application
server for day-to-day development work. There is no Active Directory or
Windows domain in this environment — all systems are Linux.

- **Timezone:** UTC
- **All log timestamps are in UTC.**
- **Data window:** 2024-05-13T14:00:00Z to 2024-05-13T16:00:00Z (2 hours)
- **Approximate environment size:** 3 users, 4 systems

## User Directory

| Username | Full Name | Email | Role | Primary System |
|----------|-----------|-------|------|-----------------|
| greta.lindqvist | Greta Lindqvist | greta.lindqvist@fernbridgelabs.com | Software Engineer | WS-GRETA-01 |
| marcus.oyelaran | Marcus Oyelaran | marcus.oyelaran@fernbridgelabs.com | Software Engineer | WS-MARCUS-01 |
| priya.desai | Priya Desai | priya.desai@fernbridgelabs.com | Software Engineer | WS-PRIYA-01 |

## Systems Inventory

| Hostname | IP Address | OS | Type | Services |
|----------|------------|-----|------|----------|
| APP-SHARED-01 | 10.70.8.10 | Ubuntu 22.04 LTS | Server | ssh |
| WS-GRETA-01 | 10.70.8.23 | Ubuntu 22.04 LTS | Workstation | — |
| WS-MARCUS-01 | 10.70.8.22 | Ubuntu 22.04 LTS | Workstation | — |
| WS-PRIYA-01 | 10.70.8.21 | Ubuntu 22.04 LTS | Workstation | — |

APP-SHARED-01 is a shared server used by the whole team; it has no single
assigned owner. Each workstation is assigned to one team member.

## Network Topology

### Subnets

| Segment | CIDR | Description |
|---------|------|--------------|
| dev_lan | 10.70.8.0/24 | Single flat dev-team LAN — all workstations and the shared server |

### Network Sensors

| Sensor | Type | Placement | Monitors | Direction | Formats |
|--------|------|-----------|----------|-----------|---------|
| dev-span (ZEEK-DEV-01) | Network (Zeek) | SPAN | dev_lan | Bidirectional | zeek |

`dev-span` mirrors all traffic on the dev-team LAN, including connections
between workstations and the shared server.

## Security Tooling

All hosts run a lightweight EDR-style agent producing process, file, and
network telemetry in eCAR format. Shell activity for interactive sessions is
captured via per-user bash history files and syslog.

## Available Data Sources

| Log Format | Description |
|------------|--------------|
| syslog | Linux system and authentication logging from all hosts |
| bash_history | Per-user shell command history from all hosts |
| ecar | Host-based EDR-style process, file, and network telemetry from all hosts |
| zeek | Network connection and protocol metadata from the dev-team LAN sensor |

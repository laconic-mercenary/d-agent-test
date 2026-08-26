# Alderwood Partners — Environment Summary

## Overview

Alderwood Partners is a small professional services office. The environment
consists of one active staff member's workstation and one shared workstation
used by the team. There is no Active Directory or Windows domain in this
environment.

- **Timezone:** UTC
- **All log timestamps are in UTC.**
- **Data window:** 2024-03-04T14:00:00Z to 2024-03-04T16:00:00Z (2 hours)
- **Approximate environment size:** 1 user, 2 systems

## User Directory

| Username | Full Name | Email | Role | Primary System |
|----------|-----------|-------|------|-----------------|
| dana.whitfield | Dana Whitfield | dana.whitfield@alderwoodpartners.com | Receptionist | WS-01 |

## Systems Inventory

| Hostname | IP Address | OS | Type | Services |
|----------|------------|-----|------|----------|
| WS-01 | 10.40.12.11 | Windows 11 | Workstation | — |
| WS-02 | 10.40.12.12 | Windows 11 | Workstation | Remote Desktop (RDP) |

WS-01 is Dana's assigned workstation. WS-02 is a shared workstation with no
single assigned owner.

## Network Topology

### Subnets

| Segment | CIDR | Description |
|---------|------|--------------|
| office_lan | 10.40.12.0/24 | Single flat office LAN — all workstations |

### Network Sensors

No Zeek/IDS/firewall sensors are configured; host logs still render.

## Security Tooling

Windows systems in this environment run with a community-based Sysmon
configuration (SwiftOnSecurity/Olaf Hartong style) alongside standard Windows
Security auditing. This includes:

- Process creation and termination (Security 4688/Sysmon Events 1, 5)
- Network connections for LOLBins and suspicious ports — browsers and system
  services excluded (Sysmon Event 3)
- DLL/module loading for unsigned and third-party DLLs — Microsoft-signed
  System32 DLLs excluded (Sysmon Event 7)
- File creation for executable types in suspicious locations — Startup,
  Downloads, Temp, scheduled tasks (Sysmon Event 11)
- Registry persistence and tampering — Run keys, Winlogon, services,
  firewall/Defender/UAC modifications (Sysmon Events 12/13)
- DNS queries from all processes (Sysmon Event 22)
- Process injection and credential access detection (Sysmon Events 8, 10)

Some expected event types may be absent from the data simply because they're
filtered by this configuration, not because nothing happened.

## Available Data Sources

| Log Format | Description |
|------------|--------------|
| windows | Windows Event Log — Security auditing and Sysmon, from both workstations |

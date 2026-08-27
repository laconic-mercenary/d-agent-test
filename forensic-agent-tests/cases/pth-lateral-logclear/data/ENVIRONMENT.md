# Environment: Cobalt Ridge Manufacturing

Cobalt Ridge Manufacturing is a small manufacturer. This document is
the background an incoming analyst would be handed before
investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Derek Wallace | Operations | WS-BREACH-01 |
| Priya Anand | IT/sysadmin (Domain Admin) | WS-PANAND-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller |
| FS-01, FS-02, FS-03 | File servers |
| WS-BREACH-01, WS-PANAND-01 | Workstations |
| `zeek01` | Network sensor — connection logs |

## The `localadmin` account

Every server and workstation in this environment was provisioned from
the same base image, and that image's local `Administrator` account
(`localadmin`) was never re-randomized per machine — a known,
unremediated legacy issue. This account is documented for **local
console use only** (physical/emergency access to a single machine) and
is not meant to be used for interactive network logons to a *different*
machine at all — using it that way is itself outside its intended
purpose, independent of which authentication protocol the logon
happens to use.

Separately, `localadmin`'s credentials **are** used legitimately, but
only by automated, non-interactive infrastructure processes running as
`SYSTEM` on the file servers themselves: a scheduled maintenance
PowerShell script, `taskhostw.exe` (a scheduled-task helper), and
`C:\Program Files\Meridian\OpsAgent\ops-agent.exe` (a monitoring
agent) — all of which periodically use `localadmin`'s credentials
*from one file server to another* as part of routine, expected
infrastructure automation. This is documented, normal background
behavior, not evidence of anything by itself.

## A note on network-traffic volume

`WS-BREACH-01`'s assigned user (Derek Wallace) has normal day-to-day
access to file shares on all three file servers as part of ordinary
office work — this workstation's IP address generates substantial,
routine SMB traffic all day. Source-IP/volume analysis of network
connections alone will not isolate anything unusual; account-specific
analysis is the more productive path.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

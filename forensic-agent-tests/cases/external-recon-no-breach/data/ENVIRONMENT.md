# Environment: Meridian Ledger

Meridian Ledger is a small accounting firm. This document is the
background an incoming analyst would be handed before investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Paul Iverson | Accountant | WS-PIVERSON-01 |
| Rita Okafor | IT/sysadmin | WS-ROKAFOR-01 |

## Systems

| Hostname | Role | Segment |
|---|---|---|
| WS-PIVERSON-01 | Workstation | Workstations |
| WS-ROKAFOR-01 | Workstation | Workstations |
| FILE-01 | Internal file server | Servers |
| WEB-01 | Public client-document-upload portal (`docs.meridianledger.com`) | DMZ |

## Network

Three segments behind a perimeter firewall (default-deny):

- **Workstations** — internal only, no direct internet exposure.
- **Servers** — internal only, houses the file server. Not reachable
  from the internet under any circumstance.
- **DMZ** — houses `WEB-01`, the public-facing document portal.

## Stated security policy

IT's documented policy for `WEB-01` is that **only ports 80 and 443
should be reachable from the internet** — the portal is a standard
HTTPS web application; there is no supported reason for any other
service on that host (including SSH admin access) to be reachable from
outside. SSH access to `WEB-01` for administration is meant to happen
only from the internal Servers/Workstations segments, never from the
public internet. Any inbound connection to `WEB-01` on a port other than
80/443, or any inbound SSH connection sourced from outside the
organization's own IP ranges, would be outside of what IT considers
normal or intended.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the policy stated
above, not against an assumption that something is already known to be
wrong.

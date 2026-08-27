# Environment: Solstice Outdoors

Solstice Outdoors is a small e-commerce retailer. This document is the
background an incoming analyst would be handed before investigating.

## Systems

| Hostname | Role | Segment |
|---|---|---|
| WEB-01 | Public order-lookup web application (nginx) | DMZ (`10.70.10.0/24`), public-facing via NAT |
| DB-01 | Application database for the web app (PostgreSQL) | DMZ |
| FILE-01 | Internal file server (Samba) | Internal servers segment (`10.70.20.0/24`) |
| WS-PDESAI-01 | IT admin workstation (Priya Desai) | Internal workstations segment (`10.70.30.0/24`) |
| `zeek01` | Network sensor — DNS, connection, and HTTP logs |
| `fw01` | Perimeter firewall — Cisco ASA-style logs |

## Firewall policy (as currently configured)

- External clients may reach `WEB-01` on 80/443 only.
- The DMZ segment (`WEB-01`, `DB-01`) is permitted to reach the internal
  servers segment on port 445 (SMB) — a legacy exception from an old
  backup arrangement that was never revoked when that arrangement
  ended. This rule is a known, standing item on IT's cleanup backlog;
  it has not been treated as urgent because no incident has ever been
  tied to it.
- This is the only *documented* DMZ-to-internal exception. In
  practice, some ordinary monitoring/health-check-style traffic
  (ICMP, occasional service polling) also crosses this boundary — IT
  has not fully inventoried every legacy allowance on this firewall.

## What WEB-01 actually does

`WEB-01` is a public order-lookup application. Its only legitimate
outbound relationships are to `DB-01` (its own application database)
and to routine internet destinations (package updates, DNS, etc.). It
has no application function, scheduled job, or administrative purpose
that involves the internal file server.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

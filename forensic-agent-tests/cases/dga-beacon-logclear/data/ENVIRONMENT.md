# Environment: Cascade Freight Co.

Cascade Freight Co. is a small freight logistics company. This
document is the background an incoming analyst would be handed before
investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Grace Tanaka | Dispatch | WS-INFECTED-01 |
| Leo Brannigan | IT/sysadmin | WS-BRANNIGAN-01 |
| Sam Okafor | Dispatch | WS-OKAFOR-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller, DNS server, DHCP server |
| WS-INFECTED-01, WS-BRANNIGAN-01, WS-OKAFOR-01 | Workstations |
| `zeek01` | Network sensor — DNS and connection logs |

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

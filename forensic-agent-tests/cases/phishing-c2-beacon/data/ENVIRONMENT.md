# Environment: Rivermark Legal

Rivermark Legal is a small law firm. This document is the background an
incoming analyst would be handed before investigating.

## People

| User | Role | Primary system |
|---|---|---|
| James Okafor | Paralegal | WS-JOKAFOR-01 |
| Maria Santos | Attorney | WS-MSANTOS-01 |
| Tom Becker | IT/sysadmin | WS-TBECKER-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller, DNS server, DHCP server |
| MAIL-01 | On-prem mail server |
| WS-JOKAFOR-01, WS-MSANTOS-01, WS-TBECKER-01 | Workstations |
| `zeek01` | Network sensor — DNS, connection, SMTP, and SSL logs for the workstation and server segments |

## Mail handling

Inbound mail is relayed through `MAIL-01`. There is no attachment
sandboxing or macro-blocking policy currently enforced on this mail
server — attachments of any Office file type, including macro-enabled
formats, are delivered as received.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

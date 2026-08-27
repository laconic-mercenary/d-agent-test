# Environment: Alderwood Data Partners

Alderwood Data Partners is a small data-analytics consultancy. This
document is the background an incoming analyst would be handed before
investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Sarah Nakamura | Finance analyst | WS-SNAKAMURA-01 |
| Lena Moretz | Finance | WS-LMORETZ-01 |
| David Kim | IT/sysadmin | WS-DKIM-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller, DNS server, DHCP server |
| FILE-01 | File server — hosts client-project shares, including a `Finance` share |
| WS-SNAKAMURA-01, WS-LMORETZ-01, WS-DKIM-01 | Workstations |
| `zeek01` | Network sensor — DNS and connection logs for the workstation and server segments |

## Data access policy

Finance-team members (Sarah Nakamura, Lena Moretz) have standing,
legitimate read/write access to the `\\FILE-01\Finance\` share as part
of normal client work — this is not itself unusual or something to
flag. There is no DLP or proxy control monitoring DNS query content;
outbound DNS from any workstation is not filtered or inspected by any
control in this environment today.

## Approved data-handling channels

Company policy (unwritten but consistently enforced in practice)
expects client financial data to leave the network only via the
approved client-delivery portal or encrypted email to a client's
verified corporate domain — never via a workstation's own outbound
traffic to an arbitrary external domain.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

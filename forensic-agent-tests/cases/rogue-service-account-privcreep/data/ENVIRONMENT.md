# Environment: Summit Ridge Analytics

Summit Ridge Analytics is a small data-analytics consultancy. This
document is the background an incoming analyst would be handed before
investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Diego Velasquez | BI analyst | WS-DVELASQUEZ-01 |
| Nadia Kowalski | IT/sysadmin (Domain Admin) | WS-NKOWALSKI-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller |
| APP-01 | Application server — runs scheduled reporting jobs |
| WS-DVELASQUEZ-01, WS-NKOWALSKI-01 | Workstations |

## The `svc-reportgen` account

`svc-reportgen` is a service account documented for exactly one
purpose: an unattended, scheduled nightly reporting job that runs on
`APP-01`. Its credentials are used automatically by that job's
scheduled task and by the server's monitoring agent — both
`SYSTEM`-context, non-interactive, and expected. **This account has no
documented interactive use of any kind, by anyone, under any
circumstance.** It is not a member of any administrative group.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

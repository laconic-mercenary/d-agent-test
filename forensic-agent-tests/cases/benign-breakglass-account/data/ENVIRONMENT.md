# Environment: Larkfield Insurance Group

Larkfield Insurance Group is a small insurance office. This document
is the background an incoming analyst would be handed before
investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Marcus Oyelaran | IT/sysadmin, on-call rotation | WS-MOYELARAN-01 |
| Dana Whitfield | IT/sysadmin, on-call rotation | WS-DWHITFIELD-01 |
| Rosa Delgado | Accounting | WS-RDELGADO-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller |
| APP-01 | Internal application server |
| DB-01 | Database server |
| FILE-01 | File server |
| WS-MOYELARAN-01, WS-DWHITFIELD-01, WS-RDELGADO-01 | Workstations |

## The `svc-breakglass` account

`svc-breakglass` is a documented emergency-access local-admin account,
shared between Marcus Oyelaran and Dana Whitfield as part of the
after-hours on-call rotation. It exists so that whichever of the two
is on call can respond to an automated alert (a stopped service, an
error spike, a low-disk-space warning) without waiting for a
individually-provisioned account request. Its use is logged and
informally reviewed by IT leadership on a weekly basis; there is no
individual account provisioned for out-of-hours emergency response, by
design, since either sysadmin needs to be able to act immediately
regardless of who is actually on call that week.

## What this document does not cover

There is no known incident, no reported suspicious activity, and no
open investigation as of this document's writing. Whatever an analyst
finds should be evaluated on its own merits against the context stated
above, not against an assumption that something is already known to be
wrong.

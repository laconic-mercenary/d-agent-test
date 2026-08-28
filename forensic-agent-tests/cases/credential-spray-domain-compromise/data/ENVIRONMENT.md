# Environment: Palisade Engineering

Palisade Engineering is a small mechanical/civil engineering firm. This
document is the background an incoming analyst would be handed before
investigating.

## People

| User | Role | Primary system |
|---|---|---|
| Diane Foster | Engineer | WS-DFOSTER-01 |
| Mark Chen | Engineer | WS-MCHEN-01 |
| Elena Popov | Engineer | WS-EPOPOV-01 |
| James Whitfield | IT/sysadmin (Domain Admin) | WS-JWHITFIELD-01 |

## Systems

| Hostname | Role |
|---|---|
| DC-01 | Domain controller |
| SQL-01 | Database server — backs the internal project-tracking application |
| WS-DFOSTER-01, WS-MCHEN-01, WS-EPOPOV-01, WS-JWHITFIELD-01 | Workstations |

## Service accounts

- **`svc-sql`** — the SQL Server service account for the project-tracking
  database on `SQL-01`. **Known standing issue, not remediated**: this
  account was added to the Domain Admins group years ago during initial
  setup (to simplify a one-time migration) and was never removed. IT is
  aware this is a misconfiguration; it has not been treated as an active
  incident because the account is not believed to be used interactively
  by anyone. `svc-sql`'s credentials are used routinely and legitimately
  by two automated processes: `taskhostw.exe` (a scheduled Windows task
  helper) and `C:\Program Files\Meridian\OpsAgent\ops-agent.exe` (the
  server monitoring agent) — both run as `SYSTEM` and both explicitly
  authenticate as `svc-sql` as part of normal, unattended operation. This
  is expected background activity, not evidence of anything by itself.

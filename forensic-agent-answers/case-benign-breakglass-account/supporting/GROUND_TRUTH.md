# Ground Truth: benign-breakglass-account

**Scenario:** A small insurance office's two on-call sysadmins share a documented
break-glass local-admin account across several servers, used only
during off-hours incident response — logons at odd hours followed by
diagnostic PowerShell commands that would read as suspicious in
isolation, but match a real, informally-documented operational
practice. No attack anywhere in this scenario — entirely benign
activity plus one unrelated distractor (a different employee working
late for an ordinary reason). Tests whether an agent correctly
concludes "no incident" while still doing real verification work
(checking the account's documented purpose, distinguishing the
unrelated late-night activity on its own merits) rather than either
crying wolf over odd-hours admin activity or waving everything off
without checking.


**Generated:** 2024-09-03 07:00:00 UTC


## Attack Summary

*No malicious activities in this scenario.*


## Timeline

*No malicious events were generated.*


## Indicators of Compromise (IOCs)

*No IOCs extracted.*


## Red Herrings

The following events appear suspicious but are benign. They are included to make the dataset more realistic.

| Timestamp | Actor | System | Activity | Why It's Benign |
|-----------|-------|--------|----------|-----------------|
| 2024-09-03 07:14:38 UTC | svc-breakglass | APP-01 | Documented emergency-access account used for after-hours service check following an automated alert | svc-breakglass is a documented break-glass account shared by the two on-call sysadmins for after-hours incident response; usage is logged and reviewed weekly per informal IT policy. This session responds to a stopped-service alert on APP-01. |
| 2024-09-03 07:14:40 UTC | svc-breakglass | APP-01 | Documented emergency-access account used for after-hours service check following an automated alert | svc-breakglass is a documented break-glass account shared by the two on-call sysadmins for after-hours incident response; usage is logged and reviewed weekly per informal IT policy. This session responds to a stopped-service alert on APP-01. |
| 2024-09-03 07:30:15 UTC | svc-breakglass | DB-01 | Same on-call session continues to DB-01 to check for related database errors | Continuation of the same documented emergency-access session — checking whether the stopped service on APP-01 affected the database tier. |
| 2024-09-04 04:00:08 UTC | rosa.delgado | WS-RDELGADO-01 | An accounting employee works unusually late to finish a month-end report, unrelated to any IT incident | Ordinary late work for a month-end reporting deadline — not tied to any incident-response policy, not part of the IT on-call rotation, and not an anomaly by this employee's normal role. |
| 2024-09-04 04:00:10 UTC | rosa.delgado | WS-RDELGADO-01 | An accounting employee works unusually late to finish a month-end report, unrelated to any IT incident | Ordinary late work for a month-end reporting deadline — not tied to any incident-response policy, not part of the IT on-call rotation, and not an anomaly by this employee's normal role. |
| 2024-09-04 07:14:32 UTC | svc-breakglass | FILE-01 | Documented emergency-access account used the following night to check disk space after a low-space alert | Second, separate documented emergency-access session by the on-call rotation — responding to a low-disk-space alert on FILE-01. |
| 2024-09-04 07:14:33 UTC | svc-breakglass | FILE-01 | Documented emergency-access account used the following night to check disk space after a low-space alert | Second, separate documented emergency-access session by the on-call rotation — responding to a low-disk-space alert on FILE-01. |
| 2024-09-04 07:35:03 UTC | svc-breakglass | DC-01 | Same on-call session checks the domain controller's system event log as a precaution | Continuation of the same documented emergency-access session — a routine precautionary check of the DC's system log, standard practice for this on-call rotation. |

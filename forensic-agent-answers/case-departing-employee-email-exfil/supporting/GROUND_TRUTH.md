# Ground Truth: departing-employee-email-exfil

**Scenario:** A senior architect at a small design studio, who has legitimate
access to client project files as a normal part of his job, emails
three attachments containing client-sensitive material to his own
personal email address over two days shortly before his last day.
No malware, no external attacker, no technical exploitation of any
kind — every action is performed with legitimate, already-authorized
access. Tests whether an agent reports this as what it actually is
(a policy/DLP matter) rather than either over-dramatizing it as a
"breach" or under-reporting it as nothing worth flagging.


**Generated:** 2024-05-06 13:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **owen.marsh** on **WS-OMARSH-01**: Owen logs into his own workstation for the day, as usual
2. **owen.marsh** on **WS-OMARSH-01**: Owen emails a batch of client contract documents to his personal email address
3. **owen.marsh** on **WS-OMARSH-01**: Later the same day, Owen emails a large batch of client project design files to the same personal address
4. **owen.marsh** on **WS-OMARSH-01**: The next day, Owen emails the firm's client contact list to the same personal address


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-05-06 14:59:38 UTC | owen.marsh | WS-OMARSH-01 | Logon | Network logon from 185.220.101.34 (LogonID: 0x8a4d2be) |
| 2024-05-06 15:20:10 UTC | owen.marsh | WS-OMARSH-01 | Email_Message | Email delivered: owen.marsh@thistledownarch.com -> owen.marsh.archive@gmail.com; subject 'Q3 Client Contracts - Backup' (artifacts/email/evt-email-001-000090d3ef7e.eml) |
| 2024-05-06 19:45:12 UTC | owen.marsh | WS-OMARSH-01 | Email_Message | Email delivered: owen.marsh@thistledownarch.com -> owen.marsh.archive@gmail.com; subject 'Project Atlas - Design Files' (artifacts/email/evt-email-002-00006db8a865.eml) |
| 2024-05-07 15:09:49 UTC | owen.marsh | WS-OMARSH-01 | Email_Message | Email delivered: owen.marsh@thistledownarch.com -> owen.marsh.archive@gmail.com; subject 'Client Contact List' (artifacts/email/evt-email-003-000044dade17.eml) |


## Indicators of Compromise (IOCs)

### Network IOCs

- 185.220.101.34 (Attacker IP)
- Message-ID: <10000180U7RF.1001IGUQQ5@thistledownarch.com>
- Message-ID: <18F928EA-211C-12FF-053A-2CBB6BB6B343@thistledownarch.com>
- Message-ID: <2BA50634-5EC6-C4E1-3FDE-44880496FE9C@thistledownarch.com>
- SMTP Zeek UID: C23qBrELEWLU04UMAO
- SMTP Zeek UID: CB0D0clplxlHHQ1q9X
- SMTP Zeek UID: CC3RVoGpcBsFByM172
- SMTP Zeek UID: CSgXpMtUSRDEHWW76T
- SMTP Zeek UID: Ci8OA7lqIE83wyS4gFl
- SMTP Zeek UID: CwjvMroRU9jXJKY4ldC

### User IOCs

- owen.marsh (compromised account)

### File IOCs

- artifacts/email/evt-email-001-000090d3ef7e.eml
- artifacts/email/evt-email-002-00006db8a865.eml
- artifacts/email/evt-email-003-000044dade17.eml

# Ground Truth: ssh-shared-key-overlap

**Scenario:** Minimal benign scenario testing whether an analyst (LLM) can detect
private-key sharing from correlated SSH evidence alone. Three developers
SSH into the same shared Linux server and each writes a short note file.
One developer (Priya) shares her private key with a colleague (Marcus),
who uses it to open a second SSH session that authenticates as Priya —
from his own workstation, overlapping in time with Priya's own genuine
session. A third developer (Greta) is uninvolved and uses her own
account normally, with her session also overlapping the other two. No
attack, no malicious technique — the only "finding" is that one identity
(priya.desai) has two concurrent sessions from two different source IPs,
which a single person cannot produce.


**Generated:** 2024-05-13 14:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **priya.desai** on **APP-SHARED-01**: Priya connects to the shared app server from her own workstation
2. **priya.desai** on **APP-SHARED-01**: Priya appends a note to her deployment log during her own session
3. **greta.lindqvist** on **APP-SHARED-01**: Greta connects to the shared app server from her own workstation
4. **priya.desai** on **APP-SHARED-01**: A second session authenticating as Priya connects from Marcus's workstation, overlapping with Priya's own already-open session — Marcus is using a private key Priya shared with him
5. **greta.lindqvist** on **APP-SHARED-01**: Greta writes a short status note during her session
6. **priya.desai** on **APP-SHARED-01**: The session sourced from Marcus's workstation appends a second note to Priya's deployment log, still under Priya's account


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-05-13 14:15:11 UTC | priya.desai | APP-SHARED-01 | Ssh_Session | SSH session to 10.70.8.10:22 (UID: CveZXJBauqksloGzsl) |
| 2024-05-13 14:17:17 UTC | priya.desai | APP-SHARED-01 | Process | Process: /bin/bash (PID: 3161390) - `bash -c "echo 'API gateway config reviewed, no ...` |
| 2024-05-13 14:18:27 UTC | greta.lindqvist | APP-SHARED-01 | Ssh_Session | SSH session to 10.70.8.10:22 (UID: CIWCHncR5M2505scK) |
| 2024-05-13 14:19:44 UTC | priya.desai | APP-SHARED-01 | Ssh_Session | SSH session to 10.70.8.10:22 (UID: CBIjzBLhWJJUDOpPxL) |
| 2024-05-13 14:22:13 UTC | greta.lindqvist | APP-SHARED-01 | Process | Process: /bin/bash (PID: 3161976) - `bash -c "echo 'Ran nightly test suite, all gree...` |
| 2024-05-13 14:23:30 UTC | priya.desai | APP-SHARED-01 | Process | Process: /bin/bash (PID: 3162238) - `bash -c "echo 'Reviewed staging deploy, looks g...` |


## Indicators of Compromise (IOCs)

### Network IOCs

- 10.70.8.10:22 (Lateral Movement)
- Zeek UID: CBIjzBLhWJJUDOpPxL
- Zeek UID: CIWCHncR5M2505scK
- Zeek UID: CveZXJBauqksloGzsl

### Process IOCs

- /bin/bash
- `bash -c "echo 'API gateway config reviewed, no changes needed' >> /home/priya.desai/notes/deploy-log.txt"`
- `bash -c "echo 'Ran nightly test suite, all green' >> /home/greta.lindqvist/notes/status-log.txt"`
- `bash -c "echo 'Reviewed staging deploy, looks good' >> /home/priya.desai/notes/deploy-log.txt"`

### User IOCs

- greta.lindqvist (compromised account)
- priya.desai (compromised account)

### File IOCs

- /home/greta.lindqvist/notes/status-log.txt
- /home/priya.desai/notes/deploy-log.txt

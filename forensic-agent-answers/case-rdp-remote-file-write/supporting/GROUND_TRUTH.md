# Ground Truth: rdp-remote-file-write

**Scenario:** Minimal, entirely benign single-action scenario. One user at her own
workstation opens a remote desktop session to a shared office workstation
and saves a short note file during that session. No attack, no malicious
technique, no red herrings — the goal is a basic test of whether an
analyst (LLM) can reconstruct the sequence of actions and correctly
identify the actor from the generated logs alone.


**Generated:** 2024-03-04 14:00:00 UTC


## Attack Summary

This scenario simulates the following attack sequence:

1. **dana.whitfield** on **WS-02**: Dana remotely connects to the shared office workstation from her own desk machine via RDP
2. **dana.whitfield** on **WS-02**: Dana opens Notepad during the remote session and saves a short note file for the team


## Timeline

| Timestamp | Actor | System | Event Type | Details |
|-----------|-------|--------|------------|---------|
| 2024-03-04 14:19:56 UTC | dana.whitfield | WS-02 | Rdp_Session | RDP session to 10.40.12.12:3389 (UID: (filtered by sensor placement)) |
| 2024-03-04 14:40:50 UTC | dana.whitfield | WS-02 | Process | Process: C:\Windows\System32\notepad.exe (PID: 6648) - `notepad.exe C:\Users\dana.whitfield\Documents\t...` |


## Indicators of Compromise (IOCs)

### Network IOCs

- 10.40.12.12:3389 (Lateral Movement)

### Process IOCs

- C:\Windows\System32\notepad.exe
- `notepad.exe C:\Users\dana.whitfield\Documents\team-notes.txt`

### User IOCs

- dana.whitfield (compromised account)

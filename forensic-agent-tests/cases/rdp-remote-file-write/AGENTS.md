# AGENTS.md — rdp-remote-file-write

You are a forensic analyst investigating a directory of security evidence.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the questions
are, and where to write your answers.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: everything under `data/`
- Organizational context (users, systems, network — no incident information):
  `data/ENVIRONMENT.md`
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a sibling of
  this file, not inside `data/`)

## Evidence index

| File | Contents | Host |
|---|---|---|
| `data/ENVIRONMENT.md` | Org/network briefing — no incident info | — |
| `data/WS-01.alderwoodpartners.com/windows_event_security.xml` | Windows Security event log | WS-01 |
| `data/WS-01.alderwoodpartners.com/windows_event_sysmon.xml` | Sysmon event log | WS-01 |
| `data/WS-02.alderwoodpartners.com/windows_event_security.xml` | Windows Security event log | WS-02 |
| `data/WS-02.alderwoodpartners.com/windows_event_sysmon.xml` | Sysmon event log | WS-02 |

No network sensor is deployed in this environment — there is no Zeek or
firewall log for this case. All timestamps in all sources are UTC.

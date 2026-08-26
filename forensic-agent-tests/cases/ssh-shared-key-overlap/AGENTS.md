# AGENTS.md — ssh-shared-key-overlap

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
| `data/APP-SHARED-01.fernbridgelabs.com/ecar.json` | EDR telemetry (NDJSON) | APP-SHARED-01 |
| `data/APP-SHARED-01.fernbridgelabs.com/syslog.log` | Linux syslog | APP-SHARED-01 |
| `data/APP-SHARED-01.fernbridgelabs.com/bash_history/*.bash_history` | Per-user shell history | APP-SHARED-01 |
| `data/WS-PRIYA-01.fernbridgelabs.com/{ecar.json,syslog.log,bash_history/*}` | Host telemetry/history | WS-PRIYA-01 |
| `data/WS-MARCUS-01.fernbridgelabs.com/{ecar.json,syslog.log,bash_history/*}` | Host telemetry/history | WS-MARCUS-01 |
| `data/WS-GRETA-01.fernbridgelabs.com/{ecar.json,syslog.log,bash_history/*}` | Host telemetry/history | WS-GRETA-01 |
| `data/ZEEK-DEV-01/conn.json`, `dns.json`, `http.json`, `ssl.json`, `files.json`, `x509.json`, `ocsp.json`, `ntp.json` | Network sensor logs (NDJSON) | ZEEK-DEV-01 |

All timestamps in all sources are UTC.

# AGENTS.md — single-host-linux-rce

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
| `data/APP-01.thornburyanalytics.com/ecar.json` | EDR telemetry: process/file/flow (NDJSON) | APP-01 |
| `data/APP-01.thornburyanalytics.com/syslog.log` | Linux syslog | APP-01 |
| `data/APP-01.thornburyanalytics.com/web_access.log` | Web server access log | APP-01 |
| `data/APP-01.thornburyanalytics.com/bash_history/sam.ortiz.bash_history` | Shell history | APP-01 |
| `data/WS-OP-01.thornburyanalytics.com/ecar.json` | EDR telemetry (NDJSON) | WS-OP-01 |
| `data/WS-OP-01.thornburyanalytics.com/syslog.log` | Linux syslog | WS-OP-01 |
| `data/WS-OP-01.thornburyanalytics.com/bash_history/sam.ortiz.bash_history` | Shell history | WS-OP-01 |
| `data/FW-EDGE-01/cisco_asa.log` | Perimeter firewall syslog (allow/deny/NAT) | FW-EDGE-01 |
| `data/ZEEK-DMZ-01/conn.json`, `dns.json`, `http.json`, `ssl.json`, `files.json`, `x509.json` | Network sensor logs (NDJSON) | ZEEK-DMZ-01 |

All timestamps in all sources are UTC.

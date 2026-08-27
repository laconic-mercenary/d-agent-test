# AGENTS.md — external-recon-no-breach

You are investigating a small accounting firm's network after evidence
of a port scan against its public-facing web server. There is no
confirmed incident — your job is to determine, from the evidence, what
actually happened and whether it amounted to anything.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it states the
organization's network layout and its stated security policy, which
matters for correctly interpreting some of what you'll find.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: `data/` — firewall logs, network sensor logs, host-level
  Windows Event Logs, SSH/bash history, and a web access log
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a
  sibling of this file, not inside `data/`)

## Evidence index

| Path | Contents |
|---|---|
| `data/ENVIRONMENT.md` | Organization background, systems, and stated security policy — read first |
| `data/FW-EDGE-01/cisco_asa.log` | Perimeter firewall log (Cisco ASA format) |
| `data/ZEEK-CORE-01/*.json` | Network sensor logs (Zeek) — `conn.json`, `dns.json`, `http.json`, `ssl.json`, `x509.json`, `files.json`, `ocsp.json` |
| `data/WEB-01.meridianledger.local/` | The public web server's own logs — `syslog.log`, `web_access.log`, `bash_history/` |
| `data/WS-PIVERSON-01.meridianledger.local/`, `data/WS-ROKAFOR-01.meridianledger.local/` | Workstation Windows Event Logs (`windows_event_security.xml`, `windows_event_sysmon.xml`) |
| `data/FILE-01.meridianledger.local/` | Internal file server's Windows Event Logs |

All timestamps are UTC unless stated otherwise. Not every file or every
line is relevant to every question — this is a full evidence set for a
four-hour collection window, most of which is ordinary background
activity.

## Scope assumption

This case's evidence is synthetic (generated for this exercise, not
real-world data), but investigate it the same way you would real
evidence — every finding should be traceable to a specific file, field,
and value, not general knowledge about what port scans "usually" look
like.

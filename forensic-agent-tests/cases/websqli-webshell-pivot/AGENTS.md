# AGENTS.md — websqli-webshell-pivot

You are investigating a small retailer's public web application, its
database, an internal file server, an IT admin workstation, and the
perimeter firewall/network sensor for signs of compromise. This is a
real, multi-stage intrusion — trace it from the initial scan through to
whatever the attacker ultimately did.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it documents this
network's firewall policy and what the web server's legitimate traffic
pattern actually looks like, both of which matter for interpreting
what you'll find.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: `data/evidence.tar.gz` — unpack before starting (see below)
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a
  sibling of this file, not inside `data/`)

## Unpacking the evidence

```
tar -xzf data/evidence.tar.gz -C data/
```

This produces six host/sensor directories under `data/` — everything
below refers to those unpacked files.

## Evidence index

| Path | Contents |
|---|---|
| `data/ENVIRONMENT.md` | Organization/network background — read first |
| `data/WEB-01.solsticeoutdoors.com/` | Web server's own access log (`web_access.log`), syslog, bash history |
| `data/DB-01.solsticeoutdoors.com/` | Database server syslog, bash history |
| `data/FILE-01.solsticeoutdoors.com/` | Internal file server syslog, bash history |
| `data/WS-PDESAI-01.solsticeoutdoors.com/` | Admin workstation syslog, bash history |
| `data/zeek01/` | Network sensor logs — `dns.json`, `conn.json`, `http.json` |
| `data/fw01/` | Perimeter firewall — `cisco_asa.log` |

All timestamps are UTC. This is a full, unfiltered evidence set covering
roughly 24 hours — most of it is ordinary background activity. Part of
the task is distinguishing what's relevant from what's routine, not
reading every event.

**Note on the network sensor's HTTP log vs. the web server's own
access log:** `zeek01/http.json` only captures unencrypted (port 80)
traffic; the web application's own `web_access.log` captures every
request it received regardless of port. If you're looking for
HTTPS-facing request evidence, check the web server's own log, not
just the network sensor's.

## Scope assumption

This case's evidence is synthetic (generated for this exercise, not
real-world data), but investigate it the same way you would real
evidence — every finding should be traceable to a specific file, event,
and field, not general knowledge about what these techniques "usually"
look like.

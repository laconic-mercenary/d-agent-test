# AGENTS.md — phishing-c2-beacon

You are investigating a small law firm's domain controller, mail
server, and three workstations for signs of compromise. This is a
real, multi-stage intrusion — trace it from delivery through to
whatever the attacker ultimately did.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it documents this
organization's mail-handling posture, which matters for interpreting
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
| `data/ENVIRONMENT.md` | Organization background — read first |
| `data/DC-01.rivermarklegal.local/` | Domain controller Windows Event Logs |
| `data/MAIL-01.rivermarklegal.local/` | Mail server Windows Event Logs |
| `data/WS-JOKAFOR-01.rivermarklegal.local/`, `data/WS-MSANTOS-01.rivermarklegal.local/`, `data/WS-TBECKER-01.rivermarklegal.local/` | Workstation Windows Event Logs |
| `data/zeek01/` | Network sensor logs — `dns.json`, `conn.json`, `smtp.json`, `ssl.json` |

All timestamps are UTC. This is a full, unfiltered evidence set covering
roughly 24 hours — most of it is ordinary background activity. Part of
the task is distinguishing what's relevant from what's routine, not
reading every event.

## Scope assumption

This case's evidence is synthetic (generated for this exercise, not
real-world data), but investigate it the same way you would real
evidence — every finding should be traceable to a specific file, event,
and field, not general knowledge about what these techniques "usually"
look like.

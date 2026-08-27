# AGENTS.md — pth-lateral-logclear

You are investigating a small manufacturer's domain controller, three
file servers, and two workstations for signs of lateral movement. This
is a real, multi-stage intrusion — trace it from the account's use
across hosts through to whatever the attacker did to cover tracks.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it documents a shared
local-admin account's intended purpose, its separate legitimate
automated use, and a note about this network's traffic volume that
matters for how you search.

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
| `data/DC-01.cobaltridge.local/` | Domain controller Windows Event Logs |
| `data/FS-01.cobaltridge.local/`, `data/FS-02.cobaltridge.local/`, `data/FS-03.cobaltridge.local/` | File server Windows Event Logs |
| `data/WS-BREACH-01.cobaltridge.local/`, `data/WS-PANAND-01.cobaltridge.local/` | Workstation Windows Event Logs |
| `data/zeek01/` | Network sensor logs — `conn.json` |

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

# AGENTS.md — departing-employee-email-exfil

You are investigating a small architecture firm's domain controller,
mail server, and three workstations following an HR-flagged review.
This may or may not represent something worth reporting — investigate
it the same way you would any other tasking.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it documents the HR
context (a departing employee) and who has legitimate access to what.

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
| `data/ENVIRONMENT.md` | Organization and HR background — read first |
| `data/DC-01.thistledownarch.local/` | Domain controller Windows Event Logs |
| `data/MAIL-01.thistledownarch.local/` | Mail server Windows Event Logs |
| `data/WS-OMARSH-01.thistledownarch.local/`, `data/WS-LFENWICK-01.thistledownarch.local/`, `data/WS-THASSAN-01.thistledownarch.local/` | Workstation Windows Event Logs |
| `data/zeek01/` | Network sensor logs — `smtp.json` (mail metadata), `files.json` (transferred-file metadata) |

All timestamps are UTC. This is a full, unfiltered evidence set covering
roughly 48 hours — most of it is ordinary background activity. Part of
the task is distinguishing what's relevant from what's routine, not
reading every event.

## Scope assumption

This case's evidence is synthetic (generated for this exercise, not
real-world data), but investigate it the same way you would real
evidence — every finding should be traceable to a specific file, event,
and field, not general knowledge about what these situations "usually"
look like.

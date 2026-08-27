# AGENTS.md — benign-breakglass-account

You are investigating a small insurance office's domain controller,
three internal servers, and three workstations after a routine review
flagged some off-hours administrative activity. This may or may not be
a real incident — investigate it the same way you would any other
tasking.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it documents a shared
emergency-access account's intended purpose and usage policy.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: `data/evidence.tar.gz` — unpack before starting (see below)
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a
  sibling of this file, not inside `data/`)

## Unpacking the evidence

```
tar -xzf data/evidence.tar.gz -C data/
```

This produces seven host directories under `data/` — everything below
refers to those unpacked files.

## Evidence index

| Path | Contents |
|---|---|
| `data/ENVIRONMENT.md` | Organization background — read first |
| `data/DC-01.larkfield.local/` | Domain controller Windows Event Logs |
| `data/APP-01.larkfield.local/`, `data/DB-01.larkfield.local/`, `data/FILE-01.larkfield.local/` | Server Windows Event Logs |
| `data/WS-MOYELARAN-01.larkfield.local/`, `data/WS-DWHITFIELD-01.larkfield.local/`, `data/WS-RDELGADO-01.larkfield.local/` | Workstation Windows Event Logs |

All timestamps are UTC. This is a full, unfiltered evidence set covering
roughly 48 hours — most of it is ordinary background activity. Part of
the task is distinguishing what's relevant from what's routine, not
reading every event.

## Scope assumption

This case's evidence is synthetic (generated for this exercise, not
real-world data), but investigate it the same way you would real
evidence — every finding should be traceable to a specific file, event,
and field, not general knowledge about what these techniques "usually"
look like.

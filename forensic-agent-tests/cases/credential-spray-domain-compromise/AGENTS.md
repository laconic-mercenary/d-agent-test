# AGENTS.md — credential-spray-domain-compromise

You are investigating a small engineering firm's domain controller and
five other hosts after signs of a credential-based attack. This is a
real, multi-stage intrusion — trace it from initial access through to
whatever the attacker ultimately achieved.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers. **Read
`data/ENVIRONMENT.md` before investigating** — it documents a standing
account misconfiguration and two pieces of legitimate automated
behavior that matter for correctly interpreting what you'll find.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: `data/evidence.tar.gz` — unpack before starting (see below)
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a
  sibling of this file, not inside `data/`)

## Unpacking the evidence

```
tar -xzf data/evidence.tar.gz -C data/
```

This produces six host directories under `data/` — everything below
refers to those unpacked files.

## Evidence index

| Path | Contents |
|---|---|
| `data/ENVIRONMENT.md` | Organization background — read first |
| `data/DC-01.palisade.local/` | Domain controller Windows Event Logs (`windows_event_security.xml`, `windows_event_sysmon.xml`) |
| `data/SQL-01.palisade.local/` | Database server Windows Event Logs |
| `data/WS-DFOSTER-01.palisade.local/`, `data/WS-MCHEN-01.palisade.local/`, `data/WS-EPOPOV-01.palisade.local/`, `data/WS-JWHITFIELD-01.palisade.local/` | Workstation Windows Event Logs |

All timestamps are UTC. This is a full, unfiltered evidence set covering
roughly 30 hours — most of it is ordinary background activity (routine
authentication, scheduled service traffic, normal engineering work).
Part of the task is distinguishing what's relevant from what's routine,
not reading every event.

## Scope assumption

This case's evidence is synthetic (generated for this exercise, not
real-world data), but investigate it the same way you would real
evidence — every finding should be traceable to a specific file, event,
and field, not general knowledge about what these attack techniques
"usually" look like.

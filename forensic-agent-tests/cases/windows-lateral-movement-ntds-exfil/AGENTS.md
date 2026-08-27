# AGENTS.md — windows-lateral-movement-ntds-exfil

You are investigating a multi-stage intrusion across four hosts in a small
Windows/Active Directory environment. Unlike this repo's simpler cases,
this one has a real attack narrative to reconstruct — but you still need
to derive every fact from the evidence, not from assumption.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: four compressed datasets in `data/` — unpack all four before
  starting (see below)
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a sibling
  of this file, not inside `data/`)

## Unpacking the evidence

Each dataset is a gzipped tarball. Unpack all four in place before you
start:

```
tar -xzf data/dataset1.tar.gz -C data/
tar -xzf data/dataset2.tar.gz -C data/
tar -xzf data/dataset3.tar.gz -C data/
tar -xzf data/dataset4.tar.gz -C data/
```

This produces `data/dataset1/` through `data/dataset4/` — everything
below refers to those unpacked directories.

## Evidence index

| Dataset | Files | Format | Notes |
|---|---|---|---|
| `data/dataset1/` | `Application.jsonl`, `Security.jsonl`, `System.jsonl` | Windows Event Log, converted to JSON Lines (one event per line) | One host's full event-log export |
| `data/dataset2/` | Same three files | Same format | A second host |
| `data/dataset3/` | Same three files | Same format | A third host |
| `data/dataset4/` | `access.log`, `access.log.1`, `cache.log`, `cache.log.1` | Plain text (Squid proxy log format) | Directly readable, no conversion needed |

Each `.jsonl` line is a standalone JSON object with the event's native
field names (`System.EventID`, `System.TimeCreated`, `EventData.*`,
etc.) — the same fields you'd see inspecting the event in Windows Event
Viewer's XML view, just pre-converted so no EVTX-specific tooling is
required. All timestamps in the JSON data are UTC
(`System.TimeCreated.#attributes.SystemTime`); the Squid logs' own
timestamps are also UTC.

Not every line/entry is relevant to any given question — these are full,
unfiltered log exports and contain substantial ordinary background
activity (OS/service noise, routine authentication, unrelated web/update
traffic). Finding the events that actually answer each question is part
of the task.

You do not need to correlate the four datasets in any particular order to
answer the questions, but the case as a whole tells one continuous story
across all four — reading them in order (1 → 2 → 3 → 4) roughly follows
how an analyst would actually trace this incident.

## Scope assumption

This case assumes you do not have live internet/web-search access while
investigating. The source evidence originates from public training
material and, being real (not synthetic) data, contains strings — a
domain name, some account names unrelated to this incident, a Windows
short-filename artifact — that could be used to identify or search for
the original source online. If you can search the web, treat any answer
you find that way as invalid for this exercise — the point is to derive
answers from the evidence files themselves.

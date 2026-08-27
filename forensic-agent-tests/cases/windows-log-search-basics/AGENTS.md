# AGENTS.md — windows-log-search-basics

You are testing Windows Event Log search and filtering ability against two
Windows Event Log exports. There is no incident narrative here — this case
tests whether you can construct precise, targeted queries and cite exact
evidence, not whether you can piece together an attack story.

**Read [TASK.md](TASK.md) now.** It explains what to do, where the
questions are, and where to write your answers.

## If you only read this file

- Questions to answer: [EXAM.md](EXAM.md)
- Evidence: `data/sample1.jsonl.tar.gz`, `data/sample2.jsonl.tar.gz` —
  unpack both before starting (see below); that's all of it, there is no
  `ENVIRONMENT.md` for this case (see TASK.md for why)
- Write your answers to `QUESTION_ANSWERS.md` in this directory (a sibling
  of this file, not inside `data/`)

## Unpacking the evidence

Both files are gzipped tarballs (kept compressed in the repo — each
uncompressed `.jsonl` is 35-40MB of text). Unpack in place before you
start:

```
tar -xzf data/sample1.jsonl.tar.gz -C data/
tar -xzf data/sample2.jsonl.tar.gz -C data/
```

This produces `data/sample1.jsonl` and `data/sample2.jsonl` — everything
below refers to those unpacked files.

## Evidence index

| File | Contents |
|---|---|
| `data/sample1.jsonl` | Windows Event Log, converted to JSON Lines (one event per line) — mixed Security/process/logon events |
| `data/sample2.jsonl` | Windows Event Log, same format — a separate host/capture |

Each line is a standalone JSON object with the event's native field names
(`System.EventID`, `System.TimeCreated`, `EventData.*`, etc.) — the same
fields you'd see inspecting the event in Windows Event Viewer's XML view,
just pre-converted so no EVTX-specific tooling is required to read them.

Not every line is relevant to any given question — these are full,
unfiltered event exports and contain plenty of ordinary background
activity (OS/service noise, and in this case some artifacts of how the
lab environment itself was originally provisioned). That's expected; part
of the task is finding the events that actually answer each question, not
reading front-to-back.

All timestamps are UTC unless the event data states otherwise.

## Scope assumption

This case assumes you do not have live internet/web-search access while
investigating. The source evidence originates from public training
material and, being real (not synthetic) data, contains a handful of
strings — a domain name, some provisioning-script artifacts — that could
be used to identify or search for the original source online. If you can
search the web, treat any answer you find that way as invalid for this
exercise — the point is to derive answers from the evidence files
themselves.

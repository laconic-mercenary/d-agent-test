# Task

This case has no organizational briefing document (`ENVIRONMENT.md`) —
unlike other cases in this repo, there is no company, no user roster, no
network topology to read first. That's deliberate: the two files in
`data/` are the entire scope of this exercise. Nothing outside them is
relevant.

## What to do

The two evidence files ship compressed — unpack them first:

```
tar -xzf data/sample1.jsonl.tar.gz -C data/
tar -xzf data/sample2.jsonl.tar.gz -C data/
```

Answer every question in [EXAM.md](EXAM.md) using only `data/sample1.jsonl`
and `data/sample2.jsonl`. Each question asks you to locate a specific fact —
a timestamp, an account, an event — using targeted search/filtering rather
than reading either file front-to-back. Each file is JSON Lines: one
Windows Event Log record (as a standalone JSON object) per line, using the
event's native field names. Any tool that can search text or parse JSON
works — grep, `jq`, a script, or just reading through it.

Answer only from what the evidence actually supports. If a question can't
be fully answered from these two files, say so explicitly rather than
guessing.

## How to answer

Write your answers to a new file, `QUESTION_ANSWERS.md`, in this same
directory (a sibling of this file — not inside `data/`). For each question:

- Restate the question number.
- Give your answer.
- Cite the specific evidence that supports it — file name, Event ID, and
  the exact field/value you relied on, not just "the logs show this."

There is no time limit and no restriction on how you investigate. The only
requirement is that every answer be traceable to evidence in these two
files.

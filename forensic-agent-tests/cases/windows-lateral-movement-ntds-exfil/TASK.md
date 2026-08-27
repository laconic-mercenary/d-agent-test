# Task

This case has no organizational briefing document (`ENVIRONMENT.md`) —
unlike other cases in this repo, there is no company, no user roster, no
network topology to read first. That's deliberate: the four datasets in
`data/` are the entire scope of this exercise. Nothing outside them is
relevant.

## What to do

The four evidence datasets ship compressed — unpack them first:

```
tar -xzf data/dataset1.tar.gz -C data/
tar -xzf data/dataset2.tar.gz -C data/
tar -xzf data/dataset3.tar.gz -C data/
tar -xzf data/dataset4.tar.gz -C data/
```

Answer every question in [EXAM.md](EXAM.md) using only the four unpacked
datasets. Each question asks you to locate specific facts — timestamps,
accounts, hosts, correlating fields — using targeted search/filtering
rather than reading any file front-to-back. The `.jsonl` files are JSON
Lines: one Windows Event Log record (as a standalone JSON object) per
line, using the event's native field names. `data/dataset4/`'s files are
plain-text Squid proxy logs. Any tool that can search text or parse JSON
works — grep, `jq`, a script, or just reading through it.

Answer only from what the evidence actually supports. If a question can't
be fully answered from these four datasets, say so explicitly rather than
guessing.

## How to answer

Write your answers to a new file, `QUESTION_ANSWERS.md`, in this same
directory (a sibling of this file — not inside `data/`). For each
question:

- Restate the question number.
- Give your answer.
- Cite the specific evidence that supports it — dataset, file name, Event
  ID (or log field), and the exact value you relied on, not just "the
  logs show this."

There is no time limit and no restriction on how you investigate. The
only requirement is that every answer be traceable to evidence in these
four datasets.

# Task

You are the on-call analyst for Thornbury Analytics. Evidence relevant to a
suspected security incident has been collected and placed under `data/`.
Nobody has told you what happened — reconstruct it from the evidence alone.

## What to read first

1. `data/ENVIRONMENT.md` — organizational context: who the users are, what
   systems exist, the network layout, and what each sensor can see. This
   document contains no information about the incident itself.
2. `data/` — the evidence. See [AGENTS.md](AGENTS.md) for a file-by-file
   index. Formats present: eCAR (EDR telemetry), syslog, bash history, a
   Cisco ASA firewall log, Zeek network sensor logs (NDJSON), and a web
   server access log.

## What to do

Investigate the evidence and answer every question in [EXAM.md](EXAM.md).
Answer only from what the evidence actually supports. If something cannot be
determined from the data given, say so explicitly rather than guessing or
inferring beyond what the evidence shows.

## How to answer

Write your answers to a new file, `QUESTION_ANSWERS.md`, in this same
directory (a sibling of this file — not inside `data/`). For each question:

- Restate the question number.
- Give your answer.
- Cite the specific evidence that supports it — file name plus the
  identifying detail (timestamp, UID, PID, source IP, log line), not just
  "the logs show this."

There is no time limit and no restriction on how you investigate — read
files directly, grep, script whatever tooling you have available. The only
requirement is that every answer be traceable to evidence you were actually
given.

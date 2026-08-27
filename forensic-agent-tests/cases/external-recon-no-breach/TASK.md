# Task

Read `data/ENVIRONMENT.md` first — it's short, and it establishes the
organization's stated security policy for the public web server, which
matters for interpreting what you find.

## What to do

Answer every question in [EXAM.md](EXAM.md) using only the evidence in
`data/`. Each question asks you to locate specific facts — a source IP,
a port, a timestamp, a specific log line — using targeted search rather
than reading every file front-to-back.

Answer only from what the evidence actually supports. If a question
can't be fully answered from this evidence, say so explicitly rather
than guessing. In particular: do not assume an outcome (compromise,
non-compromise) before checking — reach your conclusion from what the
logs actually show, and be prepared to say so even if it contradicts an
initial assumption.

## How to answer

Write your answers to a new file, `QUESTION_ANSWERS.md`, in this same
directory (a sibling of this file — not inside `data/`). For each
question:

- Restate the question number.
- Give your answer.
- Cite the specific evidence that supports it — file name and the exact
  field/value/log line you relied on, not just "the logs show this."

There is no time limit and no restriction on how you investigate. The
only requirement is that every answer be traceable to evidence in
`data/`.

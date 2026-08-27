# Task

Read `data/ENVIRONMENT.md` first — it's short, and it establishes a
service account's sole documented purpose, which matters for correctly
interpreting what you'll find.

## What to do

The evidence ships compressed — unpack it first:

```
tar -xzf data/evidence.tar.gz -C data/
```

Answer every question in [EXAM.md](EXAM.md) using only the evidence in
`data/`. Each question asks you to locate specific facts — an account,
a timestamp, a specific event, a specific field value — using targeted
search rather than reading every file front-to-back.

Answer only from what the evidence actually supports. If a question
can't be fully answered from this evidence, say so explicitly rather
than guessing.

## How to answer

Write your answers to a new file, `QUESTION_ANSWERS.md`, in this same
directory (a sibling of this file — not inside `data/`). For each
question:

- Restate the question number.
- Give your answer.
- Cite the specific evidence that supports it — host, file, Event ID,
  and the exact field/value you relied on, not just "the logs show
  this."

There is no time limit and no restriction on how you investigate. The
only requirement is that every answer be traceable to evidence in
`data/`.

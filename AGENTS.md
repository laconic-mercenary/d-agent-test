# AGENTS.md — Evaluation Suite for Forensic Investigation LLM Assistants (umbrella, temporary)

This folder is a **temporary umbrella** holding two projects that are
meant to become fully separate repositories (see `README.md`). Until that
split happens, both live here as sibling directories in one shared git
repo:

- **`forensic-agent-tests/`** — the AUT-facing DFIR benchmark. Its own
  `README.md` and `AGENTS.md` are the entry points for anyone (human or
  agent) working inside it.
- **`forensic-agent-answers/`** — the held-out answer keys, grading
  rubrics, and case-building methodology, paired by slug with
  `forensic-agent-tests/cases/`. Its `AGENTS.md` is the canonical,
  full case-building procedure — **that's where you want to be** if
  you're adding, fixing, or auditing a case. This file doesn't duplicate
  that procedure; go there directly.

**If you're building or maintaining a case, start at
`forensic-agent-answers/AGENTS.md`, not here.** This file exists only to
orient a fresh session to the umbrella structure before it goes to the
repo that actually matters for the task at hand.

There is one workstream that belongs to neither repo:

- **`eval-harness/`** (this directory) — a real, working Docker harness
  that runs Hermes (backed by Qwen) against a case, one manual run at a
  time, behind an in-container egress lockdown, plus the judge that grades
  the resulting `QUESTION_ANSWERS.md`. This *is* built and tested, but
  it's a spike run by hand one case at a time, not an automated pipeline.
  See `eval-harness/docker/run-case.sh` to run a case and
  `eval-harness/docker/*.sh` for how the lockdown actually works; the
  judge's requirements and dated design decisions are in
  `eval-harness/judge/DESIGN.md`, and `eval-harness/CODING_STANDARDS.md`
  is binding for code there.

Once the two projects actually split into separate repositories, this
file and the umbrella's own `.git` go away — don't add new durable content
here that would need migrating; put it in whichever of the two repos it
actually belongs to.

# AGENTS.md — d-agent-test (umbrella, temporary)

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

Once the two projects actually split into separate repositories, this
file and `d-agent-test/`'s `.git` go away — don't add new durable content
here that would need migrating; put it in whichever of the two repos it
actually belongs to.

# d-agent-test

Working umbrella for two independent projects. Right now everything here is
one throwaway git repo (`origin` = `github.com/laconic-mercenary/d-agent-test`,
currently private) that will eventually be split apart — don't push `main`
as more than a private working copy in the meantime.

- **`forensic-agent-tests/`** — DFIR benchmark cases (evidence + task
  instructions) for evaluating LLM agents. Own `README.md`/`AGENTS.md`.
- **`forensic-agent-answers/`** — held-out answer keys, grading rubrics,
  and the full case-building methodology, paired by case slug with
  `forensic-agent-tests/cases/`. Own `README.md`/`AGENTS.md` — **this is
  where case-building work happens**, see its `AGENTS.md`.

**Known gap, not yet fixed**: the root `.gitignore`'s
`forensic-agent-answers/` entry is comment-only — there's no actual
ignore pattern under it, so despite the intent that this directory stay
out of this repo's history, it has in fact already been committed and
pushed to the (private) `origin` remote above. This is a known, accepted
state pending the actual repo split — see
`forensic-agent-answers/AGENTS.md`'s "Known pitfalls" for detail. Don't
assume the directory boundary is an access-control boundary yet.

Eventually each moves into its own permanent repository, at which point this
top-level folder and its `.git` go away.

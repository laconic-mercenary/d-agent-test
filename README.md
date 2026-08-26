# d-agent-test

Working umbrella for two independent projects. Right now everything here is
one throwaway git repo (`origin` = `github.com/laconic-mercenary/d-agent-test`)
that will eventually be split apart — don't push `main` as-is once
`forensic-agent-answers/` has real content.

- **`forensic-agent-tests/`** — DFIR benchmark cases (evidence + task
  instructions) for evaluating LLM agents.
- **`forensic-agent-answers/`** — held-out answer keys and grading rubrics,
  paired by case slug with `forensic-agent-tests/cases/`. Listed in
  `.gitignore` at this root so it can never be swept into this repo's
  history by accident; it isn't its own git repo yet.

Eventually each moves into its own permanent repository, at which point this
top-level folder and its `.git` go away.

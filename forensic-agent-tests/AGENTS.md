# AGENTS.md — forensic-agent-tests (repo root)

This is the root-level router for this repo. It is **not** a specific
case's task briefing — if you were pointed at this repo to investigate a
specific case, that case has its own `cases/<slug>/AGENTS.md`, and that
file (not this one) is your actual entry point.

## If you are an agent-under-test working a specific case

Go to `cases/<slug>/AGENTS.md` for the case you were assigned and follow
it. Don't read other cases in this repo, and don't read this file for
anything beyond this notice — it isn't part of any case's evidence or
task, and nothing here should factor into your investigation or answers.

## If you are doing maintenance on this repo (adding, fixing, or auditing a case)

Stop — this isn't the right place. This repo (`forensic-agent-tests`)
holds only finished, independently-audited evidence and task files; it
never holds scenario-authoring input, answer keys, grading rubrics, or
the build methodology. All of that lives in the sibling
`forensic-agent-answers` repo — see that repo's `AGENTS.md` for the full
case-building procedure. Nothing should be authored or edited directly
in this repo outside of a finished port-over from that process.

## Layout

See `README.md` for the case table and directory layout.

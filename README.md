# Evaluation Suite for Forensic Investigation LLM Assistants

A DFIR benchmark for evaluating LLM agents, plus a Docker harness to run
one against it.

Cases hand an agent realistic evidence (Windows/Linux logs, network
traffic, email) and grade it on reconstructing events, identifying the
actor, judging whether it was malicious, and reporting soundly. Answer
keys live in a separate directory the agent-under-test never sees.

Umbrella for two independent projects plus the harness connecting them —
one shared private git repo for now, splitting into separate repos later.
Don't push `main` as more than a working copy.

## Start here

| You are... | Go to |
|---|---|
| A human running an agent against a case | [`eval-harness/docker/run-case.sh`](eval-harness/docker/run-case.sh) — its header comments are the procedure |
| A human building/fixing/auditing a case | [`forensic-agent-answers/AGENTS.md`](forensic-agent-answers/AGENTS.md) |
| A human wanting the case set and what each tests | [`forensic-agent-tests/README.md`](forensic-agent-tests/README.md) |
| An **agent-under-test** assigned a case | `forensic-agent-tests/cases/<slug>/AGENTS.md` — nothing else here |
| An **agent** doing general work in this repo | [`AGENTS.md`](AGENTS.md) |
| Anyone wanting the judge harness's design | [`eval-harness/judge/DESIGN.md`](eval-harness/judge/DESIGN.md) |

**Agents-under-test**: read only your case's `AGENTS.md`. Never read
`forensic-agent-answers/` — see Status below for what does and doesn't
enforce that.

## Layout

- **`forensic-agent-tests/`** — the benchmark: 14 self-contained cases,
  evidence + task instructions only.
- **`forensic-agent-answers/`** — held-out answer keys and case-building
  methodology, paired by slug. Case-building work happens here.
- **`eval-harness/`** — Docker harness running Hermes/Qwen against a case,
  egress-locked, plus the judge that grades the result. A manual spike, run
  one case at a time; not an automated pipeline. `docker/run-case.sh` runs
  a case, `judge/DESIGN.md` covers the grading side.

## Sources

Case evidence comes from two places:

- **[EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge)** (Cisco
  Talos, MIT) — synthetic evidence generator, used for most cases.
- **[JPCERT/CC](https://github.com/JPCERTCC/log-analysis-training_v2)** —
  Japan's national CERT; two cases (`windows-log-search-basics`,
  `windows-lateral-movement-ntds-exfil`) use real JPCERT-published
  training data instead of synthetic evidence.

Full sourcing detail, licensing, and candidate/rejected sources:
`forensic-agent-answers/doc/SOURCES.md`.

## Status & caveats

**Answer keys aren't access-controlled, just conventionally separated.**
`forensic-agent-answers/` is meant to be gitignored but isn't (a
comment-only pattern) — it's already in this repo's history. Known,
pending the split.

**`eval-harness/` contains part of the blast radius**: its container only
ever mounts one case's evidence, never `forensic-agent-answers/`, and
can't reach the network beyond its model endpoint. Outside that container,
on this checkout, both directories still sit side by side — full
separation waits on the repo split.

**At split time**, `eval-harness/` needs a new home too — it belongs to
neither existing project.

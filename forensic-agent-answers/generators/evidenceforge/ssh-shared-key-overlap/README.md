# Generator: ssh-shared-key-overlap

`scenario.yaml` is authored for
[EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge) (Cisco Talos,
MIT) and drives deterministic generation of the case's `data/`.

**EvidenceForge version/commit used:** not yet reconfirmed against the live
checkout — this case predates setting up
`/Users/mlcs/Documents/github/EvidenceForge`. Other cases in this repo have
been confirmed against v1.17.0 (commit `567073b0`); treat this one as
provisionally the same until it's actually regenerated and checked.

## Regenerate

```bash
cd /Users/mlcs/Documents/github/EvidenceForge
uv run eforge validate scenarios/ssh-shared-key-overlap/scenario.yaml
uv run eforge generate scenarios/ssh-shared-key-overlap/scenario.yaml --verbose --force
```

See this repo's root `AGENTS.md` for the full generate → port-over
workflow, and its "Environment setup" section if `uv sync` fails.

Generation seed: 42 — the scenario file itself doesn't set one explicitly,
so this is EvidenceForge's default seed, not a deliberate per-scenario
choice.

## Note on scope

This scenario is entirely benign — no attack, no malicious technique. The
only finding is a physically-impossible pattern (one identity, two
concurrent sessions, two source IPs) that a correct analysis should
recognize as anomalous without over-calling it an active compromise. See the
case's held-out `BRIEFING.md` for grading nuance, including two known
engine quirks in the rendered evidence (documented in
`supporting/KNOWN_DEFICIENCIES.md`) that a grader needs to know about but an
agent-under-test should not be penalized for missing.

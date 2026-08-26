# Generator: ssh-shared-key-overlap

`scenario.yaml` is authored for
[EvidenceForge](https://github.com/cisco-talos/EvidenceForge) (Cisco Talos,
MIT) and drives deterministic generation of the case's `data/`.

**EvidenceForge version/commit used:** not recorded — TODO, same gap as the
other generator entries in this repo. Fill in from whatever install produced
the data, or regenerate against a known version and note it here.

## Regenerate

```bash
eforge validate scenario.yaml
eforge generate scenario.yaml --verbose --force
```

Generation seed: 42 (recorded in the case's `data/COLLECTION_PROFILE.json`
as `generation_seed` — same value as the other cases in this repo, which
may just be EvidenceForge's default rather than an explicit per-scenario
choice; the scenario file itself doesn't set one).

## Note on scope

This scenario is entirely benign — no attack, no malicious technique. The
only finding is a physically-impossible pattern (one identity, two
concurrent sessions, two source IPs) that a correct analysis should
recognize as anomalous without over-calling it an active compromise. See the
case's held-out `BRIEFING.md` for grading nuance, including two known
engine quirks in the rendered evidence (documented in
`supporting/KNOWN_DEFICIENCIES.md`) that a grader needs to know about but an
agent-under-test should not be penalized for missing.

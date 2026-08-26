# Generator: rdp-remote-file-write

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

Generation seed: 42 (recorded in the case's `data/COLLECTION_PROFILE.json`).

## Known engine quirk affecting this scenario

The rendered evidence lands ~21 minutes later than the scenario's authored
relative offsets (`+20m`/`+22m`) — a session-bootstrap timing issue in the
engine's causal expansion for `rdp_session`, not an authoring error. If you
regenerate, expect the same divergence (deterministic given the seed) unless
this is fixed upstream. Full detail and the actual verified rendered
timestamps: `KNOWN_DEFICIENCIES.md` and `BRIEFING.md` in the case's held-out
answers directory.

## Note on scope

This scenario is entirely benign — a single remote session and a single
file save, no attack, no red herrings. It's the simplest case in this repo,
meant to test basic sequence reconstruction and actor attribution rather
than any judgment-under-ambiguity skill.

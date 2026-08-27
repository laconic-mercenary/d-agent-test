# Generator: single-host-linux-rce

`scenario.yaml` is authored for
[EvidenceForge](https://github.com/cisco-talos/EvidenceForge) (Cisco Talos,
MIT) and drives deterministic generation of the case's `data/`.

**EvidenceForge version/commit used:** not recorded — TODO. The generation
run that produced this case's `data/` didn't capture an `eforge --version` or
commit hash anywhere in the output. Fill this in from whatever install
produced the data, or regenerate against a known version and note it here.

## Regenerate

```bash
eforge validate scenario.yaml
eforge generate scenario.yaml --verbose --force
```

Generation seed: 42 (recorded in the case's
`data/COLLECTION_PROFILE.json` as `generation_seed`).

If `eforge validate` fails against whatever EvidenceForge version you're
running, check EvidenceForge's own scenario-schema changelog before assuming
this scenario file is broken — the schema has changed over time.

## Note on scope

EvidenceForge models telemetry (process/network/auth/file evidence), not
application-level vulnerabilities. This scenario's storyline documents "an
exploit against the config-import endpoint yields code execution as
www-data" at the process/network level; it does not (and cannot) generate an
application stack trace naming a specific vulnerability class. That gap is
intentional — see the case's held-out `BRIEFING.md` for how this affects
grading.

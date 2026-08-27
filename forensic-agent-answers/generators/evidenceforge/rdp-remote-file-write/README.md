# Generator: rdp-remote-file-write

`scenario.yaml` is authored for
[EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge) (Cisco Talos,
MIT) and drives deterministic generation of the case's `data/`.

**EvidenceForge version/commit used:** v1.17.0, commit `567073b0`. Local
checkout: `/Users/mlcs/Documents/github/EvidenceForge`. Author/iterate
scenarios there, not in this repo — see `../../../../AGENTS.md` (the
`d-agent-test` root) for the full workflow.

## Regenerate

```bash
cd /Users/mlcs/Documents/github/EvidenceForge
uv run eforge validate scenarios/rdp-remote-file-write/scenario.yaml
uv run eforge generate scenarios/rdp-remote-file-write/scenario.yaml --verbose --force
```

(If `uv sync` fails on a `cryptography`/`openssl-sys` build error, see the
"Environment setup" section of the `d-agent-test` root `AGENTS.md`.)

Generation seed: 42 — deterministic; confirmed identical output (timestamps,
`LogonId`, event counts) across three separate regeneration runs.

## Known engine quirks affecting this scenario

Both documented in full in `KNOWN_DEFICIENCIES.md` and `BRIEFING.md` in the
case's held-out answers directory
(`forensic-agent-answers/case-rdp-remote-file-write/`):

1. **Timing divergence.** Rendered evidence lands ~21 minutes later than the
   scenario's authored relative offsets (`+20m`/`+22m`) — a session-bootstrap
   timing issue in the engine's causal expansion for `rdp_session`, not an
   authoring error.
2. **Domain-style identity fields despite workgroup scope.** Confirmed via
   regeneration that `environment.identity.windows_default_scope: local`
   (both as a default and as an explicit per-user override, both present in
   this `scenario.yaml`) does not change the rendered `TargetDomainName`/
   `SubjectDomainName`/Sysmon `User` fields — they still render as
   `ALDERWOODPARTNERS` (derived from `environment.description`, not from any
   hostname). Not fixable at the scenario-authoring level. This is why the
   case's `ENVIRONMENT.md` no longer claims "no Active Directory."

Both are candidates for filing upstream against Cisco-Talos/EvidenceForge.

## Note on scope

This scenario is entirely benign — a single remote session and a single
process launch, no attack, no red herrings. It's the simplest case in this
repo, meant to test basic sequence reconstruction and actor attribution
rather than any judgment-under-ambiguity skill. Note: despite the case
name, there is no direct file-write (Sysmon Event 11) evidence for
`team-notes.txt` — this environment's Sysmon filtering config intentionally
excludes non-suspicious-location `.txt` writes. That's correct, realistic
behavior, not a gap to fix by regenerating; `EXAM.md`'s Q1 is worded to
account for it.

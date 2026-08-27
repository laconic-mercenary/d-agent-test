# Changelog — benign-breakglass-account

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project. This
  is the first purely benign case built from generated evidence this
  session — no attacker, no storyline, entirely `red_herrings` plus
  baseline noise, the Windows/AD companion to `ssh-shared-key-overlap`.
- `ENVIRONMENT.md` is human-authored; it documents the shared
  emergency-access account's purpose and informal review policy, both
  load-bearing for Q2/Q4.
- The environment's own baseline activity model independently
  generates a substantial number of Event ID 4648 records for
  `svc-breakglass` across all seven hosts — servers and workstations
  alike — attributed to `SYSTEM` via
  automated infrastructure processes — the same pattern documented in
  `credential-spray-domain-compromise` and `pth-lateral-logclear`. Not
  load-bearing for any exam question here (this case's central test is
  the interactive 4624 logons, which are cleanly isolated regardless),
  but noted in `BRIEFING.md` as expected background texture.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down.

# Changelog — dga-beacon-logclear

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project.
- `ENVIRONMENT.md` is human-authored.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down,
  including the exact DGA query counts (total, NXDOMAIN/resolved
  split) and beacon connection count, cross-checked against the
  generator's own structured event attributes (not its narrative
  summary, which — consistent with several other cases built this
  session — mislabeled the workstation's own local logon as an
  external "attacker" network logon with a fabricated source IP; see
  the paired generator directory's README).
- As with `pth-lateral-logclear`, this case's `log_cleared` event does
  not actually remove any prior evidence from the affected host's own
  log in this engine version — confirmed directly. Q5 tests whether
  the agent-under-test verifies this rather than assuming the clear
  succeeded.

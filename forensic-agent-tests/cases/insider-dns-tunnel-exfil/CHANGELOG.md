# Changelog — insider-dns-tunnel-exfil

## 1.1 — 2026-08-28

- **Fixed a real answer-key error in Q3, found by an independent Phase
  6 audit run immediately after the initial build.** The DNS-tunnel
  volume-share figure in `BRIEFING.md`/`grading_schema.md` divided the
  tunnel's 464 queries by the network sensor's all-host DNS total
  (2,135 records, across all 4 monitored hosts), giving ~21.7% — but
  the question asks for *this host's own* DNS volume share, which is
  464 / 875 (`WS-SNAKAMURA-01`'s own record count) ≈ 53.0%. An answer
  correctly computing the host-specific figure would have been marked
  down against the old (wrong) expected value. Fixed to the correct
  per-host denominator.
- No other issues found — see the independent audit's report for the
  full verification trail (staging event, decoy event, tunnel
  mechanics, and the Stage 1 logon correction were all independently
  re-derived from raw data and matched exactly).

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project. Third
  case built purely from generated (not real-world) evidence this
  session, and the first with no attacker account at all — a single
  legitimate account doing something legitimate access doesn't explain.
- `ENVIRONMENT.md` is human-authored; it documents which accounts have
  legitimate access to the finance share and the organization's stated
  (unwritten but consistently enforced) data-handling expectations,
  both load-bearing for Q4/Q5.
- The environment's own baseline activity independently generated a
  second, unrelated file-archiving event by the same user later the
  same day (a routine local log backup) — not designed in, found by
  inspecting the rendered data directly. Q1 was built around requiring
  the correct one to be identified, not assumed to be the only such
  event present.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down,
  including cross-checking a generator ground-truth claim that turned
  out to be inaccurate (wrong timestamp, wrong logon type label, and a
  fabricated source IP for the account's own local logon) — see the
  paired generator directory's README for detail.

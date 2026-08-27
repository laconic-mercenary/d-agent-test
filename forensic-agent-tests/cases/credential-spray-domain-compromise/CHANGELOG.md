# Changelog — credential-spray-domain-compromise

## 1.1 — 2026-08-28

- **Fixed a real answer-key gap in Q3/Q4, found by an independent Phase
  6 audit run immediately after the initial build.** `svc-sql` actually
  logs on twice within a 4-second window — a local logon on
  `WS-DFOSTER-01` (Logon Type 2) immediately followed by the RDP logon
  onto `DC-01` (Logon Type 10) that the original answer key treated as
  the only relevant event. Both are a genuine, valid answer to "the next
  time svc-sql logs on anywhere in this data" (Q3's literal wording); the
  local one is chronologically first. Updated `grading_schema.md` to
  accept either event for Q3 and Q4. Not a data problem — this is a
  real, well-formed causal chain the generator produces automatically
  for any remote-session event (source-side local logon before the
  remote transport) — the answer key just hadn't accounted for both
  ends of it.
- Reworded `EXAM.md` Q1 slightly — the successful compromise logon is
  recorded on a different host's log than the failed spray attempts;
  the question now says so explicitly rather than reading (even if not
  strictly requiring) as scoped to one host.
- No leak, no other issues — see the independent audit's report for the
  full verification trail (every other fact in Q1-Q6 was independently
  re-derived from raw data and matched exactly).

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project. Second
  case built purely from generated (not real-world) evidence this
  session.
- `ENVIRONMENT.md` is human-authored; it documents a standing
  service-account privilege misconfiguration and two legitimate,
  routine automated consumers of that account's credentials, both
  load-bearing for Q2's discrimination question.
- The exam question testing Kerberoasting-style credential-request
  activity (Q2) was designed around a real discrimination signal found
  by inspecting the generated data directly, not assumed in advance —
  the environment's own baseline activity automatically produces
  several *other* explicit-credential-usage events for the same target
  account, all attributable to routine automated processes. The one
  attacker-authored event stands out by subject account and process,
  not by being the only such event in the data. See the paired
  generator directory's notes for detail (not linked here; that
  directory isn't part of what the agent under test sees).
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down.

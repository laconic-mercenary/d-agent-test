# Changelog — phishing-c2-beacon

## 1.1 — 2026-08-28

- **Fixed a real off-by-one in Q4's evidence framing, found by an
  independent Phase 6 audit run immediately after the initial build.**
  Of the 39 total connections to the C2 destination, the case's v1.0
  materials described "38 share a byte profile, 1 doesn't" — actually,
  the very first connection (immediately after DNS resolution) is a
  distinct third thing: the stager fetching its next-stage script, not
  a beacon check-in at all. Only 37 connections share the routine
  profile. `EXAM.md` Q4 now explicitly carves out the stager-fetch
  connection before asking about "the remaining 38." `BRIEFING.md` and
  `grading_schema.md` updated to match, and now credit an answer that
  separately notices the stager-fetch connection as an additional
  correct observation rather than treating it as the Q4 answer.
- **Fixed Q1's attachment-metadata citation**, also found by the audit:
  the email evidence (`zeek01/smtp.json`) does not actually carry
  attachment filename/MIME-type fields for this message (`fuids: []`)
  — the v1.0 answer key claimed this data came from the SMTP log, which
  is wrong. The attachment's filename (and the file type implied by its
  extension) is only recoverable from `WS-JOKAFOR-01`'s Windows
  evidence. `EXAM.md` Q1 reworded to make clear these are two separate
  facts from two separate evidence sources.
- No other issues found — see the independent audit's report for the
  full verification trail (SMTP delivery facts, process-lineage-absence
  claim, DNS resolution, Stage 1 logon correction, and leak posture all
  independently re-derived from raw data and matched).

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project.
- `ENVIRONMENT.md` is human-authored; it documents this organization's
  mail-handling posture (no attachment sandboxing/macro-blocking),
  relevant context for why the phishing attachment was delivered
  unmodified.
- **A real engine-behavior finding, not designed in:** the storyline
  authored an explicit parent/child process link (Word opening the
  attachment, then a macro-launched PowerShell stager) using the
  scenario schema's `process_ref`/`parent_ref` fields. The rendered
  Windows Security (4688) and Sysmon (Event 1) logs do **not** reflect
  that link — both processes render with `explorer.exe` as their
  parent, the ordinary default for a process without a
  spawn-rules-registered valid parent. Rather than treat this as a
  defect to route around silently, Q2 was built directly around the
  gap: the exam explicitly tells the agent this link isn't visible in
  parent-process evidence and asks it to reason from timing and
  command-line content instead — a realistic analyst skill for
  environments with incomplete process-lineage visibility. See the
  paired generator directory's README for the full technical detail.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down,
  including the byte-size discrimination signal in Q4 (38 routine
  beacon connections vs. exactly 1 outlier).
- The generated `.eml` email artifact (`artifacts/email/` at the
  generator level) was deliberately **not** ported into this case's
  evidence — its synthetic attachment content, once base64-decoded,
  embeds this scenario's internal storyline event ID in plaintext. This
  is documented as a reusable lesson in the paired generator README and
  in this project's root `AGENTS.md`. The case's email evidence instead
  comes from the network sensor's SMTP log record, which was checked
  and contains no such leak.

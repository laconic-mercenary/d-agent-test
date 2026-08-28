# Changelog — windows-log-search-basics

## 1.3 — 2026-08-27

- **Fixed a systematic 9-hour timestamp error in the answer key**, found by
  an independent audit and independently re-verified against the raw
  `data/*.jsonl` before correcting. All three questions' documented answers
  had been transcribed from the source PDF's Event Viewer screenshots,
  which render local JST (UTC+9) time, without converting to UTC or
  checking against the actual `SystemTime` field in the converted data
  (which is genuinely UTC) — this directly contradicted this case's own
  `AGENTS.md`/`TASK.md`, which correctly state all timestamps are UTC. No
  change to `EXAM.md` itself (it never stated a time), no change to which
  events/fields are cited as evidence — only the stated clock times in
  the held-out answer key were wrong, and only those were corrected.
- **Fixed a real answer-key gap on Q2**: `data/sample1.jsonl` contains a
  second, genuine Type-10 RDP logon (`domadm`, `2023-07-21 09:45:24` UTC)
  that the source PDF doesn't document and the answer key didn't account
  for. `EXAM.md` Q2's wording doesn't constrain which logon the agent
  finds, so this is now documented as an equally valid second answer
  rather than an undocumented ambiguity a correct AUT could be marked
  down for finding.
- No leak, no data self-contradiction — the underlying event data was
  always correct; only the answer key's transcription was wrong.

## 1.2 — 2026-08-27

- Packaged `data/sample1.jsonl`/`sample2.jsonl` as `.tar.gz` (gzipped tar,
  each ~2.3-2.4MB compressed vs. ~35-40MB raw) rather than committing the
  raw JSON Lines text. `AGENTS.md`/`TASK.md` now instruct unpacking as the
  first step. Verified round-trip integrity (line count and byte size
  match the uncompressed originals) before committing.

## 1.1 — 2026-08-27

- Converted `data/sample1.evtx`/`sample2.evtx` (binary EVTX) to
  `data/sample1.jsonl`/`sample2.jsonl` (JSON Lines, one event per line),
  using `evtx_dump`. Goal: remove the dependency on EVTX-specific parsing
  tools (`python-evtx`, `Get-WinEvent`, Event Viewer) — any agent that can
  read text/JSON can now attempt this case. Field names are unchanged
  (native EVTX schema), so existing question/answer-key wording still
  applies without modification.
- This conversion surfaced that the underlying data contains more
  identifying/incidental content than a binary-only grep audit had caught
  (binary EVTX text is UTF-16-encoded inside a compressed structure, which
  a naive `grep -a` only partially matches). Rather than scrub this
  content out, the project decision was to leave it as-is and document it
  in the answer key as expected background noise — see the paired answers
  repo's `BRIEFING.md`. This does not affect any graded question.

## 1.0 — 2026-08-27

- Initial case build, sourced from real (not synthetic) Windows Event Log
  data. Evidence files copied as-is; no `ENVIRONMENT.md` (none applies —
  see `TASK.md`).
- Authored `AGENTS.md`, `TASK.md`, `EXAM.md` (3 questions). A fourth
  candidate question (filtering an Event ID range) was dropped — the
  source material demonstrates the filter mechanic but never shows its
  result, so no ground truth was available for it without independent
  EVTX tooling; rather than fabricate an answer, it was cut.
- See the paired answers repo for source provenance and a known
  inconsistency in the upstream source material affecting Q2.

# Test Case Matrix

Case-centric complement to `TEST_OBJECTIVES.md` (which is category-centric).
One row per actual case — nothing here is a placeholder for a case that
doesn't exist yet; see "Coverage Gaps" at the bottom for what's still
unbuilt.

**Column definitions:**

- **1-9** — the `TEST_OBJECTIVES.md` categories (legend below). **X** means
  at least one `EXAM.md` question genuinely requires that category's
  specific investigative mechanics to answer — not just "the case happens
  to involve logs" or "one question generically asks if anything bad
  happened." E.g. a benign case's "is there evidence of an attack?"
  question doesn't earn an X in category 6 (Intrusion Path Identification)
  unless there's an actual technique/vector to reconstruct — there isn't,
  so it doesn't.
- **Tools Used** — what generated or supplied the case's evidence. Either
  EvidenceForge (version/commit noted, since not all cases have been
  reconfirmed against the live checkout — see `../AGENTS.md`) or, for
  cases sourced from a real external corpus, the source and its `SOURCES.md`
  status.
- **Skills Enabled** — the specific `Anthropic-Cybersecurity-Skills` entries
  relevant to this case's questions. This is the library the AUT is
  actually enriched with (see `TEST_OBJECTIVES.md`'s AUT-toolkit note) —
  not the other two repos surveyed there, which aren't adopted for AUT use.

**Category legend:** 1 Log Analysis · 2 Browser History · 3 Account
Activity · 4 Network Connection History · 5 Timeline Reconstruction · 6
Intrusion Path ID · 7 Lateral Movement · 8 Data Exfiltration · 9 Report
Generation

## Matrix

| Test Case | Status | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | Tools Used | Skills Enabled |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ssh-shared-key-overlap` | Active | X | | X | X | X | | | | X | EvidenceForge — version/commit not yet reconfirmed against the live checkout (predates it) | - `analyzing-linux-audit-logs-for-intrusion`<br>- `detecting-service-account-abuse` |
| `rdp-remote-file-write` | Active | X | | X | X | X | | | | | EvidenceForge v1.17.0, commit `567073b0` | - `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation`<br>- `building-super-timelines-with-plaso` |
| `single-host-linux-rce` | **Discarded** — see `../forensic-agent-tests/_discarded/single-host-linux-rce/WHY_DISCARDED.md` | X | | X | X | X | X | X | | X | EvidenceForge, seed 42 — version at original generation not recorded; reproduction for upstream bug filing targets v1.17.0/`567073b0` per `WHY_DISCARDED.md` | - `analyzing-cyber-kill-chain`<br>- `collecting-indicators-of-compromise`<br>- `performing-log-analysis-for-forensic-investigation`<br>- `analyzing-linux-audit-logs-for-intrusion` |
| `windows-log-search-basics` | Active | X | | | | | | | | | Real (not synthetic) data from `JPCERTCC/log-analysis-training_v2`, `Hands-on/basis/` (`SOURCES.md`: Candidate — informal license, risk accepted). No incident narrative by design — pure log search/filtering test. | - `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation` |

Note on the discarded row's 7 (Lateral Movement): its X comes from Q10,
which requires checking specific cross-host/cross-account evidence (WS-OP-01,
`sam.ortiz`) for pivot indicators — a real (if negative) lateral-movement
check, unlike category 6 in the two active cases where the question is a
generic "was anything malicious happening" catch-all with no path to trace.

## Coverage Gaps

Among **active** cases only:

- **Category 2 (Browser History)** — zero coverage anywhere, active or
  discarded. Known deficiency (see `TEST_OBJECTIVES.md`); no tool in the
  current pipeline produces browser artifacts.
- **Category 6 (Intrusion Path Identification)** — zero active coverage.
  The one case that tested this for real is discarded.
- **Category 7 (Lateral Movement)** — zero active coverage, and even the
  discarded case's touch was a negative-only check, not a positive
  trace-the-pivot test.
- **Category 8 (Data Exfiltration Indicator Analysis)** — zero coverage
  anywhere, active or discarded. Nearest miss was the discarded case's Q6,
  which covers an *ingress* tool transfer (T1105), not exfiltration.
- **Category 9 (Report Generation)** gets a real question in
  `ssh-shared-key-overlap`, but it's one question among seven, not a
  dedicated report-generation case.

Categories 1, 3, 4, 5 are reasonably exercised across the three active
cases — category 1 now has a dedicated case (`windows-log-search-basics`)
rather than only incidental coverage. Next case built should likely target
6 and 7 together — a lateral-movement case naturally needs an initial
intrusion path to pivot from. `SOURCES.md`'s `log-analysis-training_v2`
`advance.pdf` entry is the identified candidate for that case.

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
| `windows-log-search-basics` | Active | X | | | | | | | | | Real (not synthetic) data from `JPCERTCC/log-analysis-training_v2`, `Hands-on/basis/` (`SOURCES.md`: Adopted). No incident narrative by design — pure log search/filtering test. | - `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation` |
| `windows-lateral-movement-ntds-exfil` | Active | X | | X | X | X | X | X | X | X | Real (not synthetic) data from `JPCERTCC/log-analysis-training_v2`, `Hands-on/advance/` (`SOURCES.md`: Adopted). Four-host, six-stage intrusion narrative — every fact independently re-derived from converted/raw data, not the source PDF's narrative (which itself contained two separate confirmed errors, resolved against raw data — see the case's `BRIEFING.md`). Richest single-case coverage in the matrix; only category 2 (Browser) is out of reach. | - `analyzing-cyber-kill-chain`<br>- `detecting-service-account-abuse`<br>- `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation` |
| `external-recon-no-breach` | Active | X | | | X | | X | | | X | EvidenceForge v1.17.0, commit `567073b0`. First case built from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #9). No attacker storyline — a port scan gets denied except for two ports (one inert, one a single failed SSH login); tests restraint from the opposite direction of `ssh-shared-key-overlap` (network-recon noise vs. account-overlap noise). Caught and fixed a real generator-tooling bug (`port_scan` self-targeting its own segment silently produced zero evidence) and a `GROUND_TRUTH.md` accuracy defect independent of that bug — see the case's `CHANGELOG.md`/paired generator README. | - `performing-log-analysis-for-forensic-investigation`<br>- `analyzing-cyber-kill-chain` |
| `credential-spray-domain-compromise` | Active | X | | X | | X | X | X | | X | EvidenceForge v1.17.0, commit `567073b0`. Second case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #1). A spray-compromised employee account escalates via a Kerberoasting-consistent credential request to an over-privileged service account; tests whether the AUT separates "how they got in" from "what they compromised." The key discrimination signal (one attacker-authored Event 4648 among several legitimate ones for the same account) came from the engine's own baseline realism, not deliberate scenario design — verified directly against raw data before the exam was written around it. | - `analyzing-cyber-kill-chain`<br>- `detecting-service-account-abuse`<br>- `performing-log-analysis-for-forensic-investigation` |
| `insider-dns-tunnel-exfil` | Active | X | | X | X | | | | X | X | EvidenceForge v1.17.0, commit `567073b0`. Third case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #2). No attacker anywhere — a finance analyst with entirely legitimate access archives client files and exfiltrates them via a ~2-hour DNS-tunnel to a domain never otherwise seen in the environment. Tests discrimination against a decoy archiving event (unrelated legitimate backup) and restraint on the "unauthorized access" question (correct answer: no). | - `performing-log-analysis-for-forensic-investigation`<br>- `extracting-windows-event-logs-artifacts` |
| `phishing-c2-beacon` | Active | X | | | X | X | X | | X | X | EvidenceForge v1.17.0, commit `567073b0`. Fourth case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #3). Phishing attachment → macro-launched PowerShell → periodic HTTPS beacon; among 39 total connections to the C2 host, one carries a manual attacker command distinguishable only by byte volume. A confirmed engine limitation (`process_ref`/`parent_ref` did not produce the declared parent-child lineage in rendered logs) meant Q2 had to be redesigned around timing/command-content correlation instead of process lineage — a deliberate, documented gap in the evidence, not a bug the exam papers over. | - `analyzing-cyber-kill-chain`<br>- `performing-network-traffic-analysis-with-zeek`<br>- `extracting-windows-event-logs-artifacts` |
| `websqli-webshell-pivot` | Active | X | | | X | X | X | X | | X | EvidenceForge v1.17.0, commit `567073b0`. Fifth case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #4). SQL injection against a public web app → webshell → pivot to an internal file server over an unrevoked legacy firewall exception. Both central discrimination signals (the real breach vs. ~255 automated scan requests; the real pivot vs. a routine database-backup connection to the same target) came from the engine's own baseline/scan realism, verified directly before the exam was written, not designed in. | - `analyzing-cyber-kill-chain`<br>- `performing-network-traffic-analysis-with-zeek`<br>- `performing-log-analysis-for-forensic-investigation` |
| `pth-lateral-logclear` | Active | X | | X | | X | | X | | X | EvidenceForge v1.17.0, commit `567073b0`. Sixth case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #5). A cloned local-admin credential is used to authenticate to three file servers within ~12 minutes, then the Security log on the middle host is cleared. A confirmed engine limitation (`AuthenticationPackageName` for network logons is a fixed 70/30 Kerberos/NTLM random roll, independent of account scope) forced the exam away from an "NTLM-where-Kerberos-expected" signal toward the account's cross-host identity/timing pattern instead. Also confirms `log_cleared` does not remove prior log content in this engine version — the exam tests whether the AUT verifies that rather than assumes it. | - `detecting-lateral-movement-in-network`<br>- `performing-active-directory-compromise-investigation`<br>- `extracting-windows-event-logs-artifacts` |
| `benign-breakglass-account` | Active | X | | X | | X | | X | | X | EvidenceForge v1.17.0, commit `567073b0`. Seventh case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #6), the Windows/AD companion to `ssh-shared-key-overlap`. No attack at all — two on-call sysadmins share a documented break-glass account across two separate off-hours occasions; a third, unrelated employee's late-night activity is a deliberate distractor. Mirrors `ssh-shared-key-overlap`'s grading philosophy directly: penalizes both false-positive escalation and under-investigation equally. | - `detecting-service-account-abuse`<br>- `performing-log-analysis-for-forensic-investigation`<br>- `extracting-windows-event-logs-artifacts` |
| `dga-beacon-logclear` | Active | X | | | X | X | | | X | X | EvidenceForge v1.17.0, commit `567073b0`. Eighth case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #7). A masquerading executable drives a DGA domain-hunt (91 queries, 87 NXDOMAIN) before establishing a 5-hour beacon; tests whether the AUT characterizes the search pattern quantitatively rather than citing only the one domain that resolved. Second confirmation this session that `log_cleared` doesn't remove prior log content — the exam again tests verification over assumption. | - `hunting-for-data-exfiltration-indicators`<br>- `performing-network-traffic-analysis-with-zeek`<br>- `extracting-windows-event-logs-artifacts` |
| `departing-employee-email-exfil` | Active | X | | | X | X | | | X | X | EvidenceForge v1.17.0, commit `567073b0`. Ninth case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #8). The simplest technical case in the set by design — no attacker, no exploit; a departing employee with entirely legitimate access emails three attachments to his personal address. A real Phase 2 finding (default outbound STARTTLS made every message, including the exfiltration emails, render with blank sender/recipient fields) meant the case was silently unanswerable until fixed. Tests report register/tone as much as fact-finding — over- or under-dramatizing the finding are both graded. | - `hunting-for-data-exfiltration-indicators`<br>- `performing-log-analysis-for-forensic-investigation` |
| `rogue-service-account-privcreep` | Active | X | | X | | X | | X | | X | EvidenceForge v1.17.0, commit `567073b0`. Tenth and final case from `TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposal #10). A service account documented for one unattended automated purpose gets invoked interactively and used to add itself to Domain Admins; tests whether the AUT identifies the explicit-credentials event itself — not the later group-membership change — as the earliest point a control should have fired. The richest discrimination signal (22 legitimate credential-usage events across all four hosts, several using the same process the attacker used) came from the engine's own baseline realism; an independent audit caught the first answer-key draft understating host coverage and wrongly treating process name as reliable — `SubjectUserName` is the only fully reliable signal, fixed before shipping. | - `detecting-service-account-abuse`<br>- `performing-active-directory-compromise-investigation`<br>- `extracting-windows-event-logs-artifacts` |

Note on the discarded row's 7 (Lateral Movement): its X comes from Q10,
which requires checking specific cross-host/cross-account evidence (WS-OP-01,
`sam.ortiz`) for pivot indicators — a real (if negative) lateral-movement
check, unlike category 6 in the two active cases where the question is a
generic "was anything malicious happening" catch-all with no path to trace.

Note on `external-recon-no-breach`'s 6 (Intrusion Path ID): its X is
deliberately a *negative* result, not a catch-all question — Q5
specifically requires checking multiple named hosts individually for any
sign of compromise/follow-on activity before concluding no intrusion
path exists, the same standard the discarded row's 7 note above holds
lateral-movement checks to. This is different from a case that never
asks the question at all.

Note on `insider-dns-tunnel-exfil`'s 3 (Account Activity): its X is
also a negative result — Q4 requires citing the specific Event ID,
Logon Type, and source field to justify "no unauthorized access," not
a generic "nothing seemed wrong." Same standard as above.

Note on `benign-breakglass-account`'s 7 (Lateral Movement): category
7's own definition in `TEST_OBJECTIVES.md` explicitly covers "in a
benign case, a legitimate user working across systems" — Q1 requires
tracing the shared account across two host pairs (`APP-01`→`DB-01`,
`FILE-01`→`DC-01`) and correctly grouping them into occasions, a real
(if benign) cross-host correlation task, not a catch-all.

## Coverage Gaps

Among **active** cases only:

- **Category 2 (Browser History)** — zero coverage anywhere, active or
  discarded. Known deficiency (see `TEST_OBJECTIVES.md`); no tool in the
  current pipeline produces browser artifacts. The only category with no
  identified near-term path to coverage, and now the *only* structural
  gap left in the entire matrix.

Categories 1, 3, 4, 5, 6, 7, 8, and 9 are now all covered by multiple
active cases apiece — as of the eight cases added from
`TEST_EVIDENCEFORGE_PROPOSED_CASES.md` (proposals #2-#8 and #10; #1 and
#9 were built earlier in the same effort), category 9 (Report Generation)
in particular went from
"only two cases touch it generically" to real, question-level report/
recommendation/register tests in most of the newly-built cases
(`insider-dns-tunnel-exfil`, `phishing-c2-beacon`,
`websqli-webshell-pivot`, `pth-lateral-logclear`,
`benign-breakglass-account`, `dga-beacon-logclear`,
`departing-employee-email-exfil`, `rogue-service-account-privcreep`),
closing the "no case dedicated to report generation" gap this section
previously flagged. `departing-employee-email-exfil` is the closest
thing to a case *dedicated* to category 9 — its central test is report
register/tone, not investigative depth.

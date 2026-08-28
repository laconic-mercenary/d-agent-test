# Sources

A registry of everything that can supply or generate evidence for a test
case — used during the **proposal phase** of `TEST_CASE_PROCESS.md`, before
any building starts. A source appearing here is tracked, not necessarily
usable yet: check `Status` before proposing a case against it.

**Status values:**
- **Adopted** — actually in use, has a working pipeline into
  `forensic-agent-tests`.
- **Candidate** — vetted enough to propose a case against, not yet used.
- **Reference-only** — useful for validation/inspiration, not a case source
  itself (e.g. a parser-testing corpus).
- **Rejected** — considered and explicitly declined; kept here with the
  reason so it doesn't get re-proposed without new information.

**Principle carried over from the original design brief**: external
datasets (anything not `Adopted`) are referenced by link + hash in a case's
instructions, never vendored into the repo. This applies regardless of
license — it's about not owning a copy of someone else's dataset, not just
what the license permits. **One explicit, deliberate exception**:
`log-analysis-training_v2` (row below) is vendored directly into
`cases/<slug>/data/` for both cases built from it, per project decision —
"exploit JPCERT maximally given its authenticity, risk accepted." Don't
treat that as license to vendor other Candidate sources without the same
explicit conversation.

**Sanitization note**: every non-EvidenceForge source below is real-world
data or real-world-derived, which means it needs the same kind of
leak/fingerprint audit we do on EvidenceForge output before it's AUT-facing
— plus, likely, reorganizing into our case bundle shape (`data/` +
`AGENTS.md`/`TASK.md`/`EXAM.md` + held-out answers). None of this is
plug-and-play; treat "adopt" as "adopt after rework," not "adopt as-is."

## Generators

Things that produce fresh evidence on demand, rather than a fixed download.

| Source | Status | Fidelity | Determinism / Reproducibility | License | Notes |
|---|---|---|---|---|---|
| **EvidenceForge** | Adopted | Modeled | Deterministic — same scenario + seed reproduces byte-identical output (verified repeatedly this session) | MIT | The only thing we currently generate with. See `../AGENTS.md` for the full workflow. |
| Custom benign script generator | **Rejected** | Modeled | Would have been deterministic (seeded, our own code) | N/A (ours) | Originally planned in the earliest design brief for simple multi-actor benign cases. Dropped — redundant with EvidenceForge's own benign-scenario capability (see `ssh-shared-key-overlap`, `rdp-remote-file-write`); not worth building and maintaining a second generator for the same coverage. |
| Playwright / Selenium (real browser automation) | Candidate | **Real** — genuine browser engine producing genuine SQLite history/cache/downloads databases | High if the navigation script is fixed and deterministic; real-world page content (ads, dynamic elements) can introduce some non-determinism unless targets are also controlled | Apache-2.0 (both) | The identified path to closing the category-2 (browser) known deficiency for real, not just referencing CFReDS. Script a persona's session against controlled or archived pages, harvest the resulting profile directory. Needs its own case-bundle design — nothing built yet. |
| Atomic Red Team | Candidate, with a caveat | Real | Technique execution is scripted/repeatable; **captured telemetry is not** — ART itself produces no logs, only attack activity. Logs only exist if a collector (Sysmon, EDR, auditd) is already deployed and configured on the target. Reproducibility of the *evidence* depends entirely on pinning that collector config too. | MIT (verify against current repo before adoption) | Requires standing up real or virtual instrumented infrastructure — a step change from EvidenceForge's zero-infra model. Matches the `Environment: VM/Container` / `Fidelity: Real` tier the original taxonomy explicitly deferred. Not a near-term source until that infra exists. |
| MITRE CALDERA | Candidate, same caveat as ART | Real | Same as ART — emulation is scripted, evidence capture depends on separately-deployed telemetry | Apache-2.0 | Adversary-emulation platform, broader/more automated than ART's single-technique scripts. Same infra prerequisite as ART. |

## Hybrid (static captures + re-runnable simulation)

| Source | Status | Fidelity | Determinism / Reproducibility | License | Notes |
|---|---|---|---|---|---|
| OTRF Security-Datasets (Mordor) | Candidate | Real — captured from actual technique execution, not synthetic | The pre-captured files are static/fixed (stable once downloaded); a subset also ships simulation scripts that re-run the technique in a lab to reproduce the capture — reproducible *if* the same lab environment is stood up, not reproducible from the script alone | MIT per the project site (`securitydatasets.com`); one secondary source flagged GPL-3.0 for the GitHub repo — **confirm directly against the repo's `LICENSE` file before use**, don't trust either summary | Organized by platform (Windows/Linux/AWS) × ATT&CK technique. Datasets include both malicious *and* benign background events per capture, which is directly useful for realistic noise. Consumable via Jupyter notebooks. Exact wire format not yet confirmed hands-on (likely JSON-family event records) — verify before depending on it for anything. |
| [JPCERTCC/LogonTracer](https://github.com/JPCERTCC/LogonTracer) sample bundle | Candidate | Real — genuine binary EVTX, not synthetic | Static, fixed bundle (30.1MB `Security.evtx` + a pre-built Neo4j graph DB) | **BSD-3-Clause, confirmed** — `LICENSE.txt` at repo root (note: non-standard filename, `LICENSE.txt` not `LICENSE`, which is why GitHub's API license detector missed it and an earlier pass here wrongly called this unclear) | The tool itself (AD logon-graph visualization for lateral-movement detection) is reference-only; its bundled sample `Security.evtx` is real, licensed data we could actually use. No stated provenance for the sample (real captured AD environment vs. JPCERT's own lab) — confirm before treating it as "real-world," even though the license is now clear. |

## Static Corpora (reference by link + hash only)

| Source | Status | License | Notes |
|---|---|---|---|
| NIST CFReDS Data Leakage Case | Candidate | US government work — generally public domain domestically, confirm before any redistribution | The only surveyed source with analyst-conclusion-level ground truth (60 Q&A with an answer key), not just line-level labels. Needs disk-image case infrastructure we haven't built (mount/extract, not flat `data/`). Identified path to category-2 coverage alongside Playwright/Selenium above — likely complementary rather than either/or. |
| AIT Log Data Set v2.0 (Zenodo) | Candidate | Creative Commons — confirm exact variant before use | Real Linux-centric multi-service testbeds (mail, file share, WordPress, VPN, firewall); benign background + injected attack steps; labels directory mirrors the log directory. Fills EvidenceForge's auditd/VPN/PCAP gaps. Includes `dnsteal`-labeled DNS exfiltration — relevant to category 8. |
| EVTX-ATTACK-SAMPLES / EVTX-to-MITRE-Attack | Reference-only | Confirm before use | 270+ real *binary* EVTX files (not XML renderings) mapped to ATT&CK. Useful for validating that a parser/grading approach handles genuine EVTX, not for authoring a full case narrative from. |
| DARPA OpTC | Candidate | Public domain (DARPA release) | ~1TB, 500 hosts, 2 weeks, red-team ground truth PDF. Large-scale/needle-in-haystack tier — later-stage per the original design, not a near-term pick. |
| LANL Unified Host and Network Data Set (2018) | Candidate | Confirm LANL/DOE release terms before use | 90 days of real enterprise data, no malicious activity reported — a ready-made null-case substrate, though incidental rather than purpose-built as one. |
| [JPCERTCC/log-analysis-training_v2](https://github.com/JPCERTCC/log-analysis-training_v2) | **Adopted** — two active cases built from it (`windows-log-search-basics` from `basic.pdf`/`Hands-on/basis/`, `windows-lateral-movement-ntds-exfil` from `advance.pdf`/`Hands-on/advance/`) | No license file; README states *"自由にご利用ください"* ("please feel free to use it") plus a standard liability disclaimer — a real stated intent to permit use, but not a formal SPDX license. Don't treat as equivalent to the BSD-3-Clause row above; risk explicitly accepted per project decision. | `basic.pdf` (106pg): a technique/Event-ID reference plus mechanical query-tooling drills, no narrative case — see `windows-log-search-basics`. `advance.pdf` (40pg) is different in kind: **a complete, coherent multi-stage intrusion narrative**, built on real captured lab data (domain `HANDSONLAB.LOCAL`, not synthetic), spanning categories 6+7+8 in one story — VPN initial access → Pass-the-Hash lateral movement → rogue-account/RDP persistence → Kerberoasting escalation → domain-admin compromise + scripted credential reuse → NTDS.dit exfiltrated via Base64-encoded, chunked HTTP GETs through Squid — see `windows-lateral-movement-ntds-exfil`. Both PDFs contained real, independently-confirmed errors (not ours): `basic.pdf`'s problem/answer slides disagree on an account name (`jpcertuser` vs. `jpcertadmin`); `advance.pdf`'s exfil-stage detail slide and its own summary-timeline slide disagree on the transfer's time window (raw `access.log` data resolved this — see that case's `BRIEFING.md`). Both cases independently re-derived every answer-key fact from converted/raw data rather than trusting either PDF's narrative or screenshots, after `windows-log-search-basics` v1.0-1.2 shipped with a systematic 9-hour JST/UTC transcription error caught by an independent audit. |
| [JPCERTCC/phishurl-list](https://github.com/JPCERTCC/phishurl-list) | Reference-only | No license file | Monthly CSV (date / URL / spoofed-brand description) of confirmed phishing URLs, 2019-present, actively maintained. IOC pool for phishing-themed scenarios, not a case source on its own. |

## Open items before promoting any Candidate to Adopted

- Confirm exact license terms for every row marked "confirm before use" —
  don't build against one until this is done. Lesson learned the hard way
  on this pass: GitHub's API/license detector can miss a real license file
  if it's non-standardly named (`LICENSE.txt` vs `LICENSE`) — a repo
  reporting `license: null` via the API is not proof no license exists,
  check the actual file listing before concluding that.
- `log-analysis-training_v2` is now **Adopted** — both PDFs used, both
  cases built (see its row above). The "reference by link+hash, don't
  vendor" principle was explicitly overridden for this source (see the
  note at the top of this file); the resulting case-bundle shape ended up
  matching our EvidenceForge cases closely (`data/` + thin
  `AGENTS.md`/`TASK.md`/`EXAM.md`), just with `.tar.gz`-compressed JSON
  Lines / plain-text evidence instead of EvidenceForge's native formats.
- For Playwright/Selenium and ART/CALDERA specifically: no case-bundle
  design exists yet for a *generator that isn't EvidenceForge*. The
  `AGENTS.md` Phase 1/Phase 2 workflow is EvidenceForge-specific; adopting
  a second generator means writing an equivalent workflow for it, not
  assuming the same steps transfer directly.

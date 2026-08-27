# Briefing: pth-lateral-logclear

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `3357`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/pth-lateral-logclear/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #5.

**Every fact below was independently verified directly against the
rendered XML data** before being written down. See the paired
generator README for two real engine-behavior findings that forced a
mid-authoring redesign of this case's core discrimination mechanism —
both confirmed by reading the engine source, not guessed.

## The story, stage by stage

All timestamps UTC. Prior access to `WS-BREACH-01` and extraction of
`localadmin`'s credential hash are assumed, not modeled — the evidence
starts mid-attack, at the first lateral-movement logon.

### Stage 1 — Lateral movement across three file servers
Six Event ID 4624 (Logon Type 3) records for `TargetUserName:
localadmin`, all sourced from `10.80.10.15` (`WS-BREACH-01`) — and
**only** from that IP; `localadmin` has no other 4624 events anywhere
in this dataset:

| Host | Timestamps | Auth Package |
|---|---|---|
| `FS-01` | `15:59:42.14Z`, `15:59:44.13Z` | Kerberos, Kerberos |
| `FS-02` | `16:06:27.98Z`, `16:06:39.42Z` | Kerberos, Kerberos |
| `FS-03` | `16:11:45.39Z`, `16:12:00.28Z` | NTLM, Kerberos |

(Two events per host: the authored `logon` event plus the SMB session's
own auto-generated logon.) Total span: `15:59:42Z` to `16:12:00Z` —
about 12 minutes across all three hosts.

**On auth package (a secondary, not primary, signal):** only one of
six events (`FS-03`'s first) rendered as NTLM. This is not a design
flaw — it reflects a confirmed engine limitation
(`AuthenticationPackageName` for network logons is a fixed 70/30
Kerberos/NTLM random roll, independent of account scope; see generator
README). Do **not** expect or require "NTLM" as the primary
distinguishing evidence — a correct answer may cite it as one
supporting detail among others, but the actual, reliable distinguishing
signal is Stage 3 below.

### Stage 2 — Legitimate baseline noise for the same account (the Q2 distractor)
Several Event ID 4648 records also target `localadmin`, e.g.:
`2024-07-15T13:21:48.79Z` on `FS-02` (source `10.80.20.11`, i.e.
`FS-02` itself, process `powershell.exe`, `SubjectUserName: SYSTEM`),
`22:43:32.61Z` on `FS-02` (`ops-agent.exe`), and similar entries on
`FS-01`/`FS-03` sourced from those hosts' own IPs, via `taskhostw.exe`/
`ops-agent.exe`/scheduled `powershell.exe`. **This same legitimate
4648 pattern also occurs on `WS-BREACH-01` itself** (10 records,
sourced from its own IP `10.80.10.15` — the same IP as the attacker's
4624 logons) and on `DC-01`/`WS-PANAND-01` — found by an independent
Phase 6 audit, correcting an earlier draft of this document that
claimed these events are never sourced from `WS-BREACH-01`. That
claim was wrong; source IP alone is not a fully reliable discriminator
here. The reliable distinguishing signal for Q2 is event type and
subject/process: every 4648 record is attributed to `SubjectUserName:
SYSTEM` via a known automation process (`taskhostw.exe`/
`ops-agent.exe`/scheduled `powershell.exe`), never to an actual
interactive network logon (4624) — that pairing, not source IP by
itself, is what separates the six real attacker logons from this
baseline noise.

### Stage 3 — Why the pattern is anomalous regardless of auth package
Per `ENVIRONMENT.md`, `localadmin` is documented for **local console
use only** — it is not meant to be used for interactive network logons
to a different machine at all, let alone three machines in twelve
minutes from one source. This is the case's actual primary
distinguishing signal — independent of which auth package any
individual logon happens to show.

### Stage 4 — Log clearing
**2024-07-15T16:21:55.47Z** — Event ID 1102 on `FS-02`, about 9m16s
after `FS-02`'s own two logon events, and after `FS-03`'s logons too
(the attacker's last action, targeting the middle host of the three).

### Stage 5 — Did the clear actually work? (the Q5 verification test)
**No.** Direct inspection of `FS-02.cobaltridge.local/windows_event_security.xml`
confirms both of `FS-02`'s own 4624 logon events
(`16:06:27.98Z`, `16:06:39.42Z`) and the subsequent 4634 logoff are
**still present** after the 1102 event. The `log_cleared` event is
purely additive in this engine version — it does not remove any
preceding content from the rendered log (see generator README). The
1102 event is still significant as direct evidence of attacker intent
to destroy evidence, even though — in this specific case — that intent
did not succeed. A final report can therefore express **high
confidence** in the full reconstructed chain: nothing is actually
missing, and the network-level SMB connection evidence
(`zeek01/conn.json`) independently corroborates all three hosts touched
regardless.

## The core distinction the exam tests

Two layers of discrimination, not one: (1) isolating six real events
from a noisy environment (heavy legitimate SMB volume from the same
source workstation, plus a same-named account's legitimate automated
use elsewhere) — Q1/Q2; (2) correctly calibrating confidence about an
anti-forensic action rather than assuming it worked just because the
attacker attempted it — Q5. An answer that treats the log-clear as
having successfully destroyed the FS-02 evidence (without checking) is
making the same mistake as an analyst who trusts an attacker's own
account of what they did.

## Known generator-tooling notes

See the paired generator README in full: (1) `AuthenticationPackageName`
for network logons is a fixed 70/30 random roll in this engine version,
independent of account scope — there is no way to force deterministic
NTLM rendering via scenario authoring, confirmed by reading the engine
source; (2) `log_cleared` does not remove prior log content in this
engine version, confirmed by direct inspection — it is purely additive.
Both are real, reproducible engine behaviors this case was designed
around rather than assumed away.

## Undetermined by design

- **What, if anything, the attacker actually accessed on the file
  shares.** Not evidenced beyond the SMB session establishment itself
  — `zeek01/conn.json` shows connection-level metadata (bytes
  transferred), not file-level access detail. Not required by any
  exam question.

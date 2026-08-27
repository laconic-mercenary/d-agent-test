# Briefing: departing-employee-email-exfil

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

Synthetic data, generated with EvidenceForge v1.17.0, commit
`567073b0ac0a1d7944ea4695e9bde4a305dcebb9`, seed `8842`. Scenario
source:
`forensic-agent-answers/generators/evidenceforge/departing-employee-email-exfil/scenario.yaml`.
Sourced from `doc/TEST_EVIDENCEFORGE_PROPOSED_CASES.md` proposal #8.

**Every fact below was independently verified directly against the
rendered JSON data** before being written down. See the paired
generator README for a real Phase 2 finding: this case was, as first
built, silently unanswerable (STARTTLS made every outbound message,
including the exfiltration emails themselves, render with blank
sender/recipient fields) — fixed before the exam was written, not
discovered after.

## The story

All timestamps UTC. This is the simplest case in this project by
design: three facts, no attacker, no technical exploitation of any
kind.

### The three messages (`zeek01/smtp.json` + `zeek01/files.json`)
All from `owen.marsh@thistledownarch.com` to
`owen.marsh.archive@gmail.com`, `tls: false`, `user_agent: Microsoft
Outlook 16.0`:

| Timestamp | Subject | Attachment | Type | Size |
|---|---|---|---|---|
| `2024-05-06T15:20:15Z` | Q3 Client Contracts - Backup | `Client_Contracts_Q3.pdf` | `application/pdf` | 1,850,000 bytes |
| `2024-05-06T19:45:18Z` | Project Atlas - Design Files | `Design_Specifications_ProjectAtlas.zip` | `application/zip` | 12,000,000 bytes |
| `2024-05-07T15:09:55Z` | Client Contact List | `Client_Contact_List.xlsx` | `.xlsx` (OOXML) | **2,146 bytes** (see note below) |

**Note on the third attachment's size**: the scenario authored `size:
450000` for this attachment; the rendered `files.json` record shows
`total_bytes: 2146` instead. The other two attachments rendered at
their exact authored sizes. This discrepancy is not independently
explained — use the verified rendered value (2,146 bytes) as ground
truth, not the authored one, consistent with this project's standing
rule to trust raw data over scenario intent.

### The distractor (Q1)
`owen.marsh@thistledownarch.com` also sends a legitimate outbound
business email to `orders@partnerrelay.io` ("Update: training roster
for partnerrelay") in the same window — an ordinary vendor/partner
correspondence, not part of the pattern above. Not designed in; found
in the environment's own baseline activity. Q1 tests whether the AUT
correctly excludes this from its list of the three exfiltration
messages rather than treating "any external email from Owen" as the
pattern.

## What actually happened, and what didn't (Q2/Q3)

**No unauthorized access of any kind occurred.** `owen.marsh` used his
own, already-existing, legitimate credentials and access — the same
access he had every other day at this firm — to send files he already
had standing permission to work with, to an address he controls. There
is no compromised credential, no external actor, no technical exploit,
and no evidence of any of these anywhere in this dataset. The correct
framing (Q3) is a **data-handling/DLP policy matter**, not a security
breach: nothing was "broken into." What makes this worth reporting at
all is the destination (a personal account, timed right before his
departure) and the nature of the data (client-sensitive material), not
any technical compromise.

## The core distinction the exam tests

This case is the mirror image of most others in this project: the
difficulty isn't finding the events (they're all in one small SMTP
log) — it's **not over-dramatizing a policy violation into a security
incident, and not under-reporting it as nothing worth flagging
either.** Q4 specifically grades tone/register, not just facts.

## Known generator-tooling notes

See the paired generator README in full: (1) the case was initially
unanswerable due to STARTTLS hiding all outbound message content —
fixed before the exam was written; (2) attachment metadata requires
`zeek_files` in addition to `zeek_smtp`; (3) one attachment's rendered
size doesn't match its authored size, unexplained, handled by using
the verified value; (4) `supporting/GROUND_TRUTH.md`/`.json` (the raw
generator output, not human-curated) labels a logon source IP as
"Attacker IP" and owen.marsh as "compromised account" — a stray
artifact of the engine's generic logon-labeling template, directly
contradicting this case's actual design (there is no attacker). That
IP does not appear anywhere in the actual rendered evidence and is not
an input to grading (only `BRIEFING.md`/`grading_schema.md` are) —
flagged here only so a human reviewer who opens `GROUND_TRUTH.md`
directly isn't misled by it.

## Undetermined by design

- **Why the third attachment's size doesn't match what was authored.**
  Not resolved; doesn't affect any exam question's substance since the
  exact byte count isn't independently meaningful to the case (unlike,
  say, a byte-volume discrimination signal in another case) — it's
  just a fact to cite accurately.

# Briefing: windows-log-search-basics

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

`data/sample1.jsonl` and `data/sample2.jsonl` are real (not synthetic)
Windows Event Log captures from JPCERT/CC's public log-analysis training
material — [JPCERTCC/log-analysis-training_v2](https://github.com/JPCERTCC/log-analysis-training_v2),
`Hands-on/basis/` (originally `sample1.evtx`/`sample2.evtx`, binary EVTX).
Full source PDF vendored here for durability/citation:
`supporting/log-analysis_handson_v2_basic.pdf` ("basic" edition). License
is informal (README: *"自由にご利用ください"* — "please feel free to use
it" — no formal SPDX license); risk accepted per project decision. This
case deliberately does not include `SMB.pcapng` or `test.keytab` from the
same source directory — those support an unrelated Kerberos-decryption
tooling demo (pdf p.18-19), not an investigative question.

**Format conversion (v1.1):** the two `.evtx` files were converted to JSON
Lines (`evtx_dump -o jsonl`) so the case doesn't require EVTX-specific
tooling. Conversion is 1:1 record-for-record with native EVTX field names
preserved — nothing in this document's citations changed as a result.

## Known noise in the underlying data — do not treat as a leak/defect

Converting to text surfaced content beyond what an earlier binary-only
grep audit had caught (EVTX stores text as UTF-16 inside a compressed
structure, which naive ASCII grepping only partially matches). None of it
is relevant to any graded question; documented here rather than scrubbed,
per project decision:

- **Domain name**: nearly every event's account-domain field is a
  distinctive, non-generic domain string, present tens of thousands of
  times across both files — a strong fingerprint back to the source
  material if the AUT has live web-search access (see `AGENTS.md`'s scope
  assumption).
- **Provisioning-script artifacts**: a small number of events (Azure
  Guest Agent / PowerShell command-line auditing) capture how the source
  originally built this lab environment on Azure — an Azure resource-group
  name, a subscription GUID, and one literal plaintext password
  (`Jpcertpassword1`, passed to `ConvertTo-SecureString` during an
  `Install-ADDSForest`/`ADDSDeployment` setup script). This is ephemeral
  lab-provisioning noise, not a credential relevant to this exercise or
  believed to be reused anywhere live — it predates and is unrelated to
  every scenario event our questions reference.
- **`jpcertadmin`/`jpcertuser` are the one exception that IS evidentiary**
  — see the Q2 section above. Everything else in this section is
  incidental and should not factor into grading either direction.

## Answers, sourced directly from the PDF's own answer slides

### Q1 — Microsoft Edge launch time
**Source:** pdf p.94-98 (Hands-on 2).
**Expected:** A cluster of five `msedge.exe` process-creation events
(Event ID 4688), timestamped `2023/07/21` between `18:45:33` and
`18:45:37` — the main process plus child/renderer processes launching
within the same few seconds. `NewProcessName` =
`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
**Full credit:** Cites Event ID 4688, the `NewProcessName` field/path, and
a timestamp within that ~4-second window (any one of the five, or the
full cluster, is acceptable — the exact count (5) is not required).

### Q2 — RDP logon account
**Source:** pdf p.99-102 (Hands-on 3).
**Expected:** Event ID 4624, Logon Type `10` (RemoteInteractive), account
`jpcertadmin`, timestamped `2023/07/21 17:18:43`.
**Known source inconsistency — do not penalize an agent for this:** the
PDF's own problem statement (p.99-100) names the account as `"jpcertuser"`,
but the answer slide's actual working XPath filter (p.101) and the
resulting matched event (p.102) both show `jpcertadmin`. This is a
typo/inconsistency in JPCERT's own material, not something we introduced
or something the agent-under-test should be expected to detect or
reconcile — our `EXAM.md` deliberately does not name either account in
the question, so the agent must find whichever account the *data* actually
shows. `jpcertadmin` is correct because it's what the real event data
contains, not because it's "the right answer to guess."
**Full credit:** Correct account (`jpcertadmin`), Logon Type 10, and the
17:18:43 timestamp, explicitly citing Logon Type as the RDP-identifying
field (not just "a 4624 event").

### Q3 — Who disabled Windows Defender
**Source:** pdf p.103-105 (Hands-on 4).
**Expected:** Windows Defender protection disabled around
`2023/07/21 18:18:34` (Event ID 5001), immediately preceded/accompanied by
a deleted scheduled task (TaskScheduler, "1 task deleted") and several
Windows Security Event ID 5379 ("Credential Manager credentials were
read") entries whose `Account Name` is `testadmin001`. The correlation —
Defender's disable timestamp lining up with `testadmin001`'s nearby
activity — is what identifies the responsible account; there is no single
event that directly states "testadmin001 disabled Defender."
**Full credit:** Names `testadmin001`, cites Event ID 5001 for the
disable action and Event ID 5379 (or equivalent nearby account activity)
as the correlating evidence, and states the ~18:18:34 timestamp. Partial
credit for correct account without explaining the correlation reasoning
(i.e., just guessing the right name isn't the same as demonstrating the
method).

## Note on `sample1.evtx`/`sample2.evtx` sharing a date

Both files show activity on `2023/07/21`, suggesting these may be
overlapping or related captures rather than fully independent samples.
Not confirmed, not load-bearing for grading — noted for whoever extends
this case later.

## Known deficiency: no ground truth for an ID-range filtering question

The source material's Hands-on 1 (pdf p.92-93) demonstrates filtering
`sample1.evtx` for Event IDs 8000-8999, but only shows the filter dialog
being configured — never the actual result set. We have no verified
ground truth for what that filter returns and didn't stand up independent
EVTX-parsing tooling to derive one, so this question was cut from
`EXAM.md` rather than answered with a fabricated ground truth. If this
case is revisited with EVTX tooling available, this could be added back
as a fourth question once independently verified.

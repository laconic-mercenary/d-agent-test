# Generator: departing-employee-email-exfil

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 8842`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/departing-employee-email-exfil/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/departing-employee-email-exfil/data/`) is
human-authored, not generated.

## The case was silently unanswerable on the first build — STARTTLS hid everything

The scenario's `environment.email` block, as first authored, requested
no network sensor at all. Adding one (`zeek_smtp`) still produced
`smtp.json` records with **empty `mailfrom`/`rcptto`/`subject` fields
for every single outbound message**, including the three storyline
exfiltration emails themselves — confirmed by direct inspection: 19 of
21 rendered SMTP records had blank sender/recipient. Root cause: the
mail server config's `attempt_outbound_starttls: true` (the value used
in every prior email-topology example this project has authored, e.g.
`phishing-c2-beacon`'s inbound-only topology) makes the server
negotiate STARTTLS on outbound delivery attempts, and once negotiated
Zeek's `smtp.log` correctly omits the protected header/body fields per
the engine's documented behavior (`docs/reference/scenario-reference.md`'s
Email Topology section: *"If STARTTLS protects message transfer, Zeek
SMTP rows omit protected header/body/file fields"*). This is realistic
network-sensor behavior, not a bug — but it meant the case, as first
built, had **no evidence anywhere** of what was actually sent, to
whom, or when. This would have shipped as a silently unanswerable
case had it not been checked directly against the rendered data before
writing the exam (Phase 2).

**Fix**: set `attempt_outbound_starttls: false` on the `main` mail
server. Regenerated and confirmed all three storyline messages now
render with full `mailfrom`/`rcptto`/`subject` in cleartext, consistent
with a small firm running a legacy on-prem mail server without modern
outbound TLS — a realistic, not contrived, configuration choice.
**Lesson for future email-topology cases**: always verify at least one
outbound external message renders with non-empty envelope fields in
`smtp.json` before writing an exam around it; don't assume
`attempt_outbound_starttls: true` (copied from an inbound-facing
example) is safe for a scenario whose central evidence is an
*outbound* message's content.

## Attachment metadata requires `zeek_files`, not just `zeek_smtp`

`smtp.json` records carry an `fuids` array but zero attachment
metadata (filename/size/mime type) on their own — that lives in a
separate `files.json`, which requires explicitly requesting
`zeek_files` in both the sensor's `log_formats` and top-level
`output.logs` (validation errors if only the latter is set). Added
both; confirmed `files.json` then carries `filename`, `mime_type`, and
`total_bytes` for each attachment, joinable to its parent SMTP record
via the shared `fuid`.

## Verified facts

Three exfiltration messages, all `owen.marsh@thistledownarch.com` →
`owen.marsh.archive@gmail.com`, `tls: false`, `user_agent: Microsoft
Outlook 16.0`:
- `2024-05-06T15:20:15Z`, "Q3 Client Contracts - Backup",
  `Client_Contracts_Q3.pdf`, `application/pdf`, 1,850,000 bytes
  (matches authored size exactly).
- `2024-05-06T19:45:18Z`, "Project Atlas - Design Files",
  `Design_Specifications_ProjectAtlas.zip`, `application/zip`,
  12,000,000 bytes (matches authored size; 32,760 bytes reported
  `missing_bytes`, i.e. essentially fully captured).
- `2024-05-07T15:09:55Z`, "Client Contact List",
  `Client_Contact_List.xlsx`,
  `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`,
  **2,146 bytes rendered** — the scenario authored `size: 450000` for
  this attachment; unlike the other two, it did not render at its
  authored size. Not independently explained (the other two attachments
  in the same scenario rendered exactly as authored, so this isn't a
  blanket engine limitation). The answer key uses the verified
  rendered value (2,146 bytes), not the authored one, per this
  project's standing rule.

**Distractor, verified real and useful**: baseline activity
independently generated a legitimate outbound business email from
`owen.marsh@thistledownarch.com` to `orders@partnerrelay.io`
("Update: training roster for partnerrelay") in the same window — not
designed in, found by inspecting the rendered `smtp.json` directly, and
built into Q1 as a genuine "don't just list every external email this
account sent" discrimination test.

`GROUND_TRUTH.md`'s narrative timeline was not specifically checked
for the recurring local-logon mislabeling bug documented in other
cases this session, since this case's exam doesn't depend on any logon
event at all — not relevant here.

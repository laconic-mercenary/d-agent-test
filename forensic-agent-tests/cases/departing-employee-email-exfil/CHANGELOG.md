# Changelog — departing-employee-email-exfil

## 1.0 — 2026-08-28

- Initial case build, generated synthetically for this project. The
  simplest technical case in this project's proposal set by
  design — no malware, no attacker, no technical exploitation at all;
  the entire "incident" is one legitimately-authorized account sending
  data somewhere policy doesn't allow.
- `ENVIRONMENT.md` is human-authored; it documents the HR context
  (a departing employee) and this account's standing, unchanged
  legitimate access, both load-bearing for Q2/Q3.
- **A real Phase 2 finding, caught before the exam was written:** the
  scenario's first draft requested no network sensor at all, and the
  default mail-server TLS settings (`attempt_outbound_starttls: true`)
  meant every outbound message — including the three exfiltration
  emails themselves — rendered as opaque, sender/recipient-blank
  records in the network sensor's SMTP log. The case was, as first
  built, silently unanswerable: there was no evidence anywhere of what
  was actually sent. Fixed by adding a network sensor
  (`zeek_smtp`/`zeek_files`) and setting `attempt_outbound_starttls:
  false` on the mail server, after which all three messages (sender,
  recipient, subject, and attachment metadata) render in cleartext, as
  a small firm's legacy on-prem mail server realistically might.
- **A related, smaller finding**: one attachment's rendered size
  (`Client_Contact_List.xlsx`) does not match the size authored in the
  scenario (450,000 bytes authored; 2,146 bytes rendered) — the other
  two attachments rendered at their exact authored sizes. Not
  independently explained; the answer key uses the verified rendered
  value, not the authored one, per this project's standing rule to
  trust raw data over intent. See the paired generator README.
- The generated `.eml` email artifacts (`artifacts/email/` at the
  generator level) were **not** ported into this case's evidence, for
  the same reason established in `phishing-c2-beacon`: their synthetic
  attachment content, once decoded, risks leaking internal storyline
  identifiers. This case's email evidence comes entirely from the
  network sensor's SMTP/file-transfer metadata, which was checked and
  contains no such leak.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data before being written down.

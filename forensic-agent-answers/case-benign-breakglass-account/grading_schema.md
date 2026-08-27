# Grading Schema — benign-breakglass-account

Total: 100. Applied per the process in this directory's `AGENTS.md`.

## Q1 — The logon pattern, correctly grouped (25 pts)
**Expected:** Four 4624 events: `APP-01` `07:14:35Z` (Type 10, source
`10.90.10.31`), `DB-01` `07:30:15Z` (Type 5), `FILE-01`
`2024-09-04T07:14:28Z` (Type 10, source `10.90.10.32`), `DC-01`
`07:35:01Z` (Type 5). Correctly grouped as **two distinct occasions**
(`APP-01`→`DB-01` on Sept 3; `FILE-01`→`DC-01` on Sept 4), not four
independent events or one continuous session.
**Full credit:** All four events found with correct hosts/timestamps/
sources, AND correctly grouped into the two occasions.
**Partial:** All four events found but not grouped into occasions (or
grouped incorrectly), or one event missed.
**Zero:** Fewer than 3 events found, or account/pattern misidentified.

## Q2 — No compromise, with genuine justification (20 pts)
**Expected:** No. Justification ties Q1's pattern (source IPs matching
the two documented on-call sysadmins' own workstations, diagnostic-only
commands, no lateral movement beyond the two paired hosts per occasion)
to `ENVIRONMENT.md`'s documented policy for this account.
**Full credit:** Correct "no," with reasoning that connects specific
Q1 facts to the documented policy — not just "it says in the
environment doc that this is fine."
**Partial:** Correct "no" but with vague or unsupported reasoning.
**Zero:** Concludes compromise/incident occurred (a false-positive
escalation not supported by the evidence).

## Q3 — The unrelated distractor, correctly isolated (20 pts)
**Expected:** `rosa.delgado`, `WS-RDELGADO-01`, `2024-09-04T04:00:08Z`,
opening `MonthEnd_Report.xlsx`. Different account, different host, no
admin tooling, not part of the on-call rotation per `ENVIRONMENT.md` —
should be assessed independently, not grouped with the
`svc-breakglass` pattern.
**Full credit:** Correctly identifies the event with citation, AND
explicitly explains why it's unrelated (different account/role, no
admin activity) rather than just noting its existence.
**Partial:** Identifies the event but doesn't explain why it's
distinct from the `svc-breakglass` pattern, or conflates the two in
reasoning elsewhere in the answer set.
**Zero:** Doesn't find the event, or explicitly treats it as evidence
supporting the same incident/pattern as `svc-breakglass`.

## Q4 — What would flip the conclusion (20 pts)
**Expected:** At least two concrete, checkable signals — e.g., a
source IP other than Marcus's/Dana's own workstations; commands beyond
routine diagnostics (account/group changes, staging, unfamiliar
outbound connections); usage inconsistent in volume/frequency with
"occasional response"; a third, undocumented identity using the
account.
**Full credit:** Two or more concrete, evidence-checkable signals
named (not generic statements like "if it looked more suspicious").
**Partial:** One concrete signal named, or signals given are too vague
to actually check against evidence.
**Zero:** No concrete signals given, or answer restates "if it were an
attack, it would be an attack."

## Q5 — Proportionate report register (15 pts)
**Expected:** A brief note stating no incident, describing the pattern
as consistent with documented emergency-access practice, with no
alarmist framing ("attack," "compromise," "breach") and no
under-selling either (should still note what was reviewed and why it
was concluded benign, not just "nothing to see here").
**Full credit:** Tone and content proportionate — reads like a routine
review closure, not an incident report, but still substantively
grounded in what was checked.
**Partial:** Correct substance but tone skews alarmist or dismissive.
**Zero:** No draft finding given, or frames this as a security
incident/breach.

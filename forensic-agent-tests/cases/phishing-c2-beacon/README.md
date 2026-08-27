# Case: phishing-c2-beacon

A paralegal at a small law firm opens a macro-enabled attachment from a
phishing email disguised as an overdue invoice notice. The macro
launches a hidden PowerShell stager that establishes a periodic HTTPS
beacon to external infrastructure. After roughly ninety minutes of
routine check-in traffic, one connection within that same channel
carries a byte volume far larger than any other beacon tick — a manual
attacker action riding the C2 channel, not the beacon itself. This case
specifically tests whether an agent traces delivery, execution, and C2
as three distinct, separately-citable stages, and whether it notices
the one connection that isn't like the others rather than treating
"found a beacon" as the end of the investigation.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-phishing-c2-beacon/`), not included in
this directory or this repository's evidence tree.

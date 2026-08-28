# Case: rogue-service-account-privcreep

A BI analyst at a small data-analytics consultancy uses explicit
alternate credentials to invoke a service account that is documented
for exactly one automated nightly job and nothing else, then uses that
account's access to add itself to Domain Admins. This is a genuine,
unambiguous escalation — not a benign look-alike. This case tests
whether an agent identifies the explicit-credentials event itself as
the anomaly signal (a service account being used interactively at all,
independent of what happens next), correctly distinguishes it from the
account's own legitimate automated credential usage elsewhere in the
data, and traces the escalation through to the actual privilege
change.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

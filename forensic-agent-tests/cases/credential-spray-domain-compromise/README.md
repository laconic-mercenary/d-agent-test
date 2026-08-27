# Case: credential-spray-domain-compromise

A small engineering firm's domain gets compromised through a
credential-spray attack that succeeds against one ordinary employee
account — but the lasting damage happens through a completely different,
over-privileged service account the attacker escalates to along the
way. This case specifically tests whether an agent correctly separates
"how the attacker got in" from "what they ultimately compromised,"
rather than crediting the initially-sprayed account with everything
that happens afterward.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-credential-spray-domain-compromise/`), not
included in this directory or this repository's evidence tree.

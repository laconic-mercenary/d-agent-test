# Case: insider-dns-tunnel-exfil

A finance analyst at a small data-analytics consultancy, who has
entirely legitimate access to a client-financials share, archives a
batch of those files and then exfiltrates them over roughly two hours
via DNS tunneling to a domain that never otherwise appears in this
environment's traffic. There is no external attacker and no compromised
account anywhere in this case — the only "attack" is a legitimate
account doing something legitimate access doesn't explain. This case
specifically tests whether an agent traces the full chain (staging →
exfiltration channel → destination) rather than stopping at "an
employee compressed some files."

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-insider-dns-tunnel-exfil/`), not included
in this directory or this repository's evidence tree.

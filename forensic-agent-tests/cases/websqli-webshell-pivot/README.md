# Case: websqli-webshell-pivot

A small e-commerce retailer's public order-lookup web application is
scanned by an automated SQL-injection tool, then successfully exploited
by one request that returns data the scan's other probes never got.
The attacker drops a webshell, runs basic reconnaissance through it,
then pivots from the web server to an internal file server — a
connection the firewall's own policy technically permits (a legacy
exception was never revoked) but that this host has no legitimate
business reason to make. This case specifically tests whether an agent
recognizes the web server as a stepping stone rather than the real
target, and whether it distinguishes "the firewall allowed it" from
"this traffic is normal for this host."

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-websqli-webshell-pivot/`), not included
in this directory or this repository's evidence tree.

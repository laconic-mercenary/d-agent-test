# Case: windows-log-search-basics

A minimal, standalone test of Windows Event Log search and filtering —
no incident narrative, no attack story. Given two Windows Event Log
exports (converted to JSON Lines, one event per line; shipped compressed,
unpack before use), find specific facts using targeted queries (event ID,
process path, account name, time correlation).

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-windows-log-search-basics/`), not included in
this directory or this repository's evidence tree.

# Case: dga-beacon-logclear

A dispatcher's workstation at a small freight logistics company is
infected with malware that cycles through algorithmically-generated
candidate domains hunting for a live command-and-control host — the
overwhelming majority resolve to nothing, a handful eventually
resolve, and the malware establishes a periodic beacon to the
resulting address. Before finishing, it clears the workstation's own
Security event log. This case tests whether an agent characterizes the
domain-generation pattern itself (volume, entropy, resolution ratio)
rather than only citing the one connection that worked, and whether it
verifies — rather than assumes — what the log clear actually did and
did not remove.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-dga-beacon-logclear/`), not included in
this directory or this repository's evidence tree.

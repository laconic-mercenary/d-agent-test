# Case: external-recon-no-breach

A small accounting firm's public-facing web server gets port-scanned
from an external IP. The firewall blocks nearly every probe. This case
tests whether an agent can correctly investigate real reconnaissance
activity and conclude "no compromise" — supported by evidence, not
assumed — rather than either dismissing the scan without checking, or
escalating scan noise into a breach it can't support.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-external-recon-no-breach/`), not included
in this directory or this repository's evidence tree.

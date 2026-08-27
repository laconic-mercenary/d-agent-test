# Case: pth-lateral-logclear

A workstation is already compromised (prior access assumed, not part
of this evidence) and the attacker has a credential hash for a local
Administrator account that, due to a shared base image, is identical
across three file servers. The attacker uses that hash to log directly
into all three within about twelve minutes, then clears the Security
event log on the middle host before finishing. This case tests whether
an agent can isolate this pattern from a noisy environment (the source
workstation generates heavy routine file-share traffic all day, and
the same account name also shows up in unrelated, legitimate automated
processes), correctly treats the log-clear action itself as evidence
of intent, and — critically — actually checks whether that log-clear
succeeded in removing anything, rather than assuming it did.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

**Answers are held out** in a separate repository
(`forensic-agent-answers/case-pth-lateral-logclear/`), not included in
this directory or this repository's evidence tree.

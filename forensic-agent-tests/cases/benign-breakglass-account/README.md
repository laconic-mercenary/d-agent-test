# Case: benign-breakglass-account

A small insurance office's two on-call sysadmins share a documented
break-glass local-admin account across several servers, used only
during off-hours incident response — logons at odd hours followed by
diagnostic PowerShell commands that would read as suspicious in
isolation, but match a real, documented operational practice. This
case contains no attack. It tests whether an agent reaches "no
incident" through actual verification (checking what the account is
documented for, evaluating an unrelated late-night event on its own
merits) rather than either escalating ordinary off-hours admin activity
into a false alarm, or waving everything off without checking anything.

**For the agent under test:** start at [AGENTS.md](AGENTS.md), not here.

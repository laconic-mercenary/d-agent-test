# Exam — windows-log-search-basics

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. `data/sample1.jsonl` contains evidence of Microsoft Edge (`msedge.exe`)
   being launched. At what time(s) did this happen? Cite the specific
   event type and field that establishes it.

2. **[Flexible Answer]** `data/sample1.jsonl` contains a successful
   interactive remote desktop (RDP) logon. Which account authenticated,
   and at what time? Cite the
   specific Event ID and Logon Type that establishes this was RDP
   specifically, not some other logon type.

3. `data/sample2.jsonl` is the event log from an endpoint that had a
   backdoor tool installed. Under normal circumstances, this tool should
   have been caught by Windows Defender — but it wasn't. Determine who
   disabled Windows Defender's protection, and at what time. Cite the
   specific events that establish both the disabling action and the
   account responsible.

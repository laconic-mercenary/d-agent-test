# Exam — benign-breakglass-account

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. Identify every interactive logon (Event ID 4624) by `svc-breakglass`
   across all servers in this data: host, timestamp, source
   workstation, and logon type. Group them into distinct sessions —
   how many separate occasions does this account get used, and which
   host(s) does each occasion touch?

2. Is there evidence of a compromise in this data? Answer explicitly
   yes or no, and justify your answer using both what you found in
   question 1 and what `data/ENVIRONMENT.md` documents about this
   account's intended use.

3. Separately from `svc-breakglass`, one other late-night event exists
   in this data involving a different account entirely. Identify it
   (account, host, timestamp, activity) and explain specifically why
   it should be evaluated as unrelated to the `svc-breakglass` pattern,
   rather than folded into the same "off-hours activity" bucket.

4. What specific evidence — if it were present in this data instead of
   what's actually there — would change your answer to question 2?
   Name at least two concrete things you would look for that would
   turn this from "documented practice" into "actual incident."

5. Draft the finding as it should appear in a brief internal
   incident-review note. It should reflect the actual severity of what
   you found — this is a register/tone question as much as a
   fact-finding one.

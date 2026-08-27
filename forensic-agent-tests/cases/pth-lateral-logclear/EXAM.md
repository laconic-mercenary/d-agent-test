# Exam — pth-lateral-logclear

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. One account authenticates interactively (Event ID 4624) to all
   three file servers within about twelve minutes. Identify the
   account, each host it logs onto, each timestamp, and confirm they
   all originate from the same source. What is that source?

2. This same account also appears in several Event ID 4648 (explicit
   credential usage) records elsewhere in this data — these are **not**
   part of the same activity as question 1. Identify what
   distinguishes them (source, process, or otherwise) and explain why
   they should not be counted as part of the attacker's activity.

3. Per `data/ENVIRONMENT.md`, what is this account actually documented
   for — and why does question 1's pattern fall outside that intended
   use regardless of which authentication protocol each individual
   logon happens to use?

4. Identify the log-clearing event: host, timestamp, and its position
   in the timeline relative to question 1's three logons.

5. Does the event in question 4 actually remove the host's own record
   of that host's logon from question 1? Check directly — don't
   assume either way — and cite exactly what you find. Then write a
   short final assessment: the full chain of events with citations,
   and how confident your conclusions are given what you found in this
   question.

# Exam — rogue-service-account-privcreep

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. `svc-reportgen`'s credentials are used routinely throughout this
   data by automated processes — this is expected, per
   `data/ENVIRONMENT.md`. Characterize this routine pattern: how many
   such events exist, which process(es) are responsible, and what
   subject account is consistently behind them?

2. Exactly one event involving `svc-reportgen` breaks that pattern.
   Identify it: timestamp, host, Event ID, and the specific field(s)
   that distinguish it from every routine event in question 1 — not
   just "this one seemed different."

3. What happens immediately after the event in question 2, and what
   specific privilege change results? Cite the process event and the
   account-management event, with timestamps, hosts, and exact field
   values (the group name and the member added).

4. Per `data/ENVIRONMENT.md`, at what specific, earliest point in this
   timeline should a monitoring control have fired — identify the
   earliest single event that should have triggered an alert, not the
   end result. Explain why that event alone (before anything else
   happens) is already sufficient grounds for one, independent of
   whether the escalation in question 3 had occurred yet.

5. Write a short synthesis: the full chain from question 1's baseline
   through question 3's escalation, each step cited, with a one-
   sentence statement of what ultimately changed about
   `svc-reportgen`'s privilege level.

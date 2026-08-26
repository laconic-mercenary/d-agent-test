# Exam — ssh-shared-key-overlap

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. How many SSH sessions to APP-SHARED-01 occur during the collection
   window? For each, give the authenticated account and the source IP.

2. Two of those sessions authenticate as the same account. Do they overlap
   in time? State the overlap window and both source IPs involved.

3. Is it physically possible for one person to produce two concurrent SSH
   sessions to the same server from two different source IPs? What does
   that imply about the affected account's credentials?

4. Cite specific evidence, from at least two independent log sources, that
   supports the concurrent-session finding.

5. A third session (a different account) also overlaps in time with both of
   the sessions in question 2. Does that overlap indicate any anomaly on
   that third account? Explain why simple time-overlap between different
   accounts is not, by itself, suspicious.

6. Is there any evidence of an attack, malware, or unauthorized data access
   in this environment? State your conclusion, and what would need to be
   true for this to be an active compromise rather than what you've found.

7. In 3-5 sentences, summarize this finding as you would report it to IT
   leadership, including a recommended next step scaled appropriately to
   what the evidence actually shows.

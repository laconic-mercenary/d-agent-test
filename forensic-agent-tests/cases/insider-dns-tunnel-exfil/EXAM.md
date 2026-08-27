# Exam — insider-dns-tunnel-exfil

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. `WS-SNAKAMURA-01` shows more than one file-archiving (compress) event
   for the same user on the same day — they are not the same event.
   Identify the one that stages data pulled from the `Finance` share on
   `FILE-01` specifically: the exact source path, the destination path,
   the timestamp, and the Event ID. Explain why the *other* archiving
   event on this host is not part of this incident.

2. Identify the channel used to move the staged data off the network.
   Cite the specific destination domain, DNS query type, and encoding
   pattern that distinguish this traffic from an ordinary DNS lookup —
   not just "there was unusual DNS activity."

3. How many queries carried this traffic, and over what time window
   (start timestamp, end timestamp, and total duration)? What fraction
   of this host's total DNS query volume for the full collection period
   does this traffic represent?

4. Was any unauthorized access — a compromised credential, an external
   intrusion, a logon from outside this user's own device — involved at
   any point in this incident? Answer explicitly yes or no, and cite the
   specific logon evidence (Event ID, Logon Type, source) you relied on.

5. Given what `data/ENVIRONMENT.md` states about this organization's
   current data-handling controls, what specific control — if it had
   existed — would most plausibly have caught this before the data left
   the network? Frame your answer as a recommendation appropriate to
   what actually happened here (not a generic "improve security"
   statement).

# Exam — phishing-c2-beacon

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. Identify the delivery vector for this incident: the sender address,
   the recipient, the subject line, and the delivery timestamp — cite
   the specific log record you used. Separately, identify the
   attachment's filename and what its extension indicates about the
   file type; note that this evidence set's mail-delivery log does not
   itself carry attachment metadata, so you'll need a different source
   for this part.

2. Two process-creation events on `WS-JOKAFOR-01` are tied to opening
   the attachment and executing its payload, roughly two minutes apart.
   Identify both (process name, full command line, timestamp, Event
   ID). This evidence does **not** show a parent-process relationship
   between them — explain, using timing and command-line content
   instead, why the two events should be treated as one causal chain,
   and what specifically in the second process's command line connects
   it to what happens next.

3. Identify the C2 channel established after execution: destination
   IP, port, and hostname, and the check-in interval. Cite the DNS
   evidence that resolves this hostname, and explain how it ties back
   to the process command line from question 2.

4. There are 39 total connection records to the C2 destination from
   question 3. The very first one, immediately after the domain's DNS
   resolution, is the stager fetching its next-stage script — not a
   beacon check-in. Of the **remaining 38**, 37 share a consistent
   byte-size profile, and exactly one does not. Identify that one
   record: its timestamp and its byte counts (both directions),
   compared to the routine profile the other 37 share. What does this
   specific difference indicate the attacker did at that moment, as
   distinct from ordinary beacon check-in traffic?

5. Write a short incident summary listing every stage from delivery
   through the event in question 4, each with a supporting citation
   (host, file, Event ID or log field). State plainly what, if
   anything, is still unknown or unobservable in this evidence (for
   example: the content of the manual command itself, since this
   channel is encrypted).

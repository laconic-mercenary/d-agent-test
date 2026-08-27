# Exam — credential-spray-domain-compromise

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. `DC-01`'s Security log shows a credential-spray pattern — several
   accounts targeted in quick succession from the same external source.
   Identify every targeted account, the source IP, and which one (if
   any) succeeded — the successful logon may not be recorded on the
   same host as the failed attempts, so check elsewhere too. Cite the
   specific Event ID(s) for both the failed attempts and the success.

2. Multiple Event ID 4648 (explicit credential usage) records exist
   targeting the `svc-sql` account across the collection window — most
   of them are routine. Identify the one that is not, and state
   specifically what distinguishes it from the routine ones (the
   subject account, the process, and anything else you rely on).

3. How much time elapsed between the event in question 2 and the next
   time `svc-sql` actually logs on anywhere in this data? Why is a gap
   of that length itself meaningful here, rather than incidental?

4. Identify `svc-sql`'s logon in question 3 — the Event ID, Logon Type,
   and source IP/host it originated from. What does that source tell
   you about how the attacker reached that logon, given what you found
   in questions 1-2?

5. What did the attacker do with `svc-sql`'s access to establish
   lasting presence? Cite the specific event and the exact malicious
   content (not just "a scheduled task was created").

6. List this intrusion's stages in order, from initial access through
   persistence, each with a supporting citation. Then state plainly:
   which account represents "how the attacker got in," and which
   represents what they ultimately compromised — and why those are not
   the same account.

# Exam — windows-lateral-movement-ntds-exfil

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. One of the source IPs recurring across this case's evidence belongs to
   a VPN gateway. Identify that IP, then find the *earliest* account logon
   sourced from it anywhere across `data/dataset1/`, `data/dataset2/`, and
   `data/dataset3/`. Identify the account and cite the specific Event ID
   and Logon Type.

2. `data/dataset2/Security.jsonl` shows the `itmanager` account's
   credentials being used to log onto this host. Identify the timestamp
   and the specific authentication-related field values showing this was
   not a normal interactive logon. State your reasoning for why this
   pattern indicates credential reuse (e.g. Pass-the-Hash) rather than a
   standard password-based login.

3. What new local account was created on `dataset2`'s host shortly after
   the event in question 2 (Event ID, subject account, new account name,
   timestamp), and what later event shows that new account logging on via
   RDP specifically (Event ID, Logon Type, timestamp)?

4. `data/dataset1/Security.jsonl` contains a Kerberos service-ticket
   request that names a privileged domain account as the target service.
   Give the Event ID, the `ServiceName`, the specific ticket-encryption-
   type value that marks this ticket as crackable offline, the requesting
   account, and the timestamp.

5. Identify the event showing the account named in question 4 (as the
   ticket's target service) successfully logging on — the Event ID, Logon
   Type, source IP/channel, and timestamp. Separately, characterize a
   pattern of subsequent activity in the same file that suggests this
   account's credentials were then used repeatedly and programmatically
   against this host, rather than for one ordinary session — give the
   approximate volume, timing pattern, and source you're basing that on.
   You don't need to name a specific tool.

6. `data/dataset4/access.log` shows a sustained pattern of outbound
   requests from one internal host to one external IP. Identify the
   source, the destination, the approximate time window, and the
   encoding/format of the transferred data. Decode at least one request's
   path and state what it reveals.

7. List the attack vector at each stage of this intrusion, in order — one
   line each, with a supporting citation (dataset/file, Event ID or log
   field, timestamp). There are six stages, corresponding to questions
   1-6 above.

# Exam — websqli-webshell-pivot

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. Characterize the automated scan against `WEB-01`: source IP, the
   tool it identifies itself as (cite the specific field), the
   endpoints it probed, and the approximate time range. Roughly how
   many requests came from this source during the scan?

2. Exactly one request in this scan's time range actually succeeded in
   extracting sensitive data — but it is **not** the only request that
   received an HTTP 200 response; many of the scan's own probes also
   got 200s. Identify the one specific request that represents a real
   breach. What, specifically, distinguishes it from the scan's other
   200-status requests? (There are at least two independent signals in
   this evidence — find more than one if you can.)

3. What did the attacker do immediately after the successful request in
   question 2? Cite the specific evidence (host, file, timestamp, exact
   command).

4. `FILE-01` receives exactly two inbound SMB (port 445) connections in
   this entire collection period — not one. Identify both: their
   source hosts, timestamps, and byte/duration profiles. Which one is
   the attacker's pivot, and which is unrelated routine traffic? What
   specifically distinguishes them, beyond just "one looks bigger"?

5. Write a short incident summary explaining why `WEB-01` is not the
   attacker's actual objective — what is, and why. Include a
   recommendation addressing the specific firewall policy detail in
   `data/ENVIRONMENT.md` that made the pivot possible in the first
   place.

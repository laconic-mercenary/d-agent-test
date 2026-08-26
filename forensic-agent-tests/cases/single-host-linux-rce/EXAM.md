# Exam — single-host-linux-rce

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. What is the first indication of suspicious activity directed at APP-01,
   and at approximately what time (UTC) does it occur?

2. What technique appears to have been used against the public application
   server, and what specific evidence establishes that code execution
   occurred (not just that a request was sent)?

3. Which account executes the process activity that follows the exploit
   attempt? Is it a human user account or a service/system account?

4. What is the source IP address of the external actor? Does it appear at
   more than one stage of the incident, and if so, which stages?

5. What command(s) does the attacker run immediately after gaining code
   execution, and what do they establish about the attacker's next step?

6. What additional network activity occurs after code execution is
   established, and what artifact (if any) is involved? Can its exact
   contents be determined from the evidence given? Justify your answer.

7. A second, separate cluster of process activity occurs later in the
   collection window, involving a Python script, a shell, and an archiving
   tool. Is this part of the same incident? Justify your answer with
   specific distinguishing evidence, not just a general impression.

8. Reconstruct a chronological timeline (timestamp, host, actor, action) of
   every event you attribute to the incident, from the earliest evidence to
   the latest.

9. In 3-5 sentences, summarize the incident as you would for a
   non-technical stakeholder: what happened, what is confirmed, and what
   remains unconfirmed or unknown.

10. Is there any evidence of lateral movement to WS-OP-01, or of the
    attacker using sam.ortiz's account? State your conclusion and your
    confidence in it.

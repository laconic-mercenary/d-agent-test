# Exam — dga-beacon-logclear

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. Identify the process that starts this incident: its full path, the
   host, the timestamp, and what specifically about its path or
   naming should draw suspicion given what it's disguised as.

2. Characterize the DNS query pattern that follows: the total number
   of queries involved, roughly what fraction resolve versus fail, the
   TLD and typical name length/shape, and the time span it covers. Do
   not just cite "there was unusual DNS activity" — quantify the
   pattern.

3. Of the domains in question 2, identify every one that actually
   resolved and the IP address they all resolve to. What connection
   activity follows to that address — destination, port, interval, and
   how many total connection attempts?

4. Identify the log-clearing event on the infected host: timestamp and
   its position in the timeline relative to everything above.

5. Does the event in question 4 actually remove this host's own record
   of the process in question 1 from its log? Check directly — don't
   assume either way — and cite exactly what you find. Then write a
   short final assessment: how long after initial execution did the
   malware establish working command-and-control, and how confident
   are your conclusions given what you found in this question?

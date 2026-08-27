# Exam — external-recon-no-breach

Answer every question below. See [TASK.md](TASK.md) for how and where to
write your answers.

1. `data/FW-EDGE-01/cisco_asa.log` contains evidence of a port scan
   against the DMZ web server. Identify the source IP, the destination
   IP, the number of distinct ports probed, and the approximate time
   window. Cite the specific log message type/ID you used.

2. Of the ports probed in question 1, most were denied by the firewall.
   Identify every port where the firewall instead permitted a real TCP
   connection through — name each port, and for each one, state what
   happened next (cite the specific Zeek `conn.json` entry, including
   its `conn_state` value).

3. One of the connections in question 2 involved an authentication
   attempt. Was it successful? Cite the specific host-level log entries
   (not just the network-level connection record) that establish this
   either way.

4. `data/ENVIRONMENT.md` states which ports on the web server are
   supposed to be reachable from the internet. Does the evidence in
   question 2 match that stated policy? If not, say specifically what
   doesn't match.

5. Beyond the scan itself, is there any evidence anywhere in `data/` of
   a successful compromise, persistence, or follow-on activity — on any
   host, not just the web server? State your conclusion. Then, in 3-5
   sentences, write the finding as you would report it to the
   organization, including a recommendation scaled to what the evidence
   actually shows.

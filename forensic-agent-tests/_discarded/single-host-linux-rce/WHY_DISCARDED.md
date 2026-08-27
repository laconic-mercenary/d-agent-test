# Why this case was discarded — 2026-08-26

Pulled from active use after an independent audit found the rendered
evidence contradicts itself on the case's central causal claim and on a
secondary fact, both newly discovered (not previously in
`KNOWN_DEFICIENCIES.md`):

1. **Causal inversion at the exploit pivot.** The RCE shell's process-
   creation timestamp (eCAR) precedes the TCP connection and HTTP POST
   (Zeek) that supposedly caused it, by 14-26ms, same host/clock, no skew
   explanation. This is the evidence for the single most important fact in
   the case (T1190 exploitation → code execution) rendering out of order.
2. **Process lineage contradicts the declared stack.** The exploited
   shell's `parent_image_path` is `/usr/sbin/apache2` in two eCAR records,
   while `ENVIRONMENT.md`, `scenario.yaml` (`services: ["nginx",
   "gunicorn", ...]`), and syslog all agree the host runs nginx + gunicorn.

Neither is fixable by rewording an exam question — both are data
contradictions, not question-wording problems. Held out until EvidenceForge
regenerates cleanly against a fix for both (candidates: intra-step causal
ordering for `connection`+`process` pairs in one storyline step; parent-
process template selection respecting `environment.systems[].services`
instead of falling back to a generic default).

Also present (lower severity, not why this was pulled, but worth folding in
if this is revived): the DNS-before-TCP causal expansion firing on a bare
IP-literal destination (already documented as deficiency #4 in this case's
own `KNOWN_DEFICIENCIES.md`, in the answers repo), and a Q1 ("first
indication of suspicious activity") that's genuinely ambiguous because a
baseline-noise scanner at 02:01:19 shares an identical User-Agent with the
storyline's real attacker at 02:17:35.

All four should be filed upstream against
[Cisco-Talos/EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge)
(reproducible against commit `567073b0`, scenario preserved in
`../single-host-linux-rce-generator/scenario.yaml`, seed 42) before this
case is revived.

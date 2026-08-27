# Generator: websqli-webshell-pivot

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 9130`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/websqli-webshell-pivot/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/websqli-webshell-pivot/data/`) is
human-authored, not generated.

## Do not use `adversarial_payload` for this case's SQLi content

The original design considered EvidenceForge's `adversarial_payload`
event type (`family: sql_injection`, `surface: http_request_url`) for
the successful-injection step. **Do not use it for any AUT-facing
case** — it unconditionally stamps the literal string `EFORGE_TEST`
into every payload it renders, a hard safety guardrail with no opt-out
(see `src/evidenceforge/config/activity/payload_families.yaml`'s
`default_marker`). That string is a direct brand-name leak under this
project's own leak-audit grep. This case models the SQLi content
instead via a plain `connection` event with `service: http` and a
hand-written injection-shaped `uri`, which renders exactly the intended
content with no marker. See root `AGENTS.md`'s "Known pitfalls" for the
project-wide version of this lesson.

## A real Phase 2 finding: built-in "legitimate lateral movement" collided with the case's premise

The scenario's first draft gave the pivot target (`FILE-01`) the
`roles: [file_server]` declaration, following the schema reference's
guidance that role assignment is what makes a host a realistic SMB
target. On generation, this triggered an **unplanned, engine-built-in
baseline pattern**: `src/evidenceforge/config/activity/network_params.yaml`
defines a `role: web_server` → `content_publisher` legitimate-traffic
pattern (`/opt/meridian/bin/content-publisher --share
smb://{target}/WebContent`, run as `www-data`) that automatically
routes SMB baseline traffic from any `web_server`-role host to any
`file_server`-role host in the same scenario — modeling a web server
that deploys its own content via an SMB share, a completely realistic
pattern in real environments. Independently confirmed in the first
generation attempt: `WEB-01` (`10.70.10.10`) showed multiple
`fw01/cisco_asa.log` "Built inbound TCP" records to
`inside:10.70.20.10/445` throughout the day, hours before the
storyline's own pivot event — i.e., the engine's own baseline realism
had already established a legitimate-looking precedent for exactly the
connection this case needed to be anomalous. This would have silently
broken the exam's central premise ("this host has no legitimate reason
to reach `FILE-01`") without ever producing a validation warning.

**Fix:** removed `roles: [file_server]` from `FILE-01` (kept
`services: [samba]` for narrative flavor only). Regenerated and
confirmed via direct inspection of `fw01/cisco_asa.log` and
`zeek01/conn.json` that the `content_publisher` pattern no longer
fires — `WEB-01` now has zero baseline connections to `FILE-01` for the
entire ~24-hour window, only the one authored pivot event.

**One other role-triggered pattern survived, deliberately kept**:
`DB-01` (role: `database`) still gets its own separate
`database_backup_agent` pattern (`/usr/local/sbin/database-backup-agent
--repository smb://{target}/DatabaseBackups`, run as `backup`) —
apparently targeting any reachable host regardless of the target's own
declared role, since it fired once even after `FILE-01`'s `file_server`
role was removed:
`2024-08-12T14:57:48.44Z`, `10.70.10.20 → 10.70.20.10:445`,
`orig_bytes: 110`, `resp_bytes: 566`, sub-second duration. This is
*not* a bug — it's a second, independently real legitimate pattern —
and the case was built around it rather than suppressed further: `FILE-01`
now receives exactly two SMB connections in the whole dataset, one
routine (`DB-01`'s small quick backup ping) and one the actual pivot
(`WEB-01`, `2024-08-12T15:17:25.4Z`, 28.4s duration, `orig_bytes: 6999`,
`resp_bytes: 9181`). Q4 was written directly against this real
two-connection discrimination, not a designed-in distractor.

## SQL-injection discrimination signal, verified against raw data

The scan (source `185.220.102.51`, User-Agent
`sqlmap/1.7.12#stable (https://sqlmap.org)` on every request, ~278
requests to `/products.php`, `/api/v1/data`, `/login`, `/search`,
`2024-08-12T15:00:23Z`–`15:12:23Z`) returns HTTP 200 on roughly half its
own probes — status code alone does **not** distinguish a real breach
from scanner noise in this data, confirmed directly against
`WEB-01/web_access.log` before the exam was written. The actual
successful request
(`2024-08-12T15:12:58Z`, `GET /products.php?id=1' UNION SELECT
username,password_hash,1,1 FROM admin_users-- HTTP/1.1" 200 48000`)
is distinguishable by **User-Agent** (`Mozilla/5.0`, not the sqlmap
tool signature — the attacker manually replayed the working payload
outside the automated tool) and by **payload content** (names a
specific sensitive table/columns, unlike the scan's generic
boundary-testing payloads like `AND 1=1`, `ORDER BY N`, `OR SLEEP(5)`).

**v1.1 corrections, found by an independent Phase 6 audit:** the v1.0
answer key had the breach request's timestamp wrong (`15:12:58Z`
instead of the actual `15:13:08Z`, confirmed by direct grep against
`web_access.log`) and the scan's request count wrong ("~278" claimed;
actual is 255 sqlmap-UA requests, 256 total from that source IP). Both
were narrative-recap errors introduced while writing `BRIEFING.md`, not
data problems — fixed in the case's `EXAM.md`/`BRIEFING.md`/
`grading_schema.md`.

**A separate, real engine-behavior finding, also from that audit:**
baseline-generated "legitimate" cross-segment traffic does not appear
to be fully gated by the scenario's declared firewall `policy:` rules
the way explicitly-authored storyline/scan traffic is. This scenario's
policy only lists `{src: dmz, dst: servers, ports: [445]}` as the
DMZ→servers exception, yet `fw01/cisco_asa.log` shows baseline
monitoring-style traffic (health-check-style HTTP polling, ICMP, and
generic failed-SSH-login noise) crossing that same boundary on ports
21, 22, 80, and 514 too — none of which the declared policy lists.
Compare to `external-recon-no-breach`, where the firewall *did* cleanly
gate all of that scenario's (fully attacker-authored) port-scan
traffic. The working hypothesis: baseline/world-model traffic generation
and the firewall/ASA emitter's declared `policy:` enforcement are not
the same code path, and only the latter is strictly authoritative for
storyline-authored connections. Worth re-verifying against a future
engine version rather than assumed to still hold. `ENVIRONMENT.md` was
reworded to stop overstating the declared policy as the sole source of
truth for what traffic actually crosses the DMZ boundary.

Note also: `zeek01/http.json` (the network sensor's HTTP log) captures
none of this — all storyline HTTP traffic in this case is on port 443,
which the sensor treats as encrypted/opaque regardless of the
scenario's declared `service: http`. Only the web server's own
`web_access.log` has full request/response detail for this traffic.
`zeek01/http.json` in this dataset is almost entirely unrelated
baseline plaintext (port 80) browsing traffic.

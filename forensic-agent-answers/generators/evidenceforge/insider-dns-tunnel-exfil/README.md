# Generator: insider-dns-tunnel-exfil

EvidenceForge v1.17.0, commit `567073b0ac0a1d7944ea4695e9bde4a305dcebb9`,
`generation_seed: 4417`.

Reproduce:

```bash
cd /path/to/EvidenceForge
uv run eforge generate scenarios/insider-dns-tunnel-exfil/scenario.yaml --verbose --force
```

`ENVIRONMENT.md` (in `cases/insider-dns-tunnel-exfil/data/`) is
human-authored, not generated — it documents which accounts have
legitimate access to the finance share and the organization's data-
handling expectations, both load-bearing for the case's exam questions.

## Notable findings from this build

**A real, uncredited `GROUND_TRUTH.md` inaccuracy** (third one found
this session, after `external-recon-no-breach`'s two): the generated
`GROUND_TRUTH.md`'s timeline table listed the storyline's morning logon
as `"2024-10-07 14:59:31 UTC ... Network logon from 45.33.32.156
(LogonID: 0x3ade0ff)"`. Direct inspection of the rendered
`windows_event_security.xml` shows the actual event with
`TargetLogonId 0x3ade0ff` occurred at `2024-10-07T14:19:32.0831431Z`,
is Event ID 4624 **Logon Type 2** (local/interactive — the storyline
authored `logon_type: 2` with no `source_ip`), and has a blank
`IpAddress` field, as expected for a local logon. `45.33.32.156` does
not appear anywhere in this host's security log. This looks like a
generic ground-truth template quirk (labeling every storyline actor's
logon as a "compromised account"/"Attacker IP" regardless of whether
the scenario models an actual external attacker — this scenario has
none) rather than an engine bug specific to `dns_tunnel` or `logon`
rendering, but it's a clean, independently-reproducible example of why
`GROUND_TRUTH.md` must never be trusted without checking the raw data:
the wrong timestamp, wrong logon-type characterization, and a fabricated
IP all appeared in one otherwise-plausible-looking table row. The case's
`BRIEFING.md` uses the verified values only.

**Useful, unplanned baseline realism**: the environment's baseline
activity model independently generated a second, unrelated
`Compress-Archive` process event (Event ID 4688) for the same user
later the same day — a routine local log backup
(`C:\Temp\Logs\*.log` → `C:\Backups\monthly-logs.zip`, run with
`-WindowStyle Hidden`, which if anything reads as *more* suspicious in
isolation than the actual staging event). This wasn't designed in; it
was found by inspecting the rendered data directly and built into Q1 as
a genuine discrimination test — an agent that flags the hidden-window
backup instead of the Finance-share archive has the wrong event.

DNS-tunnel volume was independently verified against `zeek01/dns.json`:
464 TXT queries to `*.sync.cloudmetrics-telemetry.net`, all base64-
encoded subdomains, from `10.40.10.31` (`WS-SNAKAMURA-01`) only, spanning
`2024-10-07T15:24:45.73Z` to `2024-10-07T17:24:29.09Z` (1h59m43s) — about
53.0% of *this host's own* DNS query volume (875 records) for the
entire ~26-hour collection window. `zeek01/dns.json` holds 2,135
records total, but that's across all 4 monitored hosts, not just this
one — the case's own independent Phase 6 audit caught a v1.0 draft of
`BRIEFING.md`/`grading_schema.md` dividing 464 by the wrong (all-host)
denominator and getting ~21.7%; fixed to the correct per-host figure in
v1.1.

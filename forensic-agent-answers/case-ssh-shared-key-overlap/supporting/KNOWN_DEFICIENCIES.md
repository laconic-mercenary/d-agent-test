# Known Deficiencies — ssh-shared-key-overlap

Two minor engine-level quirks discovered while building this scenario,
documented here rather than silently worked around. Neither breaks the core
exercise (see below), but a strict grader should know about them.

---

## 1. The two "priya.desai" sessions use different SSH key fingerprints

**Where:** `ssh_session` event type has no field to pin a key fingerprint;
fingerprints are generated independently per session.

The scenario premise is that Marcus uses Priya's *actual* shared private key
— i.e. the same physical key file — from his own workstation. A maximally
rigorous read of the evidence would expect both of Priya's sessions (her own,
and the one sourced from Marcus's workstation) to authenticate with the
*identical* key fingerprint. Instead, the two rendered sessions show two
different fingerprints:

- Priya's own session (`10.70.8.21`): `RSA SHA256:Zp4QbAUMUxM8gr9OcDYefMqxvouBubIm8RsNToYr6Ay`
- The borrowed session (`10.70.8.22`, really Marcus): `ED25519 SHA256:1cTIpVoldwCdEMIZGvs/AazRXCRnQJbradksz21qVEt`

This doesn't undermine the core tell (two concurrent sessions under one
identity from two different source IPs, which one person cannot produce),
but it means the *strongest* possible version of the tell — identical key
material used from two places — isn't present in the data. Don't grade an
analysis down for failing to notice "the same key fingerprint was used
twice," because that isn't what the generated evidence shows. Grade on the
overlapping-sessions/source-IP anomaly instead, which is fully and correctly
present at every layer (syslog, eCAR, and independently at the network layer
via Zeek `conn.json` — see `GROUND_TRUTH.md` and `data/ZEEK-DEV-01/conn.json`).

**Workaround:** none available at the scenario-authoring level.

---

## 2. Marcus's own workstation renders one command under `priya.desai`'s local bash history instead of his own

**Where:** local/source-side command attribution for a storyline step whose
`actor` is the *target-side* authenticated identity, not the physical local
operator.

`evt-004-marcus-borrowed-connect` is authored with `actor: priya.desai`
(correct — that's who authenticates on `APP-SHARED-01`). But the outbound
`ssh` command itself, which Marcus physically types at his own workstation
(`WS-MARCUS-01`), also gets attributed to `priya.desai` locally — producing a
stray `bash_history/priya.desai.bash_history` file on `WS-MARCUS-01`
containing only `ssh -p 22 priya.desai@APP-SHARED-01`, rather than that line
appearing in `marcus.oyelaran.bash_history` on his own machine (where the
rest of his normal, unrelated activity does correctly appear).

In a real environment, Priya has no local account on Marcus's workstation at
all, so a `priya.desai.bash_history` file existing there is itself a minor
tell (arguably reinforces "something is off" rather than undermining it),
but it's not the clean, expected artifact (Marcus's own history showing him
explicitly typing a command against Priya's account). The engine currently
has no way to distinguish "who authenticates on the target" from "who is
physically local at the source" for the same storyline step — both are
driven by the single `actor` field.

**Workaround:** none applied — accepted as-is. The target-side evidence
(`APP-SHARED-01`'s `priya.desai.bash_history`, which correctly shows both
file-write commands under her account) is unaffected and is the evidence
that matters for the exercise.

**Suggested fix:** allow a storyline `ssh_session` event to optionally
distinguish a `source_actor` (who is physically local at the origin) from
`actor` (who authenticates at the target), so source-side artifacts (local
bash history, local process ownership) attribute correctly even when the two
differ, as in a shared-credential scenario.

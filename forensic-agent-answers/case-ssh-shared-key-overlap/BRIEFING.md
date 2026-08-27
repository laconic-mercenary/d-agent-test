# Briefing: ssh-shared-key-overlap

Human-readable ground truth. Do not share with the agent-under-test.

## True story

No attack. Three developers use a shared Linux server normally, except one
shares her private key with a colleague, who uses it concurrently with her.

1. **~14:15:11 UTC** — `priya.desai` SSHes into APP-SHARED-01 from her own
   workstation, `10.70.8.21` (genuine session).
2. **~14:17:17 UTC** — Priya appends a note to her own deploy log during
   that session.
3. **~14:18:27 UTC** — `greta.lindqvist` SSHes in from her own workstation,
   `10.70.8.23` (unrelated, fully normal — see "Discrimination" below).
4. **~14:19:44 UTC** — A *second* session authenticating as `priya.desai`
   opens, sourced from `10.70.8.22` — Marcus's workstation IP, not Priya's.
   Priya's first session (step 1) is still open. This is Marcus, using a
   private key Priya shared with him.
5. **~14:22:13 UTC** — Greta writes a status note (normal).
6. **~14:23:30 UTC** — The borrowed (`10.70.8.22`) session appends a second
   entry to Priya's deploy log, still authenticated as `priya.desai`.

**The finding:** `priya.desai` has two concurrent SSH sessions to the same
server from two different source IPs at the same time — physically
impossible for one person. That's the entire signal. There is no malware,
no privilege escalation, no data theft, no lateral movement beyond the
shared server itself.

## Discrimination: Greta's session is a red herring by proximity, not by design

Greta's session (`10.70.8.23`, step 3) temporally overlaps with *both* of
Priya's sessions, purely because all three people are using the shared
server around the same time of day. This is NOT anomalous — different
account, single consistent source IP, ordinary activity. An answer that
treats "sessions overlapping in time" as inherently suspicious and flags
Greta's account is a false positive and should be scored down. The anomaly
is specifically **the same identity from two different source IPs at once**,
not concurrency in general.

## Known evidence quirks (engine artifacts, not part of the story)

Full detail in `supporting/KNOWN_DEFICIENCIES.md`. Two points a grader
needs but should not require of the AUT:

1. **Key fingerprints differ between Priya's two sessions** (`RSA
   SHA256:Zp4Q...` vs. `ED25519 SHA256:1cTI...`). The premise is that Marcus
   uses Priya's actual shared key, so the strongest version of this tell —
   identical key material from two locations — isn't present in the
   rendered data. **Do not penalize an answer for failing to notice
   matching key fingerprints; that evidence doesn't exist in this dataset.**
   Grade on the overlapping-session/source-IP anomaly, which is fully and
   correctly present in syslog, eCAR, and Zeek `conn.json` independently.
2. **A stray `priya.desai.bash_history` file exists on `WS-MARCUS-01`**,
   containing only `ssh -p 22 priya.desai@APP-SHARED-01` — an engine
   attribution quirk (the command should have landed in Marcus's own
   history). If an AUT notices this and reasons about it, that's a bonus,
   not a requirement — and note it actually reinforces the finding rather
   than contradicting it, so don't treat an AUT citing it as confused.

## Undetermined by design

- **Whether the key was shared voluntarily or stolen.** The evidence shows
  concurrent use of one identity from two source IPs; it does not by itself
  distinguish "Priya gave Marcus her key" from "Marcus's workstation was
  compromised and the key was taken from it, or from Priya's machine
  remotely." A good answer says "credentials used from two places at once"
  and recommends investigation/rotation; it should not assert either
  explanation as confirmed fact.

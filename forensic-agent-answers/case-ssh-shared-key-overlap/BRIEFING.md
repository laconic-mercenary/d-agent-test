# Briefing: ssh-shared-key-overlap

Human-readable ground truth. Do not share with the agent-under-test.

## True story

No attack. Three developers use a shared Linux server normally, except one
shares her private key with a colleague, who uses it concurrently with her.

**Correction (v1.2, found by independent audit):** the session list below
was incomplete in earlier revisions — it omitted Marcus's own genuine
session and Greta's second session, both real and present in
`data/APP-SHARED-01.fernbridgelabs.com/syslog.log`. `EXAM.md` Q1 asks for
*every* session in the window, so an answer enumerating only 3 was always
supposed to lose credit against the true count of 5 — the grading key
just hadn't caught up to that until now. Full session list, in order:

1. **14:11:24.37 UTC** — `marcus.oyelaran` SSHes into APP-SHARED-01 from
   his own workstation, `10.70.8.22` (genuine session, closes 15:00:56 UTC).
   This is Marcus doing his own ordinary work — not the borrowed-key
   session (that's #4 below), but note it originates from the *same
   source IP* as #4, since both are his machine.
2. **~14:15:11 UTC** — `priya.desai` SSHes into APP-SHARED-01 from her own
   workstation, `10.70.8.21` (genuine session, closes 15:51:14 UTC).
3. **~14:17:17 UTC** — Priya appends a note to her own deploy log during
   that session.
4. **~14:18:27 UTC** — `greta.lindqvist` SSHes in from her own workstation,
   `10.70.8.23` (unrelated, fully normal — see "Discrimination" below;
   closes 15:57:51 UTC).
5. **~14:19:44 UTC** — A *second* session authenticating as `priya.desai`
   opens, sourced from `10.70.8.22` — Marcus's workstation IP, not Priya's.
   Priya's first session (step 2) is still open. This is Marcus, using a
   private key Priya shared with him. Closes 15:56:33 UTC.
6. **~14:22:13 UTC** — Greta writes a status note (normal).
7. **~14:23:30 UTC** — The borrowed (`10.70.8.22`) session appends a second
   entry to Priya's deploy log, still authenticated as `priya.desai`.
8. **15:54:37.25 UTC** — `greta.lindqvist` opens a *second*, unrelated
   session, same account and source IP as her first (`10.70.8.23`) — just
   an ordinary second work session later in the afternoon. Does not close
   within the collection window (still open when it ends); nothing
   anomalous about that on its own. Overlaps Priya's session #5 only (not
   #2 — that one already closed by 15:51:14), so it does **not** qualify
   as a "third session overlapping both" for Q5 purposes.

**The finding:** `priya.desai` has two concurrent SSH sessions to the same
server from two different source IPs at the same time — physically
impossible for one person. That's the entire signal. There is no malware,
no privilege escalation, no data theft, no lateral movement beyond the
shared server itself.

## Discrimination: two sessions overlap both Priya sessions, neither is anomalous

**Correction (v1.2):** earlier revisions only documented Greta's session
(#4) as the overlapping "third session" Q5 asks about. Marcus's own
genuine session (#1) *also* overlaps both Priya sessions in time (his
session spans 14:11:24-15:00:56, which covers the open windows of both
Priya session #2, open until 15:51:14, and Priya session #5, open until
15:56:33). `EXAM.md` Q5 has been reworded to ask about every other
overlapping session, not just one, to match this.

Neither overlap is anomalous, for the same reason: different account,
single consistent source IP each, ordinary concurrent usage. An answer
that treats "sessions overlapping in time" as inherently suspicious and
flags Greta's or Marcus's own account is a false positive and should be
scored down. The anomaly is specifically **the same identity from two
different source IPs at once**, not concurrency in general — and it's
worth explicitly noting that Marcus's own account is *also* the one behind
the anomalous session (#5): the fact that his own legitimate activity
looks unremarkable is itself part of what a good answer should be able to
articulate (he's not "a suspicious actor," he's a normal user who also,
separately, holds a key that lets him log in as someone else).

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

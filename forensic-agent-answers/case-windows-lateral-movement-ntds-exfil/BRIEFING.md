# Briefing: windows-lateral-movement-ntds-exfil

Human-readable ground truth. Do not share with the agent-under-test.

## Provenance

`data/dataset1/` through `data/dataset4/` are real (not synthetic)
Windows Event Log and Squid proxy log captures from JPCERT/CC's public
log-analysis training material —
[JPCERTCC/log-analysis-training_v2](https://github.com/JPCERTCC/log-analysis-training_v2),
`Hands-on/advance/` (originally `Hands-on-1` through `Hands-on-4`,
renamed to `dataset1`-`dataset4` when vendoring — the source directory
names are themselves a fingerprint back to the repo). Full source PDF
vendored here for durability/citation:
`supporting/log-analysis_handson_v2_advance_with_comment.pdf` (the
"with comment" edition — includes both the exercise prompts and the
answer-slide annotations in one file). License is informal (README:
*"自由にご利用ください"* — "please feel free to use it" — no formal SPDX
license); risk accepted per project decision, same as
`windows-log-search-basics`.

**Every fact below was independently re-derived directly from the
vendored/converted data, not transcribed from the PDF's narrative or
screenshots.** This matters: `windows-log-search-basics` v1.0-1.2 shipped
with every timestamp wrong by 9 hours because its answer key trusted the
PDF's Event-Viewer screenshots (which render local JST) instead of the
actual UTC `SystemTime` field. This case's answer key was built the other
way around from the start — every timestamp, account name, and field
value here came from directly parsing `data/dataset*/*.jsonl` and
`data/dataset4/access.log`.

## The story, stage by stage

All timestamps UTC, all confirmed directly against the data.

### Stage 1 — Initial access (`dataset3`)
**2023-10-11T00:26:15.617912Z** — Account `testuser` logs on to this host
(the "maintenance terminal" in the source material) via VPN. Event ID
4624, **Logon Type 10** (RemoteInteractive), source IP `10.10.100.254`
(the VPN gateway's internal-facing address — this is the wire-level
source seen by the endpoint, not testuser's real external IP). Two Logon
Type 3 events immediately precede this (`00:26:11`, `00:26:13`) from the
same source IP — likely the VPN's own network-layer authentication steps
completing just before the interactive session establishes; Type 10 is
the event that actually proves RDP/interactive-remote access.
**How initial access was obtained is not evidenced in this data** — the
source PDF's own master timeline places an even earlier, out-of-scope
event ("testuser connects, password leak?") that the source material
explicitly does not investigate ("VPN investigation omitted"). Don't
expect or require the AUT to explain *how* testuser's credentials were
first obtained — only that this VPN logon is the earliest evidenced
foothold *sourced from the VPN gateway*.

**`EXAM.md` Q1 is scoped to the VPN gateway's source IP specifically —
here's why, found by a second independent audit (v1.1):** the original
Q1 wording asked for "the earliest account logon evidenced anywhere in
this case," unscoped. That's false against the raw data in two separate,
confirmed ways:
1. `jpcertadmin`/`jpcertuser` (provisioning/setup accounts, see "Known
   noise" below) have real, earlier Type-3 and Type-10 logons — e.g.
   `jpcertadmin` at `2023-10-10T02:36:53Z` in `dataset1`,
   `jpcertuser`/Type-10 at `2023-10-10T05:15:31Z` in `dataset3` — both
   well before `testuser`'s `00:26:15Z` on `2023-10-11`.
2. Even excluding jpcert-prefixed accounts, `dataset3` alone also has a
   real `domuser` Type-3 logon at `2023-10-10T05:19:14Z`, from
   `10.12.0.2` — earlier than `testuser` and not a provisioning account
   (domuser is the account behind Stage 4's Kerberoasting request).

Both of these share source IP `10.12.0.2`, which is otherwise unused
anywhere else in the case — cross-checked directly, every Type-10 logon
sourced from `10.12.0.2` is a `jpcert*` account or this one early
`domuser` entry, all clustered in a ~10-minute window on `2023-10-10`
around `05:1x`-`05:2x`. That whole cluster reads as one-time
lab-provisioning/setup activity, distinct in kind from the storyline
proper. `10.10.100.254`, by contrast, is the *only* source IP that
recurs as the origin for privileged, human-interactive (Type 10) logons
at two clearly separate narrative points — `testuser` here in Stage 1,
and `domadm` in Stage 5 — which is what makes it identifiable as the
external-access channel from the data itself, not from outside
knowledge. Confirmed independently: `testuser`'s `00:26:15Z` logon is
genuinely the earliest Type-10-or-Type-3 event sourced from
`10.10.100.254` specifically, across all three Windows datasets.

### Stage 2 — Lateral movement / credential reuse (`dataset2`)
**2023-10-11T00:44:54.185075Z** (and again at `00:45:15`) — Account
`itmanager` logs onto this host (the source material's "Client A").
Event ID 4624, **Logon Type 3** (Network), **AuthenticationPackageName:
NTLM**, source IP `10.10.100.104` (the maintenance terminal from Stage 1
— `itmanager` is a shared local-admin account across both hosts, which
is why this works). NTLM authentication for a Type-3 network logon, in an
environment where Kerberos is otherwise the norm (see Stage 4's 4769
ticket evidence), with no interactive credential entry, is the classic
Pass-the-Hash tell: the attacker replayed `itmanager`'s NTLM hash rather
than knowing its actual password.

### Stage 3 — Persistence (`dataset2`)
**2023-10-11T00:46:32.278815Z** — Event ID 4720 (user account created),
subject `itmanager`, new account `eviluser`.
**2023-10-11T00:47:44.940630Z** — Event ID 4624, **Logon Type 10**,
account `eviluser` — the newly-created account immediately used for an
RDP logon on the same host.

### Stage 4 — Escalation (`dataset1`)
**2023-10-11T01:17:17.197728Z** — Event ID 4769 (Kerberos service ticket
requested), `ServiceName: domadm`, **`TicketEncryptionType: 0x17`**
(RC4-HMAC — the weak, offline-crackable encryption type that makes
Kerberoasting viable), requesting account `domuser@HANDSONLAB.LOCAL`,
client IP `::ffff:10.10.100.105` (IPv4-mapped IPv6 notation for Client A
— note this is a *different* host than Stages 2-3's `10.10.100.104`;
worth an AUT noticing the pivot, though not required for credit).
`domadm` is a domain-admin-level account being requested as a service
ticket target — a strong Kerberoasting indicator once you also have the
weak encryption type.

### Stage 5 — Domain compromise + credential-driven data access (`dataset1`)
**2023-10-11T23:44:32.175330Z** — Event ID 4624, **Logon Type 10**,
account `domadm`, source IP `10.10.100.254` (VPN gateway again) — the
cracked/obtained `domadm` credential used to log on directly, establishing
domain-admin-level access.

**Separately** — starting **2023-10-12T00:06:42.323558Z** and continuing
through **2023-10-12T06:10:45.463918Z**, this same file shows **96
separate Event ID 4624, Logon Type 3 (network) logons as `domadm`, all
sourced from `10.10.100.105`** (Client A — the same host Stage 4's ticket
request came from). This is a large volume of repeated, tightly-clustered
network logons using the same privileged credential from the same host
over ~6 hours — consistent with a script or tool repeatedly
authenticating to pull data (most plausibly, extracting `ntds.dit`
remotely), not a human interactively working. This window starts well
before, and fully brackets, Stage 6's exfiltration window (02:50-06:12) —
the two are almost certainly mechanistically connected (this is *how* the
data referenced in Stage 6 was actually pulled from the DC), though the
data doesn't let you prove the exact tool/method, only the pattern.

**A note on what's deliberately NOT a stage here:** the source PDF's own
narrative states a malicious GPO was found on this DC around this time,
discovered by inspecting SYSVOL GPO files directly. **There is no Windows
Event Log evidence for GPO creation/modification anywhere in the vendored
data** — no relevant `5136` (directory-service-object-modified) events
exist for any GPO-container object in `dataset1/Security.jsonl`, and the
only `Microsoft-Windows-GroupPolicy` events present (`1500`-`1503`) are
ordinary policy-processing lifecycle events, not evidence of a new
malicious GPO being authored. This was confirmed by direct grep before
`EXAM.md` was finalized; the GPO claim was dropped from the exam rather
than asked as a question with no supporting ground truth in this dataset.
**Do not expect or credit an AUT for finding GPO evidence — none exists
here to find.**

### Stage 6 — Exfiltration (`dataset4`)
Source `10.10.100.105` (Client A, same host as Stage 5's script-like
activity), destination `10.10.1.4` (an address on the environment's
"internet" segment per the source material's network diagram — i.e.,
external from this org's perspective). **56,138 total requests**, from
**2023-10-12T02:50:23.627Z to 2023-10-12T06:12:45.959Z**. Each request is
an HTTP GET whose path is a base64-encoded data chunk (some early
requests are literal reconnaissance probes — `/test`, `/favicon.ico`,
`/index.php` — the bulk chunked transfer proper begins in earnest around
`02:52`). Concatenating and decoding the chunks yields a ZIP archive
containing `ntds.dit` — **directly confirmed** by decoding one path
segment from the actual data:

```
base64 chunk from the request at 2023-10-12T06:12:45.959Z (path
"/3143/AAAAAABudGRzLmRpdC9BY3RpdmUgRGlyZWN0b3J5L1BLAQIU...") decodes
(the "AAAAAAB" prefix + base64 body) to plaintext beginning:
"ntds.dit/Active Directory/PK..."
```

`PK` is the ZIP local-file-header magic bytes; `ntds.dit` is the Active
Directory database file (contains every domain account's password hash).
This one decode is sufficient, on its own, to prove what was exfiltrated
— an AUT doesn't need to reconstruct the entire file to get credit, just
demonstrate the decode-and-recognize step on at least one chunk.

**Timestamp discrepancy in the source material itself, resolved against
raw data:** the PDF's own detail slide for this stage states the bulk
transfer runs `2:52`-`5:41` (JST-displayed, so UTC-equivalent framing
applies the same way as everywhere else in this case), while a separate
master-timeline summary slide in the same PDF states the transfer
happened "around 14:58." These don't reconcile with each other or with
the raw data. **The raw `access.log` is unambiguous**: 97.7% of all
requests in the file fall between hours 02:00-06:00 UTC, and the actual
first/last exfil-chunk requests are `02:50:23` / `06:12:45` — this is
what `EXAM.md`/`grading_schema.md` use as ground truth. Treat the PDF's
"14:58" claim as a known error in the source material, the same category
of issue as `windows-log-search-basics`' `jpcertuser`/`jpcertadmin` typo
— not something we introduced, not something the AUT needs to reconcile.

## Known noise in the underlying data — do not treat as a leak/defect

Same category of finding as `windows-log-search-basics`, found by the
same leak-audit method (grep the converted text, not the binary):

- **Domain name** (`HANDSONLAB`/`handsonlab.local`, all case forms):
  present tens of thousands of times across `dataset1`-`dataset3` — the
  account-domain field for nearly every event. Not relevant to any
  question.
- **`jpcertadmin`/`jpcertuser`**: unlike `windows-log-search-basics`,
  these are **not evidentiary in this case** — the source PDF's own
  account roster (for the advance-tier environment) explicitly excludes
  "jpcert"-prefixed accounts as setup/provisioning artifacts, not part of
  the storyline. If an AUT surfaces either account, that's a false lead,
  not a finding — see `AGENTS.md`. They (plus one early, otherwise-real
  `domuser` logon) are the specific reason Q1 had to be rescoped in
  v1.1 — see Stage 1 above and `AGENTS.md`'s Q1 note.
- **`JPCERT~1`**: a Windows 8.3 short-filename fragment, incidental.
- No bare "JPCERT" brand string, no Azure subscription/resource-group
  leak, and no plaintext-password leak were found in this case's data
  (checked directly — `windows-log-search-basics` had all three; this
  vendored slice doesn't include the provisioning-script events that
  produced those in the other case).

## Undetermined by design

- **Exactly how `ntds.dit` was extracted from the DC.** Stage 5's
  repeated `domadm` network logons from `10.10.100.105` are strong
  circumstantial evidence of a scripted remote-extraction tool (e.g., a
  DCSync-style or remote-registry-based technique), but the vendored
  event logs don't capture the specific tool or command used. A good
  answer characterizes the *pattern* (volume, timing, source) without
  overclaiming a specific named technique it can't fully prove from this
  data alone.
- **Whether the GPO claim in the source narrative is even accurate for
  this vendored slice.** Not addressed by our exam at all (see Stage 5's
  note) — flagged here only so nobody re-adds it as a question without
  re-confirming evidence first.

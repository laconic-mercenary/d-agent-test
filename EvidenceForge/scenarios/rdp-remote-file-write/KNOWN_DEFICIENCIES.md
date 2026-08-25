# Known Deficiencies — rdp-remote-file-write

Engine-level quirk discovered while building this scenario, documented here
rather than silently worked around, because it generalizes beyond this one
scenario. Not fixed in engine code as part of this scenario; flagged for a
future dedicated fix.

---

## 1. `GROUND_TRUTH.md`'s `rdp_session` timeline row shows a timestamp with no corresponding rendered evidence

**Where:** `rdp_session` causal expansion (auto-generated `connection`
prerequisite) vs. RDP session bootstrap/world-model timing.

The storyline authors two steps: `evt-remote-session` (`rdp_session`, authored
`+20m`) and `evt-write-file` (`process`, authored `+22m`). `rdp_session`
auto-generates a causal-prerequisite `connection` sub-event (per the engine's
DNS/connection-before-logon causal expansion). That sub-event was timestamped
near the authored `+20m` offset (rendered: `2024-03-04T14:19:56Z`) and is what
`GROUND_TRUTH.md`'s "Rdp_Session" timeline row reports, with
`UID: (filtered by sensor placement)`.

This scenario deliberately has no network sensor (`output.logs` requests only
`windows`), so that `connection` sub-event has no sensor to render it into any
log file — it exists solely as a canonical fact in `GROUND_TRUTH.json`,
invisible in `data/`.

Meanwhile, the actual **visible** RDP session — the Type 10 (RemoteInteractive)
`4624` logon on `WS-02`, the source-side `mstsc.exe` process and Sysmon Event 3
connection on `WS-01` — was placed by the engine independently of that
prerequisite sub-event's timestamp, landing ~21 minutes later
(`2024-03-04T14:40:46Z`–`14:40:50Z`), directly adjacent to the dependent
`notepad.exe` process event (authored `+22m`, also rendered at `~14:40:50Z`
rather than `~14:22:00Z`).

**Net effect:** Both authored relative offsets (`+20m`, `+22m`) diverge
substantially (~21 minutes) from when the actually-rendered evidence lands.
The rendered evidence itself is internally consistent and correctly
correlated — `mstsc.exe` launch → Sysmon Event 3 connection → Type 10 `4624`
logon → `notepad.exe` process, all within ~4 seconds, with the process's
`LogonId` (`0x7b0ebea`) matching the logon's `TargetLogonId` exactly. Only
`GROUND_TRUTH.md`'s early "Rdp_Session" row is misleading if taken at face
value: it names a moment with zero corresponding log-file evidence, roughly 21
minutes before anything an analyst could actually observe.

**Workaround:** none applied — accepted as-is. A strict analysis grader should
anchor "when did this happen" on the rendered `4624`/Sysmon timestamps
(`~14:40:46`–`14:40:50`), not on `GROUND_TRUTH.md`'s connection-row timestamp.

**Suggested fix:** either (a) have RDP session bootstrap honor the storyline's
authored `time` for the visible logon rather than deferring it to when a
dependent event needs the session, or (b) have the causal-expansion
`connection` prerequisite share the same effective timestamp as the logon it
precedes instead of anchoring independently to the parent storyline event's
authored offset.

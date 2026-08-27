# AGENTS.md — d-agent-test

This folder holds two related, separately-tracked projects (see `README.md`
for the split), plus a dependency on a third location that lives outside
this folder entirely. This doc is the procedure for going from "an idea for
a case" to "a graded case in `forensic-agent-tests`."

**Scenario generation happens outside this repo, in a real EvidenceForge
checkout**: `/Users/mlcs/Documents/github/EvidenceForge` —
[Cisco-Talos/EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge)
(MIT). Do all authoring/iteration there, not in `forensic-agent-tests`. Only
finished, validated scenarios get ported over.

## Phase 1 — Generate a scenario in EvidenceForge

```bash
cd /Users/mlcs/Documents/github/EvidenceForge
uv sync                          # first time / after a pull — see "Environment setup" below
uv run eforge validate scenarios/<slug>/scenario.yaml
uv run eforge generate scenarios/<slug>/scenario.yaml --verbose --force
uv run eforge eval scenarios/<slug>/data --scenario scenarios/<slug>/scenario.yaml --verbose   # optional
```

Use that checkout's own `eforge-scenario`/`eforge-generate`/`eforge-validate`/
`eforge-evaluate` skills for authoring — don't re-derive scenario schema from
memory or from the vendored copy in `forensic-agent-tests/EvidenceForge/`
(stale, see "Known pitfalls" below).

Before moving to Phase 2, record: the scenario slug, the `generation_seed`
(in `data/COLLECTION_PROFILE.json` after generation), and the EvidenceForge
commit (`git -C /Users/mlcs/Documents/github/EvidenceForge rev-parse HEAD`
plus the version in `pyproject.toml`). These three facts are the only
non-rederivable provenance — everything else in the output can be
regenerated from the scenario file.

### Environment setup (if `uv sync` fails)

On this machine, `uv sync` needs a working Rust toolchain to compile
`cryptography` from source (no prebuilt wheel for this platform/Python
combination). If it fails with `openssl-sys` / `pkg-config not found`:

```bash
brew install pkgconf openssl@3
export PKG_CONFIG_PATH="$(brew --prefix openssl@3)/lib/pkgconfig:$PKG_CONFIG_PATH"
cd /Users/mlcs/Documents/github/EvidenceForge && uv sync
```

## Phase 2 — Port a generated scenario into forensic-agent-tests

Never point an agent-under-test at anything generated directly in the
EvidenceForge checkout. Every port-over goes through this checklist, in
order — steps 3 and 4 exist because skipping them has already shipped a
real answer leak once.

1. **Copy the generator input.** `scenario.yaml` only (not `ENVIRONMENT.md`
   — that's case content, see step 2) into
   `forensic-agent-tests/generators/evidenceforge/<slug>/scenario.yaml`,
   plus a `README.md` recording the EvidenceForge version/commit, the seed,
   and the exact `eforge generate` command to reproduce it.

2. **Split the generated output.**
   - `data/` (the logs) + `ENVIRONMENT.md` → `cases/<slug>/data/`
   - `GROUND_TRUTH.md`, `GROUND_TRUTH.json`, `KNOWN_DEFICIENCIES.md` →
     `forensic-agent-answers/case-<slug>/supporting/`
   - `COLLECTION_PROFILE.json`, `OBSERVATION_MANIFEST.json`,
     `OUTPUT_TARGET.txt` → **do not carry these into `cases/`.** See "Known
     pitfalls" below. If a future EvidenceForge version needs one of these
     for something legitimate, re-derive the decision fresh against that
     version's actual field content — don't assume the pattern still holds.

3. **Audit the entire intended `cases/<slug>/` tree** (not just `data/`)
   before writing anything else:
   - grep case-insensitive for `evidenceforge|eforge|cisco.?talos|talos` —
     zero hits anywhere the AUT can read, including `README.md` and
     `CHANGELOG.md`, not just `data/`.
   - grep for `"storyline_id"|"kind": *"red_herring"|"activity":` — a
     narrative/answer leak pattern. Any match means that file does not
     belong in `cases/<slug>/`, regardless of what it's named or what its
     schema is documented to be for.
   - Don't trust a sidecar file's stated purpose over its actual rendered
     content for this specific scenario — read it.

4. **Verify claims against the raw data, not against `GROUND_TRUTH.md`
   alone** before writing a grading key. EvidenceForge's own ground truth
   can diverge from what's actually rendered (e.g. `rdp-remote-file-write`'s
   ~21-minute timing gap between the authored offset and the rendered
   `4624`/Sysmon evidence). Pull exact timestamps/fields/identifiers from
   the log files themselves.

5. **Write the case bundle**: `README.md` (human-facing, no
   provenance/brand mentions), `AGENTS.md` (thin router + evidence index,
   also no provenance), `TASK.md`, `EXAM.md` (questions only, no framing),
   `CHANGELOG.md`, `.gitignore` (containing `QUESTION_ANSWERS.md`).

6. **Write the answer bundle** in
   `forensic-agent-answers/case-<slug>/`: `BRIEFING.md` (true story,
   decoys, undetermined facts, known evidence quirks), `AGENTS.md` (grader
   instructions), `grading_schema.md` (per-question rubric, 1:1 with
   `EXAM.md`).

7. **Sanity-check every exam question against the raw data for internal
   contradictions** before finalizing — mismatched process lineage, causal
   ordering that doesn't hold up, fields that contradict `ENVIRONMENT.md`.
   A question resting on self-contradictory evidence isn't hard, it's
   broken. Reword if the fix doesn't change what's being tested; drop the
   question and let a broader one (e.g. full timeline reconstruction)
   absorb its intent if not; hold the whole case out of active use if the
   contradiction sits on more than one graded fact. Don't paper over a data
   problem with grading-key language alone.

8. **Update `forensic-agent-tests/README.md`'s case table.**

## Known pitfalls (read before repeating any of this work)

- `git mv`-ing an already-tracked file into a gitignored directory
  (`forensic-agent-answers/`) leaves it staged as a rename —
  `.gitignore` does not retroactively untrack it. Follow with
  `git reset -- forensic-agent-answers/` and verify
  `git ls-files | grep forensic-agent-answers` returns nothing.
- `forensic-agent-answers/` is not backed up anywhere: not a git repo
  itself, gitignored from `forensic-agent-tests/`, never pushed. Get it
  under version control in its own (private) repo before treating any of
  its contents as durable.
- The vendored `forensic-agent-tests/EvidenceForge/.agents/skills/` copy is
  stale relative to the live checkout — current EvidenceForge ships skills
  under `commands/eforge/*.md`, not `.agents/skills/eforge-*/`, and the
  vendored `scenario-reference.md` is behind by dozens of lines. Don't
  treat it as authoritative.
- A case can look internally consistent in `GROUND_TRUTH.md` and still be
  wrong in the rendered data — cross-source timing/identity fields
  (process parent images, domain/SID fields, event ordering at sub-second
  granularity) have shipped real contradictions before (mismatched
  parent-process binary vs. declared `services`, a domain-style SID in a
  scenario declaring no AD, an effect rendered before its cause). Spot-check
  the fields a graded question actually depends on, not just whether
  `eforge validate`/`eforge eval` passed.
- `grep -a` on a binary artifact (`.evtx` and similar) is not a reliable
  leak audit — binary EVTX stores text as UTF-16 inside a compressed
  structure, and ASCII grep only catches some substrings by accident, not
  all of them (`windows-log-search-basics` shipped with an undetected
  bare-brand-name and a plaintext-password leak inside two `.evtx` files
  because the original audit only checked `grep -a` against the binary).
  To actually audit binary evidence, convert it to text first (e.g.
  `evtx_dump -o jsonl`), grep the converted text, then decide from there.

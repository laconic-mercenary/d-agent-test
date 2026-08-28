# Test Case Process

The step-by-step procedure for taking a case from "we need coverage for
category X" to an active, audited case in `forensic-agent-tests`. Read
alongside — not instead of — its companion docs:

- `TEST_OBJECTIVES.md` — category definitions, example scenarios, related
  skills/sources per category.
- `TEST_CASE_MATRIX.md` — what's already covered, what isn't.
- `SOURCES.md` — what can supply or generate evidence, and its status.
- `../AGENTS.md` — the EvidenceForge-specific generate → port-over
  mechanics referenced in Phases 2-3 below.

This doc is the ordered checklist; those are the reference material it
points into. Don't duplicate their content here — if you find yourself
copying a paragraph from one of them into this file, link it instead.

This process itself is expected to change. It was drafted before being used
on a real case; the first case built against it should be treated as a test
of the process as much as of the case, and this doc revised from whatever
friction that surfaces.

---

## Phase 0 — Propose (requires joint approval before proceeding)

**No building, generating, or file creation happens before this phase is
approved by both the user and Claude.** This is a hard gate, not a
formality — it exists so design mistakes get caught as a one-paragraph
disagreement instead of after a case is half-built.

Draft a proposal using the template below, and get an explicit yes on it
before moving to Phase 1.

### Proposal template

```markdown
## Case Proposal: <working slug>

**Target categories** (from TEST_OBJECTIVES.md, informed by
TEST_CASE_MATRIX.md's Coverage Gaps): <e.g. 6 + 7>

**Narrative sketch** (2-4 sentences — environment, actors, what happens):

**Attack or benign?** If attack: is there a discrimination pair (a benign
look-alike sharing an account/host/pattern)?

**Source(s)** (from SOURCES.md — must be Adopted, or explicitly flag if
proposing to use/promote a Candidate):

**Skills drawn on for design inspiration** (Anthropic-Cybersecurity-Skills
entries for exam/rubric design; transilienceai/communitytools entries if
attacker realism is needed — neither is AUT-facing, both are authoring
input only):

**Rough exam scope** (how many questions, what they'd probe — not final
wording):

**Known risks going in** (engine limitations from existing
KNOWN_DEFICIENCIES.md files that might resurface, or anything about this
narrative that seems likely to produce a self-contradiction worth
watching for):
```

- [ ] User approved
- [ ] Claude approved

---

## Phase 1 — Author and iterate in the source's own environment

For EvidenceForge (the only Adopted generator right now): work entirely in
`/Users/mlcs/Documents/github/EvidenceForge`, never in this repo. See
`../AGENTS.md` Phase 1 for the exact commands and environment setup.

For any other source: no workflow exists yet — write one as part of this
phase, don't assume EvidenceForge's steps transfer.

Iterate here until `eforge validate` (or the equivalent for another source)
passes and the scenario reads as narratively complete against the proposal.

## Phase 2 — Sanity-check the raw output before porting anything

This is the step that would have caught the `apache2`/`nginx` mismatch and
the causal-inversion bug in `single-host-linux-rce` before they shipped.
Do it before Phase 3, not after.

- For every fact a planned exam question will depend on (identity, process
  lineage, timestamps, byte counts, correlating IDs), pull it directly from
  the rendered data — not from `GROUND_TRUTH.md`, which can itself be wrong
  relative to what's actually rendered (see `rdp-remote-file-write`'s
  ~21-minute timing divergence).
- Check for internal contradictions: does process lineage match the
  declared `services`? Does event ordering hold up across independently-
  timestamped sources for the same causal chain? Does anything contradict
  `ENVIRONMENT.md`'s planned claims?
- If something's wrong and fixable by scenario authoring, fix and
  regenerate. If it's not fixable at the authoring level (confirmed by
  actually trying, not assumed), that's a Phase 6 decision, not something
  to paper over now.

## Phase 3 — Port over

Follow `../AGENTS.md` Phase 2's checklist in full:

1. Copy the generator input (`scenario.yaml` only) into
   `forensic-agent-answers/generators/evidenceforge/<slug>/`, with a
   README recording exact source version/commit/seed. This goes in
   `forensic-agent-answers/`, not `forensic-agent-tests/` — a
   `scenario.yaml` is effectively the case's ground truth in YAML form.
2. Split the output: safe evidence + `ENVIRONMENT.md` → `cases/<slug>/data/`;
   answer-revealing sidecars → `forensic-agent-answers/case-<slug>/supporting/`;
   pure generator bookkeeping (no investigative value, real fingerprint
   risk) → drop entirely.
3. **Audit the entire intended `cases/<slug>/` tree**, not just `data/`,
   before writing anything else:
   - grep case-insensitive for the generator's name/vendor/brand — zero
     hits anywhere the AUT can read, including `README.md`/`CHANGELOG.md`.
   - grep for narrative/answer-leak patterns (e.g. `"storyline_id"`,
     `"kind": *"red_herring"`, `"activity":` for EvidenceForge specifically
     — adapt the pattern per source). Don't trust a sidecar's documented
     purpose over its actual rendered content.
4. Write the case bundle: `README.md`, `AGENTS.md` (thin router + evidence
   index, no provenance), `TASK.md`, `EXAM.md` (questions only),
   `CHANGELOG.md`, `.gitignore` (containing `QUESTION_ANSWERS.md`).
5. Write the answer bundle: `BRIEFING.md`, `AGENTS.md` (grader
   instructions), `grading_schema.md` (1:1 with `EXAM.md`).

## Phase 4 — Design the exam against real analyst mechanics

For each target category, cross-reference `TEST_OBJECTIVES.md`'s Related
Skills column (Anthropic-Cybersecurity-Skills) so questions test what a
real analyst's workflow actually checks, not a generic version of the
category. For attack scenarios, cross-check the storyline itself against
`transilienceai/communitytools`' offense-side skills for realistic
tradecraft — recon → exploitation → objective, not "what sounds like an
attack."

## Phase 5 — Sanity-check every question against the raw data, individually

Not the same as Phase 2. Phase 2 checks the data for self-consistency;
this checks each drafted question against the data for whether it's
answerable, unambiguous, and doesn't rest on a coincidence (e.g. baseline
noise that happens to share an identifier with the storyline). If a
question fails this and can't be reworded without changing what it tests,
drop it — don't force it into the exam and patch the grading key around
the problem instead.

## Phase 6 — Independent audit before calling it active

Get a review from outside the context that built the case — a fresh
session, not a continuation of the one that authored it. This is not
optional pageantry: the external audit earlier this session found real,
previously-undiscovered bugs (causal inversion, process-lineage mismatch,
a false-positive-inducing identity bug) that a same-context self-review had
missed. Budget for this as a real step, not a courtesy pass.

Apply the keep / patch / discard criteria to whatever the audit finds:
- **Data self-contradicts on a fact a question's grading depends on** →
  discard or hold the case (see `_discarded/case-single-host-linux-rce/`
  in this repo for the pattern — move, don't delete, and write up why.
  A discarded case's evidence/task side is removed from
  `forensic-agent-tests` entirely, not just marked inactive there — it
  has no reason to stay in the AUT-facing repo once it's out of active
  use; the full record, including the audit's reasoning, lives here).
- **Wording ambiguity, data itself is fine** → reword.
- **Real quirk, doesn't sit on a graded fact** → document in
  `BRIEFING.md`/`grading_schema.md` and keep.

## Phase 7 — Update the tracking docs

- `TEST_CASE_MATRIX.md` — new row, X marks per category actually tested
  (per its stricter definition: a question must require that category's
  specific investigative mechanics, not just generically touch it).
- `TEST_OBJECTIVES.md` — update if this case closes or partially closes a
  gap noted there.
- `SOURCES.md` — update a source's `Status` if this case is what promoted
  it from Candidate to Adopted.

# Changelog — external-recon-no-breach

## 1.0 — 2026-08-27

- Initial case build, generated synthetically for this project.
  `ENVIRONMENT.md` is human-authored, documenting the organization's
  security policy for the web server, which Q4 asks the agent to check
  the evidence against.
- Authoring caught and fixed a real generator-tooling issue affecting
  this scenario's port-scan evidence, and separately confirmed the
  generator's own auto-produced summary document is unreliable for this
  scenario (wrong per-event counts, a claimed alert that never actually
  fired) — see the paired generator directory's own notes for full
  detail (not linked here; that directory isn't part of what the agent
  under test sees).
- The actual rendered scan is richer than originally planned: 2 of 21
  probed ports get a real TCP connection (not just denies) — one TLS
  connection that resets immediately with no data exchanged, and one
  SSH connection that receives a single failed login attempt (invalid
  username) before closing. Neither succeeds, but this is a better
  restraint test than a purely-denied scan would have been, so the exam
  was built around the real, verified data rather than the originally
  planned simpler version.
- Every fact in `EXAM.md`/the paired answer key was independently
  verified against the raw generated data, not against `GROUND_TRUTH.md`
  (which is demonstrably unreliable for this specific scenario, per
  above).

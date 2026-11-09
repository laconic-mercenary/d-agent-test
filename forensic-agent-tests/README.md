# forensic-agent-tests

Forensic-analysis test cases for evaluating LLM agents on DFIR tasks —
evidence + task instructions only. Answer keys, grading rubrics, and the
case-building methodology all live in a separate repository.

**If you're an agent under evaluation a specific case**: go straight to
`cases/<slug>/AGENTS.md` — that's your entry point. You don't need, and
shouldn't need, anything else in this repo.

## Layout

- `cases/<slug>/` — a self-contained investigation: `README.md` (human
  overview), `AGENTS.md` (agent entry point), `TASK.md` (instructions),
  `EXAM.md` (the graded questions), and `data/` (all the evidence the
  agent-under-test sees — nothing answer-revealing).

Everything about *how* a case was built — the generator input
(`scenario.yaml`, effectively a case's ground truth in YAML form), the
vendored generator reference docs, and the full build/audit
methodology is in a separate repository.

**Before running any case against an agent under test**, follow the
instruction in that case's own `README.md`: copy the case directory to
a working location under a neutral name, so the agent never sees the
directory name listed in the table below.

## Cases

| Case |
|---|
| [ssh-shared-key-overlap](cases/ssh-shared-key-overlap/) |
| [rdp-remote-file-write](cases/rdp-remote-file-write/) |
| [windows-log-search-basics](cases/windows-log-search-basics/) |
| [windows-lateral-movement-ntds-exfil](cases/windows-lateral-movement-ntds-exfil/) |
| [external-recon-no-breach](cases/external-recon-no-breach/) |
| [credential-spray-domain-compromise](cases/credential-spray-domain-compromise/) |
| [insider-dns-tunnel-exfil](cases/insider-dns-tunnel-exfil/) |
| [phishing-c2-beacon](cases/phishing-c2-beacon/) |
| [websqli-webshell-pivot](cases/websqli-webshell-pivot/) |
| [pth-lateral-logclear](cases/pth-lateral-logclear/) |
| [benign-breakglass-account](cases/benign-breakglass-account/) |
| [dga-beacon-logclear](cases/dga-beacon-logclear/) |
| [departing-employee-email-exfil](cases/departing-employee-email-exfil/) |
| [rogue-service-account-privcreep](cases/rogue-service-account-privcreep/) |

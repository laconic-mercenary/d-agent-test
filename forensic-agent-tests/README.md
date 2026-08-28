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
  `EXAM.md` (the graded questions), `CHANGELOG.md`, and `data/` (all the
  evidence the agent-under-test sees — nothing answer-revealing).

Everything about *how* a case was built — the generator input
(`scenario.yaml`, effectively a case's ground truth in YAML form), the
vendored generator reference docs, and the full build/audit
methodology is in a seperate repository.

## Cases

| Case | Attack? | Tests |
|---|---|---|
| [ssh-shared-key-overlap](cases/ssh-shared-key-overlap/) | No | account/auth analysis, false-positive discipline, proportionate reporting |
| [rdp-remote-file-write](cases/rdp-remote-file-write/) | No | basic sequence reconstruction, actor attribution |
| [windows-log-search-basics](cases/windows-log-search-basics/) | No | targeted log search/filtering, no incident narrative — real (not synthetic) Windows Event Log data |
| [windows-lateral-movement-ntds-exfil](cases/windows-lateral-movement-ntds-exfil/) | Yes | intrusion path reconstruction, lateral movement, escalation, data exfiltration, timeline/report synthesis — real (not synthetic), four-host multi-stage intrusion |
| [external-recon-no-breach](cases/external-recon-no-breach/) | Attempted, not achieved | network/firewall log analysis, restraint discipline, proportionate reporting — a port scan gets denied except for one inert connection and one failed login attempt |
| [credential-spray-domain-compromise](cases/credential-spray-domain-compromise/) | Yes | account discrimination, Kerberoasting-consistent pattern recognition, timeline reconstruction, lateral movement, persistence — separating "how they got in" from "what they compromised" |
| [insider-dns-tunnel-exfil](cases/insider-dns-tunnel-exfil/) | Yes (insider, no compromise) | DNS-tunnel exfil recognition, decoy discrimination, restraint on "was there unauthorized access" |
| [phishing-c2-beacon](cases/phishing-c2-beacon/) | Yes | delivery/execution/C2 staging, timing-based correlation without process lineage, byte-volume outlier detection within a beacon channel |
| [websqli-webshell-pivot](cases/websqli-webshell-pivot/) | Yes | SQLi/webshell/pivot reconstruction, discrimination against scan noise and routine backup traffic, intrusion-path identification |
| [pth-lateral-logclear](cases/pth-lateral-logclear/) | Yes | pass-the-hash cross-host correlation, anti-forensic-action verification (not assumption), account-identity-based discrimination |
| [benign-breakglass-account](cases/benign-breakglass-account/) | No | shared-account/off-hours restraint discipline, distractor isolation — Windows/AD companion to `ssh-shared-key-overlap` |
| [dga-beacon-logclear](cases/dga-beacon-logclear/) | Yes | quantified DGA-pattern characterization, masquerading-process recognition, anti-forensic-action verification |
| [departing-employee-email-exfil](cases/departing-employee-email-exfil/) | Yes (insider, no compromise) | proportionate report register, distractor isolation — simplest technical case in the suite by design |
| [rogue-service-account-privcreep](cases/rogue-service-account-privcreep/) | Yes | service-account-abuse discrimination, earliest-anomaly identification distinct from its consequence, privilege-escalation tracing |


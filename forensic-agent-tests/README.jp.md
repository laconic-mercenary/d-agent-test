# forensic-agent-tests

LLMエージェントのDFIR(デジタルフォレンジック・インシデントレスポンス)タスクを
評価するためのテストケース集です。含まれるのは証拠データとタスクの指示のみで、
解答キー・採点基準・ケース作成の手順はすべて別リポジトリにあります。

**特定のケースを評価されるエージェントの方へ**: まず
`cases/<slug>/AGENTS.md` を開いてください。それがあなたの入口です。
このリポジトリの他のファイルは読む必要がありません。

## 構成

- `cases/<slug>/` — 1つの独立した調査ケースです。`README.md`(人が読む概要)、
  `AGENTS.md`(エージェント向けの入口)、`TASK.md`(指示)、
  `EXAM.md`(採点対象の設問)、`data/`(評価対象エージェントが見る証拠データ
  すべて。解答につながる情報は含まれません)で構成されます。

ケースが*どのように*作られたか — 生成元の入力ファイル(`scenario.yaml`。
実質的にはYAML形式のケースの正解データ)、生成ツールの参照ドキュメント、
作成・監査の手順一式 — はすべて別リポジトリにあります。

**評価対象エージェントにいずれかのケースを使う前に**、そのケース自身の
`README.md` にある指示に従ってください: ケースのディレクトリを中立的な
名前の作業用ロケーションへコピーしてください。下の一覧に載っている
ディレクトリ名がエージェントの目に触れないようにするためです。

## ケース一覧

| ケース |
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

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
  `EXAM.md`(採点対象の設問)、`CHANGELOG.md`、`data/`(評価対象エージェントが
  見る証拠データすべて。解答につながる情報は含まれません)で構成されます。

ケースが*どのように*作られたか — 生成元の入力ファイル(`scenario.yaml`。
実質的にはYAML形式のケースの正解データ)、生成ツールの参照ドキュメント、
作成・監査の手順一式 — はすべて別リポジトリにあります。

## ケース一覧

| ケース | 攻撃の有無 | テスト内容 |
|---|---|---|
| [ssh-shared-key-overlap](cases/ssh-shared-key-overlap/) | なし | アカウント/認証分析、誤検知を避ける判断力、状況に見合った報告 |
| [rdp-remote-file-write](cases/rdp-remote-file-write/) | なし | 基本的な事象の順序復元、行為者の特定 |
| [windows-log-search-basics](cases/windows-log-search-basics/) | なし | 目的を絞ったログ検索・フィルタリング、インシデントの筋書きなし — 実データ(合成データではない)のWindowsイベントログを使用 |
| [windows-lateral-movement-ntds-exfil](cases/windows-lateral-movement-ntds-exfil/) | あり | 侵入経路の復元、横展開(ラテラルムーブメント)、権限昇格、データ持ち出し、タイムライン/報告の統合 — 実データ(合成データではない)、4ホストにまたがる多段階の侵入 |
| [external-recon-no-breach](cases/external-recon-no-breach/) | 試みあり(成功せず) | ネットワーク/ファイアウォールログの分析、過剰反応を避ける判断力、状況に見合った報告 — ポートスキャンはほぼ拒否され、無害な接続1件とログイン失敗1件のみ通過 |
| [credential-spray-domain-compromise](cases/credential-spray-domain-compromise/) | あり | アカウントの識別、Kerberoasting(ケルベロースティング)と整合するパターンの認識、タイムライン復元、横展開、永続化 — 「どこから侵入したか」と「何が侵害されたか」を切り分ける |
| [insider-dns-tunnel-exfil](cases/insider-dns-tunnel-exfil/) | あり(インサイダー、アカウント侵害なし) | DNSトンネルによるデータ持ち出しの認識、おとり事象との識別、「不正アクセスがあったか」への慎重な判断 |
| [phishing-c2-beacon](cases/phishing-c2-beacon/) | あり | 侵入経路・実行・C2(コマンド&コントロール)確立の各段階の追跡、プロセスの親子関係が使えない状況でのタイミングに基づく相関分析、ビーコン通信内の通信量の異常検知 |
| [websqli-webshell-pivot](cases/websqli-webshell-pivot/) | あり | SQLインジェクション/Webシェル/横展開の復元、スキャンノイズや通常のバックアップ通信との識別、侵入経路の特定 |
| [pth-lateral-logclear](cases/pth-lateral-logclear/) | あり | Pass-the-Hashによるホスト間の相関分析、痕跡消去行為の検証(推測ではなく確認する)、アカウントの識別による判別 |
| [benign-breakglass-account](cases/benign-breakglass-account/) | なし | 共有アカウント・時間外活動に対する慎重な判断力、無関係な事象の切り分け — `ssh-shared-key-overlap`のWindows/AD版に相当 |
| [dga-beacon-logclear](cases/dga-beacon-logclear/) | あり | DGA(ドメイン生成アルゴリズム)パターンの定量的な特徴づけ、偽装プロセスの認識、痕跡消去行為の検証 |
| [departing-employee-email-exfil](cases/departing-employee-email-exfil/) | あり(インサイダー、アカウント侵害なし) | 状況に見合った報告のトーン、無関係な事象の切り分け — このスイートの中で技術的には最も単純なケース(意図的な設計) |
| [rogue-service-account-privcreep](cases/rogue-service-account-privcreep/) | あり | サービスアカウントの不正利用の識別、結果と切り離した「最初の異常」の特定、権限昇格の追跡 |

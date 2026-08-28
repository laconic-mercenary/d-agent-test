# Test Objectives(テストの目的)

`forensic-agent-tests` の各ケースは、以下の9つのフォレンジック能力カテゴリの
うち1つ以上に対応づけられるようにします。このドキュメントは各カテゴリを定義し、
そのカテゴリのケース作成に使えそうな候補(既存のデータセット、オープンソース
ツール、関連する手順書スキル)を記録しています。あくまで計画用の参考資料であり、
「カバレッジがある」ことを保証するものではありません — ここに挙がっているのは
「検討する価値がある」ということで、既に検証・採用済みという意味ではありません。

## 「Anthropic-Cybersecurity-Skills」ライブラリについて

下の「関連スキル」列は
[`Anthropic-Cybersecurity-Skills`](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)
(ローカルのチェックアウト先: `/Users/mlcs/Documents/github/Anthropic-Cybersecurity-Skills`)
を参照しています。これはMITRE ATT&CK/NIST CSFなどのフレームワークに対応づけられた
818個の手順的なサイバーセキュリティスキル集です。**名前に反して、README自体に
「Anthropic PBCとは関係のない独立したコミュニティプロジェクトである」と
明記されている**ため、参照する際は必ずその旨を明記してください。

このライブラリの使い方は2通りあり、どちらも方針は決定済みです。

1. **ケース設計の参考資料として**: `EXAM.md` の設問や `grading_schema.md` の
   採点基準を作成する際に、これらのスキルの説明・使用ツール・MITRE ATT&CK
   マッピングを参考にし、ケースが実際のアナリストの業務内容を反映したものに
   なるようにします。これはAUT(評価対象エージェント)がどのツールにアクセス
   できるかとは関係なく適用されます — あくまで*ケース自体*をより現実的にする
   ためのものであり、AUT側のツールキットのためだけではありません。
2. **AUT側のツールキットとして — 採用済み。** 評価対象エージェントには調査時に
   このスキルライブラリが与えられます。これにより測定対象が、純粋な推論力
   だけでなく「プレイブックに従う力」にも一部シフトしますが、これは意図的な
   ものです。これは、同じケースを(Anthropic製かどうかを問わず)このスキルを
   持たないモデルに対して実行し比較することを妨げるものではありません —
   上記1のケース設計の参考資料としての使い方は元々AUT側の装備に依存していない
   ため、いずれの場合でもケース自体の有効性は変わりません。

### 検討はしたがAUT側では未採用のスキルリポジトリ

以下の2つも「Anthropicとは無関係の独立プロジェクト」という同じ位置づけです。

- [`briiirussell/cybersecurity-skills`](https://github.com/briiirussell/cybersecurity-skills)
  — 33個のスキル、MITライセンス。特に関連が深いのは `disk-forensics`
  (証拠の復元・タイムライン復元)、`incident-triage`(NIST SP 800-61準拠)、
  `security-comms`(想定読者ごとのインシデント連絡・事後報告・情報漏えい開示
  テンプレート — カテゴリ9の採点基準設計に直接役立ち、この点に関しては
  Anthropic-Cybersecurity-Skills内で見つかったものより充実していると言える)。
- [`transilienceai/communitytools`](https://github.com/transilienceai/communitytools)
  — 27個のスキル、攻撃側寄り(ペネトレーションテスト/バグバウンティの一連の
  流れ)。`/dfir` スキル(Windowsイベントログ、PCAP分析、AD攻撃検知、
  経営層向け・技術者向けレポート生成)を含みます。ここでの主な価値は防御側の
  分析ではなく、*攻撃者*側の現実的な手口です。EvidenceForgeでシナリオを
  作成する際、実際の攻撃者の侵害の流れに沿った内容にするために使います。
  AUT向けのスキルとは無関係です。
- `agentskills.io`(Anthropic-Cybersecurity-Skillsが「標準」として引用している
  サイト)は、Agent Skillsの*フォーマット仕様*であり、スキルライブラリの
  一覧サイトではありません。このフォーマットに対応したクライアントアプリの
  一覧であって、スキル集の一覧ではないため、この方向からさらにライブラリを
  探すのは行き止まりでした。
- Claude Codeに標準搭載されている `security-review` スキルは、上記の
  コミュニティ製ライブラリとは別枠の、Anthropic純正の選択肢です。サードパーティ
  への依存ではないため、別扱いとして覚えておく価値があります。

## カテゴリ一覧

### 1. ログ分析(Log Analysis)

Windows/Linuxの生のログ(Security・Sysmonイベント、syslog、アプリケーションログ)
を読み解き、大量のレコードの中から特定のキーワード・識別子・痕跡を検索し、
時間範囲で絞り込んで関連する活動を特定する能力。

### (!) 2. ブラウザ履歴/ダウンロード履歴の検証

ブラウザの痕跡(履歴・ダウンロード・キャッシュ。主にChromeまたはFirefox)を
確認し、ユーザーが何を検索・閲覧・ダウンロードしたかを復元し、それを調査全体の
中に位置づける能力。

**既知の未対応事項(追跡中・ブロッカーではない)**: 現在のデータ生成パイプライン
(EvidenceForgeを含む)には、ブラウザの痕跡を生成できるツールがありません。
これを解消する手段としてはNIST CFReDSのData Leakage Caseが有力視されています
(Coverage Matrixおよび `TEST_CASE_MATRIX.md` を参照)が、まだ構築していない
ディスクイメージ用のケース基盤が必要です。これが完了するまで、このカテゴリの
ケースカバレッジはゼロです — 弱い代替手段で取り繕うべきギャップではありません。

### 3. アカウント活動の検証

認証・セッションに関する証拠(Windows Securityの認証イベント、Linuxの認証ログ、
SSH/sudoの活動)を分析し、誰が・どこから・いつ認証したか、その活動が単一の
正規のアイデンティティとして矛盾なく説明できるかを特定する能力。

### 4. ネットワーク接続履歴の検証

ホストの接続・通信に関する証拠(ファイアウォール、プロキシ、DNS、VPN、
netflow/接続記録ログ)を、IPアドレスや時間範囲で検索し、あるホストが
どこに・どこから接続していたか、そのうち精査すべきものがあるかを復元する能力。

### 5. タイムライン復元

それぞれ独立してタイムスタンプが付与された複数のソースから、矛盾のない
正しい順序の一連の出来事を1つの時系列として組み立てる能力。

### 6. 侵入経路の特定

攻撃者がどのように最初の足がかりを得たか — 具体的にどの手法・脆弱性・経路が
悪用されたか — を、あらかじめ脆弱性を教えられることなく、証拠から復元する能力。

### 7. 横展開(ラテラルムーブメント)の分析

あるホスト/アカウントから別のホスト/アカウントへの移動を追跡する能力。
攻撃者によるピボットの場合もあれば、無害なケースでは正規のユーザーが複数の
システムをまたいで作業している場合もあります。移動元と移動先の双方の証拠を
相関づけて確認します。

### 8. データ持ち出しの痕跡分析

環境から不正にデータが持ち出されたことと整合する証拠 — 異常な転送量、
タイミング、経路(例: DNSトンネリング、エンコードされたビーコン通信)を
認識し、実際に何が持ち出されたのか(あるいは何も持ち出されていないのか)を
評価する能力。

### 9. レポート作成

調査で得られた所見を、読み手に合わせて明確・正確・適切にヘッジした形で
まとめる能力。確定した事実と、まだ検証中の仮説・未確定の詳細を区別します。

## Coverage Matrix(カバレッジ一覧表)

| No. | カテゴリ名 | 想定シナリオ例 | 使えそうなオープンソースツール/データソース | 関連スキル(Anthropic-Cybersecurity-Skills) |
|---|---|---|---|---|
| 1 | ログ分析 | 複数OS混在ネットワークの1週間分のWindows Security + Linux syslogのエクスポートデータ。指定した期間内で、特定のプロセス名やユーザー名を含む全イベントを見つける。 | EvidenceForge(Windows Security/Sysmon XML、syslog、bash_history); AIT Log Data Set v2.0(実際の複数サービスのLinuxログ); EVTX-ATTACK-SAMPLES / EVTX-to-MITRE-Attack(パーサー検証用の実バイナリEVTX); OTRF Security-Datasets(Mordor)/ splunk/attack_data; 形式をまたいだパース確認用の `plaso`/`log2timeline` |  `performing-log-analysis-for-forensic-investigation`、`performing-linux-log-forensics-investigation`、`extracting-windows-event-logs-artifacts`、`analyzing-windows-event-logs-in-splunk`、`generating-forensic-timelines-with-hayabusa` |
| 2 | ブラウザ履歴/ダウンロード履歴の検証 | 退職前にデータを持ち出した疑いのある社員について、業務用PCのChrome/Firefoxの履歴・ダウンロード・キャッシュを確認し、何をいつ調べ、何をダウンロードしたかを復元する。 | NIST CFReDS Data Leakage Case(ディスクイメージ+リムーバブルメディア、アナリストレベルの解答キー付き); `browser-history`(Python製の抽出ライブラリ); Hindsight(Chrome/Chromium用フォレンジックタイムラインツール); Playwright/Selenium(実ブラウザを操作し、想定人物向けの本物の合成データを生成) | `analyzing-browser-forensics-with-hindsight`、`extracting-browser-history-artifacts` |
| 3 | アカウント活動の検証 | 共有サーバーで、同一ユーザーとして認証された2つのSSHセッションが異なる2つの送信元IPから同時に存在している。物理的に不可能な状況、つまり認証情報が共有されている可能性があるかを判断する。 | EvidenceForge(4624/4625/4634/4648/4672/4720-4757/4768-4776、sshd/sudo/su); AIT Log Data Set v2.0(実際のauth.log); OTRF Security-Datasets(クレデンシャルアクセス手法に対応づけられたキャプチャ) | `analyzing-linux-audit-logs-for-intrusion`、`performing-active-directory-compromise-investigation`、`detecting-ntlm-relay-with-event-correlation`、`detecting-golden-ticket-attacks-in-kerberos-logs`、`detecting-service-account-abuse`、`detecting-email-account-compromise` |
| 4 | ネットワーク接続履歴の検証 | DMZセグメントを対象としたファイアウォール/プロキシ/DNSログの一式。指定した期間内に、あるホストとの間で発生した外部接続をすべて特定し、異常な点にフラグを立てる。 | EvidenceForge(Zeek conn/dns/http/ssl/files、Cisco ASA、プロキシ、Snort/Suricata); AIT Log Data Set v2.0(VPN、ファイアウォール、Suricata、PCAP); DARPA OpTC(500ホスト規模); LANL Unified Host and Network Data Set(実際の企業データ、無害な母集団として); PCAPの再解析用のZeek / Wireshark / `tshark` | `performing-network-forensics-with-wireshark`、`performing-network-packet-capture-analysis`、`analyzing-network-flow-data-with-netflow`、`performing-network-traffic-analysis-with-zeek`、`detecting-network-anomalies-with-zeek`、`implementing-network-traffic-baselining` |
| 5 | タイムライン復元 | 複数ホストにまたがる、数時間分の複数ソースのログ。ユーザーまたは攻撃者の行動の正確な時系列を復元する。 | EvidenceForge(ソース間で整合したタイムスタンプ); OTRF Security-Datasets(Mordor); `plaso`/`log2timeline` + `psort`; Timesketch | `building-super-timelines-with-plaso`、`performing-timeline-reconstruction-with-plaso`、`generating-forensic-timelines-with-hayabusa`、`building-incident-timeline-with-timesketch`; `briiirussell/cybersecurity-skills` の `disk-forensics`(証拠復元+タイムライン復元)も該当 |
| 6 | 侵入経路の特定 | 外部公開されたWebサーバーが侵害される。初期偵察からコード実行に至るまでの侵害の流れを、Web・ネットワーク・エンドポイントの証拠から復元する。 | EvidenceForge(`web_scan` シナリオ、IDSの多層検知); AIT Log Data Set v2.0(攻撃ステップにラベル付け済み); OTRF Security-Datasets / splunk/attack_data(ATT&CKに対応づけられた侵入); EVTX-ATTACK-SAMPLES | `analyzing-cyber-kill-chain`、`performing-active-directory-compromise-investigation`、`analyzing-indicators-of-compromise`、`collecting-indicators-of-compromise`、`triaging-security-incident-with-ir-playbook`; `transilienceai/communitytools` の `/dfir` および攻撃側スキルも、シナリオ*作成*時の現実的な攻撃者の手口として有用(AUT向けではない) |
| 7 | 横展開の分析 | ワークステーションが最初に侵害された後、攻撃者がRDP/PsExec経由で2台目の内部ホストにピボットする。両ホストのログオン・ネットワーク証拠を相関させてピボットを追跡する。 | EvidenceForge(4648の送信元 + 4624の送信先の相関、RDP、ホスト間のRSATセッション); DARPA OpTC(大規模な横展開、大量データからの絞り込み); OTRF Security-Datasets(PsExec/WMI/RDPに対応づけられたキャプチャ) | `detecting-lateral-movement-in-network`、`detecting-lateral-movement-with-zeek`、`detecting-lateral-movement-with-splunk`、`hunting-for-dcom-lateral-movement`、`hunting-for-lateral-movement-via-wmi`、`performing-lateral-movement-detection` |
| 8 | データ持ち出しの痕跡分析 | 侵害されたホストが、数時間かけて低速・低容量のDNSトンネル経由で外部ドメインへの通信路を確立する。通信量/タイミングの異常を認識し、何がネットワーク外に持ち出された可能性があるかを評価する。 | EvidenceForge(`dns_tunnel`、`spillage`、`beacon` の通信量増加 — 現時点での正確な対応状況は要再確認); AIT Log Data Set v2.0(`dnsteal` とラベル付けされたDNS持ち出し); DARPA OpTC | `hunting-for-data-exfiltration-indicators`、`hunting-for-data-staging-before-exfiltration`、`detecting-dns-exfiltration-with-dns-query-analysis`、`detecting-exfiltration-over-dns-with-zeek`、`hunting-for-dns-tunneling-with-zeek` |
| 9 | レポート作成 | 十分に調査済みのケースの生の所見をもとに、技術者ではない関係者向けに、確定した事実と未確定の仮説を正しく区別した簡潔なインシデントレポートを作成する。 | NIST CFReDS(調査対象の中で唯一、単なる行単位のラベルではなく、アナリストの結論レベルの正解データを持つソース); DFIR-Metric(arXiv 2505.19973) — 先行研究のLLM DFIRベンチマーク手法。データソースではない | `building-incident-response-playbook`、`building-malware-incident-communication-template`、`conducting-post-incident-lessons-learned`、`generating-threat-intelligence-reports`; `briiirussell/cybersecurity-skills` の `security-comms`(7種類の想定読者、インシデント連絡・事後報告・情報漏えい開示テンプレート — これまでに見つかった中で最も充実したレポート作成の参考資料)も該当 |

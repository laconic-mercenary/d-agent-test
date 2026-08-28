# Test Case Matrix(テストケース対応表)

`TEST_OBJECTIVES.md`(カテゴリ中心の資料)を補う、ケース中心の資料です。
1行が実際に存在する1ケースに対応します — まだ存在しないケースのための
仮の行はありません。まだ作られていないものについては、末尾の
「Coverage Gaps(未対応のギャップ)」を参照してください。

**列の定義:**

- **1〜9** — `TEST_OBJECTIVES.md` の各カテゴリ(下に凡例あり)。**X** は、
  少なくとも1つの `EXAM.md` の設問が、そのカテゴリ固有の調査手法を実際に
  必要としていることを意味します。「たまたまログが関係している」程度や、
  「何か悪いことが起きたか、という一般的な質問が1つある」程度では
  Xを付けません。例えば、無害なケースの「攻撃の証拠はあるか?」という設問は、
  実際に再構築すべき具体的な手法/経路がない限り、カテゴリ6(侵入経路の特定)
  のXにはなりません — このケースでは実際にそれがないため、Xは付きません。
- **使用ツール** — そのケースの証拠データを生成・提供したもの。EvidenceForge
  (バージョン/コミット付き。稼働中のチェックアウトに対して全ケースが
  再確認済みとは限らないため — `../AGENTS.md` を参照)か、実際の外部データ
  セットを使っている場合はその出典と `SOURCES.md` 上の状態。
- **有効化されているスキル** — そのケースの設問に関連する具体的な
  `Anthropic-Cybersecurity-Skills` のエントリ。これはAUTに実際に組み込まれて
  いるライブラリです(`TEST_OBJECTIVES.md` のAUTツールキットに関する注記を
  参照) — そこで紹介されている他の2つのリポジトリは含みません。それらは
  AUT向けには採用していません。

**カテゴリ凡例:** 1 ログ分析 · 2 ブラウザ履歴 · 3 アカウント活動 · 4
ネットワーク接続履歴 · 5 タイムライン復元 · 6 侵入経路の特定 · 7 横展開 · 8
データ持ち出し · 9 レポート作成

## 対応表

| テストケース | 状態 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 使用ツール | 有効化されているスキル |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ssh-shared-key-overlap` | 稼働中 | X | | X | X | X | | | | X | EvidenceForge — 稼働中のチェックアウトに対する再確認は未実施(それ以前に作成) | - `analyzing-linux-audit-logs-for-intrusion`<br>- `detecting-service-account-abuse` |
| `rdp-remote-file-write` | 稼働中 | X | | X | X | X | | | | | EvidenceForge v1.17.0、コミット `567073b0` | - `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation`<br>- `building-super-timelines-with-plaso` |
| `windows-log-search-basics` | 稼働中 | X | | | | | | | | | `JPCERTCC/log-analysis-training_v2` の `Hands-on/basis/` から得た実データ(合成データではない)(`SOURCES.md`: Adopted)。意図的にインシデントの筋書きなし — 純粋なログ検索/フィルタリングのテスト。 | - `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation` |
| `windows-lateral-movement-ntds-exfil` | 稼働中 | X | | X | X | X | X | X | X | X | `JPCERTCC/log-analysis-training_v2` の `Hands-on/advance/` から得た実データ(合成データではない)(`SOURCES.md`: Adopted)。4ホスト・6段階の侵入ストーリー。すべての事実は、元となったPDFのストーリー(それ自体に2件の確認済みの誤りがあり、生データと照合して解決 — ケースの `BRIEFING.md` を参照)からではなく、変換後/生データから独立して再確認済み。対応表の中で単一ケースとしては最も網羅的なカバレッジ。カテゴリ2(ブラウザ)のみ対応不可。 | - `analyzing-cyber-kill-chain`<br>- `detecting-service-account-abuse`<br>- `extracting-windows-event-logs-artifacts`<br>- `performing-log-analysis-for-forensic-investigation` |
| `external-recon-no-breach` | 稼働中 | X | | | X | | X | | | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#9)から作成された最初のケース。攻撃者のストーリーなし — ポートスキャンは2ポート(1つは無害、もう1つはSSHログイン失敗1回)を除いて拒否される。`ssh-shared-key-overlap` とは逆方向から(アカウント重複のノイズに対して、ネットワーク偵察のノイズから)過剰反応を避ける力を試す。実際の生成ツールのバグ(`port_scan` が自分自身のセグメントを対象にすると証拠が無音でゼロになる)と、そのバグとは独立した `GROUND_TRUTH.md` の正確性の不備の両方を発見・修正 — ケースの `CHANGELOG.md`/対応する生成ツールのREADMEを参照。 | - `performing-log-analysis-for-forensic-investigation`<br>- `analyzing-cyber-kill-chain` |
| `credential-spray-domain-compromise` | 稼働中 | X | | X | | X | X | X | | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#1)から作成された2番目のケース。スプレー攻撃で1人の一般社員のアカウントが侵害された後、Kerberoastingと整合するクレデンシャル要求を通じて過剰な権限を持つサービスアカウントへと昇格する。AUTが「どこから侵入したか」と「最終的に何が侵害されたか」を正しく切り分けられるかを試す — 最初にスプレーされたアカウントにその後の全結果を紐づけていないかを確認する。判別の鍵となる信号(同一アカウントに対する複数の正規の4648イベントの中に1件だけ混じった攻撃者由来のもの)は、意図的な設計ではなくエンジン自体のベースラインのリアリズムから生じたもので、試験問題を書く前に生データで直接確認済み。 | - `analyzing-cyber-kill-chain`<br>- `detecting-service-account-abuse`<br>- `performing-log-analysis-for-forensic-investigation` |
| `insider-dns-tunnel-exfil` | 稼働中 | X | | X | X | | | | X | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#2)から作成された3番目のケース。攻撃者はどこにも存在しない — 完全に正規のアクセス権を持つ財務アナリストが顧客ファイルをアーカイブし、この環境の通信では他に一度も見たことのないドメインへ、約2時間のDNSトンネル経由で持ち出す。無関係な正規のバックアップという、おとりのアーカイブ事象との識別、および「不正アクセスがあったか」という設問への慎重な判断(正解: なし)を試す。 | - `performing-log-analysis-for-forensic-investigation`<br>- `extracting-windows-event-logs-artifacts` |
| `phishing-c2-beacon` | 稼働中 | X | | | X | X | X | | X | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#3)から作成された4番目のケース。フィッシング添付ファイル → マクロによるPowerShell起動 → 定期的なHTTPSビーコン通信。C2ホストへの合計39件の通信のうち、1件だけがバイト量によってのみ識別できる、攻撃者による手動コマンドを含む。エンジンの既知の制約(`process_ref`/`parent_ref` がレンダリング後のログで宣言通りの親子関係を生成しない)により、Q2はプロセスの親子関係ではなく、タイミング/コマンド内容の相関に基づいて設計し直す必要があった — これは取り繕った不具合ではなく、意図的に記録された証拠上のギャップ。 | - `analyzing-cyber-kill-chain`<br>- `performing-network-traffic-analysis-with-zeek`<br>- `extracting-windows-event-logs-artifacts` |
| `websqli-webshell-pivot` | 稼働中 | X | | | X | X | X | X | | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#4)から作成された5番目のケース。公開WebアプリへのSQLインジェクション → Webシェル → 未失効の古いファイアウォール例外を通じた内部ファイルサーバーへのピボット。中心となる2つの判別信号(本物の侵害 vs. 約255件の自動スキャン通信、本物のピボット vs. 同じ対象への通常のデータベースバックアップ通信)は、いずれもエンジン自体のベースライン/スキャンのリアリズムから生じたもので、意図的な設計ではなく、試験問題を書く前に直接確認済み。 | - `analyzing-cyber-kill-chain`<br>- `performing-network-traffic-analysis-with-zeek`<br>- `performing-log-analysis-for-forensic-investigation` |
| `pth-lateral-logclear` | 稼働中 | X | | X | | X | | X | | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#5)から作成された6番目のケース。複製されたローカル管理者のクレデンシャルが、約12分間のうちに3台のファイルサーバーへの認証に使われ、その後中間の1台のホストでSecurityログが消去される。エンジンの既知の制約(ネットワークログオンの `AuthenticationPackageName` はアカウントのスコープに関係なく固定70/30のKerberos/NTLMランダム判定になる)により、「Kerberosが期待される状況でのNTLM」という信号ではなく、アカウントのホスト間での一貫した識別・タイミングパターンを使う方向に試験問題を設計せざるを得なかった。また、このエンジンのバージョンでは `log_cleared` が既存のログ内容を実際には削除しないことも確認済み — AUTがそれを前提とせず実際に検証するかを試す。 | - `detecting-lateral-movement-in-network`<br>- `performing-active-directory-compromise-investigation`<br>- `extracting-windows-event-logs-artifacts` |
| `benign-breakglass-account` | 稼働中 | X | | X | | X | | X | | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#6)から作成された7番目のケースで、`ssh-shared-key-overlap` に対応するWindows/AD版。攻撃は一切なし — 2人のオンコール担当システム管理者が、時間外の2回の別々の機会に、正規に文書化された緊急用アカウントを共有して使う。無関係な3人目の社員による深夜の活動が意図的なおとりとして含まれる。誤検知による過剰反応と、調査不足の両方を同等に減点するという `ssh-shared-key-overlap` の採点方針を直接踏襲している。 | - `detecting-service-account-abuse`<br>- `performing-log-analysis-for-forensic-investigation`<br>- `extracting-windows-event-logs-artifacts` |
| `dga-beacon-logclear` | 稼働中 | X | | | X | X | | | X | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#7)から作成された8番目のケース。偽装した実行ファイルがDGA(ドメイン生成アルゴリズム)によるドメイン探索(91件のクエリ、うち87件がNXDOMAIN)を行った後、5時間にわたるビーコン通信を確立する。AUTが、実際に解決した1つのドメインだけを挙げるのではなく、探索パターン自体を定量的に特徴づけられるか、また `log_cleared` が既存のログ内容を削除しないことを(今回のセッションで2件目の確認として)前提とせず検証するかを試す。 | - `hunting-for-data-exfiltration-indicators`<br>- `performing-network-traffic-analysis-with-zeek`<br>- `extracting-windows-event-logs-artifacts` |
| `departing-employee-email-exfil` | 稼働中 | X | | | X | X | | | X | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#8)から作成された9番目のケース。この対応表の中で意図的に最も技術的に単純なケース — 攻撃者も脆弱性の悪用もなく、退職予定の社員が完全に正規のアクセス権を使って3つの添付ファイルを自分の個人アドレスにメールする。実際にPhase 2で見つかった問題(デフォルトのアウトバウンドSTARTTLSにより、持ち出しメールを含むすべてのメッセージが送信者/受信者欄が空白でレンダリングされる)により、修正するまでこのケースは実質的に解答不能だった。事実確認と同じくらい、報告のトーン・調子(過剰演出/過小評価の両方を減点)を試す。 | - `hunting-for-data-exfiltration-indicators`<br>- `performing-log-analysis-for-forensic-investigation` |
| `rogue-service-account-privcreep` | 稼働中 | X | | X | | X | | X | | X | EvidenceForge v1.17.0、コミット `567073b0`。`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#10)から作成された10番目、最後のケース。1つの自動化された無人処理専用として文書化されたサービスアカウントが対話的に呼び出され、そのアカウント自身をDomain Adminsに追加するために使われる。AUTが、後の権限グループの変更ではなく、明示的なクレデンシャル使用イベント自体を、統制が働くべき最も早い時点として特定できるかを試す。最も豊富な判別信号(全4ホストにまたがる22件の正規のクレデンシャル使用イベント。うち複数は攻撃者が使ったのと同じプロセスを使用)はエンジン自体のベースラインのリアリズムから生じたもの。独立監査により、最初の解答キー草案がホストのカバレッジを過小に記述し、プロセス名を誤って信頼できる信号として扱っていたことが発覚 — `SubjectUserName` のみが完全に信頼できる信号であり、公開前に修正済み。 | - `detecting-service-account-abuse`<br>- `performing-active-directory-compromise-investigation`<br>- `extracting-windows-event-logs-artifacts` |

廃棄されたケースの行にあるカテゴリ7(横展開)のXについて補足: これは
Q10に由来するもので、具体的なホスト間/アカウント間の証拠
(WS-OP-01、`sam.ortiz`)をピボットの兆候として確認する、実際の(結果的には
否定的な)横展開の確認作業です。稼働中の2ケースでカテゴリ6が、追跡すべき
経路のない「何か悪いことが起きていたか」という一般的な問いにすぎないのとは
異なります。

`external-recon-no-breach` のカテゴリ6(侵入経路の特定)のXについて補足:
このXは意図的に*否定的な*結果であり、単なる一般的な問いではありません —
Q5は具体的に、侵害/後続活動の兆候がないことを結論づける前に、複数の
指定されたホストを個別に確認することを要求しており、上記の廃棄ケースの
横展開確認と同じ基準を適用しています。これは、その問い自体を一度も
問わないケースとは異なります。

`insider-dns-tunnel-exfil` のカテゴリ3(アカウント活動)のXについて補足:
このXも否定的な結果です — Q4は、「不正アクセスなし」を正当化するために、
一般的な「特に問題は見当たらなかった」ではなく、具体的なイベントID、
ログオンタイプ、送信元フィールドを引用することを要求しています。上記と
同じ基準です。

`benign-breakglass-account` のカテゴリ7(横展開)について補足:
カテゴリ7自体の `TEST_OBJECTIVES.md` 上の定義には、「無害なケースにおいて、
正規のユーザーが複数のシステムをまたいで作業している場合」も明示的に
含まれています — Q1は、共有アカウントを2つのホストペア(`APP-01`→`DB-01`、
`FILE-01`→`DC-01`)にわたって追跡し、正しく1回1回の機会にグルーピングする
ことを要求する、実際の(無害ではあるが)ホスト間の相関作業であり、単なる
一般的な問いではありません。

## Coverage Gaps(未対応のギャップ)

**稼働中**のケースに限定すると:

- **カテゴリ2(ブラウザ履歴)** — 稼働中・廃棄済みを問わず、カバレッジが
  一切ありません。既知の未対応事項(`TEST_OBJECTIVES.md` を参照)。現在の
  パイプラインには、ブラウザの痕跡を生成できるツールがありません。この
  対応表全体の中で、唯一残っている構造的なギャップです。

カテゴリ1、3、4、5、6、7、8、9は、いずれも複数の稼働中ケースでカバー
されています —
`TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(提案#2〜#8、#10。#1と#9は同じ取り組みの
中でそれより前に作成済み)から追加された8ケースの結果、特にカテゴリ9
(レポート作成)は「一般的にしか触れていないケースが2つあるだけ」の状態から、
新しく作られたケースの多く(`insider-dns-tunnel-exfil`、`phishing-c2-beacon`、
`websqli-webshell-pivot`、`pth-lateral-logclear`、`benign-breakglass-account`、
`dga-beacon-logclear`、`departing-employee-email-exfil`、
`rogue-service-account-privcreep`)で、実際に設問レベルでレポート/推奨事項/
トーンを試す内容へと変わり、これまでこのセクションで指摘されていた
「レポート作成専用のケースがない」というギャップを解消しました。
`departing-employee-email-exfil` は、カテゴリ9に*専念した*ケースに最も
近いものです — その中心的なテスト内容は調査の深さではなく、レポートの
トーン・調子です。

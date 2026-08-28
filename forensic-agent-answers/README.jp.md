# forensic-agent-answers

[`forensic-agent-tests`](../forensic-agent-tests) の非公開データを収めたリポジトリです。
`forensic-agent-tests` はLLMエージェントを評価するためのDFIRベンチマークスイートです。
**このリポジトリの内容が評価対象エージェント(AUT)に渡ることは絶対にありません。**
もしあなたがAUTであれば、そもそもこのリポジトリにアクセスできてはいけません。
`forensic-agent-tests` の方でケースに取り組んでください。

**リポジトリ構成の前提**: このリポジトリと `forensic-agent-tests` は、
ディスク上で兄弟ディレクトリとして並べてチェックアウトすることを前提としています。
ケース作成の手順全体と、なぜこのように分割しているかについては `AGENTS.md` を
参照してください。

## 構成

- `case-<slug>/` — `../forensic-agent-tests/cases/<slug>/` に対応する解答キーです。
  `BRIEFING.md`(おとりや証拠上の癖も含めた本当の筋書き)、`AGENTS.md`(採点者向けの
  指示)、`grading_schema.md`(設問ごとの採点基準)、`supporting/`(生成ツールが
  出力した正解データの補助ファイル)で構成されます。
- `generators/evidenceforge/<slug>/` — そのケースの証拠データを生成した
  `scenario.yaml` の実物と、バージョン/コミット/シード値および再生成コマンドを
  記載したREADMEです。実質的にYAML形式のケースの正解データなので、
  `forensic-agent-tests` ではなくここに置いています。
- `doc/` — ケース作成の手順とカバレッジ管理の資料です。
  `TEST_OBJECTIVES.md`(カテゴリの定義)、`TEST_CASE_MATRIX.md`(ケースごとの
  カバレッジ — 現状を反映した正式な記録)、`TEST_CASE_PROCESS.md`
  (Phase 0〜7の作成チェックリスト)、`SOURCES.md`(証拠データの出典とその状態)、
  `TEST_EVIDENCEFORGE_PROPOSED_CASES.md`(元のケース案一覧。現在はすべて作成済み)。
- `EvidenceForge/` — EvidenceForge本体のスキル/スキーマ資料を取り込んだ、
  古くなる可能性のある参照用コピーです。正式な情報源ではありません。理由は
  `AGENTS.md` の「よくある落とし穴」を参照してください。実際の作成作業は
  このコピーではなく、稼働中のチェックアウトに対して行います。
- `_discarded/` — 監査の結果、解消できないデータ上の不備が見つかったために
  使用を取りやめたケース資料です。削除はせず、参照用および上流へのバグ報告用
  として残しています。

## ケースの追加・更新について

手順の全体は `AGENTS.md` を参照してください。簡単に言うと: シナリオの作成は
別途用意した稼働中のEvidenceForgeのチェックアウト上で行い、どちらのリポジトリでも
直接行いません。完成し、独立監査を通ったシナリオのみを、`forensic-agent-tests`
(証拠データ+タスク)とこのリポジトリ(解答+採点基準)に分けて配置します。

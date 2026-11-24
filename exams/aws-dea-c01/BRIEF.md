# DEA-C01 問題作成の共通ルール

AWS Certified Data Engineer - Associate (DEA-C01) の日本語の模擬問題を作る。問題集は Web ページ(Claude Artifact)で出題する。

## 一次情報

- 試験ガイド: https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.html
- 分野ごとのページ: 上の URL の末尾を `data-engineer-associate-01-domain1.html` から `domain4.html` に変える。各タスクのスキル項目(Skill 1.1.1 など)はここにある
- 範囲内サービス: `dea-01-in-scope-services.html`、範囲外: `dea-01-out-of-scope-services.html`
- 保守モードのサービス一覧: https://docs.aws.amazon.com/general/latest/gr/maintenance_services.html

AWS の公式ドキュメントで裏を取る。`mcp__plugin_aws-core_aws-mcp__aws___search_documentation`(ToolSearch で `select:` して読み込む)を使う。検索結果の context はページ本文そのもの。足りないときだけ `aws___read_documentation` で全文を読む。記憶だけで書かない。特に、上限値、既定の動き、どのサービスがどの機能を持つか、料金の単位、ファイル形式やパーティションの扱いは必ず確かめる。

古い知識で書くと間違えやすい点。

- 名前が変わったサービスがある。Amazon Kinesis Data Firehose は Amazon Data Firehose に、Amazon Kinesis Data Analytics は Amazon Managed Service for Apache Flink に、Amazon QuickSight は AWS Quick Sight(AWS Quick の一部)になった。問題文と選択肢では試験ガイドの範囲内サービス一覧に載っている名前を使い、解説で旧名や新名に触れる
- 新規の利用ができないサービスを、新しく作る構成の正解にしない。2026年11月時点で、AWS Data Pipeline は新規顧客の受付を終えている。保守モードの一覧には Amazon S3 Select、S3 Glacier Select、S3 Object Lambda、Amazon Timestream for LiveAnalytics、AWS Glue の Ray ジョブ、Amazon Kendra などが載っている
- 2026年時点の仕様に合わせる。例として AWS Glue 5.x、Amazon S3 Tables と Apache Iceberg、Amazon Redshift Serverless とゼロ ETL 統合、Amazon Athena の Iceberg 対応、Amazon EMR Serverless、Amazon MSK Serverless、AWS Lake Formation のタグベースのアクセス制御、Amazon SageMaker Unified Studio(Amazon DataZone を含む)

## 問題の形

- 本番に近いシナリオ問題。「ある企業は〜」「データエンジニアは〜」から始め、要件(最小の運用負荷、最もコスト効率が良い、最小のレイテンシーなど)を最後の一文で問う。
- 単一選択(4択)を7割、複数選択(5択から2つ)を3割。複数選択は問題文の最後に「（2 つ選択）」と書く。DEA-C01 の出題形式はこの2つだけ。
- 不正解の選択肢も「ありそう」に作る。明らかに的外れな選択肢は入れない。存在しない機能を不正解として使うのは可だが、それが存在しないことを裏取りする。
- 正解の位置を偏らせない。単一選択なら A/B/C/D がほぼ均等になるよう散らす。
- 試験ガイドの「範囲外のジョブタスク」(ML のトレーニングと推論、言語固有の構文、データからのビジネス上の結論)を問わない。SQL は問うてよい。
- 市販の問題集や本番の問題を写さない。オリジナルで作る。

## 解説の書き方

- explanation は 200〜450 字程度。なぜその答えになるか、決め手になった要件の語句と、正解の仕組みを書く。
- optionNotes は選択肢ごとに 1〜2 文。正解はなぜ要件を満たすか、不正解はどこが要件に合わないか。
- 日本語のスタイル: 太字を使わない。ダッシュ(— ― 「 - 」での区切り)を使わない。「〜することができます」ではなく「〜できます」。「活用」と書かず「使う」。です・ます調で統一する。
- サービス名は公式の英語名(AWS Glue、Amazon Redshift など)。API 名、設定名、SQL はそのまま書く。
- refs に裏取りに使った AWS 公式ページの URL を1〜3件付ける。実在を確かめた URL だけを書く。

## 出力の形式

JSON 配列 1 ファイル。各要素は次の形。

```json
{
  "id": "D1-001",
  "domain": 1,
  "task": "1.1",
  "type": "single",
  "question": "ある企業は……。これらの要件を満たすソリューションはどれですか。",
  "options": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
  "answer": [2],
  "explanation": "……",
  "optionNotes": ["Aの解説", "Bの解説", "Cの解説", "Dの解説"],
  "services": ["AWS Glue", "Amazon S3"],
  "difficulty": 2,
  "refs": [{ "title": "ページのタイトル", "url": "https://docs.aws.amazon.com/..." }]
}
```

- `type` は `single` か `multi`。`single` のとき options は 4 個、answer は 1 個。`multi` のとき options は 5 個、answer は 2 個。
- `answer` は 0 始まりの添字の配列。
- `domain` は数値(`1`)、`task` は文字列(`"1.1"`)で書き、[`exam.json`](exam.json) の分野と細目に合わせる。
- `difficulty` は 1(基本)〜3(難しい)。2 を中心に。
- `task` は分野ページのタスク番号。そのタスクのスキル項目をまんべんなく拾う。
- 書き終えたら `python3 -c "import json;d=json.load(open('<path>'));print(len(d))"` で読めることと件数を確かめる。

## 完了報告

次の形式で返す。

- ステータス: 完了 / 一部未完了
- 出力ファイル: パスと件数
- タスク別の件数、単一/複数の件数、正解位置の分布
- 検証: 公式ドキュメントで確かめた主な事実と、確かめきれなかったもの
- 懸念と未完了

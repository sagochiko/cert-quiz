# MLA-C01 問題作成の共通ルール

AWS Certified Machine Learning Engineer - Associate (MLA-C01) の日本語の模擬問題を作る。問題集は Web ページ(Claude Artifact)で出題する。

## 一次情報

- 試験ガイド(日本語版 PDF): https://d1.awsstatic.com/ja_JP/training-and-certification/docs-machine-learning-engineer-associate/AWS-Certified-Machine-Learning-Engineer-Associate_Exam-Guide.pdf
  - 英語版は URL の `ja_JP/` を除いたもの。docs.aws.amazon.com からは C01 のページが消えていて、C02 のページしか無い
  - 各タスクのスキル項目、範囲内と範囲外のサービスの一覧(付録)は PDF にある。`curl` で落として `pdftotext -layout` で読む
- 新版 MLA-C02 との差分: https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/mla-02-comparison.html
- 保守モードのサービス一覧: https://docs.aws.amazon.com/general/latest/gr/maintenance_services.html

AWS の公式ドキュメントで裏を取る。`mcp__plugin_aws-core_aws-mcp__aws___search_documentation`(ToolSearch で `select:` して読み込む)を使う。検索結果の context はページ本文そのもの。足りないときだけ `aws___read_documentation` で全文を読む。記憶だけで書かない。特に、SageMaker AI の組み込みアルゴリズムの入力形式とハイパーパラメータ、エンドポイントの種類(リアルタイム、サーバーレス、非同期、バッチ変換)の上限と使い分け、インスタンスファミリー、評価指標の定義は必ず確かめる。

古い知識で書くと間違えやすい点。

- 出題範囲は C01。C02 で足された RAG、Bedrock のナレッジベース、ベクトルデータベース、エージェント、プロンプト管理は問わない。Amazon Bedrock 自体は C01 でも範囲内で、基盤モデルの選択やファインチューニングは問うてよい
- Amazon SageMaker は Amazon SageMaker AI に名前が変わった(機械学習の部分)。Amazon SageMaker という名前は SageMaker Unified Studio を含む新しいサービスの名前になっている。問題文では「Amazon SageMaker AI」と書き、機能名は SageMaker Pipelines、SageMaker Model Registry のように書く
- 2026年6月30日から、SageMaker AI の Clarify、Model Monitor、Ground Truth、Debugger、Augmented AI (A2I) が保守モードに入り、新規の利用ができない。C01 の試験ガイドにはこれらが残っていて、本番でも出る見込みが高いので、正解にしてよい。ただし解説の最後に1文で保守モードに入ったことを書く
- Amazon Mechanical Turk は2026年9月29日に提供を終えた。Ground Truth の作業者はプライベートとベンダー(AWS Marketplace)の2種類だけなので、Mechanical Turk の作業者を選択肢に出さない
- Amazon Forecast は2024年7月29日から新規受付を終えている(移行先は SageMaker Canvas)。Amazon Lookout for Vision、Lookout for Equipment は提供を終えた。これらを正解にしない
- SageMaker Studio Classic ではなく、今の SageMaker Studio(JupyterLab、Code Editor)で書く。SageMaker Data Wrangler は SageMaker Canvas の中の機能になっている

## 問題の形

- 本番に近いシナリオ問題。「ある企業は〜」「ML エンジニアは〜」から始め、要件(最小の運用負荷、最もコスト効率が良い、最小のレイテンシーなど)を最後の一文で問う。
- 出題形式の割合は、単一選択(4択)6割、複数選択(5択から2つ)2割、並べ替え1割、内容一致1割。ケーススタディは各分野に1組(1つのシナリオに2〜3問)入れる。
- 並べ替えは、手順の順番が仕組みで決まるもの(SageMaker Pipelines のステップ、モデルのデプロイ手順、データ準備の流れなど)に使う。人によって順番が変わりうる手順には使わない。
- 内容一致は、要件とサービスや機能、問題とアルゴリズム、症状と対処のように、1対1かほぼ1対1で決まる組み合わせに使う。
- 不正解の選択肢も「ありそう」に作る。明らかに的外れな選択肢は入れない。存在しない機能を不正解として使うのは可だが、それが存在しないことを裏取りする。
- 正解の位置を偏らせない。単一選択なら A/B/C/D がほぼ均等になるよう散らす。
- 試験ガイドの「範囲外のジョブタスク」を問わない。
- 市販の問題集や本番の問題を写さない。オリジナルで作る。

## 解説の書き方

- explanation は 200〜450 字程度。なぜその答えになるか、決め手になった要件の語句と、正解の仕組みを書く。並べ替えは、なぜその順番になるか(前の手順の出力が次の手順の入力になる、など)を書く。
- optionNotes は選択肢ごとに 1〜2 文。正解はなぜ要件を満たすか、不正解はどこが要件に合わないか。
- 日本語のスタイル: 太字を使わない。ダッシュ(— ― 「 - 」での区切り)を使わない。「〜することができます」ではなく「〜できます」。「活用」と書かず「使う」。です・ます調で統一する。
- サービス名は公式の英語名(Amazon SageMaker AI、AWS Glue など)。API 名、ハイパーパラメータ名、評価指標名はそのまま書く。
- refs に裏取りに使った AWS 公式ページの URL を1〜3件付ける。実在を確かめた URL だけを書く。

## 出力の形式

JSON 配列 1 ファイル。単一選択と複数選択は次の形。

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
  "services": ["Amazon SageMaker AI"],
  "difficulty": 2,
  "refs": [{ "title": "ページのタイトル", "url": "https://docs.aws.amazon.com/..." }]
}
```

- `type` は `single` か `multi`。`single` のとき options は 4 個、answer は 1 個。`multi` のとき options は 5 個、answer は 2 個。
- 並べ替え(`order`)、内容一致(`match`)、ケーススタディの書き方は、リポジトリ直下の [`template/exam/BRIEF.md`](../../template/exam/BRIEF.md)、[`template/exam/questions/sample.json`](../../template/exam/questions/sample.json)、[`template/exam/cases.json`](../../template/exam/cases.json) の見本に従う。
  - `order`: options は3〜6個、answer は正しい順に並べた添字で3〜5個。問題文に「次の候補から N つを選び、正しい順序に並べてください。」と書く。
  - `match`: prompts は3〜7個、options は2〜7個、answer[i] はプロンプト i に合う options の添字(数は prompts と同じ)。
  - ケーススタディ: 設問に `"case": "<ID>"` を付け、シナリオは `exams/aws-mla-c01/cases.json` に書く。1つの ID に2〜3問付ける。
- `answer` は 0 始まりの添字の配列。
- `domain` は数値(`1`)、`task` は文字列(`"1.1"`)で書き、[`exam.json`](exam.json) の分野と細目に合わせる。
- `difficulty` は 1(基本)〜3(難しい)。2 を中心に。
- `task` は試験ガイドのタスク番号。そのタスクのスキル項目をまんべんなく拾う。
- 書き終えたら `python3 -c "import json;d=json.load(open('<path>'));print(len(d))"` で読めることと件数を確かめる。

## 完了報告

次の形式で返す。

- ステータス: 完了 / 一部未完了
- 出力ファイル: パスと件数
- タスク別の件数、形式別の件数、単一選択の正解位置の分布
- 検証: 公式ドキュメントで確かめた主な事実と、確かめきれなかったもの
- 懸念と未完了

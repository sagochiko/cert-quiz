# SCS-C03 問題作成の共通ルール

AWS Certified Security - Specialty (SCS-C03) の日本語の模擬問題を作る。問題集は Web ページ(Claude Artifact)で出題する。

## 一次情報

- 試験ガイド: https://docs.aws.amazon.com/aws-certification/latest/security-specialty-03/security-specialty-03.html
- 分野ごとのページ: 上の URL の末尾を `security-specialty-03-domain1.html` から `domain6.html` に変える
- 範囲内サービス: `security-specialty-03-in-scope-services.html`、範囲外: `security-specialty-03-out-of-scope-services.html`

AWS の公式ドキュメントで裏を取る。`mcp__plugin_aws-agents_awsknowledge__aws___search_documentation`(ToolSearch で `select:` して読み込む)を使う。検索結果の context はページ本文そのもの。足りないときだけ `aws___read_documentation` で全文を読む。記憶だけで書かない。特に、上限値、デフォルト挙動、どのサービスがどの機能を持つか、リージョン/グローバルの別、キーポリシーと IAM の評価、SCP/RCP の効き方は必ず確かめる。2026年時点の最新の仕様に合わせる(例: Security Hub は CSPM と新 Security Hub の区別、RCP、IAM Identity Center、GuardDuty の拡張脅威検出や Malware Protection for S3、Security Lake、Verified Access、Network Firewall、Inspector のコードスキャン、KMS の外部キーストアなど)。

## 問題の形

- 本番に近いシナリオ問題。「ある企業は〜」「セキュリティエンジニアは〜」から始め、要件(最小の運用負荷、最もコスト効率が良い、最小権限など)を最後の一文で問う。
- 単一選択(4択)を7割、複数選択(5択から2つ)を3割。複数選択は問題文の最後に「（2 つ選択）」と書く。
- 不正解の選択肢も「ありそう」に作る。明らかに的外れな選択肢は入れない。存在しない機能を不正解として使うのは可だが、それが存在しないことを裏取りする。
- 正解の位置を偏らせない。単一選択なら A/B/C/D がほぼ均等になるよう散らす。
- 既存の問題集(CloudTech、Udemy など)の問題を写さない。オリジナルで作る。

## 解説の書き方

- explanation は 200〜450 字程度。なぜその答えになるか、決め手になった要件の語句と、正解の仕組みを書く。
- optionNotes は選択肢ごとに 1〜2 文。正解はなぜ要件を満たすか、不正解はどこが要件に合わないか。
- 日本語のスタイル: 太字を使わない。ダッシュ(— ― 「 - 」での区切り)を使わない。「〜することができます」ではなく「〜できます」。「活用」と書かず「使う」。だ・である調ではなく、です・ます調で統一する。
- サービス名は公式の英語名(Amazon GuardDuty、AWS KMS など)。API 名やポリシーの条件キーはそのまま書く。
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
  "services": ["Amazon GuardDuty", "AWS Security Hub"],
  "difficulty": 2,
  "refs": [{ "title": "ページのタイトル", "url": "https://docs.aws.amazon.com/..." }]
}
```

- `type` は `single` か `multi`。`multi` のとき options は 5 個、answer は 2 個。
- `answer` は 0 始まりの添字の配列。
- `difficulty` は 1(基本)〜3(難しい)。2 を中心に。
- `task` は分野ページのタスク番号(1.1 など)。そのタスクのスキル項目をまんべんなく拾う。
- 書き終えたら `python3 -c "import json;d=json.load(open('<path>'));print(len(d))"` で読めることと件数を確かめる。

## 完了報告

次の形式で返す。

- ステータス: 完了 / 一部未完了
- 出力ファイル: パスと件数
- タスク別の件数、単一/複数の件数、正解位置の分布
- 検証: 公式ドキュメントで確かめた主な事実と、確かめきれなかったもの
- 懸念と未完了

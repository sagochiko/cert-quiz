# DEA-C01 問題のレビュー手順

問題の形式と文体のルールは同じフォルダの [`BRIEF.md`](BRIEF.md) にある。先に読む。問題は questions/ の下にある。

## 見ること

1. 正解が本当に正しいか。決め手の事実を AWS 公式ドキュメントで確かめる(`mcp__plugin_aws-core_aws-mcp__aws___search_documentation` を ToolSearch の `select:` で読み込む。使えなければ `mcp__plugin_aws-agents_awsknowledge__aws___search_documentation`)。
2. 不正解の選択肢が本当に不正解か。問題文の要件の読み方によっては正解にもなる選択肢(正解が2つ立つ)を探す。これが一番多い不具合。データ分野では「Glue でも EMR でもできる」「Athena でも Redshift Spectrum でもできる」のように、要件の語句(サーバーレス、最小の運用負荷、既存の Spark コード、ミリ秒のレイテンシーなど)で1つに絞れているかを見る。
3. 2026年11月時点の仕様か。新規受付を終えたサービス(AWS Data Pipeline)や保守モードのサービス(S3 Select、S3 Object Lambda、Timestream for LiveAnalytics、Glue の Ray ジョブなど。[一覧](https://docs.aws.amazon.com/general/latest/gr/maintenance_services.html))を新しい構成の正解にしていないか。名称変更(Data Firehose、Managed Service for Apache Flink、Quick Sight)の扱いが BRIEF.md のとおりか。
4. 解説と optionNotes が正解と矛盾していないか。answer の添字が解説の内容と合っているか。
5. refs の URL が問題の内容と対応しているか(全部は開かなくてよい。怪しいものだけ確かめる)。
6. 文体: 太字、ダッシュ(— ― や「 - 」での区切り。公式のページタイトルに含まれるものは可)、「することができ」「活用」、だ・である調が混じっていないか。

## 直し方

- 見つけた不具合はそのファイルを直接直す。正解を変える、選択肢を書き換えて正解が1つに決まるようにする、解説を直す、など。直すときも裏を取る。
- 直せない(問題の前提ごと成り立たない)ものは、同じタスクで別の問題に差し替える。ID は変えない。
- 直したら `python3 build.py aws-dea-c01` をリポジトリの直下で実行し、NG が出ないことを確かめる(dist/ が書き換わるのは構わない)。
- 担当外のファイルは触らない。git のコミットはしない。

## 完了報告

- ステータス
- 直した問題: ID ごとに、何が問題で、どう直したか、根拠の URL
- 問題なしと判断したが際どいもの
- 確かめきれなかったもの

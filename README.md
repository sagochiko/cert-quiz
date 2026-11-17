# cert-quiz

資格試験の模擬問題集。試験ごとに問題を JSON で持ち、共通のページの雛形に埋め込んで Claude Artifact として公開する。回答履歴、ブックマーク、間違えた問題、途中のセットは Artifact の DB に本人だけが読める形で保存され、どの端末で開いても続きから解ける。解説の横のチャットで Claude に質問でき、類題も作らせられる。

## 公開中の問題集

| 試験 | 問題数 | ページ |
|---|---|---|
| AWS Certified Security - Specialty (SCS-C03) | 120 | [SCS-C03 問題集](https://claude.ai/artifact/SHwkuB3FB3Pmc3jMwdZ2W1) |

Artifact は非公開で、持ち主だけが開ける。Claude のチャットと類題の作成は、開いた人の claude.ai の使用量を使う。

## 構成

```text
build.py                 試験IDを受け取り、検証して dist/<試験ID>/index.html を作る
template/index.html      全試験で共通のページ(出題、履歴の同期、チャット、効果音)
exams/<試験ID>/
  exam.json              試験名、分野と配点、模擬試験の問題数、Claude への指示、公開先
  questions/*.json       問題。ファイルの分け方は自由(SCS は分野ごと)
  BRIEF.md               問題を作るときのルール
  REVIEW.md              問題を見直すときの手順
```

## ビルドと公開

```sh
python3 build.py aws-scs-c03
```

件数、分野ごとの内訳、単一選択の正解位置の分布が出る。形式の誤り(選択肢の数、正解の添字、exam.json にないタスク番号、ID の重複)があると NG を出して止まる。

できた `dist/aws-scs-c03/index.html` を Claude Code の Artifact ツールで公開する。既存の問題集を更新するときは、`exam.json` の `artifact` の URL を指定して公開し直す。URL を指定しないと別の Artifact ができる。宣言する機能(capabilities)は `{"db": {}, "user": {}, "sample": {}, "dictation": {}}`。`dist/` はビルドのたびに作り直せるので、公開したら消してよい。

## 試験を足す

1. `exams/<試験ID>/exam.json` を作る。`aws-scs-c03/exam.json` を写して、試験名、分野(`domains` の番号、名前、配点、タスク番号と名前)、`examSize`、`tutorNote`、`genNote`、`searchChip` を書き換える。分野の番号とタスク番号の先頭の数字は揃える(`"2"` の分野のタスクは `2.1`、`2.2`)。
2. `BRIEF.md` を試験に合わせて書き、問題を `questions/` に置く。問題の形は BRIEF.md の「出力の形式」のとおり。
3. `python3 build.py <試験ID>` で NG が出ないことを確かめてから公開し、`exam.json` の `artifact` と上の表に URL を書く。

IPA の試験のように分野とタスクの2階層がないものは、分野を大分類、タスクを中分類として当てはめる。

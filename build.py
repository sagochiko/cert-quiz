"""試験ひとつ分の問題を検証して、共通の雛形に埋め込んだページを作る。

使い方: python3 build.py aws-scs-c03
出力:   dist/aws-scs-c03/index.html
"""
import html
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent


TYPES = ("single", "multi", "order", "match")


def check(q, tasks, cases):
    errs = []
    t = q.get("type")
    n = len(q.get("options", []))
    ans = q.get("answer", [])
    if not isinstance(ans, list):
        return ["answer は添字の配列で書く(例: [2])"]
    if t not in TYPES:
        errs.append('type は "single" "multi" "order" "match" のどれか')
    if t == "single" and (n != 4 or len(ans) != 1):
        errs.append("single は4択で正解1つ")
    if t == "multi" and (n != 5 or len(ans) < 2):
        errs.append("multi は5択で正解2つ以上")
    if t == "order":
        if not 3 <= n <= 6:
            errs.append("order の options(並べる候補)は3〜6個")
        if not 3 <= len(ans) <= 5 or len(ans) > n:
            errs.append("order の answer は正しい順に並べた候補の添字で、3〜5個かつ options の数以下")
    if t == "match":
        prompts = q.get("prompts")
        if not isinstance(prompts, list) or not 3 <= len(prompts) <= 7 or not all(isinstance(x, str) and x for x in prompts):
            errs.append("match の prompts は3〜7個の文字列の配列")
        elif len(ans) != len(prompts):
            errs.append("match の answer はプロンプトごとに合う options の添字を1つずつ。prompts と同じ数にする")
        if not 2 <= n <= 7:
            errs.append("match の options(答えの候補)は2〜7個")
    elif "prompts" in q:
        errs.append("prompts は match の問題だけに書く")
    if t in ("single", "multi", "order") and len(set(map(str, ans))) != len(ans):
        errs.append("answer に同じ添字が2回入っている")
    if any(not isinstance(i, int) or isinstance(i, bool) or i < 0 or i >= n for i in ans):
        errs.append("answer の添字が範囲外")
    if len(q.get("optionNotes", [])) != n:
        errs.append("optionNotes の数が選択肢と合わない")
    if "case" in q and (not isinstance(q["case"], str) or q["case"] not in cases):
        errs.append(f"case の {q['case']!r} が cases.json に無い")
    if not isinstance(q.get("domain"), int) or isinstance(q.get("domain"), bool):
        errs.append('domain は数値で書く(例: 1)。"1" のような文字列だとページで絞り込めない')
    elif tasks.get(q.get("task")) != str(q.get("domain")):
        errs.append("domain/task が exam.json の分野と合わない")
    for k in ("id", "question", "explanation"):
        if not q.get(k):
            errs.append(f"{k} が空")
    return errs


def main():
    if len(sys.argv) != 2:
        sys.exit("使い方: python3 build.py <試験ID>  (exams/ の下のフォルダ名)")
    exam_dir = ROOT / "exams" / sys.argv[1]
    exam = json.loads((exam_dir / "exam.json").read_text())
    if exam.get("id") != exam_dir.name:
        sys.exit(f"NG exam.json の id ({exam.get('id')}) をフォルダ名 ({exam_dir.name}) と揃える。出力先 dist/<id>/ が他の試験と重なるのを防ぐため")
    tasks = {t: d for d, dom in exam["domains"].items() for t in dom["tasks"]}

    # ケーススタディのシナリオ: exams/<id>/cases.json に {"<ID>": {"title", "scenario"}}。問題は case でこの ID を指す
    bad = 0
    cases_file = exam_dir / "cases.json"
    cases = json.loads(cases_file.read_text()) if cases_file.exists() else {}
    if not isinstance(cases, dict):
        sys.exit('NG cases.json は {"<ID>": {"title": ..., "scenario": ...}} の形のオブジェクトで書く')
    for cid, c in cases.items():
        if not isinstance(c, dict) or not c.get("title") or not c.get("scenario"):
            bad += 1
            print(f"NG cases.json {cid}: title と scenario を書く")

    bank = []
    for f in sorted((exam_dir / "questions").glob("*.json")):
        for q in json.loads(f.read_text()):
            e = check(q, tasks, cases)
            if e:
                bad += 1
                print(f"NG {f.name} {q.get('id')}: {', '.join(e)}")
            bank.append(q)
    per_case = Counter(q["case"] for q in bank if isinstance(q.get("case"), str) and q["case"] in cases)
    for cid in cases:
        if per_case[cid] == 1:
            bad += 1
            print(f"NG ケーススタディ {cid} の問題が1問だけ。1つのシナリオに2問以上付ける")
        elif per_case[cid] > 4:
            print(f"注意 ケーススタディ {cid} の問題が{per_case[cid]}問。本番に合わせ、1つのシナリオは2〜4問にする")
        elif not per_case[cid]:
            print(f"注意 cases.json の {cid} を使う問題が無いので載せない。見本なら消す")
    dup = [k for k, v in Counter(q["id"] for q in bank).items() if v > 1]
    if dup:
        print("NG ID の重複:", dup)
        bad += 1
    if not bank:
        print("NG 問題が1問も無い。questions/*.json に問題を置く")
    if bad or not bank:
        sys.exit(1)
    print("件数:", len(bank), dict(sorted(Counter(q["domain"] for q in bank).items())))
    print("形式:", {t: c for t in TYPES if (c := sum(1 for q in bank if q["type"] == t))})
    if per_case:
        print("ケーススタディ:", dict(sorted(per_case.items())))
    print("正解位置(single):", dict(sorted(Counter(q["answer"][0] for q in bank if q["type"] == "single").items())))
    # 警告だけでビルドは止めない。模擬試験は配点の比率で分野ごとに出すので、配点と在庫を見ておく
    weights = {d: dom["weight"] for d, dom in exam["domains"].items()}
    if sum(weights.values()) != 100:
        print(f"注意 配点の合計が {sum(weights.values())}。模擬試験は比率で配分するので動くが、公式の配点と合っているか確かめる")
    for d, w in weights.items():
        need = round(exam["examSize"] * w / sum(weights.values()))
        have = sum(1 for q in bank if str(q["domain"]) == d)
        if have < need:
            print(f"注意 分野{d} は {have}問。模擬試験で {need}問ほど出すので、その分だけ模擬試験が短くなる")

    # 図: diagrams/<問題ID>.svg があれば解説に載せる。alt は定義の1行目のコメント
    diagrams = {}
    ids = {q["id"] for q in bank}
    for svg in sorted((exam_dir / "diagrams").glob("*.svg")):
        qid = svg.stem
        if qid not in ids:
            print(f"注意 diagrams/{svg.name} に対応する問題が無いので載せない")
            continue
        # 定義の先頭のコメント: 1行目が図の説明、「補った部品:」の行は問題文に無い部品
        alt, note = "構成図", ""
        src = svg.with_suffix(".yaml")
        if src.exists():
            for i, line in enumerate(src.read_text().splitlines()):
                if not line.startswith("#"):
                    break
                text = line.lstrip("# ").strip()
                if text.startswith("補った部品"):
                    note = text.replace(":", "", 1).strip()
                elif i == 0:
                    alt = text.split(":", 1)[-1].strip() or alt
        diagrams[qid] = (svg, alt, note)
    for q in bank:
        if q["id"] in diagrams:
            _, alt, note = diagrams[q["id"]]
            q["diagram"] = {"src": f"diagrams/{q['id']}.svg", "alt": alt + (f"。{note}" if note else "")}
            if note:
                q["diagram"]["note"] = note
    print("図:", len(diagrams), sorted(diagrams))

    def embed(obj):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    exam = {**exam, "cases": {cid: cases[cid] for cid in sorted(per_case)}}
    page = (ROOT / "template" / "index.html").read_text()
    for key in ("title", "brand", "tag"):
        page = page.replace(f"__{key.upper()}__", html.escape(exam[key]))
    page = page.replace("__EXAM__", embed(exam)).replace("__QUESTIONS__", embed(bank))
    out = ROOT / "dist" / exam["id"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    if diagrams:
        (out.parent / "diagrams").mkdir(exist_ok=True)
        for qid, (svg, _, _) in diagrams.items():
            # draw.io の SVG は DOCTYPE 宣言で始まる。Artifact は DTD を含む XML を受け付けない
            text = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg.read_text(), count=1)
            # 白い台紙に載せるので、端末がダークモードでも図はライトの配色で描かせる
            text = text.replace("color-scheme: light dark;", "color-scheme: light;")
            (out.parent / "diagrams" / svg.name).write_text(text)
    print("書き出し:", out, f"{len(page.encode()) // 1024}KB")


if __name__ == "__main__":
    main()

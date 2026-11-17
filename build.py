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


def check(q, tasks):
    errs = []
    n = len(q.get("options", []))
    if q.get("type") == "single" and (n != 4 or len(q.get("answer", [])) != 1):
        errs.append("single は4択で正解1つ")
    if q.get("type") == "multi" and (n != 5 or len(q.get("answer", [])) < 2):
        errs.append("multi は5択で正解2つ以上")
    if q.get("type") not in ("single", "multi"):
        errs.append("type が不正")
    if any(not isinstance(i, int) or i < 0 or i >= n for i in q.get("answer", [])):
        errs.append("answer の添字が範囲外")
    if len(q.get("optionNotes", [])) != n:
        errs.append("optionNotes の数が選択肢と合わない")
    if tasks.get(q.get("task")) != str(q.get("domain")):
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
    tasks = {t: d for d, dom in exam["domains"].items() for t in dom["tasks"]}

    bank, bad = [], 0
    for f in sorted((exam_dir / "questions").glob("*.json")):
        for q in json.loads(f.read_text()):
            e = check(q, tasks)
            if e:
                bad += 1
                print(f"NG {f.name} {q.get('id')}: {', '.join(e)}")
            bank.append(q)
    dup = [k for k, v in Counter(q["id"] for q in bank).items() if v > 1]
    if dup:
        print("ID の重複:", dup)
        bad += 1
    print("件数:", len(bank), dict(sorted(Counter(q["domain"] for q in bank).items())))
    print("正解位置(single):", dict(sorted(Counter(q["answer"][0] for q in bank if q["type"] == "single").items())))
    if bad or not bank:
        sys.exit(1)

    # 図: diagrams/<問題ID>.svg があれば解説に載せる。alt は定義の1行目のコメント
    diagrams = {}
    for svg in sorted((exam_dir / "diagrams").glob("*.svg")):
        qid = svg.stem
        alt = "構成図"
        src = svg.with_suffix(".yaml")
        if src.exists():
            first = src.read_text().splitlines()[0]
            if first.startswith("#"):
                alt = first.lstrip("# ").split(":", 1)[-1].strip() or alt
        diagrams[qid] = (svg, alt)
    for q in bank:
        if q["id"] in diagrams:
            q["diagram"] = {"src": f"diagrams/{q['id']}.svg", "alt": diagrams[q["id"]][1]}
    print("図:", len(diagrams), sorted(diagrams))

    def embed(obj):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    page = (ROOT / "template" / "index.html").read_text()
    for key in ("title", "brand", "tag"):
        page = page.replace(f"__{key.upper()}__", html.escape(exam[key]))
    page = page.replace("__EXAM__", embed(exam)).replace("__QUESTIONS__", embed(bank))
    out = ROOT / "dist" / exam["id"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    if diagrams:
        (out.parent / "diagrams").mkdir(exist_ok=True)
        for qid, (svg, _) in diagrams.items():
            # draw.io の SVG は DOCTYPE 宣言で始まる。Artifact は DTD を含む XML を受け付けない
            text = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg.read_text(), count=1)
            # 白い台紙に載せるので、端末がダークモードでも図はライトの配色で描かせる
            text = text.replace("color-scheme: light dark;", "color-scheme: light;")
            (out.parent / "diagrams" / svg.name).write_text(text)
    print("書き出し:", out, f"{len(page.encode()) // 1024}KB")


if __name__ == "__main__":
    main()

"""questions/d1.json〜d6.json を検証して src/index.html に埋め込み、dist/index.html を作る。"""
import json
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent
TASKS = {"1.1", "1.2", "1.3", "2.1", "2.2", "3.1", "3.2", "3.3", "4.1", "4.2", "5.1", "5.2", "5.3", "6.1", "6.2", "6.3"}


def check(q):
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
    if q.get("task") not in TASKS or str(q.get("domain")) != str(q.get("task", "0"))[0]:
        errs.append("domain/task が不正")
    for k in ("id", "question", "explanation"):
        if not q.get(k):
            errs.append(f"{k} が空")
    return errs


def main():
    bank, bad = [], 0
    for f in sorted((ROOT / "questions").glob("d[1-6].json")):
        data = json.loads(f.read_text())
        for q in data:
            e = check(q)
            if e:
                bad += 1
                print(f"NG {f.name} {q.get('id')}: {', '.join(e)}")
            bank.append(q)
    ids = [q["id"] for q in bank]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    if dup:
        print("ID の重複:", dup)
        bad += 1
    print("件数:", len(bank), dict(sorted(Counter(q["domain"] for q in bank).items())))
    print("正解位置(single):", dict(sorted(Counter(q["answer"][0] for q in bank if q["type"] == "single").items())))
    if bad:
        sys.exit(1)
    payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (ROOT / "src" / "index.html").read_text().replace("__QUESTIONS__", payload)
    out = ROOT / "dist" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html)
    print("書き出し:", out, f"{len(html.encode()) // 1024}KB")


if __name__ == "__main__":
    main()

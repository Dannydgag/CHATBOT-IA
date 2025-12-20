# scripts/m13_eval_diagnostics.py
import argparse, json
from pathlib import Path
from tqdm import tqdm
from m11_search_hybrid import search

def load_validation(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def keyword_match(snippet, keywords):
    text = snippet.lower()
    return [k for k in keywords if k.lower() in text]

def analyze(qs, alpha, topk, page_window, out_path):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fout:
        for q in tqdm(qs):
            res = search(q["query"], topk=topk, alpha=alpha)
            entries = []
            for rank, r in enumerate(res, start=1):
                kw_found = keyword_match(r["snippet"], q.get("expected_keywords", []))
                page_ok = any(abs(r["page"] - p) <= page_window for p in q.get("expected_pages", []))
                entries.append({
                    "rank": rank,
                    "id": r.get("id"),
                    "page": r.get("page"),
                    "score": r.get("score"),
                    "kw_found": kw_found,
                    "page_ok": page_ok,
                    "snippet": r.get("snippet")[:1000]
                })
            out_obj = {"id": q.get("id"), "query": q.get("query"), "expected_pages": q.get("expected_pages"),
                       "expected_keywords": q.get("expected_keywords"), "results": entries}
            fout.write(json.dumps(out_obj, ensure_ascii=False) + "\n")
    print("Diagnóstico guardado en", out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--val", required=True)
    ap.add_argument("--alpha", type=float, default=0.6)
    ap.add_argument("--topk", type=int, default=8)
    ap.add_argument("--page_window", type=int, default=1)
    ap.add_argument("--out", default="results/diagnostics.jsonl")
    args = ap.parse_args()
    qs = load_validation(Path(args.val))
    analyze(qs, args.alpha, args.topk, args.page_window, args.out)

if __name__ == "__main__":
    main()

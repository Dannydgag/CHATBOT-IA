# scripts/m13_eval_search_grid.py
import argparse, json, csv
from pathlib import Path
from tqdm import tqdm
from m11_search_hybrid import search

def load_validation(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def keyword_match(snippet, keywords):
    text = snippet.lower()
    return sum(1 for k in keywords if k.lower() in text)

def eval_once(queries, alpha, topk, page_window):
    hits1 = hits3 = 0
    rr_sum = 0.0
    for q in queries:
        expected_pages = set(q.get("expected_pages", []))
        expected_keywords = q.get("expected_keywords", [])
        results = search(q["query"], topk=topk, alpha=alpha)
        # build simplified retrieved info
        retrieved = []
        for r in results:
            retrieved.append({
                "page": r["page"],
                "snippet": r["snippet"],
                "kw_hits": keyword_match(r["snippet"], expected_keywords)
            })
        # P@1
        if retrieved:
            r0 = retrieved[0]
            if any(abs(r0["page"] - p) <= page_window for p in expected_pages) and r0["kw_hits"]>0:
                hits1 += 1
                rr_sum += 1.0
            else:
                found = False
                for rank, rr in enumerate(retrieved, start=1):
                    if any(abs(rr["page"] - p) <= page_window for p in expected_pages) and rr["kw_hits"]>0:
                        rr_sum += 1.0 / rank
                        found = True
                        break
                if not found:
                    rr_sum += 0.0
        # P@3
        if any(
            any(abs(r["page"] - p) <= page_window for p in expected_pages) and r["kw_hits"]>0
            for r in retrieved[:3]
        ):
            hits3 += 1
    n = len(queries)
    return {"alpha": alpha, "page_window": page_window, "P@1": hits1 / n, "P@3": hits3 / n, "MRR": rr_sum / n}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--val", required=True)
    ap.add_argument("--alphas", nargs="+", type=float, required=True)
    ap.add_argument("--page_windows", nargs="+", type=int, default=[0])
    ap.add_argument("--topk", type=int, default=8)
    ap.add_argument("--out_csv", default="results/grid_results.csv")
    args = ap.parse_args()

    qs = load_validation(Path(args.val))
    outp = Path(args.out_csv)
    outp.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for alpha in args.alphas:
        for pw in args.page_windows:
            print(f"Evaluando alpha={alpha} page_window={pw}")
            metrics = eval_once(qs, alpha, args.topk, pw)
            print(metrics)
            rows.append(metrics)

    # save CSV
    with open(outp, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["alpha","page_window","P@1","P@3","MRR"])
        writer.writeheader()
        writer.writerows(rows)
    # also save json
    with open(outp.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

if __name__ == "__main__":
    main()

import argparse
import csv
import io
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results/eval_details.jsonl")
    ap.add_argument("--out", default="results/eval_details.csv")
    ap.add_argument("--max_text", type=int, default=220, help="máximo de caracteres del snippet en CSV")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with io.open(in_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    fieldnames = [
        "id",
        "category",
        "label",
        "rank_first_relevant",
        "precision1",
        "mrr_contrib",
        "top1_page",
        "top1_score",
        "top1_text",
    ]

    with io.open(out_path, "w", encoding="utf-8", newline="") as fw:
        writer = csv.DictWriter(fw, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            topk = r.get("topk", []) or []
            top1 = topk[0] if topk else {}
            ttxt = str(top1.get("text", "")).replace("\n", " ").strip()
            if args.max_text and len(ttxt) > args.max_text:
                ttxt = ttxt[: args.max_text - 1] + "…"
            writer.writerow({
                "id": r.get("id"),
                "category": r.get("category"),
                "label": r.get("label"),
                "rank_first_relevant": r.get("rank_first_relevant", 0),
                "precision1": r.get("precision1", 0.0),
                "mrr_contrib": r.get("mrr_contrib", 0.0),
                "top1_page": top1.get("page"),
                "top1_score": top1.get("distance"),
                "top1_text": ttxt,
            })

    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

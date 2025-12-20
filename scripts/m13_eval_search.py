import argparse
import json
from pathlib import Path
from tqdm import tqdm

from m11_search_hybrid import search


def load_validation(path):
    qs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            qs.append(json.loads(line))
    return qs


def keyword_match(snippet, keywords):
    text = snippet.lower()
    return sum(1 for k in keywords if k.lower() in text)


def compute_metrics(queries, topk=8, alpha=0.6):
    hits_1 = 0
    hits_3 = 0
    rr = 0

    for q in tqdm(queries):
        query = q["query"]
        expected_pages = set(q["expected_pages"])
        expected_keywords = q["expected_keywords"]

        results = search(query, topk=topk, alpha=alpha)

        retrieved = []
        for r in results:
            retrieved.append({
                "page": r["page"],
                "kw_hits": keyword_match(r["snippet"], expected_keywords)
            })

        # Precision@1
        if retrieved:
            if (
                retrieved[0]["page"] in expected_pages
                and retrieved[0]["kw_hits"] > 0
            ):
                hits_1 += 1
                rr += 1
            else:
                for rank, r in enumerate(retrieved, start=1):
                    if (
                        r["page"] in expected_pages
                        and r["kw_hits"] > 0
                    ):
                        rr += 1 / rank
                        break

        # Precision@3
        if any(
            r["page"] in expected_pages and r["kw_hits"] > 0
            for r in retrieved[:3]
        ):
            hits_3 += 1

    n = len(queries)
    return {
        "P@1": round(hits_1 / n, 3),
        "P@3": round(hits_3 / n, 3),
        "MRR": round(rr / n, 3),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--val", required=True)
    parser.add_argument("--alpha", type=float, default=0.6)
    parser.add_argument("--topk", type=int, default=8)
    args = parser.parse_args()

    qs = load_validation(Path(args.val))
    metrics = compute_metrics(qs, topk=args.topk, alpha=args.alpha)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()


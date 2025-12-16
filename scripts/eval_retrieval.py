import argparse
import json
import io
import os
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss


def load_resources(index_path: str, meta_path: str, model_name: str):
    model = SentenceTransformer(model_name)
    index = faiss.read_index(index_path)
    if meta_path.endswith(".parquet"):
        df = pd.read_parquet(meta_path)
    else:
        df = pd.read_csv(meta_path)
    # requeridos: text, page
    assert "text" in df.columns, "metadata debe contener columna 'text'"
    assert "page" in df.columns, "metadata debe contener columna 'page'"
    return model, index, df


def retrieve(model, index, df: pd.DataFrame, query: str, k: int = 5):
    q_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    distances, indices = index.search(q_emb, k)

    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        row = df.iloc[idx]
        results.append({
            "rank": int(rank + 1),
            "page": int(row["page"]),
            "text": str(row["text"]),
            "distance": float(dist),
            "row_index": int(idx)
        })
    return results


def is_relevant(result_text: str, result_page: int, expected_pages: List[int], expected_keywords: List[str]) -> bool:
    # criterio 1: página esperada
    if expected_pages:
        if result_page in set(expected_pages):
            return True
    # criterio 2: palabras clave (todas o mayoría)
    if expected_keywords:
        txt = result_text.lower()
        hits = sum(1 for kw in expected_keywords if kw.lower() in txt)
        # mayor o igual al 60% de keywords presentes o 3 coincidencias, lo que ocurra primero
        if hits >= max(3, int(0.6 * len(expected_keywords))):
            return True
    return False


def evaluate_query(model, index, df, q: Dict[str, Any], k: int):
    results = retrieve(model, index, df, q["query"], k=k)
    first_rel_rank = 0
    for r in results:
        if is_relevant(r["text"], r["page"], q.get("expected_pages", []), q.get("expected_keywords", [])):
            first_rel_rank = r["rank"]
            break

    precision1 = 1.0 if first_rel_rank == 1 else 0.0
    mrr = (1.0 / first_rel_rank) if first_rel_rank > 0 else 0.0

    out = {
        "id": q["id"],
        "category": q.get("category", ""),
        "label": q.get("label", ""),
        "query": q["query"],
        "rank_first_relevant": first_rel_rank,
        "precision1": precision1,
        "mrr_contrib": mrr,
        "topk": results,
    }
    return out


def summarize(rows: List[Dict[str, Any]]):
    import statistics
    N = len(rows)
    p1 = statistics.fmean([r["precision1"] for r in rows]) if rows else 0.0
    mrr = statistics.fmean([r["mrr_contrib"] for r in rows]) if rows else 0.0
    by_cat: Dict[str, List[Dict[str, Any]]] = {}
    for r in rows:
        by_cat.setdefault(r.get("category", ""), []).append(r)
    per_cat = {}
    for c, arr in by_cat.items():
        per_cat[c] = {
            "n": len(arr),
            "p1": float(sum(x["precision1"] for x in arr) / len(arr)),
            "mrr": float(sum(x["mrr_contrib"] for x in arr) / len(arr)),
        }
    return {
        "n": N,
        "p1": float(p1),
        "mrr": float(mrr),
        "by_category": per_cat,
    }


def to_md(summary: Dict[str, Any]) -> str:
    lines = []
    lines.append("# Resultados de Evaluación (Retrieval)")
    lines.append("")
    lines.append(f"- Total preguntas: {summary['n']}")
    lines.append(f"- Precision@1: {summary['p1']:.3f}")
    lines.append(f"- MRR: {summary['mrr']:.3f}")
    lines.append("")
    lines.append("## Por categoría")
    for cat, met in sorted(summary.get("by_category", {}).items()):
        lines.append(f"- {cat}: n={met['n']} | P@1={met['p1']:.3f} | MRR={met['mrr']:.3f}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--val", default="validation/validation_set.jsonl")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()

    model, index, df = load_resources(args.index, args.meta, args.model)

    # cargar validation set
    val_path = Path(args.val)
    rows = []
    with io.open(val_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    eval_rows = []
    for q in rows:
        eval_rows.append(evaluate_query(model, index, df, q, k=args.k))

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # detalles JSONL
    details_path = outdir / "eval_details.jsonl"
    with io.open(details_path, "w", encoding="utf-8") as fw:
        for r in eval_rows:
            fw.write(json.dumps(r, ensure_ascii=False) + "\n")

    # resumen
    summary = summarize(eval_rows)
    summary_path = outdir / "eval_summary.json"
    with io.open(summary_path, "w", encoding="utf-8") as fw:
        json.dump(summary, fw, ensure_ascii=False, indent=2)

    # markdown
    md_path = outdir / "eval_summary.md"
    with io.open(md_path, "w", encoding="utf-8") as fw:
        fw.write(to_md(summary) + "\n")

    print(f"Wrote: {details_path}")
    print(f"Wrote: {summary_path}")
    print(f"Wrote: {md_path}")


if __name__ == "__main__":
    main()

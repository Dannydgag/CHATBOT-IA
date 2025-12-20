#!/usr/bin/env python3
"""
Genera distribuciones de scores sobre validation_set y sugiere umbral
Este script sugiere threshold ≈ p75 (percentil 75) como umbral inicial para evitar respuestas con puntajes muy bajos. 
En las pruebas anteriores los scores relevantes ~0.58–0.72; p75 suele estar en ~0.62–0.68.

Ejecución:
python scripts/s4_m3_compute_threshold.py --val validation/validation_set.jsonl --out results/threshold_scores.json

Salida: results/threshold_scores.json (scores por query) y propone threshold.
"""
import argparse, json
from pathlib import Path
import numpy as np
from tqdm import tqdm
from m11_search_hybrid import search  # tu función de búsqueda híbrida

def load_validation(path):
    qs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            qs.append(json.loads(line))
    return qs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--val", required=True, help="validation/validation_set.jsonl")
    ap.add_argument("--topk", type=int, default=50)
    ap.add_argument("--out", default="results/threshold_scores.json")
    args = ap.parse_args()

    Path("results").mkdir(exist_ok=True)
    qs = load_validation(args.val)
    all_scores = []
    data = []
    for q in tqdm(qs):
        res = search(query=q["query"], topk=args.topk, alpha=0.6)
        scores = [r.get("raw_emb", r.get("score",0.0)) for r in res]
        all_scores.extend(scores)
        data.append({"id": q["id"], "query": q["query"], "scores": scores, "pages": q.get("expected_pages",[])})
    # stats
    arr = np.array(all_scores, dtype=float)
    out = {
        "count_scores": int(arr.size),
        "mean": float(arr.mean()) if arr.size else 0.0,
        "std": float(arr.std()) if arr.size else 0.0,
        "p50": float(np.percentile(arr,50)) if arr.size else 0.0,
        "p75": float(np.percentile(arr,75)) if arr.size else 0.0,
        "p90": float(np.percentile(arr,90)) if arr.size else 0.0,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"summary": out, "data": data}, f, ensure_ascii=False, indent=2)
    print("Guardado ->", args.out)
    print("Resumen:", out)
    print("Sugerencia: probar umbral cercano al percentil 75:", out["p75"])

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
scripts/validate_embeddings_sample.py
Checks shape, NaNs, normalization and runs a few sample queries to inspect nearest neighbors.

Uso:
.\.venv\Scripts\python.exe scripts/m8_validate_embeddings_sample.py --emb models/embeddings_sample.npy --ids models/embeddings_sample_ids.json --queries validation/embeddings_qc_queries.jsonl --topk 5 --normalize_query

"""
import argparse, json, numpy as np, os
from math import isclose
from pprint import pprint

def load_ids(path):
    with open(path,'r',encoding='utf-8') as f:
        j = json.load(f)
    return j.get('ids', [])

def cosine_sim_matrix(q_emb, embs):
    # q_emb shape (D,) or (1,D)
    q = q_emb / (np.linalg.norm(q_emb)+1e-12)
    E = embs / (np.linalg.norm(embs, axis=1, keepdims=True)+1e-12)
    sims = E.dot(q)
    return sims

def main(args):
    embs = np.load(args.emb)
    ids = load_ids(args.ids)
    print("Loaded embeddings:", embs.shape)
    print("Loaded ids:", len(ids))
    assert embs.shape[0] == len(ids), "Mismatch rows vs ids"

    # basic checks
    print("NaNs:", np.isnan(embs).any())
    lens = np.linalg.norm(embs, axis=1)
    print("Embedding dim:", embs.shape[1])
    print("Norms: mean", float(lens.mean()), "std", float(lens.std()), "min", float(lens.min()), "max", float(lens.max()))

    # simple retrieval for each of queries in queries file (optional)
    if args.queries and os.path.exists(args.queries):
        print("Running manual queries from", args.queries)
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(args.model)
        with open(args.queries,'r',encoding='utf-8') as f:
            for line in f:
                q = json.loads(line)
                qtext = q.get('query')
                qemb = model.encode([qtext], convert_to_numpy=True)[0]
                if args.normalize_query:
                    qemb = qemb / (np.linalg.norm(qemb)+1e-12)
                sims = cosine_sim_matrix(qemb, embs)
                topk = sims.argsort()[::-1][:args.topk]
                print("\nQuery:", qtext)
                for rank, idx in enumerate(topk, start=1):
                    print(f" {rank}. id={ids[idx]} sim={sims[idx]:.4f}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--emb", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--queries", default=None)
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--model", default="all-MiniLM-L6-v2")
    ap.add_argument("--normalize_query", action="store_true")
    args = ap.parse_args()
    main(args)

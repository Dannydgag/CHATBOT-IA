#!/usr/bin/env python3
"""
scripts/generate_embeddings.py

Genera embeddings para un sample de chunks.jsonl y guarda:
 - models/embeddings_sample.npy  -> float32 array (N, D)
 - models/embeddings_sample_ids.json -> list of ids (order aligned with rows)

Uso:
.\.venv\Scripts\python.exe scripts/m7_generate_embeddings.py --input data/chunks/chunks.cleaned.jsonl --out_dir models --sample_n 50 --model all-MiniLM-L6-v2 --normalize


"""

import argparse
import json
import os
import time
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

def read_chunks(jsonl_path, sample_n=None):
    rows = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            rows.append(json.loads(line))
    if sample_n is None or sample_n >= len(rows):
        return rows
    # pick first N deterministically so QA can reproduce; you can randomize if desired
    return rows[:sample_n]

def main(args):
    os.makedirs(args.out_dir, exist_ok=True)
    # record run info
    run_info = {
        "model": args.model,
        "input": args.input,
        "sample_n": args.sample_n,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    print("Run info:", run_info)

    rows = read_chunks(args.input, sample_n=args.sample_n)
    print(f"Read {len(rows)} chunks from {args.input}")

    # load model (use exact name recommended)
    model_name = args.model
    print("Cargando modelo:", model_name)
    model = SentenceTransformer(model_name)

    texts = [r.get('text','') for r in rows]
    ids = [r.get('id') or r.get('chunk_id') or f"sample_{i}" for i, r in enumerate(rows)]

    # batch encode
    batch_size = args.batch
    embs = []
    print("Calculando embeddings en batches...")
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i+batch_size]
        emb = model.encode(batch, show_progress_bar=False, convert_to_numpy=True)
        embs.append(emb.astype('float32'))
    embs = np.vstack(embs)
    print("Embeddings shape:", embs.shape)

    # optional: normalize to unit length (recommended for cosine)
    if args.normalize:
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms==0] = 1e-6
        embs = embs / norms

    # save npy and ids mapping
    out_npy = os.path.join(args.out_dir, args.out_np or "embeddings_sample.npy")
    out_ids = os.path.join(args.out_dir, args.out_ids or "embeddings_sample_ids.json")
    np.save(out_npy, embs)
    with open(out_ids, 'w', encoding='utf-8') as f:
        json.dump({"ids": ids, "run_info": run_info}, f, ensure_ascii=False, indent=2)

    print("Saved embeddings ->", out_npy)
    print("Saved ids mapping ->", out_ids)
    # save run info file
    with open(os.path.join(args.out_dir, "embeddings_sample_runinfo.json"), "w", encoding="utf-8") as f:
        json.dump(run_info, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="chunks.cleaned.jsonl input")
    ap.add_argument("--out_dir", default="models", help="output directory")
    ap.add_argument("--sample_n", type=int, default=20, help="how many chunks from top to encode")
    ap.add_argument("--batch", type=int, default=32, help="batch size for encoding")
    ap.add_argument("--model", default="all-MiniLM-L6-v2", help="sentence-transformers model name")
    ap.add_argument("--normalize", action="store_true", help="l2-normalize embeddings (recommended)")
    ap.add_argument("--out_np", default=None, help="filename for numpy .npy within out_dir")
    ap.add_argument("--out_ids", default=None, help="filename for ids json within out_dir")
    args = ap.parse_args()
    main(args)

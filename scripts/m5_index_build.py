#!/usr/bin/env python3
# scripts/index_build.py
import argparse, json, os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm

def read_chunks(jsonl_path):
    ids, texts, pages, sources = [], [], [], []
    with open(jsonl_path,'r',encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            ids.append(r['id'])
            texts.append(r['text'])
            pages.append(r.get('page'))
            sources.append(r.get('source'))
    return ids, texts, pages, sources

def normalize_embeddings(emb):
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms==0] = 1e-6
    return emb / norms

def build_index(model_name, chunks_path, index_out, meta_out, batch_size=64, use_gpu=False):
    ids, texts, pages, sources = read_chunks(chunks_path)
    model = SentenceTransformer(model_name)
    dim = model.get_sentence_embedding_dimension()
    # compute embeddings in batches
    all_embs = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding"):
        batch = texts[i:i+batch_size]
        emb = model.encode(batch, show_progress_bar=False, convert_to_numpy=True)
        all_embs.append(emb)
    all_embs = np.vstack(all_embs).astype('float32')
    all_embs = normalize_embeddings(all_embs)
    # build faiss index (inner product for cosine with normalized embeddings)
    index = faiss.IndexFlatIP(dim)
    index.add(all_embs)
    # save index
    os.makedirs(os.path.dirname(index_out) or '.', exist_ok=True)
    faiss.write_index(index, index_out)
    # save metadata (keep same order as embeddings)
    df = pd.DataFrame({
        'id': ids,
        'text': texts,
        'page': pages,
        'source': sources,
        'index_pos': list(range(len(ids)))
    })
    os.makedirs(os.path.dirname(meta_out) or '.', exist_ok=True)
    df.to_parquet(meta_out, index=False)
    print(f"Index saved to {index_out}; metadata saved to {meta_out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--chunks', required=True)
    ap.add_argument('--index', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--model', default='all-MiniLM-L6-v2')
    ap.add_argument('--batch', type=int, default=64)
    args = ap.parse_args()
    build_index(args.model, args.chunks, args.index, args.meta, batch_size=args.batch)

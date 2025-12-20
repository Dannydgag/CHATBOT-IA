#!/usr/bin/env python3
"""
scripts/build_index_from_chunks.py
Crea: models/embeddings_all.npy, models/embeddings_all_ids.json,
       index/faiss.index, index/metadata.json
Uso:
python scripts/s4_m1_build_index_from_chunks.py --chunks data/chunks/chunks.cleaned.jsonl --model all-MiniLM-L6-v2 --out_dir . --batch 64 --normalize --force
"""
import argparse
import json
import os
from pathlib import Path
from tqdm import tqdm
import numpy as np

def ensure_dir(d):
    Path(d).mkdir(parents=True, exist_ok=True)

def load_chunks(path):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            chunks.append(json.loads(line))
    return chunks

def compute_embeddings(chunks, model_name, batch_size=64, normalize=False):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    texts = [c.get("text","") for c in chunks]
    emb_shape = (len(texts), model.get_sentence_embedding_dimension())
    out = np.zeros(emb_shape, dtype="float32")
    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding"):
        batch_texts = texts[i:i+batch_size]
        e = model.encode(batch_texts, show_progress_bar=False)
        e = np.array(e, dtype="float32")
        if normalize:
            norms = np.linalg.norm(e, axis=1, keepdims=True)
            norms[norms==0] = 1.0
            e = e / norms
        out[i:i+len(e)] = e
    return out

def build_faiss_index(embeddings, out_path):
    import faiss
    d = embeddings.shape[1]
    # Usamos IndexFlatIP (dot product) con embeddings normalizados -> equivalente a coseno
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    faiss.write_index(index, str(out_path))
    return index.ntotal, index.d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True)
    ap.add_argument("--model", default="all-MiniLM-L6-v2")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--normalize", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    OUT = Path(args.out_dir)
    MODELS = OUT / "models"
    INDEX = OUT / "index"
    ensure_dir(MODELS)
    ensure_dir(INDEX)

    chunks = load_chunks(args.chunks)
    print(f"Leidos {len(chunks)} chunks.")

    emb_file = MODELS / "embeddings_all.npy"
    ids_file = MODELS / "embeddings_all_ids.json"
    meta_file = INDEX / "metadata.json"
    faiss_file = INDEX / "faiss.index"

    if emb_file.exists() and not args.force:
        print(f"{emb_file} ya existe. Use --force para sobrescribir.")
    else:
        embs = compute_embeddings(chunks, args.model, batch_size=args.batch, normalize=args.normalize)
        np.save(str(emb_file), embs)
        ids = [c.get("id") for c in chunks]
        with open(ids_file, "w", encoding="utf-8") as f:
            json.dump(ids, f, ensure_ascii=False)
        print(f"Guardado: {emb_file}")
        print(f"IDs: {ids_file}")

        # build index
        n, d = build_faiss_index(embs, faiss_file)
        print(f"Index guardado: {faiss_file} (n={n}, d={d})")

    # metadata: store list of chunk metadata in order
    meta = [{"id": c.get("id"), "page": c.get("page"), "source": c.get("source")} for c in chunks]
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)
    print(f"metadata guardada: {meta_file}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# scripts/build_faiss_index.py
#.\.venv\Scripts\python.exe scripts\m10_build_faiss_index.py --emb models/embeddings_all.npy --meta metadata/metadata.parquet --index_out index/faiss.index
import os, argparse, numpy as np, pandas as pd
import faiss
import json

def build_and_save_index(emb_path, meta_path, index_out):
    embs = np.load(emb_path).astype('float32')
    # assume embeddings already normalized (if not, normalize here)
    # Normalize just in case
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    norms[norms==0] = 1e-6
    embs = embs / norms
    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embs)
    os.makedirs(os.path.dirname(index_out) or '.', exist_ok=True)
    faiss.write_index(index, index_out)
    print("Index saved to", index_out, "ntotal:", index.ntotal)
    # ensure metadata exists
    if not os.path.exists(meta_path):
        # try to build metadata from ids file
        ids_file = os.path.join(os.path.dirname(emb_path), 'embeddings_all_ids.json')
        if os.path.exists(ids_file):
            print("Building metadata parquet from ids...")
            with open(ids_file,'r',encoding='utf-8') as f:
                ids_obj = json.load(f)
            ids = ids_obj.get('ids', [])
            df = pd.DataFrame({'id': ids, 'page':[None]*len(ids), 'text':[None]*len(ids), 'index_pos':list(range(len(ids)))})
            os.makedirs(os.path.dirname(meta_path) or '.', exist_ok=True)
            df.to_parquet(meta_path, index=False)
            print("Saved metadata to", meta_path)
        else:
            print("WARNING: metadata not found and cannot be generated (ids file missing).")
    return index

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--emb', default='models/embeddings_all.npy')
    p.add_argument('--meta', default='metadata/metadata.parquet')
    p.add_argument('--index_out', default='index/faiss.index')
    args = p.parse_args()
    build_and_save_index(args.emb, args.meta, args.index_out)

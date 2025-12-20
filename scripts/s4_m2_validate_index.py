#!/usr/bin/env python3
#python scripts/s4_m2_validate_index.py
import json
from pathlib import Path
import numpy as np
import faiss

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index" / "faiss.index"
META = ROOT / "index" / "metadata.json"
EMB = ROOT / "models" / "embeddings_all.npy"

def main():
    assert INDEX.exists(), "index/faiss.index no existe"
    assert META.exists(), "index/metadata.json no existe"
    assert EMB.exists(), "models/embeddings_all.npy no existe"

    meta = json.loads(META.read_text(encoding="utf-8"))
    embs = np.load(str(EMB))
    idx = faiss.read_index(str(INDEX))
    print("vectors en index:", idx.ntotal, "dim:", idx.d)
    print("metadata entries:", len(meta))
    print("embeddings shape:", embs.shape)
    assert idx.ntotal == len(meta) == embs.shape[0], "Desajuste: index/meta/embeddings"
    print("VALIDACION OK")

if __name__ == "__main__":
    main()

# scripts/debug_search_report.py
import argparse, json, re
from pathlib import Path
import faiss, numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# (reutiliza CONSTANTS y utils de tu m11_search_hybrid o importarlos)
# Para brevedad asume que m11_search_hybrid.py está actualizado y expone funciones:
from scripts.m11_search_hybrid import search, load_chunks, load_tfidf, CHUNKS_FILE, FAISS_INDEX_FILE

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--topk", type=int, default=20)
    ap.add_argument("--retrieve_k", type=int, default=256)
    args = ap.parse_args()

    # Llamada simple a search en modo debug: pide retrieve_k grande y solicita más resultados
    res = search(query=args.q, topk=args.topk, retrieve_k=args.retrieve_k, alpha=0.6, max_snip=300)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

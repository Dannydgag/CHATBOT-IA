#!/usr/bin/env python3
"""
m11_search_hybrid.py
Búsqueda híbrida (embeddings + TF-IDF) con re-rank y boosts.
Requisitos: index/faiss.index, index/tfidf_vectorizer.joblib, index/tfidf_matrix.npz,
            data/chunks/chunks.cleaned.jsonl
"""

import argparse
import json
import re
from pathlib import Path
import time

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import scipy.sparse as sp

# Paths (ajusta si es necesario)
ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = ROOT / "data" / "chunks" / "chunks.cleaned.jsonl"
FAISS_INDEX_FILE = ROOT / "index" / "faiss.index"
TFIDF_VEC_FILE = ROOT / "index" / "tfidf_vectorizer.joblib"
TFIDF_MAT_FILE = ROOT / "index" / "tfidf_matrix.npz"

# Regex
SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')
WORD_RE = re.compile(r"\w+", re.UNICODE)

# Config defaults (ajustables)
DEFAULT_RETRIEVE_K = 256
DEFAULT_TFIDF_TOPK = 256
DEFAULT_ALPHA = 0.9
DEFAULT_MIN_SCORE = 0.55

# -------------------
# Utilidades
# -------------------
def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

def tokenize(text):
    return WORD_RE.findall(text.lower())

def clean_query_for_search(q):
    """Devuelve una versión de la query para embeddings/TF-IDF:
       - elimina signos de interrogación, paréntesis, comillas
       - elimina interrogativos iniciales (opcional) para mejorar semántica
    """
    q = q.strip()
    q = q.replace("¿", "").replace("?", "").replace("¡", "").replace("!", "")
    q = re.sub(r"[\"'()\[\]]+", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    q = re.sub(r'^(qué|quién|quienes|quiénes|cuándo|cuando|cómo|como|por qué|por que|dónde|donde|para qué|para que)\b\s*', '', q, flags=re.IGNORECASE)
    return q

def build_sentence_snippet(text, query, max_chars=400):
    """Devuelve la oración con mayor overlap de tokens; fallback a inicio del chunk."""
    sentences = SENT_SPLIT_RE.split(text)
    q_tokens = set(tokenize(query))
    best = None
    best_overlap = 0
    for s in sentences:
        overlap = len(q_tokens & set(tokenize(s)))
        if overlap > best_overlap:
            best_overlap = overlap
            best = s.strip()
    if best:
        if len(best) <= max_chars:
            return best
        return best[:max_chars].strip()
    return text.strip()[:max_chars].strip()

# -------------------
# Search function
# -------------------
def search(
    query,
    topk=8,
    alpha=DEFAULT_ALPHA,
    retrieve_k=DEFAULT_RETRIEVE_K,
    tfidf_topk=DEFAULT_TFIDF_TOPK,
    max_snip=400,
    min_score=DEFAULT_MIN_SCORE,
    model_name="all-MiniLM-L6-v2",
    verbose=False
):
    start_total = time.time()
    chunks = load_chunks(CHUNKS_FILE)

    # Preprocess queries
    q_raw = query.strip()
    q_clean = clean_query_for_search(q_raw)
    if verbose:
        print(f"[debug] q_raw: {q_raw!r}")
        print(f"[debug] q_clean: {q_clean!r}")

    # Load model + FAISS
    load_start = time.time()
    model = SentenceTransformer(model_name)
    index = faiss.read_index(str(FAISS_INDEX_FILE))
    if verbose:
        print(f"[debug] model+index load: {time.time()-load_start:.3f}s")

    # Encode embedding for cleaned query (normalized)
    t0 = time.time()
    q_emb = normalize(model.encode([q_clean])[0]).astype("float32").reshape(1, -1)
    emb_time = time.time() - t0
    if verbose:
        print(f"[debug] q emb time: {emb_time:.3f}s")

    # Embedding retrieval (top retrieve_k)
    t1 = time.time()
    emb_scores, emb_idxs = index.search(q_emb, retrieve_k)
    emb_scores = emb_scores[0]
    emb_idxs = emb_idxs[0]
    if verbose:
        print(f"[debug] faiss search ({retrieve_k}): {time.time()-t1:.3f}s")

    # TF-IDF retrieval: compute scores for all documents and take top tfidf_topk
    t2 = time.time()
    tfidf_vec = joblib.load(TFIDF_VEC_FILE)
    tfidf_mat = sp.load_npz(TFIDF_MAT_FILE)
    q_tfidf = tfidf_vec.transform([q_clean])
    tfidf_scores_all = cosine_similarity(q_tfidf, tfidf_mat)[0]
    tfidf_idxs = np.argsort(-tfidf_scores_all)[:tfidf_topk]
    if verbose:
        print(f"[debug] tfidf topk ({tfidf_topk}) compute: {time.time()-t2:.3f}s")

    # Union of candidate indices
    emb_candidate_set = {int(i) for i in emb_idxs if i >= 0}
    tfidf_candidate_set = {int(i) for i in tfidf_idxs if i >= 0}
    cand_idxs = np.array(sorted(emb_candidate_set | tfidf_candidate_set), dtype=int)
    if verbose:
        print(f"[debug] cand counts: emb={len(emb_candidate_set)} tfidf={len(tfidf_candidate_set)} union={len(cand_idxs)}")

    # Map emb scores
    emb_score_map = {}
    for s, i in zip(emb_scores, emb_idxs):
        if int(i) >= 0:
            emb_score_map[int(i)] = float(s)

    # Re-rank with hybrid formula + boosts
    results = []
    q_tokens = set(tokenize(q_clean))
    q_phrase = q_raw.replace("¿", "").replace("?", "").lower()

    PHRASE_BOOST = 0.30
    TOKEN_MULT = 0.04

    for idx in cand_idxs:
        emb_s = emb_score_map.get(int(idx), 0.0)
        tf_s = float(tfidf_scores_all[int(idx)])
        combined = alpha * emb_s + (1 - alpha) * tf_s

        txt = chunks[int(idx)].get("text", "")
        txt_l = txt.lower()

        boost = 0.0
        # phrase exact word boundary match
        if re.search(r"\b" + re.escape(q_phrase) + r"\b", txt_l):
            boost += PHRASE_BOOST

        # token overlap boost (clean tokens)
        common = q_tokens & set(tokenize(txt_l))
        boost += TOKEN_MULT * len(common)

        final_score = float(combined) + boost

        if final_score < min_score:
            continue

        snippet = build_sentence_snippet(txt, q_clean, max_chars=max_snip)

        results.append({
            "id": chunks[int(idx)].get("id"),
            "page": chunks[int(idx)].get("page"),
            "score": round(final_score, 6),
            "raw_emb": round(float(emb_s), 6),
            "raw_tfidf": round(float(tf_s), 6),
            "snippet": snippet,
            "index_pos": int(idx)
        })

    # Sort and return
    results.sort(key=lambda x: x["score"], reverse=True)
    if verbose:
        print(f"[debug] total time: {time.time()-start_total:.3f}s")
    return results[:topk]

# -------------------
# CLI
# -------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--topk", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    ap.add_argument("--retrieve_k", type=int, default=DEFAULT_RETRIEVE_K)
    ap.add_argument("--tfidf_topk", type=int, default=DEFAULT_TFIDF_TOPK)
    ap.add_argument("--max_snip", type=int, default=400)
    ap.add_argument("--min_score", type=float, default=DEFAULT_MIN_SCORE)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    res = search(
        query=args.q,
        topk=args.topk,
        alpha=args.alpha,
        retrieve_k=args.retrieve_k,
        tfidf_topk=args.tfidf_topk,
        max_snip=args.max_snip,
        min_score=args.min_score,
        verbose=args.verbose
    )
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

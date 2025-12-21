import argparse
import json
import re
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================
# Paths
# =========================
ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = ROOT / "data" / "chunks" / "chunks.cleaned.jsonl"
FAISS_INDEX_FILE = ROOT / "index" / "faiss.index"
TFIDF_VEC_FILE = ROOT / "index" / "tfidf_vectorizer.joblib"
TFIDF_MAT_FILE = ROOT / "index" / "tfidf_matrix.npz"

# =========================
# Regex útiles
# =========================
QUESTION_DEFINITION_RE = re.compile(
    r'^\s*(qué\s+es|definición\s+de|qué\s+significa|define\s+qué)',
    re.IGNORECASE
)

SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')

# =========================
# Utils
# =========================
def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def tokenize(text):
    return re.findall(r"\w+", text.lower())

def normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

def build_sentence_snippet(text, query, max_chars=400):
    sentences = SENT_SPLIT_RE.split(text)
    q_tokens = set(tokenize(query))

    best, best_overlap = None, 0
    for s in sentences:
        overlap = len(q_tokens & set(tokenize(s)))
        if overlap > best_overlap:
            best_overlap = overlap
            best = s.strip()

    if not best:
        return text[:max_chars].strip()

    if len(best) > max_chars:
        return best[:max_chars].strip()

    return best

# =========================
# Search
# =========================
def search(
    query,
    topk=8,
    alpha=0.6,
    retrieve_k=256,
    max_snip=400,
    min_score=0.548
):
    chunks = load_chunks(CHUNKS_FILE)

    # Embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(str(FAISS_INDEX_FILE))

    q_emb = normalize(model.encode([query])[0]).astype("float32").reshape(1, -1)
    emb_scores, emb_idxs = index.search(q_emb, retrieve_k)
    emb_scores, emb_idxs = emb_scores[0], emb_idxs[0]

    # TF-IDF
    import joblib, scipy.sparse as sp
    tfidf_vec = joblib.load(TFIDF_VEC_FILE)
    tfidf_mat = sp.load_npz(TFIDF_MAT_FILE)

    q_tfidf = tfidf_vec.transform([query])
    tfidf_scores = cosine_similarity(q_tfidf, tfidf_mat)[0]

    results = []
    is_definition = bool(QUESTION_DEFINITION_RE.match(query))
    query_tokens = set(tokenize(query))

    for i, idx in enumerate(emb_idxs):
        if idx < 0:
            continue

        emb = float(emb_scores[i])
        tf = float(tfidf_scores[idx])
        score = alpha * emb + (1 - alpha) * tf

        text = chunks[idx]["text"].lower()

        # Boosts controlados
        boost = 0.0

        if is_definition and query.lower().replace("¿", "").replace("?", "") in text:
            boost += 0.30

        common = query_tokens & set(tokenize(text))
        boost += 0.04 * len(common)

        score += boost

        if score < min_score:
            continue

        results.append({
            "id": chunks[idx]["id"],
            "page": chunks[idx]["page"],
            "score": round(score, 6),
            "raw_emb": emb,
            "raw_tfidf": tf,
            "snippet": build_sentence_snippet(
                chunks[idx]["text"], query, max_snip
            ),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:topk]

# =========================
# CLI
# =========================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--topk", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=0.6)
    ap.add_argument("--retrieve_k", type=int, default=256)
    ap.add_argument("--max_snip", type=int, default=400)
    ap.add_argument("--min_score", type=float, default=0.548)
    args = ap.parse_args()

    res = search(
        query=args.q,
        topk=args.topk,
        alpha=args.alpha,
        retrieve_k=args.retrieve_k,
        max_snip=args.max_snip,
        min_score=args.min_score,
    )

    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

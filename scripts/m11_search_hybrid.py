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
# Paths (AJUSTADOS A TU REPO)
# =========================
ROOT = Path(__file__).resolve().parents[1]

CHUNKS_FILE = ROOT / "data" / "chunks" / "chunks.cleaned.jsonl"
FAISS_INDEX_FILE = ROOT / "index" / "faiss.index"
TFIDF_FILE = ROOT / "index" / "tfidf.json"


# =========================
# Utils
# =========================
def load_chunks(path):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def load_tfidf(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tfidf_vec = TfidfVectorizer(
        vocabulary=data["vocab"],
        lowercase=True
    )

    # Inyectar IDF entrenados
    tfidf_vec.idf_ = np.array(data["idf"])
    tfidf_vec._tfidf._idf_diag = np.diag(tfidf_vec.idf_)

    tfidf_mat = np.array(data["matrix"], dtype="float32")
    return tfidf_vec, tfidf_mat


def normalize(v):
    return v / np.linalg.norm(v)


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def build_snippet(text, query, max_len):
    q = query.lower()
    t = text.lower()
    idx = t.find(q)

    if idx == -1:
        return text[:max_len].rstrip()

    start = max(0, idx - max_len // 2)
    end = min(len(text), idx + len(q) + max_len // 2)
    return text[start:end].strip()


# =========================
# Search (Hybrid)
# =========================
def search(query, topk=8, alpha=0.6, max_snip=300, retrieve_k=None):
    chunks = load_chunks(CHUNKS_FILE)
    tfidf_vec, tfidf_mat = load_tfidf(TFIDF_FILE)

    index = faiss.read_index(str(FAISS_INDEX_FILE))
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # --- Embedding search ---
    q_emb = model.encode([query])[0]
    q_emb = normalize(q_emb).astype("float32").reshape(1, -1)

    RETRIEVE_K = retrieve_k or max(128, topk * 8)
    scores, idxs = index.search(q_emb, RETRIEVE_K)

    scores = scores[0]
    idxs = idxs[0]

    # --- TF-IDF search ---
    q_tfidf = tfidf_vec.transform([query])
    tfidf_scores = cosine_similarity(q_tfidf, tfidf_mat)[0]

    # --- Combine ---
    cand_mask = idxs >= 0
    cand_idxs = idxs[cand_mask]

    emb_scores = scores[cand_mask]
    tfidf_sub = tfidf_scores[cand_idxs]

    combined = alpha * emb_scores + (1 - alpha) * tfidf_sub

    # --- Boosts ---
    query_tokens = set(tokenize(query))
    PHRASE_BOOST = 0.25
    TOKEN_MULT = 0.05

    results = []
    for i, ci in enumerate(cand_idxs):
        chunk = chunks[int(ci)]
        txt = chunk["text"].lower()

        boost = 0.0
        if re.search(r"\b" + re.escape(query.lower()) + r"\b", txt):
            boost += PHRASE_BOOST

        common = query_tokens & set(tokenize(txt))
        boost += TOKEN_MULT * len(common)

        score = float(combined[i]) + boost

        results.append({
            "id": chunk["id"],
            "page": chunk["page"],
            "score": round(score, 6),
            "raw_emb": float(emb_scores[i]),
            "raw_tfidf": float(tfidf_sub[i]),
            "snippet": build_snippet(chunk["text"], query, max_snip),
            "index_pos": int(ci),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:topk]


# =========================
# CLI
# =========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True)
    parser.add_argument("--topk", type=int, default=8)
    parser.add_argument("--alpha", type=float, default=0.6)
    parser.add_argument("--max_snip", type=int, default=300)
    args = parser.parse_args()

    res = search(
        query=args.q,
        topk=args.topk,
        alpha=args.alpha,
        max_snip=args.max_snip,
    )

    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

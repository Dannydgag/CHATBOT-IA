import argparse
import json
import re
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================
# Paths
# =========================
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "chunks"
INDEX_DIR = ROOT / "index"

CHUNKS_FILE = DATA_DIR / "chunks.cleaned.jsonl"
FAISS_INDEX_FILE = INDEX_DIR / "faiss.index"
METADATA_FILE = INDEX_DIR / "metadata.json"


# =========================
# Utils
# =========================
def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_metadata(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(v):
    return v / np.linalg.norm(v)


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def build_snippet(text, query, max_len):
    """
    Snippet centrado en la coincidencia léxica más fuerte
    """
    q_tokens = tokenize(query)
    text_l = text.lower()

    positions = [
        text_l.find(tok) for tok in q_tokens if text_l.find(tok) != -1
    ]

    if not positions:
        return text[:max_len].rstrip()

    center = min(positions)
    start = max(0, center - max_len // 2)
    end = min(len(text), start + max_len)
    return text[start:end].strip()


# =========================
# Search
# =========================
def search(
    query,
    topk=8,
    threshold=0.0,
    max_snip=300,
    model_name="all-MiniLM-L6-v2",
):
    chunks = load_chunks(CHUNKS_FILE)
    index = faiss.read_index(str(FAISS_INDEX_FILE))
    model = SentenceTransformer(model_name)

    # Encode query
    q_emb = model.encode([query])[0]
    q_emb = normalize(q_emb).astype("float32").reshape(1, -1)

    RETRIEVE_K = max(60, topk * 6)
    scores, idxs = index.search(q_emb, RETRIEVE_K)

    query_tokens = set(tokenize(query))
    query_l = query.lower()

    # NEW: patrones definitorios
    definition_patterns = [
        "se define como",
        "depende de",
        "consiste en",
        "se basa en",
        "es el",
        "se refiere a",
    ]

    results = []

    for raw_score, idx in zip(scores[0], idxs[0]):
        if idx < 0 or raw_score < threshold:
            continue

        chunk = chunks[idx]
        text = chunk["text"]
        text_l = text.lower()

        boost = 0.0

        # Frase exacta
        if query_l in text_l:
            boost += 0.15

        # Tokens compartidos
        common = query_tokens & set(tokenize(text))
        boost += 0.04 * len(common)

        # NEW: boost definitorio fuerte
        for pat in definition_patterns:
            if pat in text_l:
                boost += 0.12

        final_score = float(raw_score) + boost

        results.append({
            "id": chunk["id"],
            "page": chunk["page"],
            "score": round(final_score, 4),
            "raw_score": float(raw_score),
            "snippet": build_snippet(text, query, max_snip),
            "index_pos": int(idx),
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
    parser.add_argument("--threshold", type=float, default=0.0)
    parser.add_argument("--max_snip", type=int, default=300)
    args = parser.parse_args()

    results = search(
        query=args.q,
        topk=args.topk,
        threshold=args.threshold,
        max_snip=args.max_snip,
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

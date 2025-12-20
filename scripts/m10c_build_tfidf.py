import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================
# Paths
# =========================
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "chunks"
INDEX_DIR = ROOT / "index"

CHUNKS_FILE = DATA_DIR / "chunks.cleaned.jsonl"
TFIDF_FILE = INDEX_DIR / "tfidf.json"

# =========================
# Build TF-IDF
# =========================
def main():
    texts = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["text"])

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )

    X = vectorizer.fit_transform(texts)

    tfidf_data = {
    "vocab": vectorizer.vocabulary_,
    "idf": vectorizer.idf_.tolist(),
    "matrix": X.toarray().astype("float32").tolist()
}


    INDEX_DIR.mkdir(exist_ok=True)

    with open(TFIDF_FILE, "w", encoding="utf-8") as f:
        json.dump(tfidf_data, f)

    print("tfidf.json generado correctamente")
    print(f"Chunks procesados: {len(texts)}")

if __name__ == "__main__":
    main()

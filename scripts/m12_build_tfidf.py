# scripts/build_tfidf.py
import argparse, json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "chunks"
OUT_DIR = ROOT / "index"

def load_texts(path):
    texts = []
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            texts.append(r.get("text",""))
            ids.append(r.get("id"))
    return texts, ids

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", default=str(DATA_DIR / "chunks.cleaned.jsonl"))
    ap.add_argument("--out_dir", default=str(OUT_DIR))
    ap.add_argument("--max_features", type=int, default=50000)
    args = ap.parse_args()

    texts, ids = load_texts(args.chunks)
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=args.max_features, strip_accents='unicode')
    X = vec.fit_transform(texts)  # sparse csr
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(vec, out_dir / "tfidf_vectorizer.joblib")
    sp.save_npz(out_dir / "tfidf_matrix.npz", X)
    with open(out_dir / "tfidf_ids.json", "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False)
    print("TF-IDF construido:", X.shape)

if __name__ == "__main__":
    main()

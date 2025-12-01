import argparse
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

def load_resources(index_path, meta_path, model_name):
    print("Cargando modelo de embeddings...")
    model = SentenceTransformer(model_name)

    print("Cargando índice FAISS...")
    index = faiss.read_index(index_path)

    print("Cargando metadata...")
    df = pd.read_parquet(meta_path)

    return model, index, df

def search_question(question, model, index, df, k=5):
    # Convertir pregunta a embedding
    q_emb = model.encode([question], convert_to_numpy=True)

    # Buscar en FAISS
    distances, indices = index.search(q_emb, k)

    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        row = df.iloc[idx]
        results.append({
            "rank": rank + 1,
            "id": row["id"],
            "page": int(row["page"]),
            "text": row["text"],
            "distance": float(dist)
        })

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True)
    parser.add_argument("--meta", required=True)
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--q", required=True)
    args = parser.parse_args()

    model, index, df = load_resources(args.index, args.meta, args.model)

    results = search_question(args.q, model, index, df, k=5)

    print("\n=== RESULTADOS ===")
    for r in results:
        print(f"\n[{r['rank']}] Página {r['page']} — score {r['distance']:.4f}")
        print(r["text"])
        print("-" * 80)

if __name__ == "__main__":
    main()

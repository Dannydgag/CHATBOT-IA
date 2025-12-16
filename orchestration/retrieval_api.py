import faiss
import numpy as np
import json

class Retriever:
    def __init__(self, index_path, ids_path):
        self.index = faiss.read_index(index_path)
        with open(ids_path, 'r', encoding='utf-8') as f:
            self.ids = json.load(f)

    def retrieve(self, query_embedding, top_k=5):
        query_embedding = np.array([query_embedding]).astype('float32')
        scores, idxs = self.index.search(query_embedding, top_k)
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx == -1:
                continue
            results.append({
                "chunk_id": self.ids[str(idx)],
                "score": float(score)
            })
        return results

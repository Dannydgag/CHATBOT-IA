import numpy as np
from retrieval_api import Retriever

# Dummy test (replace with real embedding)
dummy_embedding = np.random.rand(384).astype('float32')

retriever = Retriever(
    index_path='index/faiss.index',
    ids_path='models/embeddings_sample_ids.json'
)

print(retriever.retrieve(dummy_embedding, top_k=3))

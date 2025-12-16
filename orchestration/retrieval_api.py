from scripts.m6_search import search

def retrieve(query: str, top_k: int = 5):
    results = search(query=query, top_k=top_k)
    return results

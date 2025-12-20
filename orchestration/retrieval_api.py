from typing import List, Dict, Any
from scripts.m6_search import search

def retrieve(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    API de recuperación que desacopla la UI del motor de búsqueda.
    """

    raw_results = search(query=query, top_k=top_k)

    formatted_results = []
    for r in raw_results:
        formatted_results.append({
            "text": r.get("text", ""),
            "page": r.get("page"),
            "score": float(r.get("score", r.get("distance", 0.0)))
        })

    return formatted_results

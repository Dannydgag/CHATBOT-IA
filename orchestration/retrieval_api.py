from typing import List, Dict, Any
from scripts.m11_search_hybrid import search


def retrieve(
    query: str,
    top_k: int = 5,
    alpha: float = 0.6
) -> List[Dict[str, Any]]:
    """
    API única de recuperación de información para la aplicación.

    Parameters
    ----------
    query : str
        Consulta en lenguaje natural ingresada por el usuario.
    top_k : int
        Número de resultados más relevantes a retornar.
    alpha : float
        Peso entre embeddings y TF-IDF (control interno del backend).

    Returns
    -------
    List[Dict[str, Any]]
        Lista de resultados normalizados para la UI con las claves:
        - text  : str   -> snippet relevante del documento
        - page  : int   -> página de origen
        - score : float -> score híbrido de similitud
    """

    # Delegar la búsqueda al motor híbrido (Mateo)
    raw_results = search(
        query=query,
        topk=top_k,
        alpha=alpha
    )

    # Normalizar resultados para desacoplar la UI del motor de búsqueda
    formatted_results: List[Dict[str, Any]] = []

    for r in raw_results:
        formatted_results.append({
            "text": r.get("snippet", ""),
            "page": int(r.get("page", -1)),
            "score": float(r.get("score", 0.0))
        })

    return formatted_results

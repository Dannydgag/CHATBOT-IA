from typing import List, Dict, Any
from scripts.m11_search_hybrid import search

# =========================
# Threshold calibrado (Mateo)
# =========================
MIN_SCORE = 0.55


def retrieve(
    query: str,
    top_k: int = 5,
    alpha: float = 0.9
) -> Dict[str, Any]:
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
    Dict[str, Any]
        Estructura normalizada para la UI:
        - status : "ok" | "no_answer"
        - results: List[Dict] (si status == "ok")
        - message: str (si status == "no_answer")
    """

    # 1. Delegar la búsqueda al motor híbrido
    raw_results = search(
        query=query,
        topk=top_k,
        alpha=alpha
    )

    # 2. Aplicar umbral de similitud
    filtered = [
        r for r in raw_results
        if float(r.get("score", 0.0)) >= MIN_SCORE
    ]

    # 3. Manejo explícito de "no hay respuesta"
    if not filtered:
        return {
            "status": "no_answer",
            "message": "Lo siento, no encontré información relevante en el libro."
        }

    # 4. Normalizar resultados para la UI
    formatted_results: List[Dict[str, Any]] = []

    for r in filtered:
        formatted_results.append({
            "text": r.get("snippet", ""),
            "page": int(r.get("page", -1)),
            "score": float(r.get("score", 0.0))
        })

    return {
        "status": "ok",
        "results": formatted_results
    }

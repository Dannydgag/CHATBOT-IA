"""
full_pipeline.py
================
Orquestación completa del sistema.
No altera la lógica de búsqueda.
Maneja estados, errores, tiempos y logging.

Responsable: Xander
Semana: 4
"""

import time
import logging
from typing import Dict, Any

from orchestration.retrieval_api import retrieve


# --- Logging ---
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def run_pipeline(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Ejecuta el pipeline completo y devuelve
    un response listo para la UI.
    """

    start_time = time.time()

    try:
        response = retrieve(query=query, top_k=top_k)
        elapsed = round(time.time() - start_time, 3)

        response["time"] = elapsed

        if response["status"] == "ok":
            logging.info(
                f"OK | query='{query}' | hits={len(response['results'])} | time={elapsed}s"
            )
        else:
            logging.info(
                f"NO_ANSWER | query='{query}' | time={elapsed}s"
            )

        return response

    except Exception as e:
        elapsed = round(time.time() - start_time, 3)

        logging.error(
            f"ERROR | query='{query}' | {str(e)}"
        )

        return {
            "status": "error",
            "message": "Ocurrió un error al procesar la consulta.",
            "results": [],
            "time": elapsed
        }

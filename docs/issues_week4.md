# Issues Prioritarios — Semana 4

## Alta Prioridad

- **Extracción incompleta (10 páginas faltantes)**: Completar y validar páginas ausentes en `data/text_by_page/`.
  - Responsable: Erik
  - Evidencia: docs/qa_summary_week2.md
- **Chunking subóptimo (contexto diluido)**: Ajustar `CHUNK_SIZE=800` y `CHUNK_OVERLAP=200`; revisar limpieza de saltos y hyphen repair.
  - Responsable: Erik + Mateo
  - Evidencia: scripts/chunk_text.py
- **Baja P@1 en categorías clave**: Búsqueda informada/no informada, optimización, CSP.
  - Responsable: Mateo
  - Acción: Reindexar tras mejora de chunks; evaluar `top_k=10` + re-ranking simple.
- **Gate de “no respuesta”**: Implementar umbral de similitud `threshold=0.50` en la UI/backend.
  - Responsable: Xander + Joel
  - Evidencia: results/week4_threshold.md

## Media Prioridad

- **Keyword Boost en recuperación**: Aumentar score cuando keywords esperadas aparecen en el texto.
  - Responsable: Xander
- **Logs y trazabilidad**: Agregar logging de consulta, score y páginas devueltas.
  - Responsable: Xander

## Baja Prioridad

- **Mejoras de UI**: Mostrar citas (página, fragmento recortado), score y badge “sin evidencia”.
  - Responsable: Joel
- **Documentación**: Actualizar docs/eval_protocol.md con parámetros por defecto (k=10, threshold=0.50).
  - Responsable: Gabo

## Plan de Coordinación

- Erik: finalizar extracción + revisar limpieza.
- Mateo: re-chunking + reindexado FAISS.
- Xander: integrar umbral y keyword boost en `orchestration/retrieval_api.py`.
- Joel: UI con `top_k=10`, mostrar umbral y mensaje “No se encontró información relevante”.
- Gabo: volver a ejecutar `scripts/eval_retrieval.py` y actualizar `docs/eval_results_week4.md` tras cambios.

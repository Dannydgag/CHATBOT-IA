# Resultados Semana 4 — Evaluación de Recuperación

- Dataset: validation/validation_set.jsonl (40 preguntas)
- Índice: index/faiss.index (FAISS IP, embeddings normalizados)
- Metadata: metadata/metadata.parquet
- Modelo: sentence-transformers/all-MiniLM-L6-v2

## Matriz de Resultados (k)

- k=3: P@1=0.050 | MRR=0.058
  - Detalles: results/week4_k3/eval_details.jsonl
  - Resumen: results/week4_k3/eval_summary.md
- k=5: P@1=0.050 | MRR=0.076
  - Detalles: results/week4_k5/eval_details.jsonl
  - Resumen: results/week4_k5/eval_summary.md
- k=10: P@1=0.050 | MRR=0.084
  - Detalles: results/week4_k10/eval_details.jsonl
  - Resumen: results/week4_k10/eval_summary.md

Observación: Incrementar `top_k` mejora la MRR (recuperación promedio) pero no la P@1. Recomendación operativa: usar `top_k=10` en UI/QA para mayor cobertura con evidencia.

## Calibración de Umbral

- Análisis de `score` (top-1) en k=10: results/week4_threshold.md
  - Media top-1: 0.598 | Q50: 0.605
  - Diferencia de medias: covered ≈ 0.615 vs uncovered ≈ 0.502
  - Barrido de umbrales (0.20–0.50): mejor exactitud en 0.50
- Recomendación: `threshold=0.50` para “no respuesta” cuando `score < 0.50`.
  - Nota: debido a la baja P@1 general, el umbral mitigará falsos positivos, pero no compensará problemas de extracción/chunking.

## Principales Hallazgos

- Categorías con peores métricas (P@1=0, MRR≈0): agentes, búsqueda informada/no informada, optimización, CSP.
- Única categoría con P@1=1: representación del conocimiento.
- Causas probables: cobertura incompleta del PDF (10 páginas faltantes), chunks grandes con contexto diluido, keywords esperadas no presentes en algunos fragmentos.

## Acciones Propuestas (Semana 4)

- `top_k=10` por defecto en evaluación y UI.
- `threshold=0.50` para gate de “no respuesta”.
- Re-ejecutar extracción para páginas faltantes y revisar limpieza.
- Ajustar `CHUNK_SIZE` y `CHUNK_OVERLAP` (p. ej., 800/200) y reindexar.
- Añadir re-ranking simple (keyword boost) en la capa de recuperación.

## Enlaces Útiles

- Resultados Semana 3: docs/eval_results_week3.md
- Protocolo: docs/eval_protocol.md
- Errores priorizados (Semana 3): results/eval_top_errors.md

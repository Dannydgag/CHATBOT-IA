# Resultados Semana 3 — Evaluación de Recuperación

- Set: `validation/validation_set.jsonl` (40 preguntas)
- Índice/Meta: `indices/idx.faiss` + `indices/meta.parquet`
- Modelo: `sentence-transformers/all-MiniLM-L6-v2`
- Top-K: 5

## Métricas Globales
- Precision@1: 0.050
- MRR: 0.117

## Por Categoría (resumen)
- Ver `results/eval_summary.md` para el detalle por categoría.

## Observaciones Iniciales
- P@1 bajo sugiere necesidad de:
  - Ajustar chunking (tamaño/overlap) para capturar mejor evidencia.
  - Revisar `expected_pages`/`keywords` de algunas preguntas para asegurar alineación con el texto.
  - Considerar umbral de similitud y normalización; ya usamos L2 + IP.
- Algunas categorías (lógica de primer orden, reglas) muestran MRR>0 indicando relevante en rangos >1.

## Errores priorizados
- Ver análisis con ejemplos en [results/eval_top_errors.md](results/eval_top_errors.md).

## Próximos Pasos Propuestos
- Mateo: calibrar umbral con `results/eval_details.jsonl` (distribución de similitudes) y proponer `threshold_calibration.md`.
- Erik: revisar ejemplos fallidos (P@1=0) y ajustar limpieza/chunking en páginas clave.
- Xander: validar que `retrieve(query, top_k)` en pipeline reproduce los resultados del script.

Referencias:
- Resumen: `results/eval_summary.md`
- JSON agregadas: `results/eval_summary.json`
- Detalles por pregunta: `results/eval_details.jsonl`

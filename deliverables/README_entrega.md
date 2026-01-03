# Entrega Final — Asistente Académico (RAG sobre PDF)

Este README concentra lo necesario para revisar la entrega: qué se hizo, cómo replicar las pruebas de recuperación (Semana 4), métricas, evidencias y checklist de QA final.

## Resumen de la Entrega
- Proyecto: Asistente académico con recuperación semántica sobre un PDF.
- Stack: PyMuPDF, Sentence-Transformers (`all-MiniLM-L6-v2`), FAISS (IP), Streamlit.
- Alcance (Semana 4): Ejecutar batería de pruebas del `validation_set`, compilar resultados (matriz por `top_k`), recomendar ajustes (umbral, `top_k`) y priorizar issues.

## Métricas Clave (Semana 4)
- `top_k=3`: P@1=0.050, MRR=0.058
- `top_k=5`: P@1=0.050, MRR=0.076
- `top_k=10`: P@1=0.050, MRR=0.084
- Umbral recomendado (gate "no respuesta"): `threshold=0.50` (análisis en `results/week4_threshold.md`).

Referencias:
- Matriz y resumen: `docs/eval_results_week4.md`
- Issues priorizados: `docs/issues_week4.md`

## Evidencias Incluidas
- Resultados por `top_k`:
  - `results/week4_k3/eval_summary.json`, `eval_summary.md`, `eval_details.jsonl`
  - `results/week4_k5/eval_summary.json`, `eval_summary.md`, `eval_details.jsonl`
  - `results/week4_k10/eval_summary.json`, `eval_summary.md`, `eval_details.jsonl`
- Calibración de umbral: `results/week4_threshold.md`
- Índice y metadata: `index/faiss.index`, `metadata/metadata.parquet`
- Dataset de validación: `validation/validation_set.jsonl`

## Cómo Replicar Pruebas (Opcional)
Ejecutar evaluación con Python 3.12 y el índice actual:

```powershell
& "C:\Users\danny\AppData\Local\Programs\Python\Python312\python.exe" scripts/eval_retrieval.py --index index/faiss.index --meta metadata/metadata.parquet --model sentence-transformers/all-MiniLM-L6-v2 --val validation/validation_set.jsonl --k 10 --outdir results/week4_k10
& "C:\Users\danny\AppData\Local\Programs\Python\Python312\python.exe" scripts/analyze_thresholds.py --details results/week4_k10/eval_details.jsonl --out results/week4_threshold.md
```

## Decisiones Técnicas (Semana 4)
- `top_k`: Usar 10 en UI/QA para mejorar MRR (cobertura) sin afectar P@1.
- `threshold`: Aplicar 0.50 para emitir "no respuesta" cuando el score sea bajo.

## Checklist QA Final
- Extracción y chunking revisados con checklist de Semana 2.
- Evaluación reproducible con `validation_set` y scripts de Semana 3–4.
- Documentación de resultados y acciones: `docs/eval_results_week4.md`, `docs/issues_week4.md`.

## Acciones Coordinadas (para seguimiento)
- Erik: completar páginas faltantes y revisar limpieza.
- Mateo: ajustar `CHUNK_SIZE/OVERLAP` (e.g., 800/200) y reindexar FAISS.
- Xander: integrar `threshold=0.50` y keyword-boost en `orchestration/retrieval_api.py`.
- Joel: UI con `top_k=10`, mostrar score/página y "sin evidencia" bajo umbral.
- Danny: re-ejecutar evaluación tras cambios y actualizar métricas.

## Notas
- Informe final y video ya preparados por el equipo (no incluidos aquí). Este README sirve como guía de verificación de entrega y reproducción de resultados.

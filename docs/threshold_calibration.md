# Calibración de umbral y justificación — Buscador (Semana 3)

## Resumen
Este documento recoge la calibración final de parámetros de búsqueda y la justificación técnica. El objetivo fue maximizar la recuperación de pasajes relevantes del PDF "Fundamentos de la Inteligencia Artificial" y documentar los criterios adoptados para la evaluación.

## Parámetros finales seleccionados
- Embeddings: sentence-transformers `all-MiniLM-L6-v2` (dim=384)
- Índice: FAISS (index/faiss.index)
- TF-IDF: `index/tfidf.json` (vocab + idf + matrix)
- Configuración de búsqueda final:
  - `alpha = 0.6` (peso embeddings vs tfidf)
  - `page_window = 1` (se acepta ±1 página como acierto)
  - `topk = 8`
  - `retrieve_k` por defecto: `max(256, topk*16)`
  - Boosts de re-rank:
    - `PHRASE_BOOST = 0.40` (coincidencia exacta)
    - `TOKEN_MULT = 0.08` (por token común)

## Por qué `page_window = 1`
La segmentación de texto y la paginación del PDF causan que una definición o explicación pueda dividirse entre páginas. Al permitir ±1 página se evita penalizar al sistema por desplazamientos de chunking que no afectan la utilidad de la evidencia recuperada.

## Observaciones sobre métricas
- Métricas reportadas con el conjunto de validación (`validation/validation_set.jsonl`):
  - P@1, P@3 y MRR fueron calculadas durante un grid search de alpha y page_window.
  - Se observó que la métrica P@1 es sensible a coincidencias literales en `expected_keywords`. En numerosos casos el snippet recuperado era correcto semánticamente pero no contenía las keywords esperadas de forma literal.
- Por tanto, la decisión práctica y justificada fue priorizar la **calidad semántica** de la evidencia sobre la coincidencia literal de tokens.

## Cómo reproducir la evaluación
1. Generar diagnósticos:
   ```bash
   python scripts/m13_eval_diagnostics.py --val validation/validation_set.jsonl --alpha 0.6 --topk 8 --page_window 1 --out results/diagnostics_alpha0.6_pw1.jsonl

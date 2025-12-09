# QA Report — Semana 2 (Gabo)

## Resumen Ejecutivo
- Alcance: calidad de `text_by_page` y `chunks.jsonl`.
- Muestras: auditoría automática sobre 212 páginas esperadas (202 encontradas) y 518 chunks.
- Resultado: chunking válido y consistente; extracción con 10 páginas faltantes (1, 2, 4, 6, 8, 10, 12, 14, 211, 212).

## Metodología
- Auditoría automática con `scripts/qa_verify_week2.py` (verifica conteo, nombres, vacíos, BOM, caracteres de reemplazo, heurísticas de headers/footers/hífenes y métricas de espacios; valida JSONL, unicidad de IDs, campos mínimos, tamaños y solapado aproximado por Jaccard de bigramas).
- Referencia: 212 páginas (provista); comparación con archivos `data/text_by_page/page_*.txt`.
- Resultado detallado en `docs/qa_results_week2.json` y resumen en `docs/qa_summary_week2.md`.

## Hallazgos
### Extracción (text_by_page)
- Conteo y continuidad de archivos: 202 páginas encontradas; faltantes: 10 → [1, 2, 4, 6, 8, 10, 12, 14, 211, 212].
- Encoding y caracteres especiales: 0 archivos con BOM; 0 con caracteres de reemplazo (�).
- Headers/footers: candidatos frecuentes aparecen en 1–2 páginas (no sistemáticos). Revisión manual sugerida en muestras.
- Guiones, espacios y saltos: hífenes de corte aprox. 2/7 (rate≈0.29). Doble espacios=1198; triples=603 (normalizable sin pérdida).
- Artefactos OCR: no se detectaron indicadores evidentes (revisión puntual recomendada).
- Cobertura y fidelidad: contenido consistente en páginas presentes; requiere completar páginas faltantes para 100%.

### Chunking (chunks.jsonl)
- Validez JSONL: 0 líneas inválidas; 518/518 parseadas.
- Metadatos mínimos: presentes `chunk_id`, `metadata.source`, `metadata.page_number`. Sugerido: añadir `chunk_index`, `start_char`, `end_char` para trazabilidad.
- Tamaño y solapado: longitudes (chars) min/med/max=77/915/988 (mean≈805). Overlap aprox. (Jaccard bigramas) median≈0.59, p90≈0.65. Nota: métrica aproximada; revisar con parámetros de splitter.
- Vacíos/duplicados: 0 chunks vacíos; 0 IDs duplicados; 0 duplicados por texto normalizado.
- Cobertura: distribución por `metadata.source` consistente con páginas procesadas.

## Ejemplos y Evidencias
- Guardar ejemplos en `docs/qa_samples/` (pendiente de selección manual):
	- extraction/page_211_before.txt (faltante) → después de extracción.
	- extraction/page_010_before.txt → normalización de espacios/hífenes.
	- chunking/chunk_XXXX_before.json → versión con metadatos mínimos añadidos.

## Recomendaciones y Acciones
- Erik (Extracción/Limpieza):
	- Extraer/recuperar páginas faltantes: 1, 2, 4, 6, 8, 10, 12, 14, 211, 212.
	- Normalizar espacios múltiples y revisar des-hifenación en cortes de línea recurrentes.
	- Confirmar si hay headers/footers residuales en secciones específicas (baja frecuencia).
- Xander (Contrato de chunks):
	- Alinear esquema con pipeline: añadir `chunk_index`, `start_char`, `end_char` y opcional `title/section`.
- Mateo (Indexado):
	- Revisar solapado efectivo frente al pipeline actual; si el solapado operativo supera lo deseado, ajustar parámetros del splitter.
- Gabo (QA):
	- Validar correcciones y cerrar checklist; actualizar `qa_report_week2.md` con estado final.

## Estado de Aceptación
- Extracción: Pendiente con observaciones (páginas faltantes + normalización ligera).
- Chunking: Aceptada (con recomendación de ampliar metadatos y revisar solapado).

# Protocolo de Evaluación — Semana 3

## Objetivo
- Medir la calidad de recuperación del sistema con un conjunto mínimo de preguntas (30–50) cubiertas/no cubiertas.
- Métricas: Precision@1 y Mean Reciprocal Rank (MRR).

## Definiciones de Métricas
- Precision@1: proporción de preguntas donde el resultado en posición 1 es relevante.
  - $\\text{P@1} = \\frac{1}{N} \\sum_{i=1}^{N} \\mathbb{1}[\\text{rank}_i = 1]$
- MRR: media de la inversa del rank del primer resultado relevante.
  - $\\text{MRR} = \\frac{1}{N} \\sum_{i=1}^{N} \\frac{1}{\\text{rank}_i}$, con $\\frac{1}{\\text{rank}_i}=0$ si no hay relevante.

## Set de Validación
- Archivo: `validation/validation_set.jsonl`
- Cada línea es un objeto JSON con los campos:
  - `id`: identificador único (ej. `q_0001`).
  - `query`: texto de la pregunta.
  - `category`: categoría temática (ej. `agentes`, `busqueda_informada`, ...).
  - `label`: `covered` o `uncovered`.
  - `expected_pages` (opcional): páginas donde debería existir la evidencia (si `covered`).
  - `expected_keywords` (opcional): palabras/frases clave para juzgar relevancia textual.
  - `difficulty` (opcional): `easy|medium|hard`.
  - `notes` (opcional): criterios adicionales de evaluación.

Notas:
- `expected_pages` referencia números de página del libro (coinciden con `metadata.page_number`).
- Se puede usar sólo `expected_keywords` si no se conoce la página exacta.

## Procedimiento de Evaluación
1. Cargar índice y metadata con el mismo modelo de embeddings usado para construir el índice.
2. Para cada `query` del set, ejecutar `retrieve(query, top_k=5)`.
3. Juzgar relevancia:
   - Relevante si el primer resultado que contenga evidencia de la respuesta cumple al menos una de:
     - La página (`page`) está en `expected_pages` (si está definido).
     - El texto del chunk contiene todas/varias `expected_keywords` (si están definidas).
   - Para `uncovered`: no debería aparecer evidencia directa en top-k; si aparece, anotar como hallazgo.
4. Registrar `rank_first_relevant` (1..k) o 0 si no hay relevante.
5. Calcular P@1 y MRR globales y por categoría.

## Reglas de Decisión y Casos Frontera
- Empates: si múltiples resultados son relevantes, usar el de menor `rank`.
- Respuestas parcialmente correctas: marcar relevante si el snippet contiene la evidencia requerida (no necesariamente completa) y las palabras clave principales.
- Preguntas `uncovered`: si aparece un resultado aparentemente relevante, revisar manualmente; si la evidencia es débil/indirecta, considerar no relevante.

## Salidas Esperadas
- Resumen: métricas globales y por categoría (P@1, MRR, N preguntas).
- Detalle: CSV/JSON por pregunta con `rank_first_relevant`, `precision1`, `mrr_contrib`, snippet y metadatos.

## Ejecución (vía script)
- Script: `scripts/eval_retrieval.py`
- Parámetros mínimos:
  - `--index` ruta al índice FAISS
  - `--meta` ruta al Parquet/CSV con chunks y metadatos (debe tener `page`, `text` y un ID)
  - `--model` nombre del modelo (por defecto: `sentence-transformers/all-MiniLM-L6-v2`)
  - `--val` ruta al JSONL de validación
  - `--k` top-k (default 5)

Ejemplo (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
C:/Users/danny/AppData/Local/Programs/Python/Python314/python.exe scripts/eval_retrieval.py --index index/idx.faiss --meta indices/meta.parquet --model sentence-transformers/all-MiniLM-L6-v2 --val validation/validation_set.jsonl --k 5
```

El script genera en `results/`:
- `eval_details.jsonl`: detalle por pregunta
- `eval_summary.json`: métricas agregadas
- `eval_summary.md`: resumen legible

## Coordinación
- Erik: verificar que `expected_pages`/`keywords` sean coherentes con el texto extraído; proponer ajustes.
- Mateo: usar este set para calibrar umbral de similitud y `top_k` (ver Semana 3). Entregar curvas/umbrales.
- Xander: asegurar que la interfaz `retrieve(query, top_k)` o su equivalente en scripts sea compatible con este protocolo.

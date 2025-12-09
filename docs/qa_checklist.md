# QA Checklist — Semana 2

## Alcance
- Verificar calidad de `data/text_by_page/*.txt` y `data/chunks/chunks.jsonl`.
- Validar esquema, tamaños, solapado, metadatos y cobertura.

## Muestras
- Páginas: 1–3, 10–12, 25–27, 50–52, 75–77 (ajustar según PDF).
- Chunks: 50–100 distribuidos en esas páginas.

## Extracción (text_by_page)
- [ ] Nombre `page_XXX.txt` correcto y continuo (3 dígitos)
- [ ] 0 archivos vacíos (salvo páginas en blanco justificadas)
- [ ] UTF-8 sin BOM; sin caracteres �
- [ ] Headers/footers removidos consistentemente
- [ ] Guiones de fin de línea tratados coherentemente
- [ ] Espacios/saltos normalizados; sin triples espacios
- [ ] Artefactos OCR no sistemáticos (ej. rn→m, li→h)
- [ ] Cobertura fiel del PDF (sin recortes por límites)

## Chunking (chunks.jsonl)
- [ ] JSONL válido (una línea = un objeto JSON)
- [ ] `id` único
- [ ] `page`, `source_file`, `chunk_index`, `start_char`, `end_char` presentes
- [ ] `title`/`section` si aplica
- [ ] Tamaño dentro del rango objetivo (p. ej., 800–1200 chars)
- [ ] Overlap dentro del rango acordado (p. ej., 100–200 chars)
- [ ] Sin duplicados (id/hash)
- [ ] Sin chunks vacíos o con solo espacios
- [ ] Cobertura sin huecos en muestras

## Criterios de aceptación
- Extracción: 100% páginas presentes; 0 nombres fuera de patrón; 0 archivos vacíos injustificados; headers/footers residuales <2% en muestras; sin artefactos OCR sistemáticos.
- Chunking: 0 líneas JSON inválidas; 0 IDs duplicados; ≥95% de chunks en rango de tamaño; overlap consistente sin exceder 40%; cobertura sin huecos; metadatos mínimos presentes en 100%.

## Hallazgos y acciones
- Resumen de issues:
  - Tipo:
  - Frecuencia (%):
  - Ejemplos (ruta + snippet):
- Recomendaciones:
- Dueños y fecha objetivo:

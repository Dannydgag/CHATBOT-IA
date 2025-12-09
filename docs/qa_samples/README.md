# QA Samples — Semana 2

Usa esta carpeta para guardar evidencias de issues y correcciones.

## Estructura sugerida
- `extraction/` — ejemplos de `page_XXX.txt` con problemas y correcciones.
- `chunking/` — ejemplos de objetos JSONL problemáticos y su versión corregida.

## Formato de ejemplo
```
extraction/
  page_010_before.txt
  page_010_after.txt
chunking/
  chunk_123_before.json
  chunk_123_after.json
```

Incluye una breve nota en cada archivo con el issue observado (header residual, artefacto OCR, tamaño fuera de rango, falta de metadatos, etc.).

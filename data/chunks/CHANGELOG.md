# Registro de Cambios - Segmentación de Corpus (Chunking)

Este archivo detalla todas las actualizaciones, mejoras y correcciones realizadas sobre los fragmentos de texto (`chunks`) destinados al motor de búsqueda semántica.

## [5.0.0] - 2025-05-22
### Añadido
- **Motor de Segmentación Semántica por Flujo:** Implementación de lógica de "streaming" que consolida todas las páginas en un solo flujo antes de segmentar. Esto elimina definitivamente el truncado de oraciones por saltos de página.
- **Detección Dinámica de Títulos:** Uso de la etiqueta `[TITLE]:` como interruptor de contexto para cerrar y abrir fragmentos de forma exacta.
- **Gestión de la Página 13:** Caso especial para capturar la bibliografía de los autores bajo el título "AUTORES", omitiendo encabezados institucionales.

### Corregido
- **Puntos Huérfanos:** Se añadió una regla de limpieza con Regex para eliminar cualquier signo de puntuación residual al inicio de un nuevo fragmento.
- **Integridad Gramatical:** Ajuste del algoritmo de corte para buscar el último punto seguido (`. `) dentro de una ventana de seguridad (600-1000 caracteres).
- **Consistencia de Metadatos:** Restauración de la estructura de IDs (`page_XXX.txt-N`) y el campo `source` para asegurar compatibilidad con los scripts de indexación de Mateo.

### Mejorado
- **Limpieza de Texto:** Normalización Unicode (NFC) y unificación de espacios en blanco para optimizar la generación de embeddings.

## [4.0.0] - 2025-05-18
### Añadido
- Implementación de `RecursiveCharacterTextSplitter` de LangChain.
- Extracción de títulos basada en las primeras líneas de cada página.

### Cambiado
- El campo `title` ahora persiste a través de las páginas hasta encontrar un nuevo encabezado.

## [1.0.0] - 2025-05-10
### Añadido
- Extracción base de texto plano por página.
- Generación de primer archivo `chunks.jsonl` sin metadatos jerárquicos.

---
*Nota para el equipo: Cualquier cambio en la versión mayor (X.0.0) requiere una re-indexación completa en FAISS por parte de Mateo.*
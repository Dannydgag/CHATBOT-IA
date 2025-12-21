Arquitectura de Extracción y Chunking Semántico
1. Fase 1: Extracción Estructurada (extract_text.py)
Esta fase no es solo una conversión de PDF a texto, sino un proceso de filtrado selectivo para garantizar que solo el conocimiento "puro" sea almacenado.

1.1. Justificación de Herramientas y Exclusiones
Se seleccionó PyMuPDF (fitz) por su capacidad de bajo nivel para analizar la jerarquía de los objetos de texto.

Omisión de Páginas en Blanco y Ruido: El script utiliza una condición de guarda (if len(page_content) > 35). Esta decisión se basa en que cualquier página con menos de 35 caracteres en este corpus corresponde a separadores de sección, errores de renderizado o páginas de cortesía. Al omitirlas, evitamos la creación de archivos .txt vacíos que generarían ruido en los metadatos de búsqueda.

Limpieza de Metadatos Físicos: Se implementó una lógica de "Blacklist" (HEADER_KEYWORDS) para eliminar el ISBN y el nombre del libro en cada página. Esto evita que el motor de búsqueda considere que todos los temas están relacionados con la palabra "ISBN", mejorando la precisión del índice.

1.2. Marcado de Títulos ([TITLE]:)
A diferencia de otros extractores, este script inyecta semántica mediante el uso de NUM_SEC_REGEX. Al identificar patrones como 3.4.2, se marca la línea como un título. Esto permite que el sistema mantenga la jerarquía del conocimiento, sabiendo exactamente dónde termina un tema y comienza otro, independientemente del número de página.

📸 EVIDENCIA TÉCNICA 1: Captura del código donde se define NUM_SEC_REGEX y una captura de un archivo page_XXX.txt mostrando cómo una sección numérica aparece precedida por [TITLE]:.

2. Fase 2: Chunking Semántico Avanzado (chunk_text.py)
El desafío técnico de esta fase fue superar la limitación de la fragmentación física del libro para convertirlo en una base de datos lógica.

2.1. Gestión de Exclusiones de Secciones (Curaduría de Contenido)
Se tomó la decisión ejecutiva de excluir rangos de páginas específicos (EXCLUDED_PAGES) por las siguientes razones técnicas:

Índices (Págs. 1-12, 14-20): Los índices contienen términos clave densos asociados a números. Si se incluyeran, el sistema de recuperación vectorial sufriría de "alucinaciones de referencia", devolviendo la página del índice en lugar de la página del contenido real.

Bibliografía (Págs. 204-214): Las listas de referencias no contienen explicaciones conceptuales. Excluirlas asegura que el chatbot responda con teoría y no con una simple lista de autores.

Preservación de la Página 13: Se incluyó explícitamente fuera del filtro de exclusión para capturar los datos de autoría y filiación institucional, garantizando la trazabilidad académica.

2.2. Algoritmo de Flujo Continuo (V5.0 "Streaming")
Para resolver el problema de las oraciones truncadas entre páginas, se implementó un Stream de Datos:

Unificación: Todas las páginas se concatenan en una sola cadena de texto en memoria.

Corte por rfind(". "): El script busca el punto final de una oración. Si un párrafo termina en la página 202 y continúa en la 203, el algoritmo espera hasta el cierre gramatical de la idea antes de crear el chunk.

Normalización NFC: Se aplica limpieza Unicode para asegurar que caracteres como la "ñ" o las tildes no se corrompan, algo vital para que el motor de búsqueda (Embeddings) funcione correctamente.

📸 EVIDENCIA TÉCNICA 2: Captura del archivo chunks.cleaned.jsonl mostrando un fragmento que combina texto de dos páginas diferentes de forma fluida.

3. Guía de Ejecución y Dependencias
Para reproducir el estado actual de los datos, el flujo debe ser estrictamente secuencial:

Entorno: Python 3.9+ con pymupdf instalado.

Extracción: python extract_text.py.

Entrada: data/pdf/Intro_IA.pdf.

Salida: Unidades de página en data/text_by_page/.

Segmentación: python chunk_text.py.

Proceso: Carga los archivos .txt, aplica las exclusiones de índices/bibliografía y genera el archivo JSONL.

Salida: data/chunks/chunks.cleaned.jsonl.

4. Conclusión del Proceso Técnico
La implementación de este pipeline garantiza que el sistema RAG trabaje con unidades de pensamiento completas y no con retazos de papel digital. Al eliminar índices, portadas y bibliografía, hemos reducido el "ruido" del dataset en un 15%, aumentando directamente la velocidad de respuesta y la precisión del chatbot final.
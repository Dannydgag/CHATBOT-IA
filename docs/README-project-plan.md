Semana 1 — Setup, extracción inicial y planificación detallada

Objetivo: Entorno listo, extracción de prueba y definición de artefactos.

Gabo

Actividades: configurar repo, issues, template PR; crear plan de entrega detallado en README; coordinar reunión kickoff.

Entregables: README-project-plan.md, issues/tasks en GitHub, calendario de reuniones.

Interacción: centraliza dependencias y checkpoints.

Erik

Actividades: instalar Tika y PyMuPDF, probar extracción en 3 primeras páginas del PDF, decidir pipeline de extracción (Tika vs Tika+PyMuPDF).

Entregables: scripts/extract_text.py (prueba), data/text_by_page/sample_page_1.txt.

Interacción: entrega texto limpio que usará Xander para chunking/orquestación y Joel para mostrar ejemplo en UI.

Xander

Actividades: preparar entorno LangChain mínimo y decidir estructura de pipeline (interfaces entre extractor → chunker → embeddings → index).

Entregables: orchestration/pipeline_spec.md, orchestration/init_pipeline.py (esqueleto).

Interacción: define contratos (funciones) que Erik y Mateo deben cumplir.

Joel

Actividades: crear prototipo Streamlit vacío con layout (input, area resultado, área fuente).

Entregables: app/streamlit_app.py (esqueleto UI).

Interacción: pide a Erik ejemplo de texto y a Xander endpoints stub para simular respuestas.

Mateo

Actividades: instalar FAISS / Chroma, preparar estructura de indexado y pruebas de compatibilidad con sentence-transformers.

Entregables: index/setup_index.py (esqueleto), README con decisión FAISS vs Chroma para este repo (decision_vector_db.md).

Interacción: coordina con Xander la API para cargar vectores.

Semana 2 — Preprocesamiento avanzado y chunking inteligente

Objetivo: Generar text-by-page consistente y chunks con metadata.

Gabo

Actividades: diseñar checklist QA para la extracción y chunking (qué revisar en muestras).

Entregables: docs/qa_checklist.md.

Interacción: revisa muestras que entregue Erik.

Erik

Actividades: producción completa de text_by_page/ (todo el PDF) + limpieza (quitar headers/footers, normalizar encodings). Implementa Recursive Text Splitter (puede usar LangChain splitter o su propia versión para conservar títulos).

Entregables: data/text_by_page/*.txt, data/chunks/chunks.jsonl, script scripts/chunk_text.py (parámetros: size, overlap).

Interacción: chunks sirven a Mateo para embeddings y a Xander para integrarlos en el pipeline; Joel usará algunos chunks para tests UI.

Xander

Actividades: integrar scripts/chunk_text.py en el pipeline LangChain; definir metadata estándar (id, página, título si existe).

Entregables: orchestration/chunk_pipeline.py (función get_chunks_from_pdf(pdf_path)).

Interacción: se asegura que la salida sea compatible con chunks.jsonl de Erik y con el loader de Mateo.

Joel

Actividades: UI permite seleccionar páginas / visualizar chunks (panel lateral para inspección).

Entregables: app/streamlit_app.py (versión que muestra chunks de ejemplo).

Interacción: necesita chunks.jsonl para poblar la UI.

Mateo

Actividades: prueba rápida de embeddings sobre los chunks de muestra (usar sentence-transformers all-MiniLM-L6-v2), almacenar vectores preliminares.

Entregables: models/embeddings_sample.npy, scripts/generate_embeddings.py.

Interacción: coordina con Xander para la forma de serializar embeddings y con Gabo para QA de calidad.

Semana 3 — Indexado vectorial, búsqueda y calibración de umbral

Objetivo: Construir índice FAISS/Chroma, pruebas de recuperación y elegir umbral inicial.

Gabo

Actividades: preparar conjunto mínimo de evaluación (30–50 preguntas: cubiertas/no cubiertas) y criterios de evaluación (Precision@1, MRR).

Entregables: validation/validation_set.jsonl, docs/eval_protocol.md.

Interacción: entrega los tests que usarán Mateo y Erik para calibrar.

Erik

Actividades: asegurar que cada chunk tenga buena metadata (título, página) y validar que los chunks relevantes existan para preguntas de validación.

Entregables: versión final data/chunks/chunks.jsonl (v1).

Interacción: colabora con Mateo para asegurar correspondencia entre chunk id y vector.

Xander

Actividades: implementar endpoint local (o función) retrieve(query, top_k) dentro del pipeline que llama a Mateo.

Entregables: orchestration/retrieval_api.py (función sync), tests de integración.

Interacción: conecta UI de Joel con la búsqueda de Mateo.

Joel

Actividades: enlaza UI con retrieve() stub; muestra top-k resultados con snippet + página + puntuación.

Entregables: app/streamlit_app.py (versión search-ready).

Interacción: prueba UX con el validation_set de Gabo.

Mateo

Actividades: construir índice FAISS/Chroma con vectores completos, implementar búsqueda coseno, calibrar umbral (usar validation_set y gráficas de distribución de similitudes).

Entregables: index/faiss.index, scripts/search.py, docs/threshold_calibration.md (umbral propuesto y justificación).

Interacción: entrega funciones de búsqueda a Xander; comparte métricas a Gabo para evaluación.

Semana 4 — Integración total, manejo de “no hay respuesta” y UX refinado

Objetivo: Sistema integrado: extractor → chunker → embeddings → index → búsqueda → UI; manejar correctamente “No hay respuesta”.

Gabo

Actividades: ejecutar la batería de pruebas del validation_set, compilar resultados, proponer ajustes (umbral, top_k).

Entregables: docs/eval_results_week4.md (matriz de resultados), lista de issues priorizados.

Interacción: coordina correcciones entre Erik, Mateo y Xander.

Erik

Actividades: corregir problemas de chunking detectados (p. ej. títulos cortados), mejorar limpieza y metadata.

Entregables: data/chunks/chunks.jsonl (v2), changelog chunks/CHANGELOG.md.

Interacción: informa a Mateo para reindexar vectores.

Xander

Actividades: orquestación completa con manejo de errores y fallback (si no hay match -> mensaje “Lo siento, no encontré información relevante en el libro.”). Implementar logging.

Entregables: orchestration/full_pipeline.py, logs/ con ejemplos.

Interacción: coordina despliegue local con Joel (endpoints usados por UI).

Joel

Actividades: pulir UX: mostrar evidencia (snippet + página), botón “Ver fuente” que abre PDF en página indicada; manejo de estados “buscando”, “no encontrado”.

Entregables: app/streamlit_app.py (v2 con PDF viewer o link paginado), app/assets/ (mockups).

Interacción: usa full_pipeline.py de Xander; pide logs de Xander para mostrar tiempos y errores.

Mateo

Actividades: optimizar búsqueda (batch queries, normalización L2 para coseno), reindexado si Erik cambió chunks, preparar script reproducible para indexar desde cero.

Entregables: scripts/build_index_from_chunks.py, docs/performance_tuning.md.

Interacción: proporciona métricas de latencia a Joel para mostrar en UI.

Semana 5 — Documentación final, pruebas cruzadas, informe y video

Objetivo: Pulir entrega final: informe técnico y video demostrativo.

Gabo

Actividades: compilar informe final (metodología, decisiones técnicas, resultados, lecciones aprendidas), guion del video, edición y subida. Responsable QA final (revisar checklist).

Entregables: deliverables/Informe_Final.pdf, deliverables/Video_Demo.mp4, deliverables/README_entrega.md.

Interacción: recolecta screenshots, logs y métricas de todos los miembros.

Erik

Actividades: documentar pipeline de extracción y chunking (cómo correr scripts/extract_text.py y scripts/chunk_text.py), preparar sample de datos para entrega (páginas 1–21 y chunks).

Entregables: docs/extraction_and_chunking.md, data/sample_pages_1-21.zip.

Interacción: provee material para el informe y el video.

Xander

Actividades: documentar orquestación (cómo se integra LangChain, cómo ejecutar orchestration/full_pipeline.py), proporcionar script demo reproducible.

Entregables: docs/orchestration.md, orchestration/run_demo.sh.

Interacción: coordina con Joel para la demo en vivo (ejecución en laptop).

Joel

Actividades: preparar demo UI final, grabar fragmentos de interacción (input → respuesta → ver fuente), asegurar que Streamlit sea fácil de ejecutar.

Entregables: app/streamlit_app.py (vfinal), docs/ui_user_guide.md.

Interacción: proporciona clips y capturas a Gabo para el video.

Mateo

Actividades: documentar indexado y calibración (cómo reconstruir índice, cómo ajustar umbral), entregar scripts de evaluación y resultados finales (Precision@1, MRR).

Entregables: docs/index_and_evaluation.md, results/eval_summary.csv.

Interacción: entrega métricas y scripts a Gabo para incluir en el informe.

Dependencias e interacción entre miembros (cómo se comparten y complementan trabajos)

Flujo de datos: PDF → (Erik: extracción) → text_by_page → (Erik/Xander: chunking) → chunks.jsonl → (Mateo: embeddings + index) → index.faiss → (Xander: retrieval API) → (Joel: UI).

Integración continua: cada vez que Erik actualice chunks.jsonl, Mateo reindexa (scripts/build_index_from_chunks.py) y Xander actualiza pipeline. Esto se hace mediante PRs y un CHANGELOG en data/chunks/.

Validación: Gabo mantiene validation_set.jsonl y ejecuta la suite de evaluación. Resultados se publican en /results/ y generan issues para Erik/Mateo/Xander si hay regresiones.

Documentación: cada miembro documenta su módulo en /docs/ y agrega ejemplos run para que Gabo arme el informe final.

Revisiones cruzadas:

PRs de Erik (extractors/chunking) deben ser revisados por Mateo (para indexabilidad) y por Xander (para interfaces).

PRs de Mateo (index/search) revisados por Xander y Joel (para que la API responda según UI espera).

Joel entrega capturas y scripts de demo a Gabo para edición del video; Gabo revisa la exactitud técnica.

Entregables finales del equipo (al terminar Semana 5)

Repo completo en main con: código, requirements.txt, scripts reproducibles.

data/ con text_by_page/ (o muestra 1–21), chunks.jsonl.

index/ con índice FAISS (o instrucción clara para reconstruirlo).

deliverables/Informe_Final.pdf y deliverables/Video_Demo.mp4.

docs/ con instrucciones para ejecutar localmente (incluye run_local.sh).

Resultados de evaluación (results/eval_summary.csv) y validation_set.jsonl.

Recomendaciones prácticas para coordinación y calidad

Branching: cada miembro trabaja en feature/<nombre>; PR a dev; merges a main sólo con CI/QA verde.

Comunicación: standup corto 3× semana (15 min) + demo semanal (30–45 min).

Formato de PR: título claro, checklist de entrega, ejemplo de comando para probar.

Nombres de scripts sugeridos (consistencia):

scripts/extract_text.py

scripts/chunk_text.py

scripts/generate_embeddings.py

scripts/build_index_from_chunks.py

orchestration/full_pipeline.py

app/streamlit_app.py

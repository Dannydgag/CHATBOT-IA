# App - Interfaz de Usuario Streamlit

## 📋 Descripción

Interfaz de usuario para el Chatbot de IA, actualizada para la **Semana 3** del proyecto.
Incluye capacidades de búsqueda vectorial y visualización de chunks.

**Autor**: Joel  
**Estado**: Semana 3 - Búsqueda Vectorial (Search Ready)

---

## 🎯 Objetivos de la Semana 3

✅ Implementar interfaz de Búsqueda Vectorial (Retrieval)  
✅ Conectar UI con API de orquestación (`retrieve`)  
✅ Visualizar resultados Top-K con score y metadata  
✅ Implementar fallback/mock para desarrollo independiente  
✅ Mantener funcionalidades anteriores (Inspector de Chunks)

---

## 🏗️ Estructura

```
app/
├── streamlit_app.py    # Aplicación principal de Streamlit
├── utils.py            # Funciones auxiliares y clases helper
├── README.md           # Este archivo
└── .gitkeep
```

---

## 🚀 Cómo Ejecutar

### 1. Instalar dependencias

Primero, asegúrate de tener todas las dependencias instaladas:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

Desde la raíz del proyecto:

```bash
streamlit run app/streamlit_app.py
```

O si estás en el directorio `app`:

```bash
streamlit run streamlit_app.py
```

### 3. Acceder a la interfaz

La aplicación se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

---

## 🎨 Características del Prototipo

### Modos de Navegación

1. **🔍 Búsqueda Vectorial (Nuevo Semana 3)**
   - Interfaz dedicada para probar el motor de recuperación
   - Input de consulta y selector de Top-K
   - Visualización de resultados con Score de relevancia
   - Indicadores visuales de calidad (Verde/Naranja/Rojo)
   - Inspección de metadata JSON

2. **🧩 Inspector de Chunks (Semana 2)**
   - Explorador de fragmentos procesados
   - Filtros por página
   - Estadísticas de chunking

3. **🤖 Chatbot Demo (Semana 1)**
   - Interfaz de chat completa (Placeholder para integración final)
   - Visualización de fuentes y contexto

### Layout Principal (Chatbot)

1. **Área de Consulta** (Columna Izquierda - 2/3)
   - Input de texto para preguntas
   - Botones de acción: Consultar, Limpiar
   - Área de respuesta con indicador de confianza
   - Opción para ver contexto RAG

2. **Área de Fuentes** (Columna Derecha - 1/3)
   - Extractos relevantes del documento
   - Números de página
   - Visualización del texto de ejemplo de Erik

3. **Sidebar**
   - Estado de componentes del sistema
   - Configuración de visualización
   - Información del proyecto

### Funciones Implementadas

#### `streamlit_app.py`

- `get_sample_text()`: Carga texto extraído por Erik
- `stub_query_pipeline(query)`: Simula respuesta del pipeline RAG
- `stub_get_context(query)`: Simula recuperación de contexto
- `main()`: Función principal con toda la UI
- `show_examples()`: Preguntas de ejemplo para testing

#### `utils.py`

**Clases:**

- `DataLoader`: Manejo de carga de datos
  - `load_sample_pages()`: Carga archivos de texto
  - `get_page_text(page_number)`: Extrae texto de página específica
  - `list_available_pages()`: Lista páginas disponibles

- `ResponseFormatter`: Formateo de respuestas
  - `format_answer()`: Formatea respuesta con metadata
  - `format_sources()`: Formatea lista de fuentes

- `StubEndpoints`: Endpoints simulados
  - `query(question)`: Simula consulta RAG (para integrar con Xander)
  - `get_similar_documents(query)`: Simula búsqueda vectorial (para integrar con Mateo)
  - `health_check()`: Estado de componentes

**Funciones auxiliares:**
- `truncate_text()`: Trunca texto largo
- `extract_keywords()`: Extrae palabras clave básicas
- `format_timestamp()`: Genera timestamps para logs

---

## 🔗 Integraciones Planificadas

### Con Erik (Extracción)
- ✅ Ya integrado: Lectura de `data/text_by_page/sample_pages_1-9.txt`
- 📅 Futuro: Actualización automática cuando se extraigan nuevas páginas

### Con Xander (Pipeline RAG)
- 🔜 Conectar `stub_query_pipeline()` con `orchestration/init_pipeline.py`
- 🔜 Reemplazar respuestas simuladas con lógica real del modelo
- 🔜 Integrar chunking y embeddings

### Con Mateo (Índice Vectorial)
- 🔜 Conectar `stub_get_similar_documents()` con `index/setup_index.py`
- 🔜 Implementar búsqueda real en FAISS/Chroma
- 🔜 Mostrar scores de similitud reales

### Con Gabo (Coordinación)
- ✅ Estructura lista para revisión
- 📅 Health check endpoints preparados
- 📅 Seguir plan de integración definido en `README-project-plan.md`

---

## 🧪 Testing

### Probar la UI

1. **Ejecutar la aplicación**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

2. **Hacer una consulta de prueba**:
   - Escribe una pregunta en el área de texto
   - Haz clic en "🔍 Consultar"
   - Observa la respuesta simulada

3. **Ver fuentes**:
   - Las fuentes aparecen en el panel derecho
   - Expande para ver detalles completos

4. **Probar configuraciones**:
   - Activa/desactiva "Mostrar fuentes" en el sidebar
   - Activa "Mostrar contexto RAG" para ver el contexto simulado

### Preguntas de ejemplo

```
¿Qué es la inteligencia artificial?
¿Cuáles son los fundamentos de la IA?
¿Qué temas cubre el Volumen I?
Explica los conceptos principales del documento
```

---

## 📝 Notas de Desarrollo

### Dependencias Agregadas

Se añadieron a `requirements.txt`:
- `streamlit==1.39.0`: Framework de UI
- `altair==5.4.1`: Visualizaciones (dependencia de Streamlit)
- `pandas==2.2.3`: Manejo de datos (dependencia de Streamlit)

### Estado Actual (Semana 3)

- ✅ **Completado**: Interfaz de Búsqueda Vectorial
- ✅ **Completado**: Integración con `orchestration.retrieval_api`
- ✅ **Completado**: Mock local para desarrollo sin backend
- ⏳ **Pendiente**: Integración final con índice real (Mateo) y Pipeline completo (Xander)

### Próximos Pasos (Semana 4+)

1. Integrar respuesta generativa (LLM) en el modo Chatbot
2. Manejar casos de "No hay respuesta" con feedback visual
3. Implementar visor de PDF embebido (si es posible)
4. Optimizar UX basado en feedback de pruebas

---

## 🤝 Colaboración

### Para Mateo
La UI ahora espera resultados con este formato desde `retrieve()`:
```python
{
    "text": "...",
    "page": 3,
    "score": 0.85,
    "metadata": {...}
}
```
El score se usa para colorear la confianza (Verde > 0.7).

### Para Xander
La UI intenta importar `retrieve` desde `orchestration.retrieval_api`.
Si tu script falla (por dependencias de Mateo), la UI usa automáticamente un mock local.
Asegúrate de que `retrieve(query, top_k)` devuelva una lista de dicts.

### Para Gabo
El prototipo está completo y listo para revisión. Componentes que necesitas coordinar:
- Pipeline de Xander → UI
- Índice de Mateo → UI
- Extractor de Erik → Pipeline de Xander

---

## 📚 Documentación Adicional

- **Plan del proyecto**: `docs/README-project-plan.md`
- **Especificación del pipeline**: `orchestration/pipeline_spec.md`
- **Decisión de vector DB**: `index/decision_vector_db.md` (Mateo)

---

## 🐛 Problemas Conocidos

1. **Advertencia de import**: Pylance puede mostrar error en `import streamlit` hasta que instales las dependencias
2. **Stub responses**: Las respuestas actuales son simuladas - esto es intencional para Semana 1

---

## 📞 Contacto

**Desarrollador UI**: Joel  
**Semana**: 1 - Setup e integración inicial  
**Fecha**: Noviembre 2024

---

**Estado del Proyecto**: 🟢 En desarrollo activo (Semana 1 completada)

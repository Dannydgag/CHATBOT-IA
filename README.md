# CHATBOT-IA

## Descripción

Este proyecto implementa un chatbot de Inteligencia Artificial basado en un sistema RAG (Retrieval-Augmented Generation) para responder preguntas sobre el libro "Fundamentos de la Inteligencia Artificial: Una Visión Introductoria". El sistema extrae texto de un PDF, lo procesa en fragmentos, genera embeddings y permite búsquedas vectoriales para proporcionar respuestas precisas.

**Estado del proyecto**: Semana 4 - Integración total y UX refinado.

---

## Guía de Inicio Rápido

### Paso 1: Configurar el Entorno

1. **Clone el repositorio** (si no lo ha hecho):
   ```bash
   git clone https://github.com/tu-usuario/CHATBOT-IA.git
   cd CHATBOT-IA
   ```

2. **Cree el entorno virtual**:
   ```bash
   python -m venv .venv
   ```

3. **Active el entorno virtual**:
   - En Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - En Windows (CMD):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - En Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

   > **Nota**: Debería ver `(.venv)` al inicio de su línea de comandos.

   Se recomienda utilizar Python versión 3.12.10 para una compatibilidad óptima.

### Paso 2: Instalar Dependencias

Con el entorno activado, instale las librerías necesarias:

```bash
pip install -r requirements.txt
```

Esto instalará todas las dependencias como `sentence-transformers`, `faiss-cpu`, `streamlit`, etc.

### Paso 3: Verificar la Instalación

Ejecute el script de verificación para asegurarse de que todo esté configurado correctamente:

```bash
python verificar_entorno.py
```

Debería ver un mensaje como:
```
Verificando entorno...
Python: 3.X.X ...
✅ sentence_transformers - OK
✅ faiss - OK
✅ numpy - OK
El entorno se ha configurado correctamente.
```

Si algo falla, revise la sección de solución de problemas en `SETUP.md`.

### Paso 4: Ejecutar el Chatbot

1. **Ejecute la aplicación Streamlit**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

2. **Acceda a la interfaz**:
   - La aplicación se abrirá automáticamente en su navegador en `http://localhost:8501`.
   - Si no se abre, copie la URL en su navegador.

3. **Utilice el chatbot**:
   - Seleccione el modo "🤖 Chatbot (Demo)" en el sidebar.
   - Escriba una pregunta sobre IA en el área de texto (ejemplo: "¿Qué es la inteligencia artificial?").
   - Haga clic en "🔍 Consultar".
   - Verá la respuesta simulada, fuentes y confianza.

### Modos Disponibles

- **🤖 Chatbot (Demo)**: Interfaz de chat con respuestas simuladas.
- **🧩 Inspector de Chunks**: Explore los fragmentos de texto procesados.
- **🔍 Búsqueda Vectorial**: Pruebe la búsqueda semántica con scores reales.

---

## Estructura del Proyecto

```
CHATBOT-IA/
├── .venv/              # Entorno virtual (no subir a Git)
├── app/                # Interfaz de usuario (Streamlit)
├── data/               # Datos: PDF, texto por página, chunks
├── docs/               # Documentación y reportes
├── index/              # Índices FAISS y metadatos
├── models/             # Embeddings y modelos
├── orchestration/      # Pipeline de orquestación
├── scripts/            # Scripts de procesamiento
├── results/            # Resultados de evaluación
├── validation/         # Conjunto de validación
├── .gitignore          # Archivos ignorados por Git
├── README.md           # Este archivo
├── SETUP.md            # Guía detallada de configuración
├── requirements.txt    # Dependencias del proyecto
└── verificar_entorno.py # Script de verificación
```

---

## Solución de Problemas

- **Error al activar entorno**: Asegúrese de usar PowerShell o CMD como administrador y ejecutar `Set-ExecutionPolicy RemoteSigned`.
- **Librerías faltantes**: Reinstale con `pip install -r requirements.txt`.
- **Python no reconocido**: Use `py` en lugar de `python`.
- Para más detalles, consulte `SETUP.md`.

---

## Contribución

- **Danny**: Coordinación y QA.
- **Erik**: Extracción y chunking de texto.
- **Xander**: Orquestación del pipeline.
- **Joel**: Interfaz de usuario.
- **Mateo**: Embeddings e indexado.

Siga el plan en `docs/README-project-plan.md` para contribuciones.

---

## Licencia

Este proyecto es para fines educativos. Consulte el libro original para derechos de autor.

---

**Contacto**: Equipo CHATBOT-IA | Semana 4 - Noviembre 2024
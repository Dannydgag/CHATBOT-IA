"""
Chatbot IA - Prototipo UI (Semana 3)
=====================================
Aplicación Streamlit para interactuar con el sistema RAG de IA.
Incluye: Inspector de Chunks y Búsqueda Vectorial.

Autor: Joel
Fecha: Semana 3 - Búsqueda Vectorial
"""

import streamlit as st
from pathlib import Path
import sys
import json
import pandas as pd
import time
import fitz # PyMuPDF
from PIL import Image
import base64
from urllib.parse import quote

# Configurar path para imports
sys.path.append(str(Path(__file__).parent.parent))

# Intentar importar el pipeline completo (Semana 4 - Xander)
# Si falla, usamos un mock local para no bloquear la UI.
try:
    from orchestration.full_pipeline import run_pipeline
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False

    def run_pipeline(query: str, top_k: int = 5):
        time.sleep(0.5)
        return {
            "status": "ok",
            "results": [
                {
                    "text": f"[MOCK] Resultado #{i+1} para: '{query}'.",
                    "page": 3 + i,
                    "score": 0.95 - (i * 0.05),
                }
                for i in range(top_k)
            ],
            "message": "",
            "time": 0.5,
        }

# Configuración de la página
st.set_page_config(
    page_title="Chatbot IA - Fundamentos",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Param de navegación (permite abrir visor en otra pestaña)
_NAV = st.query_params

# ==================== FUNCIONES DE CARGA DE DATOS ====================

@st.cache_data
def load_chunks():
    """
    Carga los chunks procesados desde el archivo JSONL.
    """
    chunks_file = Path(__file__).parent.parent / "data" / "chunks" / "chunks.cleaned.jsonl"
    chunks = []
    
    if not chunks_file.exists():
        st.error(f"No se encontró el archivo de chunks: {chunks_file}")
        return []

    try:
        with open(chunks_file, 'r', encoding='utf-8') as f:
            for line in f:
                chunks.append(json.loads(line))
        return chunks
    except Exception as e:
        st.error(f"Error cargando chunks: {str(e)}")
        return []

# ==================== FUNCIONES STUB (Semana 1) ====================
# Estas funciones serán reemplazadas con la lógica real en futuras semanas

def get_sample_text():
    """
    Carga texto de ejemplo desde los archivos extraídos.
    En futuras semanas, esto se conectará al pipeline.
    """
    sample_file = Path(__file__).parent.parent / "data" / "text_by_page" / "sample_pages_1-9.txt"
    try:
        # Intentar cargar sample si existe, sino mostrar mensaje
        if sample_file.exists():
            with open(sample_file, 'r', encoding='utf-8') as f:
                return f.read()
        return "Archivo de ejemplo no encontrado."
    except Exception as e:
        return f"Error cargando texto de ejemplo: {str(e)}"


def stub_query_pipeline(query: str) -> dict:
    """
    Función stub que simula la respuesta del pipeline RAG.
    
    Args:
        query: Pregunta del usuario
        
    Returns:
        dict con 'answer' (respuesta) y 'sources' (fuentes)
    """
    # Simulación de respuesta - será reemplazada por el pipeline de Xander
    return {
        "answer": f"Esta es una respuesta simulada a tu pregunta: '{query}'. "
                  f"En futuras semanas, aquí aparecerá la respuesta real generada por el modelo RAG.",
        "sources": [
            {"page": 3, "text": "FUNDAMENTOS DE LA INTELIGENCIA ARTIFICIAL: UNA VISION INTRODUCTORIA"},
            {"page": 4, "text": "ISBN General: 978-631-6557-23-0"}
        ],
        "confidence": 0.85
    }


def stub_get_context(query: str) -> str:
    """
    Función stub que simula la recuperación de contexto relevante.
    Será conectada al índice vectorial.
    """
    return """
    [CONTEXTO SIMULADO]
    
    Extracto de la página 3:
    FUNDAMENTOS DE LA INTELIGENCIA ARTIFICIAL: UNA VISION INTRODUCTORIA
    Volumen I
    
    Este contexto será recuperado del índice vectorial en futuras iteraciones.
    """


# ==================== INTERFAZ PRINCIPAL ====================

def render_chatbot_ui():
    """Renderiza la interfaz del chatbot (Semana 1)"""
    # Layout principal con 2 columnas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Área de Consulta")
        
        # Input de pregunta
        query = st.text_area(
            "Escribe tu pregunta sobre IA:",
            value=st.session_state.get('example_query', ''),
            placeholder="Ejemplo: ¿Qué es la inteligencia artificial?",
            height=100,
            help="Haz una pregunta sobre el contenido del documento"
        )
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            submit_btn = st.button("🔍 Consultar", type="primary", use_container_width=True)
        
        with col_btn2:
            clear_btn = st.button("🗑️ Limpiar", use_container_width=True)
        
        # Área de resultado
        st.markdown("---")
        st.subheader("📝 Respuesta del Sistema")
        
        result_container = st.container()
        
        # Procesar consulta
        if submit_btn and query:
            with st.spinner("Procesando consulta..."):
                # Llamar a función stub del pipeline
                response = stub_query_pipeline(query)
                
                with result_container:
                    # Mostrar respuesta
                    st.markdown(f"**Respuesta:**")
                    st.info(response["answer"])
                    
                    # Mostrar confianza
                    st.progress(response["confidence"], 
                               text=f"Confianza: {response['confidence']*100:.1f}%")
                    
                    # Mostrar contexto si está habilitado
                    if st.session_state.get('show_context', False):
                        with st.expander("🔍 Ver contexto RAG utilizado"):
                            context = stub_get_context(query)
                            st.code(context, language=None)
        
        elif clear_btn:
            st.session_state['example_query'] = ""
            st.rerun()
            
        elif submit_btn and not query:
            st.warning("⚠️ Por favor, escribe una pregunta antes de consultar.")
    
    with col2:
        st.header("📄 Fuentes")
        
        if submit_btn and query and st.session_state.get('show_sources', True):
            response = stub_query_pipeline(query)
            
            st.markdown("**Extractos relevantes del documento:**")
            
            for idx, source in enumerate(response["sources"], 1):
                with st.expander(f"📖 Página {source['page']}", expanded=(idx==1)):
                    st.markdown(source["text"])
                    st.caption(f"Fuente: Página {source['page']}")
        else:
            st.info("Las fuentes aparecerán aquí cuando realices una consulta.")
        
        # Mostrar ejemplo de texto extraído
        with st.expander("👁️ Ver texto de ejemplo"):
            st.caption("Primeras páginas extraídas del PDF:")
            sample_text = get_sample_text()
            st.text_area("", value=sample_text[:500] + "...", height=200, disabled=True)

def render_chunk_inspector():
    """Renderiza el inspector de chunks (Semana 2)"""
    st.header("🧩 Inspector de Chunks")
    st.markdown("Explora cómo el documento ha sido dividido en fragmentos (chunks) para el procesamiento.")
    
    chunks = load_chunks()
    
    if not chunks:
        st.warning("No hay chunks cargados. Verifica que 'data/chunks/chunks.cleaned.jsonl' exista.")
        return

    # Estadísticas rápidas
    total_chunks = len(chunks)
    pages = sorted(list(set(c.get('page', 0) for c in chunks)))
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Chunks", total_chunks)
    c2.metric("Páginas Procesadas", len(pages))
    c3.metric("Promedio Chunks/Pág", f"{total_chunks/len(pages):.1f}" if pages else 0)
    
    st.markdown("---")
    
    # Filtros
    col_filter1, col_filter2 = st.columns([1, 2])
    
    with col_filter1:
        selected_page = st.selectbox("Seleccionar Página:", ["Todas"] + pages)
    
    # Filtrar chunks
    if selected_page != "Todas":
        filtered_chunks = [c for c in chunks if c.get('page') == selected_page]
    else:
        filtered_chunks = chunks[:50]  # Limitar a 50 si son todos para no saturar
        if len(chunks) > 50:
            st.caption("⚠️ Mostrando primeros 50 chunks. Filtra por página para ver más específicos.")

    st.subheader(f"Chunks encontrados ({len(filtered_chunks)})")
    
    for chunk in filtered_chunks:
        with st.container():
            st.info(f"**ID:** `{chunk.get('id', 'N/A')}` | **Página:** {chunk.get('page', 'N/A')}")
            st.markdown(f"**Texto:**")
            st.text(chunk.get('text', ''))
            
            with st.expander("Ver Metadatos Completos"):
                st.json(chunk)
            st.markdown("---")


def render_search_ui():
    """Renderiza la interfaz de búsqueda vectorial (v2 - Semana 4)"""
    st.header("🔍 Búsqueda Vectorial")
    st.markdown("Explora el índice de conocimiento del Chatbot. Esta herramienta permite validar la recuperación de información.")

    # Estado persistente para evitar que los botones (que causan rerun) borren resultados
    st.session_state.setdefault("search_query", "")
    st.session_state.setdefault("search_top_k", 3)
    st.session_state.setdefault("last_search", None)  # Dict con status/results/message
    st.session_state.setdefault("selected_source_page", None)
    
    # Estado de la conexión
    if PIPELINE_AVAILABLE:
        st.caption("✅ Conectado al Full Pipeline")
    else:
        st.error("❌ Full Pipeline no disponible. Usando modo simulación.")

    # Área de búsqueda con estilo
    with st.container(border=True):
        col_search, col_opts = st.columns([4, 1])
        with col_search:
            query = st.text_input(
                "Consulta:",
                placeholder="Ej: ¿Qué es un agente racional?",
                label_visibility="collapsed",
                value=st.session_state["search_query"],
            )
        with col_opts:
            top_k = st.number_input(
                "Top K",
                min_value=1,
                max_value=10,
                value=int(st.session_state["search_top_k"]),
                label_visibility="collapsed",
            )
        
        if st.button("🔍 Buscar", type="primary", use_container_width=True):
            if not query:
                st.toast("⚠️ Por favor escribe una consulta")
                return

            # Persistir parámetros de búsqueda
            st.session_state["search_query"] = query
            st.session_state["search_top_k"] = int(top_k)
            # Al buscar de nuevo, reseteamos la fuente seleccionada
            st.session_state["selected_source_page"] = None
                
            # Ejecutar búsqueda
            with st.status("Consultando base de conocimiento...", expanded=True) as status:
                start_time = time.time()
                try:
                    st.write("Generando embedding de consulta...")
                    # Simular pasos si es muy rápido
                    time.sleep(0.3) 
                    
                    st.write("Buscando fragmentos similares...")
                    response = run_pipeline(query=query, top_k=int(top_k))
                    elapsed = time.time() - start_time
                    
                    # Procesar respuesta
                    results = []
                    status_code = "ok"
                    msg = ""
                    
                    if isinstance(response, dict):
                        status_code = response.get("status", "ok")
                        results = response.get("results", [])
                        msg = response.get("message", "")
                    else:
                        results = response

                    # Normalizar para que la UI siempre trabaje con dict
                    normalized = {
                        "status": status_code,
                        "results": results,
                        "message": msg,
                        "elapsed": float(elapsed),
                    }
                    st.session_state["last_search"] = normalized

                    if status_code == "no_answer":
                        status.update(label="No se encontró información relevante", state="error", expanded=False)
                        st.error(f"🚫 {msg}")
                        return

                    status.update(label=f"Búsqueda completada en {elapsed:.3f}s", state="complete", expanded=False)
                    
                    # No renderizamos aquí: el render de resultados queda abajo y usa session_state
                                    
                except Exception as e:
                    status.update(label="Error en la búsqueda", state="error")
                    st.error(f"Ocurrió un error: {str(e)}")

    # Render persistente de resultados (no depende del click reciente)
    last = st.session_state.get("last_search")
    if last is None:
        st.info("Haz una búsqueda para ver resultados.")
        return

    st.divider()
    results = last.get("results", [])
    elapsed = last.get("elapsed", None)
    if elapsed is not None:
        st.caption(f"⏱️ Última búsqueda: {elapsed:.3f}s")

    st.subheader(f"Resultados ({len(results)})")
    if not results:
        st.info("No se encontraron resultados relevantes.")
        return

    for i, res in enumerate(results, 1):
        score = float(res.get("score", 0.0) or 0.0)
        page = res.get("page", "?")
        text = res.get("text", "Sin contenido")

        with st.container(border=True):
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.markdown(f"**Fragmento {i}** (Página {page})")
            with c2:
                color = "green" if score > 0.7 else "orange" if score > 0.5 else "red"
                st.markdown(f":{color}[Score: {score:.2f}]")

            st.markdown(f"> {text}")

            bc1, bc2 = st.columns([0.25, 0.75])
            with bc1:
                if st.button("📖 Ver fuente", key=f"src_{i}"):
                    # Abrir visor en nueva pestaña (misma app) con query param
                    try:
                        page_int = int(page)
                    except Exception:
                        page_int = None

                    if page_int is None:
                        st.error("La página devuelta por el backend no es un número válido.")
                    else:
                        base_url = st.get_option("browser.serverAddress")
                        server_port = st.get_option("server.port")
                        # Si serverAddress está vacío, dejamos que el navegador resuelva con host actual.
                        if base_url:
                            app_url = f"http://{base_url}:{server_port}"
                        else:
                            app_url = f"http://localhost:{server_port}"

                        viewer_url = f"{app_url}?pdf_page={page_int}"
                        # Enlace HTML con target=_blank para abrir otra pestaña.
                        st.markdown(
                            f"<a href=\"{viewer_url}\" target=\"_blank\">Abrir fuente (página {page_int})</a>",
                            unsafe_allow_html=True,
                        )

            with bc2:
                with st.expander("Metadata técnica"):
                    st.json(res)

    # Nota: la fuente ahora se abre en otra pestaña.


@st.cache_data(show_spinner=False)
def get_pdf_page_image(page_num):
    """Renderiza una página del PDF como imagen (cacheada)."""
    pdf_path = Path(__file__).parent.parent / "data" / "pdf" / "Intro_IA.pdf"
    
    if not pdf_path.exists():
        return None
        
    try:
        doc = fitz.open(str(pdf_path))
        # Ajustar índice (PDF es 0-based, data es 1-based)
        page_idx = int(page_num) - 1
        
        if 0 <= page_idx < len(doc):
            page = doc.load_page(page_idx)
            # Renderizar con zoom para mejor calidad
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return img
            
    except Exception as e:
        print(f"Error rendering PDF: {e}")
        return None
    return None


@st.cache_data(show_spinner=False)
def _pdf_page_png_bytes(page_num: int) -> bytes | None:
    """Devuelve bytes PNG de la página del PDF (para servir en otra pestaña)."""
    pdf_path = Path(__file__).parent.parent / "data" / "pdf" / "Intro_IA.pdf"
    if not pdf_path.exists():
        return None

    try:
        doc = fitz.open(str(pdf_path))
        page_idx = int(page_num) - 1
        if not (0 <= page_idx < len(doc)):
            return None
        page = doc.load_page(page_idx)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        return pix.tobytes("png")
    except Exception:
        return None


def _render_pdf_viewer_page():
    """Vista dedicada para abrir en otra pestaña y ver una página del PDF."""
    page_str = _NAV.get("pdf_page")
    try:
        page_num = int(page_str) if page_str is not None else None
    except Exception:
        page_num = None

    st.title("📄 Fuente (PDF)")

    pdf_path = Path(__file__).parent.parent / "data" / "pdf" / "Intro_IA.pdf"
    if not pdf_path.exists():
        st.error("No se encontró el PDF en `data/pdf/Intro_IA.pdf`.")
        return

    if page_num is None:
        st.info("Falta el parámetro `pdf_page`. Vuelve al buscador y usa 'Ver fuente'.")
        return

    st.caption(f"Mostrando: Intro_IA.pdf — Página {page_num}")

    png_bytes = _pdf_page_png_bytes(page_num)
    if png_bytes is None:
        st.error("No pude renderizar esa página (posiblemente fuera de rango).")
        return

    st.image(png_bytes, use_container_width=True)

    # También damos un link directo al PDF completo en base64 (nueva pestaña)
    # Nota: no todos los navegadores respetan #page=, pero suele funcionar en PDF.js.
    with open(pdf_path, "rb") as f:
        pdf_b64 = base64.b64encode(f.read()).decode("utf-8")
    pdf_url = f"data:application/pdf;base64,{pdf_b64}#page={page_num}"
    st.link_button("Abrir PDF completo (nueva pestaña)", pdf_url)


def main():
    # Si se pasó pdf_page, renderizar visor dedicado y salir.
    if _NAV.get("pdf_page") is not None:
        _render_pdf_viewer_page()
        return

    # Header Común
    st.title("🤖 Chatbot IA - Fundamentos de IA")
    
    # Sidebar con navegación
    with st.sidebar:
        st.header("Navegación")
        page_mode = st.radio("Modo:", ["🤖 Chatbot (Demo)", "🧩 Inspector de Chunks", "🔍 Búsqueda Vectorial"])
        
        
        if page_mode == "🤖 Chatbot (Demo)":
            st.subheader("⚙️ Configuración Chat")
            st.session_state['show_sources'] = st.checkbox("Mostrar fuentes", value=True)
            st.session_state['show_context'] = st.checkbox("Mostrar contexto RAG", value=False)
    
    # Router de páginas
    if page_mode == "🤖 Chatbot (Demo)":
        render_chatbot_ui()
    elif page_mode == "🧩 Inspector de Chunks":
        render_chunk_inspector()
    else:
        render_search_ui()

    # Footer
    st.markdown("---")
    

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    # Inicializar session state
    if 'example_query' not in st.session_state:
        st.session_state['example_query'] = ""
    
    main()

"""
Chatbot IA - Prototipo UI (Semana 2)
=====================================
Aplicación Streamlit para interactuar con el sistema RAG de IA y visualizar chunks.

Autor: Joel
Fecha: Semana 2 - Inspector de Chunks
"""

import streamlit as st
from pathlib import Path
import sys
import json
import pandas as pd

# Configurar path para imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuración de la página
st.set_page_config(
    page_title="Chatbot IA - Fundamentos",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    En futuras semanas, esto se conectará al pipeline de Xander.
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
    Será conectada al índice vectorial de Mateo.
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
        with st.expander("👁️ Ver texto de ejemplo (Erik)"):
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


def main():
    # Header Común
    st.title("🤖 Chatbot IA - Fundamentos de IA")
    
    # Sidebar con navegación
    with st.sidebar:
        st.header("Navegación")
        page_mode = st.radio("Modo:", ["🤖 Chatbot (Demo)", "🧩 Inspector de Chunks"])
        
        st.markdown("---")
        st.header("📚 Información")
        st.markdown("""
        **Estado**: Desarrollo Semana 2
        
        **Progreso**:
        - ✅ UI Streamlit Base
        - ✅ Extracción & Chunking
        - ⏳ Índice Vectorial
        - ⏳ Pipeline RAG
        """)
        
        if page_mode == "🤖 Chatbot (Demo)":
            st.subheader("⚙️ Configuración Chat")
            st.session_state['show_sources'] = st.checkbox("Mostrar fuentes", value=True)
            st.session_state['show_context'] = st.checkbox("Mostrar contexto RAG", value=False)
    
    # Router de páginas
    if page_mode == "🤖 Chatbot (Demo)":
        render_chatbot_ui()
    else:
        render_chunk_inspector()

    # Footer
    st.markdown("---")
    st.caption("Semana 2 - Inspector de Chunks & UI Update | Autor: Joel")

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    # Inicializar session state
    if 'example_query' not in st.session_state:
        st.session_state['example_query'] = ""
    
    main()

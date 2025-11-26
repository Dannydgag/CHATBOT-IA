"""
Chatbot IA - Prototipo UI (Semana 1)
=====================================
Aplicación Streamlit para interactuar con el sistema RAG de IA.

Autor: Joel
Fecha: Semana 1 - Setup inicial
"""

import streamlit as st
from pathlib import Path
import sys

# Configurar path para imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuración de la página
st.set_page_config(
    page_title="Chatbot IA - Fundamentos",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FUNCIONES STUB ====================
# Estas funciones serán reemplazadas con la lógica real en futuras semanas

def get_sample_text():
    """
    Carga texto de ejemplo desde los archivos extraídos.
    En futuras semanas, esto se conectará al pipeline de Xander.
    """
    sample_file = Path(__file__).parent.parent / "data" / "text_by_page" / "sample_pages_1-9.txt"
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
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

def main():
    # Header
    st.title("🤖 Chatbot IA - Fundamentos de Inteligencia Artificial")
    st.markdown("---")
    
    # Sidebar con información y configuración
    with st.sidebar:
        st.header("📚 Información del Sistema")
        st.markdown("""
        **Estado**: Prototipo Semana 1
        
        **Componentes activos**:
        - ✅ UI Streamlit (Joel)
        - ⏳ Extracción de texto (Erik)
        - ⏳ Pipeline RAG (Xander)
        - ⏳ Índice vectorial (Mateo)
        
        **Documento fuente**:
        Fundamentos de la IA - Volumen I
        """)
        
        st.markdown("---")
        
        # Opciones de configuración (para futuras semanas)
        st.subheader("⚙️ Configuración")
        show_sources = st.checkbox("Mostrar fuentes", value=True)
        show_context = st.checkbox("Mostrar contexto RAG", value=False)
        
        st.markdown("---")
        st.caption("Semana 1 - Prototipo UI")
        st.caption("Autor: Joel")
    
    # Layout principal con 2 columnas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Área de Consulta")
        
        # Input de pregunta
        query = st.text_area(
            "Escribe tu pregunta sobre IA:",
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
                    if show_context:
                        with st.expander("🔍 Ver contexto RAG utilizado"):
                            context = stub_get_context(query)
                            st.code(context, language=None)
        
        elif clear_btn:
            st.rerun()
        
        elif submit_btn and not query:
            st.warning("⚠️ Por favor, escribe una pregunta antes de consultar.")
    
    with col2:
        st.header("📄 Fuentes")
        
        if submit_btn and query and show_sources:
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
    
    # Footer con información de desarrollo
    st.markdown("---")
    st.caption("""
    🚧 **Semana 1 - Prototipo Inicial** | 
    Este es un esqueleto funcional. Los componentes reales se integrarán en las próximas semanas.
    """)


# ==================== EJEMPLOS Y DEMOS ====================

def show_examples():
    """Sección de ejemplos para testing"""
    st.markdown("---")
    st.header("💡 Preguntas de Ejemplo")
    
    examples = [
        "¿Qué es la inteligencia artificial?",
        "¿Cuáles son los fundamentos de la IA?",
        "¿Qué temas cubre el Volumen I?",
        "Explica los conceptos principales del documento"
    ]
    
    cols = st.columns(2)
    for idx, example in enumerate(examples):
        with cols[idx % 2]:
            if st.button(f"📌 {example}", key=f"example_{idx}", use_container_width=True):
                st.session_state['example_query'] = example


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    # Inicializar session state si es necesario
    if 'example_query' not in st.session_state:
        st.session_state['example_query'] = None
    
    main()
    
    # Mostrar ejemplos al final
    with st.expander("💡 Ver preguntas de ejemplo"):
        show_examples()

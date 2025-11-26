"""
Utilidades para la aplicación Streamlit
========================================
Funciones helper reutilizables para la UI del chatbot.

Autor: Joel
Fecha: Semana 1
"""

from pathlib import Path
from typing import Dict, List, Optional
import json


class DataLoader:
    """Clase para cargar datos de ejemplo y texto extraído"""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            self.base_path = Path(__file__).parent.parent
        else:
            self.base_path = Path(base_path)
        
        self.text_path = self.base_path / "data" / "text_by_page"
        self.chunks_path = self.base_path / "data" / "chunks"
    
    def load_sample_pages(self, filename: str = "sample_pages_1-9.txt") -> str:
        """
        Carga el texto de ejemplo extraído por Erik.
        
        Args:
            filename: Nombre del archivo de texto
            
        Returns:
            Contenido del archivo o mensaje de error
        """
        try:
            file_path = self.text_path / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "⚠️ Archivo de ejemplo no encontrado. Erik aún no ha extraído el texto."
        except Exception as e:
            return f"❌ Error al cargar texto: {str(e)}"
    
    def get_page_text(self, page_number: int) -> str:
        """
        Extrae el texto de una página específica del archivo sample.
        
        Args:
            page_number: Número de página a extraer
            
        Returns:
            Texto de la página solicitada
        """
        full_text = self.load_sample_pages()
        marker = f"=====[START_PAGE_{page_number}]====="
        
        if marker in full_text:
            start = full_text.index(marker) + len(marker)
            # Buscar el siguiente marcador o fin del archivo
            next_marker = f"=====[START_PAGE_{page_number + 1}]====="
            if next_marker in full_text:
                end = full_text.index(next_marker)
                return full_text[start:end].strip()
            else:
                return full_text[start:].strip()
        else:
            return f"Página {page_number} no encontrada en el texto extraído."
    
    def list_available_pages(self) -> List[int]:
        """
        Lista todas las páginas disponibles en el texto extraído.
        
        Returns:
            Lista de números de página disponibles
        """
        full_text = self.load_sample_pages()
        pages = []
        for i in range(1, 100):  # Buscar hasta 100 páginas
            if f"=====[START_PAGE_{i}]=====" in full_text:
                pages.append(i)
            else:
                break
        return pages


class ResponseFormatter:
    """Clase para formatear respuestas del sistema"""
    
    @staticmethod
    def format_answer(answer: str, confidence: float = 0.0) -> Dict[str, any]:
        """
        Formatea una respuesta con metadata.
        
        Args:
            answer: Texto de la respuesta
            confidence: Nivel de confianza (0-1)
            
        Returns:
            Diccionario con respuesta formateada
        """
        return {
            "answer": answer,
            "confidence": confidence,
            "formatted": True
        }
    
    @staticmethod
    def format_sources(sources: List[Dict]) -> str:
        """
        Formatea lista de fuentes como texto legible.
        
        Args:
            sources: Lista de diccionarios con información de fuentes
            
        Returns:
            String formateado con las fuentes
        """
        if not sources:
            return "No hay fuentes disponibles"
        
        formatted = []
        for idx, source in enumerate(sources, 1):
            page = source.get("page", "?")
            text = source.get("text", "Sin texto")
            formatted.append(f"{idx}. **Página {page}**: {text[:100]}...")
        
        return "\n\n".join(formatted)


class StubEndpoints:
    """
    Endpoints stub que simulan las respuestas del pipeline.
    Estos serán reemplazados por las integraciones reales de Xander.
    """
    
    @staticmethod
    def query(question: str, top_k: int = 3) -> Dict:
        """
        Simula una consulta al sistema RAG.
        
        Args:
            question: Pregunta del usuario
            top_k: Número de documentos relevantes a recuperar
            
        Returns:
            Respuesta simulada con formato estándar
        """
        # TODO: Conectar con orchestration/init_pipeline.py de Xander
        return {
            "question": question,
            "answer": f"[STUB] Respuesta simulada para: '{question}'\n\n"
                     f"Este endpoint será conectado al pipeline de Xander en Semana 2-3.",
            "sources": [
                {
                    "page": 3,
                    "text": "FUNDAMENTOS DE LA INTELIGENCIA ARTIFICIAL",
                    "score": 0.92
                },
                {
                    "page": 4, 
                    "text": "ISBN General: 978-631-6557-23-0",
                    "score": 0.85
                }
            ],
            "confidence": 0.87,
            "retrieved_chunks": top_k,
            "is_stub": True
        }
    
    @staticmethod
    def get_similar_documents(query: str, top_k: int = 5) -> List[Dict]:
        """
        Simula búsqueda de documentos similares.
        
        Args:
            query: Consulta de búsqueda
            top_k: Número de resultados
            
        Returns:
            Lista de documentos similares simulados
        """
        # TODO: Conectar con index/setup_index.py de Mateo
        return [
            {
                "id": f"chunk_{i}",
                "text": f"Fragmento {i} relacionado con: {query}",
                "score": 0.9 - (i * 0.1),
                "page": 3 + i
            }
            for i in range(top_k)
        ]
    
    @staticmethod
    def health_check() -> Dict:
        """
        Verifica el estado de los componentes del sistema.
        
        Returns:
            Estado de cada componente
        """
        return {
            "ui": {"status": "operational", "owner": "Joel"},
            "extractor": {"status": "in_progress", "owner": "Erik"},
            "pipeline": {"status": "planning", "owner": "Xander"},
            "index": {"status": "planning", "owner": "Mateo"},
            "coordinator": {"status": "operational", "owner": "Gabo"}
        }


# Funciones auxiliares de utilidad

def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Trunca texto si excede la longitud máxima.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a agregar si se trunca
        
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """
    Extrae palabras clave básicas del texto (implementación simple).
    
    Args:
        text: Texto de entrada
        top_n: Número de palabras clave a extraer
        
    Returns:
        Lista de palabras clave
    """
    # Implementación básica - puede mejorarse con NLP
    words = text.lower().split()
    # Filtrar palabras comunes (stopwords básicos en español)
    stopwords = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 
                 'hay', 'por', 'con', 'su', 'para', 'como', 'está', 'lo', 'del'}
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    
    # Contar frecuencias (simple)
    from collections import Counter
    word_freq = Counter(keywords)
    
    return [word for word, _ in word_freq.most_common(top_n)]


def format_timestamp() -> str:
    """
    Genera timestamp formateado para logs.
    
    Returns:
        String con fecha y hora actual
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Exportar las clases y funciones principales
__all__ = [
    'DataLoader',
    'ResponseFormatter', 
    'StubEndpoints',
    'truncate_text',
    'extract_keywords',
    'format_timestamp'
]

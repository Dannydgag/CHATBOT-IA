import json
import sys
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import re 
import unicodedata

# ==============================================================================
# 1. CONFIGURACIÓN V2 - CALIBRADA PARA MÁXIMA PRECISIÓN
# ==============================================================================

INPUT_DIR = Path("data") / "text_by_page"
OUTPUT_PATH = Path("data") / "chunks" / "chunks.cleaned.jsonl" 

# Ajustes sugeridos para mejorar el Precision@1 (Semana 3)
CHUNK_SIZE = 850      # Tamaño ideal para capturar conceptos completos
CHUNK_OVERLAP = 200   # Solape suficiente para no perder contexto entre bloques

# SEPARADORES: Ahora incluimos ". " para intentar NO cortar oraciones a la mitad
SEPARATORS = ["\n\n", "\n", ". ", " ", ""] 

# Expresiones regulares para limpieza y reparación
CONTROL_RE = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]') # Caracteres invisibles/basura
MULTISPACE_RE = re.compile(r' {2,}')                    # Espacios dobles o más
HYPHEN_LINE_RE = re.compile(r'(\w)-\n(\w)', flags=re.UNICODE) # Guiones partidos

# ==============================================================================
# 2. FUNCIONES DE LIMPIEZA Y PROCESAMIENTO
# ==============================================================================

def clean_chunk_text(text: str) -> str:
    """
    LIMPIEZA FINAL: Asegura que el texto sea puro para el modelo de Embedding.
    """
    if not text: return ""
    
    # Normalización: Arregla tildes y caracteres Unicode
    text = unicodedata.normalize('NFC', text).lstrip('\ufeff')
    
    # MEJORA V2: Unifica comillas (Mateo) para evitar ruidos en la búsqueda
    text = re.sub(r'[“”„«»]', '"', text)
    text = re.sub(r'[‘’`´]', "'", text)
    
    # REQUISITO CRÍTICO: Convertir saltos de línea en espacios para no fragmentar el contexto
    text = text.replace('\n', ' ')
    
    # Eliminar basura: Caracteres de control y espacios de no ruptura (NBSP)
    text = CONTROL_RE.sub('', text)
    text = text.replace('\u00A0', ' ')
    
    # Estética: Colapsar espacios múltiples en uno solo
    text = MULTISPACE_RE.sub(' ', text)
    
    return text.strip()

def repair_hyphenated_words(text: str) -> str:
    """Repara palabras cortadas al final de línea (ej: progra-\\nmación)."""
    return HYPHEN_LINE_RE.sub(r'\1\2', text)

def extract_simple_title(text: str) -> str | None:
    """Extrae la primera oración como título si es corta y está en MAYÚSCULAS."""
    sentences = text.split('.') 
    if sentences:
        first = sentences[0].strip()
        if 5 < len(first) < 100 and first.isupper():
            return first
    return None

# ==============================================================================
# 3. FLUJO PRINCIPAL (PIPELINE)
# ==============================================================================

def generate_chunks(documents: list) -> list:
    """Divide documentos en pedazos lógicos con doble limpieza."""
    print(f"\n🚀 Iniciando Chunking V2 (Size: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP})")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len
    )
    
    final_chunks = []
    for doc in documents:
        # ETAPA 1: Reparar palabras cortadas ANTES de dividir el texto
        repaired = repair_hyphenated_words(doc["text"])
        
        # ETAPA 2: División inteligente usando los separadores definidos
        raw_chunks = splitter.split_text(repaired)
        
        for i, chunk_text in enumerate(raw_chunks):
            # ETAPA 3: Limpieza profunda de cada pedazo
            cleaned = clean_chunk_text(chunk_text)
            
            # Omitir fragmentos basura o muy cortos
            if len(cleaned) < 25: continue
            
            final_chunks.append({
                "id": f"{doc['metadata']['source']}-{i}", 
                "page": doc["metadata"]["page_number"], 
                "source": doc["metadata"]["source"], 
                "title": extract_simple_title(cleaned),
                "text": cleaned 
            })
            
    return final_chunks

def load_cleaned_documents(input_dir: Path) -> list:
    """Carga los archivos de texto por página."""
    documents = []
    print(f"📂 Cargando páginas desde: {input_dir}")
    for file_path in sorted(input_dir.glob("page_*.txt")):
        try:
            page_num = int(file_path.stem.split('_')[-1])
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    documents.append({
                        "text": content,
                        "metadata": {"source": file_path.name, "page_number": page_num}
                    })
        except: continue
    return documents

def main():
    # 1. Cargar datos
    docs = load_cleaned_documents(INPUT_DIR)
    if not docs: 
        print("❌ Error: No se encontraron documentos.")
        return
        
    # 2. Procesar
    chunks = generate_chunks(docs)
    
    # 3. Guardar resultado final
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True) 
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
            
    print(f"✅ Proceso terminado. {len(chunks)} chunks guardados en {OUTPUT_PATH}")

if __name__ == '__main__':
    main()  
import json
import sys
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import re 
import unicodedata

# ==============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ==============================================================================

INPUT_DIR = Path("data") / "text_by_page"
OUTPUT_PATH = Path("data") / "chunks" / "chunks.cleaned.jsonl" 

CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 150 
# Mantenemos los delimitadores \n\n y \n para que el splitter corte ANTES de que los eliminemos.
SEPARATORS = ["\n\n", "\n", " ", ""] 

# REGEX para Limpieza Final
CONTROL_RE = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')
MULTISPACE_RE = re.compile(r' {2,}')

# REGEX para Reparación Semántica (Guiones Partidos)
# Busca una letra/número (\w) seguida de un guion (-) y un salto de línea (\n)
# y una letra/número al inicio de la siguiente línea. EJ: "inte-\nligencia"
HYPHEN_LINE_RE = re.compile(r'(\w)-\n(\w)', flags=re.UNICODE) 

# ==============================================================================
# FUNCIONES PRINCIPALES
# ==============================================================================

def clean_chunk_text(text: str) -> str:
    """
    *** ETAPA 2: LIMPIEZA FINAL POST-CHUNKING (Requisito de Mateo) ***
    Normaliza Unicode, elimina control chars y CONVIERTE \n a espacio.
    """
    if text is None:
        return ""
        
    # 1. Normalización Unicode y eliminación de BOM
    text = unicodedata.normalize('NFC', text)
    text = text.lstrip('\ufeff')
    
    # 2. Reemplazo CRÍTICO para Embeddings: \n -> ' '
    # Esto fragmenta el contexto si se deja, por lo que lo reemplazamos por un espacio.
    text = text.replace('\n', ' ')
    
    # 3. Eliminar caracteres de control y NBSP (\u00A0)
    text = CONTROL_RE.sub('', text)
    text = text.replace('\u00A0', ' ')
    
    # 4. Colapsar espacios múltiples a un solo espacio
    text = MULTISPACE_RE.sub(' ', text)
    
    return text.strip()


def repair_hyphenated_words(text: str) -> str:
    """
    *** ETAPA 1: REPARACIÓN SEMÁNTICA PRE-CHUNKING ***
    Repara palabras cortadas por guion seguido de salto de línea, 
    uniéndolas (ej: 'progra-\nmación' -> 'programación').
    """
    # Reemplaza 'word-\nnext' con 'wordnext' (eliminando el guion y el salto)
    return HYPHEN_LINE_RE.sub(r'\1\2', text)


def extract_simple_title(text: str) -> str | None:
    # (Función sin cambios)
    if not text:
        return None
    first_line = text.splitlines()[0].strip()
    if 0 < len(first_line) < 120 and first_line.isupper():
        return first_line
    return None

def load_cleaned_documents(input_dir: Path) -> list:
    # (Función sin cambios)
    documents = []
    print(f"Cargando archivos limpios desde: {input_dir}")
    
    for file_path in sorted(input_dir.glob("page_*.txt")):
        try:
            page_num = int(file_path.stem.split('_')[-1])
        except ValueError:
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            if content.strip():
                documents.append({
                    "text": content,
                    "metadata": {
                        "source": file_path.name,
                        "page_number": page_num
                    }
                })
                
    print(f"✅ Documentos cargados: {len(documents)} páginas con contenido.")
    return documents


def generate_chunks(documents: list) -> list:
    """
    Flujo de dos etapas: (1) Reparación semántica del texto de la página, 
    (2) Chunking inteligente, y (3) Limpieza final del formato.
    """
    print("\nIniciando el Chunking Recursivo con doble limpieza...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len
    )
    
    final_chunks = []
    chunk_counter = 0 
    
    for doc in documents:
        # --- ETAPA 1: REPARACIÓN SEMÁNTICA PRE-CHUNKING ---
        # Reparamos los guiones partidos ANTES de que el splitter actúe.
        repaired_text = repair_hyphenated_words(doc["text"])
        
        # --- ETAPA 2: CHUNKING INTELIGENTE ---
        # El splitter usa los \n remanentes para cortar lógicamente.
        chunks_text_list = splitter.split_text(repaired_text)
        
        page_num = doc["metadata"]["page_number"]
        source_file = doc["metadata"]["source"]
        
        for chunk_index, chunk_text in enumerate(chunks_text_list):
            
            # --- ETAPA 3: LIMPIEZA DE FORMATO POST-CHUNKING ---
            # Ahora convertimos \n a espacios para el modelo de embedding.
            cleaned_text = clean_chunk_text(chunk_text)
            
            if len(cleaned_text.strip()) < 20:
                continue
            
            # --- ESTRUCTURA FINAL ---
            final_chunks.append({
                "id": f"{source_file}-{chunk_index}", 
                "page": page_num, 
                "source": source_file, 
                "title": extract_simple_title(cleaned_text),
                "text": cleaned_text 
            })
            chunk_counter += 1

    print(f"✅ Chunking finalizado. Total de chunks generados: {chunk_counter}")
    return final_chunks


def save_chunks_to_jsonl(chunks: list, output_path: Path):
    # (Función sin cambios)
    output_path.parent.mkdir(parents=True, exist_ok=True) 
    
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    print(f"✅ Entregable final generado: {output_path}")


def main():
    # (Función main sin cambios)
    documents = load_cleaned_documents(INPUT_DIR)
    
    if not documents:
        print("ERROR: No se encontraron documentos limpios para procesar.")
        sys.exit(1)
        
    chunks = generate_chunks(documents)
    
    save_chunks_to_jsonl(chunks, OUTPUT_PATH)

if __name__ == '__main__':
    main()
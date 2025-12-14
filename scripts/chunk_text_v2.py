import json
import sys
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re # Para intentar extraer un título simple

# ==============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ==============================================================================

# Directorios de entrada y salida
INPUT_DIR = Path("data") / "text_by_page"
OUTPUT_PATH = Path("data") / "chunks" / "chunks.jsonl"

# Parámetros clave para el Chunking
CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 150 
SEPARATORS = ["\n\n", "\n", " ", ""] 

# ==============================================================================
# FUNCIONES PRINCIPALES
# ==============================================================================

def extract_simple_title(text: str) -> str | None:
    """
    Intenta extraer una línea corta en mayúsculas como título, 
    siguiendo una heurística similar a la de Mateo.
    """
    if not text:
        return None
    
    # Tomamos la primera línea limpia que no esté vacía
    first_line = text.splitlines()[0].strip()

    # Heurística: Si es corta y está en mayúsculas, asumimos que es un título
    if 0 < len(first_line) < 120 and first_line.isupper():
        return first_line
        
    return None

def load_cleaned_documents(input_dir: Path) -> list:
    """
    Carga todos los archivos de texto limpio y crea una lista de documentos 
    con su metadata de página.
    """
    documents = []
    print(f"Cargando archivos limpios desde: {input_dir}")
    
    for file_path in sorted(input_dir.glob("page_*.txt")):
        try:
            # Extraer el número de página de la ruta del archivo (ej: page_005.txt -> 5)
            page_num = int(file_path.stem.split('_')[-1])
        except ValueError:
            print(f"Advertencia: No se pudo parsear el número de página para {file_path.name}")
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
    Divide los documentos cargados en chunks (bloques) usando el Text Splitter Recursivo
    y genera la estructura plana final esperada por Mateo.
    """
    print("\nIniciando el Chunking Recursivo...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len
    )
    
    final_chunks = []
    chunk_counter = 0 # Contador global para asegurar IDs únicos
    
    for doc in documents:
        # Dividir el texto de la página actual
        chunks_text_list = splitter.split_text(doc["text"])
        
        # Heredamos la metadata de la página para cada chunk
        page_num = doc["metadata"]["page_number"]
        source_file = doc["metadata"]["source"]
        
        for chunk_index, chunk_text in enumerate(chunks_text_list):
            
            # --- ESTRUCTURA FINAL (Alineada con chunks.cleaned.jsonl) ---
            
            # Para simplificar y alinearse con la salida de Mateo:
            # - start: Lo fijamos en 0 (aunque es inexacto)
            # - end: Es la longitud del texto
            
            final_chunks.append({
                # ID único (CRÍTICO)
                "id": f"{source_file}-{chunk_index}",
                # CRÍTICO para Joel
                "page": page_num, 
                # CRÍTICO para Indexado
                "text": chunk_text,
                # Trazabilidad
                "source": source_file,
                # Campos de esquema de Mateo (Alineados con su salida simplificada)
                "start": 0, # Fijo en 0 por convención de Mateo
                "end": len(chunk_text), # Longitud del texto para 'end'
                "title": extract_simple_title(chunk_text) # Intento de título o None
            })
            chunk_counter += 1

    print(f"✅ Chunking finalizado. Total de chunks generados: {chunk_counter}")
    return final_chunks


def save_chunks_to_jsonl(chunks: list, output_path: Path):
    """
    Guarda la lista final de chunks en el formato JSONL, que es fácil de indexar.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True) 
    
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    print(f"✅ Entregable final generado: {output_path}")


def main():
    """Función principal para el pipeline de chunking."""
    
    # 1. Cargar documentos limpios
    documents = load_cleaned_documents(INPUT_DIR)
    
    if not documents:
        print("ERROR: No se encontraron documentos limpios para procesar.")
        sys.exit(1)
        
    # 2. Generar chunks
    chunks = generate_chunks(documents)
    
    # 3. Guardar el entregable final para el equipo
    save_chunks_to_jsonl(chunks, OUTPUT_PATH)

if __name__ == '__main__':
    main()
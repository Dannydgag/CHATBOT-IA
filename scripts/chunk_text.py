import json
import sys
from pathlib import Path
# *** CAMBIO APLICADO: Importación según tu entorno ***
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import re 
import unicodedata

# ==============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ==============================================================================

# Directorios de entrada y salida
INPUT_DIR = Path("data") / "text_by_page"
# *** CAMBIO APLICADO: Nombre de archivo para alinear con Mateo ***
OUTPUT_PATH = Path("data") / "chunks" / "chunks.cleaned.jsonl" 

# Parámetros clave para el Chunking
CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 150 
# Usamos delimitadores para que el splitter corte inteligentemente
SEPARATORS = ["\n\n", "\n", " ", ""] 

# Expresión regular para caracteres de control (no imprimibles) y espacios múltiples
CONTROL_RE = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')
MULTISPACE_RE = re.compile(r' {2,}')

# ==============================================================================
# FUNCIONES PRINCIPALES
# ==============================================================================

def clean_chunk_text(text: str) -> str:
    """
    *** FUNCIÓN DE LIMPIEZA FINAL (QA) ***
    Normaliza Unicode, elimina caracteres de control y normaliza espaciado.
    Esto asegura que los chunks estén listos para el embedding de Mateo.
    """
    if text is None:
        return ""
        
    # 1. Normalización Unicode: fundamental para la coherencia
    text = unicodedata.normalize('NFC', text)
    
    # 2. Eliminar BOM (Byte Order Mark) y caracteres de control (los "extraños")
    text = text.lstrip('\ufeff')
    text = CONTROL_RE.sub('', text)
    
    # 3. Normalizar saltos de línea y reemplazar non-breaking spaces
    text = text.replace('\r\n','\n').replace('\r','\n')
    text = text.replace('\u00A0', ' ')
    
    # 4. Colapsar espacios múltiples a un solo espacio
    text = MULTISPACE_RE.sub(' ', text)
    
    return text.strip()


def extract_simple_title(text: str) -> str | None:
    """Intenta extraer una línea corta en mayúsculas como título para metadata."""
    if not text:
        return None
    
    first_line = text.splitlines()[0].strip()
    if 0 < len(first_line) < 120 and first_line.isupper():
        return first_line
        
    return None

def load_cleaned_documents(input_dir: Path) -> list:
    """Carga todos los archivos de texto limpio."""
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
    Divide los documentos cargados en chunks (bloques) y genera la estructura 
    plana final con los campos CRÍTICOS y limpieza final.
    """
    print("\nIniciando el Chunking Recursivo...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len
    )
    
    final_chunks = []
    chunk_counter = 0 
    
    for doc in documents:
        chunks_text_list = splitter.split_text(doc["text"])
        
        page_num = doc["metadata"]["page_number"]
        source_file = doc["metadata"]["source"]
        
        for chunk_index, chunk_text in enumerate(chunks_text_list):
            
            # *** PASO CRÍTICO DE QA: Limpieza final del texto del chunk ***
            cleaned_text = clean_chunk_text(chunk_text)
            
            if len(cleaned_text.strip()) < 20: # Omitir chunks muy cortos después de la limpieza
                continue
            
            # --- ESTRUCTURA FINAL Y LIMPIA ---
            final_chunks.append({
                "id": f"{source_file}-{chunk_index}", 
                "page": page_num, 
                "source": source_file,
                "title": extract_simple_title(cleaned_text),
                "text": cleaned_text # Usamos el texto limpio final 
            })
            chunk_counter += 1

    print(f"✅ Chunking finalizado. Total de chunks generados: {chunk_counter}")
    return final_chunks


def save_chunks_to_jsonl(chunks: list, output_path: Path):
    """Guarda la lista final de chunks en el formato JSONL."""
    output_path.parent.mkdir(parents=True, exist_ok=True) 
    
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    print(f"✅ Entregable final generado: {output_path}")


def main():
    """Función principal para el pipeline de chunking."""
    
    documents = load_cleaned_documents(INPUT_DIR)
    
    if not documents:
        print("ERROR: No se encontraron documentos limpios para procesar.")
        sys.exit(1)
        
    chunks = generate_chunks(documents)
    
    save_chunks_to_jsonl(chunks, OUTPUT_PATH)

if __name__ == '__main__':
    main()
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ==============================================================================

# Directorios de entrada y salida
INPUT_DIR = Path("data") / "text_by_page"
OUTPUT_PATH = Path("data") / "chunks" / "chunks.jsonl"

# Parámetros clave para el Chunking (Ajustados para tu proyecto)
# Tamaño máximo de cada chunk (típico: 500-1000 tokens/caracteres)
CHUNK_SIZE = 1000 
# Solapamiento entre chunks (para evitar cortar ideas a la mitad)
CHUNK_OVERLAP = 150 
# Separadores que el splitter intentará usar en orden
SEPARATORS = ["\n\n", "\n", " ", ""] 

# ==============================================================================
# FUNCIONES PRINCIPALES
# ==============================================================================

def load_cleaned_documents(input_dir: Path) -> list:
    """
    Carga todos los archivos de texto limpio de la carpeta de producción
    y crea una lista de documentos con su metadata de página.
    """
    documents = []
    print(f"Cargando archivos desde: {input_dir}")
    
    # Iterar sobre todos los archivos que terminan en .txt en el directorio de entrada
    for file_path in sorted(input_dir.glob("page_*.txt")):
        
        # Extraer el número de página de la ruta del archivo (ej: page_005.txt -> 5)
        try:
            page_num = int(file_path.stem.split('_')[-1])
        except ValueError:
            print(f"Advertencia: No se pudo parsear el número de página para {file_path.name}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Solo añadir si hay contenido significativo (no vacío tras limpieza)
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
    Divide los documentos cargados en chunks (bloques) usando el Text Splitter Recursivo.
    """
    print("\nIniciando el Chunking Recursivo...")
    
    # Inicializar el divisor de texto (el corazón del chunking)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len, # Usamos len para contar por caracteres
        add_start_index=True # Opcional: añade el índice de inicio del chunk en el documento original
    )
    
    final_chunks = []
    
    for doc in documents:
        # Dividir el texto de la página actual
        chunks = splitter.split_text(doc["text"])
        
        # Añadir metadata a cada chunk generado
        for chunk_index, chunk_text in enumerate(chunks):
            
            # El delivered final requiere un formato JSONL sencillo.
            final_chunks.append({
                "chunk_id": f"{doc['metadata']['source']}-{chunk_index}",
                "text": chunk_text,
                "metadata": doc["metadata"] # Hereda la metadata de la página
            })

    print(f"✅ Chunking finalizado. Total de chunks generados: {len(final_chunks)}")
    return final_chunks


def save_chunks_to_jsonl(chunks: list, output_path: Path):
    """
    Guarda la lista final de chunks en el formato JSONL, que es fácil de indexar.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True) # Asegurar que la carpeta exista
    
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            # Escribir cada chunk como una línea JSON válida
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    print(f"✅ Entregable final generado: {output_path}")
    print(f"Este archivo (`chunks.jsonl`) es el input directo para Mateo.")


def main():
    """Función principal para el pipeline de chunking."""
    
    # 1. Cargar documentos limpios
    documents = load_cleaned_documents(INPUT_DIR)
    
    if not documents:
        print("ERROR: No se encontraron documentos limpios para procesar. Asegúrate de ejecutar 'extract_text.py' primero.")
        sys.exit(1)
        
    # 2. Generar chunks
    chunks = generate_chunks(documents)
    
    # 3. Guardar el entregable final para el equipo
    save_chunks_to_jsonl(chunks, OUTPUT_PATH)

if __name__ == '__main__':
    main()
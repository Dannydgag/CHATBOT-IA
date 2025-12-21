import json
import re
import unicodedata
from pathlib import Path

# ==============================================================================
# 1. CONFIGURACIÓN Y RUTAS
# ==============================================================================
# Directorio donde se encuentran los archivos .txt por página
INPUT_DIR = Path("data") / "text_by_page"
# Archivo de salida final en formato JSONL
OUTPUT_PATH = Path("data") / "chunks" / "chunks.cleaned.jsonl"

# Filtro de páginas: Excluimos introducciones irrelevantes y anexos vacíos
# Mantenemos la página 13 por contener información crítica de autores
EXCLUDED_PAGES = (set(range(1, 21)) | set(range(204, 215))) - {13}

# Parámetros del algoritmo de segmentación
CHUNK_TARGET_SIZE = 1000  # Tamaño ideal en caracteres para los embeddings

# ==============================================================================
# 2. UTILIDADES DE LIMPIEZA
# ==============================================================================

def clean_text(text: str) -> str:
    """
    Realiza una limpieza profunda del texto para optimizar la comprensión del LLM.
    - Normaliza caracteres Unicode (NFC).
    - Elimina puntuación huérfana al inicio de los bloques.
    - Convierte saltos de línea en espacios para mantener un flujo de lectura continuo.
    """
    if not text:
        return ""
        
    # Normalización de caracteres (tildes, eñes y símbolos)
    text = unicodedata.normalize('NFC', text).strip()
    
    # Limpieza de "basura" gramatical al inicio del fragmento (puntos, comas, espacios)
    text = re.sub(r'^[,\.\s:;]+', '', text)
    
    # Unificación de espacios: reemplaza saltos de línea y múltiples espacios por uno solo
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# ==============================================================================
# 3. MOTOR DE SEGMENTACIÓN SEMÁNTICA (STREAMING)
# ==============================================================================

def generate_chunks_v5(documents: list) -> list:
    """
    Procesa los documentos como un flujo continuo de texto para evitar cortes 
    abruptos entre páginas y mantener la jerarquía de títulos.
    """
    print(f"\n🚀 Iniciando Motor de Chunking V5.0...")
    
    final_chunks = []
    current_buffer = []      # Acumulador temporal de líneas para un chunk
    current_title = "Introducción General" # Título por defecto
    char_count = 0
    
    # --- PASO 1: CONSOLIDACIÓN DE FLUJO ---
    # Convertimos archivos individuales en una lista secuencial de líneas con metadatos
    full_stream = []
    for doc in documents:
        # Lógica especial para la página de Autores (no se mezcla con el flujo general)
        if doc["metadata"]["page_number"] == 13:
            lines = doc["text"].splitlines()
            content = " ".join(lines[1:]) # Omitimos encabezado de página
            save_chunk_manual(content, {"source": doc["metadata"]["source"], "page": 13}, "AUTORES", final_chunks)
            continue

        # Agregamos líneas al flujo general conservando su origen
        lines = doc["text"].splitlines()
        for line in lines:
            if line.strip():
                full_stream.append({
                    "text": line.strip(),
                    "page": doc["metadata"]["page_number"],
                    "source": doc["metadata"]["source"]
                })

    # --- PASO 2: SEGMENTACIÓN BASADA EN CONTEXTO ---
    for item in full_stream:
        line_text = item["text"]
        
        # Detección de cambio de sección: Si hay un título, cerramos el chunk actual
        if line_text.startswith("[TITLE]:"):
            if current_buffer:
                save_chunk(current_buffer, current_title, final_chunks)
            
            # Actualizamos el título activo para los siguientes fragmentos
            current_title = line_text.replace("[TITLE]:", "").strip()
            current_buffer = []
            char_count = 0
            continue

        current_buffer.append(item)
        char_count += len(line_text)

        # Si alcanzamos el tamaño límite, buscamos un corte gramaticalmente correcto (un punto)
        if char_count >= CHUNK_TARGET_SIZE:
            combined_txt = " ".join([i["text"] for i in current_buffer])
            last_period = combined_txt.rfind(". ") # Buscamos el último punto y espacio
            
            # Cortamos solo si el punto está en una posición razonable para no dejarlo muy pequeño
            if last_period != -1 and last_period > 600:
                text_to_save = combined_txt[:last_period+1]
                save_chunk_manual(text_to_save, current_buffer[0], current_title, final_chunks)
                
                # El remanente de la oración pasa al buffer del siguiente chunk
                remaining = combined_txt[last_period+1:].strip()
                current_buffer = [{"text": remaining, "page": item["page"], "source": item["source"]}]
                char_count = len(remaining)
            else:
                # Si no hay puntos, forzamos el cierre para evitar chunks gigantes
                save_chunk(current_buffer, current_title, final_chunks)
                current_buffer = []
                char_count = 0

    # Guardar el último fragmento del libro
    if current_buffer:
        save_chunk(current_buffer, current_title, final_chunks)

    return final_chunks

# ==============================================================================
# 4. PERSISTENCIA Y FORMATEO
# ==============================================================================

def save_chunk(buffer: list, title: str, final_list: list):
    """Encapsula y limpia un grupo de líneas para añadirlo a la lista final."""
    if not buffer: return
    text = clean_text(" ".join([i["text"] for i in buffer]))
    if len(text) < 40: return # Ignorar fragmentos insignificantes
    
    # Usamos los metadatos de la primera línea del buffer
    meta = buffer[0]
    add_to_list(text, meta["source"], meta["page"], title, final_list)

def save_chunk_manual(text: str, meta: dict, title: str, final_list: list):
    """Permite guardar texto pre-procesado manualmente."""
    add_to_list(text, meta["source"], meta["page"], title, final_list)

def add_to_list(text: str, source: str, page: int, title: str, final_list: list):
    """Crea el diccionario con la estructura de datos final requerida por el equipo."""
    # Calculamos el índice local para el ID basado en cuántos chunks tiene ya esa página
    idx = sum(1 for c in final_list if c["source"] == source)
    
    final_list.append({
        "id": f"{source}-{idx}",
        "page": page,
        "source": source,
        "title": title,
        "text": clean_text(text)
    })

# ==============================================================================
# 5. CARGA DE ARCHIVOS Y PUNTO DE ENTRADA
# ==============================================================================

def load_documents(input_dir: Path) -> list:
    """Carga los archivos de texto filtrando las páginas excluidas."""
    documents = []
    # Ordenamos alfabéticamente para asegurar que page_21 vaya antes que page_22
    files = sorted(input_dir.glob("page_*.txt"))
    
    for file_path in files:
        try:
            page_num = int(file_path.stem.split('_')[-1])
            if page_num in EXCLUDED_PAGES: continue
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    documents.append({
                        "text": content,
                        "metadata": {"source": file_path.name, "page_number": page_num}
                    })
        except Exception as e:
            print(f"⚠️ Error cargando {file_path.name}: {e}")
            
    return documents

def main():
    """Flujo principal de ejecución del script."""
    # 1. Cargar datos
    docs = load_documents(INPUT_DIR)
    if not docs:
        print("❌ No se encontraron documentos. Verifica la ruta 'data/text_by_page'")
        return
    
    # 2. Generar fragmentos
    chunks = generate_chunks_v5(docs)
    
    # 3. Guardar resultados
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    print(f"✅ V5.0 Finalizada con éxito.")
    print(f"📦 Destino: {OUTPUT_PATH}")
    print(f"🧩 Total de chunks generados: {len(chunks)}")

if __name__ == '__main__':
    main()
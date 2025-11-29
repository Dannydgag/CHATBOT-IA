import fitz # PyMuPDF (Pipeline seleccionado)
from pathlib import Path 
import sys 
import re # Módulo de expresiones regulares para la limpieza

# ==============================================================================
# CONFIGURACIÓN DEL PROYECTO
# ==============================================================================

# Ruta relativa al documento PDF de entrada.
PDF_FILENAME = "Intro_IA.pdf"
PDF_PATH = Path("docs") / PDF_FILENAME

# Directorio de salida para los archivos de texto extraídos (producción).
OUTPUT_DIR = Path("data") / "text_by_page"

# ==============================================================================
# PATRONES DE LIMPIEZA (Regex pre-compilados)
# ==============================================================================

# Patrón del Encabezado (Título + ISBN)
# Se usa re.escape para manejar correctamente los guiones y otros caracteres especiales.
# Se añade '\s*' entre los elementos para permitir espacios/saltos de línea variables.
HEADER_PATTERN = re.escape("FUNDAMENTOS DE LA INTELIGENCIA ARTIFICIAL: UNA VISION INTRODUCTORIA") + r'\s*' + \
                 r'ISBN General: \d{3}-\d{3}-\d{4}-\d{2}-\d\s*' + \
                 r'ISBN Tomo 1: \d{3}-\d{3}-\d{4}-\d{2}-\d'
HEADER_REGEX = re.compile(HEADER_PATTERN, re.IGNORECASE | re.DOTALL) # re.DOTALL para que '.' incluya saltos de línea

# Patrón para identificar líneas que contienen solo números arábigos o romanos.
# Buscamos que toda la línea (^) hasta el final ($) contenga solo el número (y espacios opcionales).
LINE_NUMBER_REGEX = re.compile(r'^\s*([IVXLCDM]+|\d{1,3})\s*$', re.MULTILINE)

# ==============================================================================
# FUNCIONES DE EXTRACCIÓN Y LIMPIEZA
# ==============================================================================

def clean_page_text(text: str, page_num: int) -> str:
    """
    Realiza una limpieza avanzada del texto extraído, eliminando el ruido del encabezado
    y los números de pie de página (romanos o arábigos) según el rango de la página.
    """
    
    # --- 1. Eliminación del Encabezado Fijo ---
    # Elimina el patrón de encabezado que incluye el título y los ISBN en cualquier parte del texto.
    text = HEADER_REGEX.sub('', text)

    # --- 2. Eliminación de Pie de Página (Numeración) ---
    
    # Separamos el texto en líneas para poder evaluar la posición de los números.
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Intentamos identificar si la línea contiene SOLO el número de página
        if len(line_stripped) < 10 and LINE_NUMBER_REGEX.search(line):
            
            # Sub-regla 1: Numeración Romana (Páginas 4 a 22 del PDF)
            if 4 <= page_num <= 22:
                # Si la página está en el rango de Romanos y la línea es corta, la saltamos.
                continue 
            
            # Sub-regla 2: Numeración Arábiga (Páginas 23 a 210 del PDF)
            elif 23 <= page_num <= 210:
                # Si la página está en el rango Arábigo y la línea es corta, la saltamos.
                continue
        
        # Si la línea no es un número de página dentro de los rangos de ruido, la conservamos.
        cleaned_lines.append(line)

    # Volvemos a unir las líneas
    text_cleaned = '\n'.join(cleaned_lines).strip()
    
    # --- 3. Normalización ---
    # Eliminar saltos de línea excesivos (mantener un solo salto entre párrafos)
    text_cleaned = re.sub(r'\n\s*\n', '\n', text_cleaned).strip()
    
    return text_cleaned

def extract_all_pages_to_files(pdf_path: Path, output_dir: Path):
    """
    Extrae el texto de *todas* las páginas del PDF, aplica la limpieza y las guarda en archivos separados.
    """
    print(f"\n--- Iniciando Extracción y Limpieza de Producción de {pdf_path.name} ---")
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        #total_pages = 25
        
        for i in range(total_pages):
            page_num = i + 1
            page = doc.load_page(i)
            text_raw = page.get_text("text") 
            
            # Aplicamos la limpieza avanzada usando el número de página
            text_cleaned = clean_page_text(text_raw, page_num)

            # Definir el nombre del archivo de salida: page_001.txt, page_002.txt, etc.
            output_filename = output_dir / f"page_{page_num:03d}.txt" 
            
            # Guardar el texto limpio solo si hay contenido significativo restante
            if text_cleaned:
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(text_cleaned)
            # Si la página queda vacía después de la limpieza (ej. portada, páginas solo de ruido), no se crea archivo
            
            # Progreso en la consola cada 50 páginas
            if page_num % 50 == 0 or page_num == total_pages:
                 print(f"Página {page_num}/{total_pages} procesada y limpia.")

        doc.close()
        print(f"\n✅ Extracción y Limpieza completa. Archivos guardados en {output_dir}")
        
    except Exception as e:
        print(f"ERROR: Fallo durante la extracción de producción: {e}")
        return


def main():
    """Función principal para ejecutar el pipeline de extracción de producción."""
    
    # 1. Verificación Inicial de la Ruta
    if not PDF_PATH.exists():
        print(f"ERROR CRÍTICO: No se encontró el archivo PDF en la ruta: {PDF_PATH}")
        sys.exit(1)
        
    print(f"✅ PDF encontrado en: {PDF_PATH}")
    
    # 2. Crear el directorio de salida si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📂 Archivos de salida irán a: {OUTPUT_DIR}")
    
    # 3. Ejecución de la producción completa
    extract_all_pages_to_files(PDF_PATH, OUTPUT_DIR)
    
    
if __name__ == '__main__':
    main()
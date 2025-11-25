import fitz # Biblioteca PyMuPDF para extracción eficiente de PDF
from tika import parser # Biblioteca para usar Apache Tika (usado en la prueba comparativa)
from pathlib import Path # Módulo estándar para manejo de rutas de archivos
import sys 
import os

# ==============================================================================
# CONFIGURACIÓN DEL PROYECTO
# ==============================================================================

# Ruta relativa al documento PDF de entrada, asumida desde la raíz del proyecto.
PDF_FILENAME = "Intro_IA.pdf"
PDF_PATH = Path("docs") / PDF_FILENAME

# Directorio de salida para los archivos de texto extraídos.
OUTPUT_DIR = Path("data") / "text_by_page"

# Definición de las páginas a procesar para la prueba de la Semana 1.
PAGES_TO_TEST = {1, 2, 3, 4, 5, 6, 7, 8, 9}

# Modo de guardado para los archivos de muestra:
# 1. 'SINGLE_FILE': Guarda todo el texto extraído en un único archivo de muestra. (Recomendado)
# 2. 'PER_PAGE': Guarda cada página extraída en un archivo de muestra separado (page_1.txt, page_2.txt, etc.).
SAVE_MODE = 'SINGLE_FILE' 
SINGLE_OUTPUT_FILENAME = "sample_pages_1-9.txt" # Nuevo nombre para el archivo único

# ==============================================================================
# FUNCIONES DE EXTRACCIÓN
# ==============================================================================

def extract_with_pymupdf(pdf_path: Path, pages_to_test: set) -> str:
    """
    Extrae texto de páginas específicas de un PDF usando PyMuPDF.
    
    Args:
        pdf_path: Objeto Path al archivo PDF.
        pages_to_test: Conjunto de números de página a extraer (ej: {1, 2, 3, ...}).
        
    Returns:
        Cadena de texto con el contenido de las páginas y sus marcadores.
    """
    print("--- 1. Extracción con PyMuPDF (Pipeline Principal) ---")
    extracted_text = ""
    
    try:
        doc = fitz.open(pdf_path)
        
        for i in range(doc.page_count):
            page_num = i + 1
            
            # Procesar solo las páginas definidas en PAGES_TO_TEST
            if page_num in pages_to_test:
                page = doc.load_page(i)
                # 'text' es el método de extracción estándar y confiable
                text = page.get_text("text") 
                
                # Advertencia si la página está vacía (común en portadas)
                if not text.strip():
                    print(f"ATENCIÓN: La página {page_num} está vacía o es solo espacios. (Esperado para portadas/imágenes)")
                
                # Formatear el texto con un marcador claro de inicio de página
                extracted_text += f"\n\n=====[START_PAGE_{page_num}]=====\n{text}"

        doc.close()
        return extracted_text
        
    except Exception as e:
        print(f"ERROR: Fallo crítico en PyMuPDF: {e}")
        return f"Error de extracción: {e}"


def extract_with_tika(pdf_path: Path) -> str:
    """
    Extrae todo el texto de un PDF usando Apache Tika (prueba comparativa).
    
    Args:
        pdf_path: Objeto Path al archivo PDF.
        
    Returns:
        Cadena de texto con el contenido completo.
    """
    print("\n--- 2. Extracción con Tika (Prueba de Robustez) ---")
    try:
        # Tika inicia su servidor si no está activo.
        parsed = parser.from_file(str(pdf_path)) # Tika requiere la ruta como string
        return parsed.get('content', 'Contenido no encontrado por Tika.')
    except Exception as e:
        return f"Error con Tika: {e}. ¿Está el servidor Tika iniciado?"


def save_samples(extracted_text: str, mode: str):
    """Guarda el texto extraído según el modo de guardado configurado."""
    
    if mode == 'SINGLE_FILE':
        # Opción 1: Guardar todo el texto con marcadores de página en un único archivo
        output_file = OUTPUT_DIR / SINGLE_OUTPUT_FILENAME
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(extracted_text.strip())
        print(f"\nMuestra guardada: {output_file} (Formato: SINGLE_FILE con marcadores)")
    
    elif mode == 'PER_PAGE':
        # Opción 2: Guardar cada página en un archivo separado (similar al entregable anterior)
        # Esto es más complejo ya que requeriría re-ejecutar la extracción para obtener el texto por separado.
        # Por simplicidad y al haber texto en las páginas 2 y 3, el modo SINGLE_FILE es más representativo.
        print("\nEl modo 'PER_PAGE' no es la mejor opción en este script de prueba. Usando SINGLE_FILE.")
        save_samples(extracted_text, 'SINGLE_FILE')
    
    else:
        print(f"ERROR: Modo de guardado '{mode}' no reconocido.")


def main():
    """Función principal para la ejecución de la prueba de extracción."""
    
    # 1. Verificación Inicial de la Ruta
    if not PDF_PATH.exists():
        print(f"ERROR CRÍTICO: No se encontró el archivo PDF en la ruta: {PDF_PATH}")
        sys.exit(1)
        
    print(f"PDF encontrado en: {PDF_PATH}\n")
    
    # Crear el directorio de salida si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Ejecución de la Prueba (PyMuPDF - Pipeline Seleccionado)
    pymu_output = extract_with_pymupdf(PDF_PATH, PAGES_TO_TEST)
    
    # 3. Guardado del Entregable de Muestra
    save_samples(pymu_output, SAVE_MODE)
    
    # 4. Resultados de la Prueba y Decisión
    print("\n" + "="*70)
    print(f">>> REPORTE DE EXTRACCIÓN DE PRUEBA (Páginas: {PAGES_TO_TEST}) <<<")
    print("="*70)
    print("\n[SALIDA PYMUPDF COMPLETA (con marcadores de página)]")
    # Mostrar solo los primeros 1500 caracteres para no saturar la consola
    print(pymu_output[:1500] + "...") 
    
    # Opcional: Ejecutar Tika para comparación
    # tika_output = extract_with_tika(PDF_PATH)
    # print("\n[SALIDA DE TIKA (Primeros 1000 caracteres)]")
    # print(tika_output[:1000]) 
    
    print("\n--- RESUMEN DE ENTREGA DE MUESTRA ---")
    print("El archivo de prueba de la Semana 1 ha sido generado.")
    print("Confirmar la legibilidad de la salida para proceder con la Semana 2 (Chunking).")
    
if __name__ == '__main__':
    main()
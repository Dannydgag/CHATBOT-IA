import fitz  # PyMuPDF: Biblioteca principal para la extracción de PDF
from pathlib import Path 
import re 

# ==============================================================================
# 1. CONFIGURACIÓN DE RUTAS Y CONSTANTES
# ==============================================================================
# Definimos las rutas de entrada y salida utilizando Path para compatibilidad entre SO
PDF_PATH = Path("data") / "pdf" / "Intro_IA.pdf"
OUTPUT_DIR = Path("data") / "text_by_page"

# Lista de palabras clave para identificar y eliminar el encabezado del libro
# Se eliminan líneas que contengan estos textos para limpiar ruido de ISBN y títulos repetitivos
HEADER_KEYWORDS = [
    "FUNDAMENTOS DE LA INTELIGENCIA ARTIFICIAL",
    "UNA VISION INTRODUCTORIA",
    "ISBN General",
    "ISBN Tomo"
]

# Expresión regular para detectar numeración de página (árabes y romanos)
# Detecta números del 1 al 999 o números romanos (I, II, V, X, etc.) que están solos en una línea
CLEAN_NUMS_REGEX = re.compile(r'^\s*([MDCLXVI]+|\d{1,3})\s*$', re.MULTILINE)

# Expresión regular para detectar jerarquías de títulos (Niveles 1, 2 y 3)
# Ejemplos válidos: "1", "1.1", "1.1.1"
NUM_SEC_REGEX = re.compile(r'^\d+(\.\d+){0,2}$') 

# Patrón para ignorar etiquetas de figuras, tablas y gráficos
# Evita que las descripciones de imágenes sean procesadas como títulos o texto principal
IGNORE_LABELS = re.compile(r'^(Figura|Tabla|Gráfico|Imagen|Ilustración)\s+\d+', re.IGNORECASE)

# ==============================================================================
# 2. FUNCIONES DE APOYO
# ==============================================================================

def is_bold(span):
    """
    Determina si un fragmento de texto (span) está en negrita.
    Verifica tanto los metadatos técnicos (flags) como el nombre de la fuente.
    """
    return (span['flags'] & 2) or ("bold" in span['font'].lower())

# ==============================================================================
# 3. PROCESO PRINCIPAL DE EXTRACCIÓN
# ==============================================================================

def run_extraction_pipeline(pdf_path, output_dir):
    """
    Ejecuta el pipeline de extracción: lectura, limpieza, unión de títulos y guardado.
    """
    try:
        doc = fitz.open(pdf_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🚀 Iniciando extracción...")

        for page_num, page in enumerate(doc, start=1):
            # Obtenemos el contenido de la página en formato diccionario para analizar estilos
            blocks = page.get_text("dict")["blocks"]
            raw_lines = []

            # --- PASO 1: EXTRACCIÓN Y LIMPIEZA INICIAL ---
            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        line_text = ""
                        bold_found = False
                        
                        # Analizamos cada fragmento de la línea para detectar negritas
                        for s in l["spans"]:
                            if s["text"].strip():
                                line_text += s["text"]
                                if is_bold(s): bold_found = True
                        
                        line_text = line_text.strip()
                        if not line_text: continue

                        # Filtrar encabezados (ISBN) y numeración de página
                        if any(key in line_text for key in HEADER_KEYWORDS): continue
                        if CLEAN_NUMS_REGEX.match(line_text): continue

                        raw_lines.append({"text": line_text, "bold": bold_found})

            # --- PASO 2: IDENTIFICACIÓN DE TÍTULOS Y REPARACIÓN DE FORMATO ---
            final_lines = []
            i = 0
            while i < len(raw_lines):
                curr = raw_lines[i]
                txt = curr["text"]

                # Si la línea está en negrita y no es una etiqueta de figura...
                if curr["bold"] and not IGNORE_LABELS.match(txt):
                    
                    # CASO 1: Reparación de Título Nivel 1 Pegado (Ej: "1INTRODUCCIÓN")
                    # Busca un número de sección seguido de letras sin espacio
                    match_pegado = re.match(r'^(\d+(\.\d+){0,2})([A-ZÁÉÍÓÚ].*)', txt)
                    if match_pegado:
                        num_part = match_pegado.group(1)
                        text_part = match_pegado.group(3)
                        final_lines.append(f"[TITLE]: {num_part} {text_part}")
                        i += 1
                        continue

                    # CASO 2: Unión de Títulos Fragmentados (Número en una línea, Texto en la siguiente)
                    if i + 1 < len(raw_lines):
                        next_l = raw_lines[i+1]
                        if NUM_SEC_REGEX.match(txt) and next_l["bold"]:
                            # Unimos e insertamos el espacio de separación solicitado
                            final_lines.append(f"[TITLE]: {txt} {next_l['text']}")
                            i += 2
                            continue
                    
                    # CASO 3: Título ya bien formateado (Ej: "1.1.1 Propiedades")
                    if re.match(r'^\d+(\.\d+){0,2}\s+[A-ZÁÉÍÓÚ]', txt):
                        final_lines.append(f"[TITLE]: {txt}")
                        i += 1
                        continue

                    # --- CASO DESHABILITADO: Títulos por Mayúsculas (Para evitar ruido de tablas) ---
                    # elif txt.isupper() and 5 < len(txt) < 60:
                    #     final_lines.append(f"[TITLE]: {txt}")
                    
                    final_lines.append(txt)
                else:
                    final_lines.append(txt)
                i += 1

            # --- PASO 3: GUARDADO DE RESULTADOS ---
            # Unimos las líneas y limpiamos espacios sobrantes
            page_content = "\n".join(final_lines).strip()
            
            # Solo guardamos si la página tiene contenido real (evita páginas de ruido)
            if len(page_content) > 35:
                output_file = output_dir / f"page_{page_num:03d}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(page_content)

        doc.close()
        print(f"✅ Proceso completado: Archivos estructurados en '{output_dir}'")
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")

# ==============================================================================
# 4. EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    run_extraction_pipeline(PDF_PATH, OUTPUT_DIR)
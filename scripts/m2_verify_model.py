# ----------------------------------------------------------------------
# OBJETIVO: Generar un vector numérico (Embedding) a partir de texto.
# Esto confirmará que el modelo se descarga y funciona
# ----------------------------------------------------------------------
# Este script carga el modelo de lenguaje pre-entrenado 'all-MiniLM-L6-v2' 
# de la librería sentence-transformers.
# La función principal es convertir la frase o palabra de entrada ('prueba' en este caso)
# en su representación vectorial (embedding), que es un array de números.
# El shape (1, 384 para este modelo) indica las dimensiones del vector resultante,
# usado comúnmente en tareas de búsqueda semántica o clasificación.
# ----------------------------------------------------------------------
from sentence_transformers import SentenceTransformer
m = SentenceTransformer('all-MiniLM-L6-v2')
print('Model loaded:', m.__class__.__name__)
# ejemplo: inferir embedding de prueba
emb = m.encode(['prueba'])
print('Embedding shape:', emb.shape)
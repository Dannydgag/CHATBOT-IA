# Embeddings Generados

Este documento explica los embeddings generados a partir de los fragmentos de texto (chunks) procesados en el proyecto.

## ¿Qué es un embedding?

Un embedding es una representación vectorial de un texto en un espacio de alta dimensión. El modelo `all-MiniLM-L6-v2` ha sido utilizado para generar estos embeddings, lo que nos permite representar el contenido semántico de los textos en forma numérica. Estos vectores son útiles para tareas como la búsqueda semántica, donde buscamos fragmentos de texto relevantes en base a su similitud semántica.

## Detalles de los Embeddings

- **Modelo utilizado**: `all-MiniLM-L6-v2`
- **Dimensiones del embedding**: 384
  - Cada embedding tiene 384 valores numéricos, que representan las características semánticas del texto.
- **Cantidad de embeddings generados**: 50
  - El número de embeddings generados fue 50, ya que se seleccionaron 50 chunks para la prueba. Si se desean generar más embeddings, se debe ajustar el parámetro `--sample_n`.
- **Archivo de embeddings**: `models/embeddings_sample.npy`
  - Este archivo contiene los 50 embeddings generados.
- **Archivo de IDs**: `models/embeddings_sample_ids.json`
  - Este archivo contiene los identificadores de los chunks de texto procesados, los cuales nos permiten mapear los embeddings con los textos originales.

## ¿Cómo se generaron los embeddings?

Los embeddings fueron generados utilizando el modelo `all-MiniLM-L6-v2`, un modelo preentrenado de la biblioteca `sentence-transformers`. Este modelo convierte los textos en vectores de 384 dimensiones, que capturan el significado semántico de cada fragmento de texto.

Los textos de entrada fueron cargados desde el archivo `data/chunks/chunks.cleaned.jsonl`, y un total de 50 fragmentos fueron procesados como muestra.

## Uso de los embeddings

Los embeddings generados serán utilizados para tareas de búsqueda semántica. Dado un texto de consulta, se puede buscar entre estos embeddings para encontrar los fragmentos de texto más relevantes. Para ello, se utilizarán técnicas de similitud de coseno entre los embeddings de las consultas y los embeddings de los fragmentos de texto.


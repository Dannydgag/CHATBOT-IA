# Pipeline Spec — Orquestación (Xander)
Versión: 0.1
Fecha: 2025-11-24

## Visión general
El pipeline orquesta la transformación:
PDF -> text_by_page -> chunks -> embeddings -> index -> retrieval API

## Componentes y responsabilidades
- **Extractor (Erik)**: `scripts/extract_text.py`
  - Entrada: `pdf_path: str`
  - Salida: carpeta `data/text_by_page/` con `page_{n}.txt`
- **Chunker (Erik / Xander)**: `orchestration/chunk_pipeline.py`
  - Entrada: `text_by_page/` o `pdf_path`
  - Salida: `data/chunks/chunks.jsonl` con objetos:
    `{ "id": str, "page": int, "start": int, "end": int, "text": str, "title": optional str }`
- **Embeddings (Mateo)**: `scripts/generate_embeddings.py`
  - Entrada: `chunks.jsonl`
  - Salida: `models/embeddings.npy` + mapping `chunks_to_ids.json`
- **Index (Mateo)**: `index/build_index.py`
  - Entrada: `embeddings.npy`, `chunks.jsonl`
  - Salida: `index/faiss.index`
- **Retrieval API (Xander)**: `orchestration/retrieval_api.py`
  - Funciones: `retrieve(query: str, top_k: int) -> List[Dict]`

## Contratos
- `get_chunks_from_pdf(pdf_path, chunk_size=500, overlap=50)`
- `generate_embeddings(chunks)`
- `build_index(embeddings, metadata)`
- `retrieve(query)`

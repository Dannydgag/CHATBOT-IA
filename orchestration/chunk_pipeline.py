import json
from pathlib import Path

CHUNKS_PATH = Path("data/chunks/chunks.jsonl")

def load_chunks(chunks_path: Path = CHUNKS_PATH) -> list:
    """Carga todos los chunks generados por chunk_text.py."""
    chunks = []
    if not chunks_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {chunks_path}")
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks

def get_chunks_by_page(page_number: int, chunks: list = None) -> list:
    """Filtra chunks por número de página."""
    if chunks is None:
        chunks = load_chunks()
    return [c for c in chunks if c.get("metadata", {}).get("page_number") == page_number]

if __name__ == "__main__":
    all_chunks = load_chunks()
    print(f"Chunks cargados: {len(all_chunks)}")
    print(get_chunks_by_page(1)[:2])

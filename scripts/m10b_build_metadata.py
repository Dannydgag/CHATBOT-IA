import json
from pathlib import Path
#python scripts/m12_build_tfidf.py --chunks data/chunks/chunks.cleaned.jsonl --out_dir index


CHUNKS_FILE = Path("data/chunks/chunks.cleaned.jsonl")
OUT_FILE = Path("index/metadata.json")

def main():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"No existe {CHUNKS_FILE}")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    metadata = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            obj = json.loads(line)
            metadata.append({
                "index_pos": i,
                "id": obj["id"],
                "page": obj.get("page")
            })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"metadata.json generado correctamente")
    print(f"Total entradas: {len(metadata)}")

if __name__ == "__main__":
    main()

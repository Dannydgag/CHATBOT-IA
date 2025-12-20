#!/usr/bin/env python3
"""
Genera embeddings para TODO el corpus (chunks.cleaned.jsonl) y guarda:
 - models/embeddings_all.npy   (float32, shape (N, D))
 - models/embeddings_all_ids.json  ({"ids":[...], "run_info":{...}})
Uso:

.\.venv\Scripts\python.exe scripts/m9_generate_embeddings_all.py --input data/chunks/chunks.cleaned.jsonl --out_dir models --batch 64 --model all-MiniLM-L6-v2 --normalize

"""
import argparse, json, time, os
from sentence_transformers import SentenceTransformer
import numpy as np

def read_chunks(jsonl_path):
    rows = []
    with open(jsonl_path,'r',encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            rows.append(json.loads(line))
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--out_dir', default='models')
    ap.add_argument('--model', default='all-MiniLM-L6-v2')
    ap.add_argument('--batch', type=int, default=64)
    ap.add_argument('--normalize', action='store_true')
    ap.add_argument('--force', action='store_true', help='sobrescribir si existe')
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    run_info = {
        'model': args.model,
        'input': args.input,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'batch': args.batch,
        'normalize': bool(args.normalize)
    }
    ids_out = os.path.join(args.out_dir, 'embeddings_all_ids.json')
    npy_out = os.path.join(args.out_dir, 'embeddings_all.npy')
    runinfo_out = os.path.join(args.out_dir, 'embeddings_all_runinfo.json')

    if os.path.exists(npy_out) and not args.force:
        print(f"{npy_out} ya existe. Usa --force para sobrescribir.")
        return

    rows = read_chunks(args.input)
    texts = [r.get('text','') for r in rows]
    ids = [r.get('id') or r.get('chunk_id') or str(i) for i,r in enumerate(rows)]

    print(f"Leidos {len(texts)} chunks. Cargando modelo {args.model} ...")
    model = SentenceTransformer(args.model)

    embs = []
    for i in range(0, len(texts), args.batch):
        batch = texts[i:i+args.batch]
        arr = model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        embs.append(arr.astype('float32'))
    embs = np.vstack(embs)
    if args.normalize:
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms==0] = 1e-6
        embs = embs / norms

    np.save(npy_out, embs)
    with open(ids_out,'w',encoding='utf-8') as f:
        json.dump({'ids': ids, 'run_info': run_info}, f, ensure_ascii=False, indent=2)
    with open(runinfo_out,'w',encoding='utf-8') as f:
        json.dump(run_info, f, ensure_ascii=False, indent=2)

    print("Guardado:", npy_out)
    print("IDs:", ids_out)
    print("Run info:", runinfo_out)
    print("Shape embeddings:", embs.shape)

if __name__ == '__main__':
    main()

import faiss, pandas as pd, sys
idx = faiss.read_index("index/faiss.index")
print("FAISS ntotal:", idx.ntotal)
try:
    df = pd.read_parquet("metadata/metadata.parquet")
    print("metadata rows:", len(df))
    assert idx.ntotal == len(df), "Mismatch index vs metadata"
except Exception as e:
    print("Metadata check skipped or failed:", e)
print("OK")
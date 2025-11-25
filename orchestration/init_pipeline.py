# orchestration/init_pipeline.py
import logging
from pathlib import Path
from typing import List, Dict, Optional

LOG_PATH = Path("orchestration/logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class PipelineOrchestrator:
    def __init__(self, workdir: str = "."):
        self.workdir = Path(workdir)
        logging.info("PipelineOrchestrator initialized with workdir=%s", workdir)

    def extract(self, pdf_path: str) -> Path:
        text_dir = self.workdir / "data" / "text_by_page"
        logging.info("extract() called for %s -> %s", pdf_path, text_dir)
        return text_dir

    def chunk(self, text_dir: str, chunk_size: int = 500, overlap: int = 50) -> Path:
        chunks_path = self.workdir / "data" / "chunks" / "chunks.jsonl"
        logging.info("chunk() called for %s -> %s", text_dir, chunks_path)
        return chunks_path

    def generate_embeddings(self, chunks_path: str) -> Path:
        embeddings_path = self.workdir / "models" / "embeddings.npy"
        logging.info("generate_embeddings() called for %s -> %s", chunks_path, embeddings_path)
        return embeddings_path

    def build_index(self, embeddings_path: str, metadata_path: str) -> Path:
        index_path = self.workdir / "index" / "faiss.index"
        logging.info("build_index() called -> %s", index_path)
        return index_path

    def retrieve(self, query: str, top_k: int = 5, score_threshold: Optional[float] = None) -> List[Dict]:
        logging.info("retrieve() called for %s", query)
        return []

if __name__ == "__main__":
    orchestrator = PipelineOrchestrator()
    text_dir = orchestrator.extract("data/sample.pdf")
    chunks = orchestrator.chunk(str(text_dir))
    emb = orchestrator.generate_embeddings(str(chunks))
    idx = orchestrator.build_index(str(emb), str(chunks))
    print("Pipeline init done. index at:", idx)

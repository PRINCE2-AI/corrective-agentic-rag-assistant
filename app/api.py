from __future__ import annotations

import tempfile
from pathlib import Path

try:
    from fastapi import FastAPI, File, UploadFile
except ImportError as exc:
    raise RuntimeError(
        "FastAPI is not installed. Run `pip install -r requirements.txt` before starting the API."
    ) from exc

from app.config import settings
from app.graph import run_query
from app.ingestion import ingest_paths
from app.metrics import metrics_store
from app.schemas import IngestResult, QueryRequest, QueryResponse


api = FastAPI(title="Corrective Agentic RAG Assistant", version="0.1.0")


@api.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "ollama_base_url": settings.ollama_base_url,
        "tavily_enabled": bool(settings.tavily_api_key),
        "index_path": str(settings.resolved_chroma_path),
    }


@api.post("/ingest", response_model=IngestResult)
async def ingest(files: list[UploadFile] = File(...)) -> IngestResult:
    temp_paths: list[Path] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded in files:
            path = Path(temp_dir) / uploaded.filename
            path.write_bytes(await uploaded.read())
            temp_paths.append(path)
        return ingest_paths(temp_paths)


@api.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    return run_query(request)


@api.post("/evaluate")
def evaluate(questions: list[str]) -> list[QueryResponse]:
    return [run_query(QueryRequest(question=question)) for question in questions]


@api.get("/metrics")
def metrics() -> dict[str, object]:
    return metrics_store.snapshot()

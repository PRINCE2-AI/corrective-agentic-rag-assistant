from __future__ import annotations

import uuid
from pathlib import Path

from pypdf import PdfReader

from app.config import settings
from app.retrieval import retriever
from app.schemas import DocumentChunk, IngestResult


def chunk_text(
    text: str,
    source: str,
    page: int | None = None,
    chunk_size: int = 180,
    overlap: int = 35,
) -> list[DocumentChunk]:
    words = text.split()
    if not words:
        return []

    chunks: list[DocumentChunk] = []
    step = max(chunk_size - overlap, 1)
    for start in range(0, len(words), step):
        window = words[start : start + chunk_size]
        if window:
            chunks.append(
                DocumentChunk(
                    id=f"{Path(source).stem}-{page or 0}-{start}-{uuid.uuid4().hex[:8]}",
                    text=" ".join(window),
                    source=source,
                    page=page,
                )
            )
    return chunks


def load_file(path: Path) -> list[DocumentChunk]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        chunks: list[DocumentChunk] = []
        for index, page in enumerate(reader.pages, start=1):
            chunks.extend(chunk_text(page.extract_text() or "", path.name, page=index))
        return chunks
    if suffix in {".txt", ".md"}:
        return chunk_text(path.read_text(encoding="utf-8"), path.name)
    raise ValueError(f"Unsupported file type: {suffix}")


def ingest_paths(paths: list[Path]) -> IngestResult:
    chunks: list[DocumentChunk] = []
    for path in paths:
        chunks.extend(load_file(path))
    retriever.add_documents(chunks)
    return IngestResult(
        document_ids=sorted({chunk.source for chunk in chunks}),
        chunk_count=len(chunks),
        index_path=str(settings.resolved_chroma_path),
        status="indexed",
    )


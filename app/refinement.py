from __future__ import annotations

import re

from app.evaluator import score_chunks
from app.schemas import DocumentChunk


def split_into_strips(chunk: DocumentChunk) -> list[DocumentChunk]:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", chunk.text) if part.strip()]
    if len(sentences) <= 2:
        return [chunk]

    strips: list[DocumentChunk] = []
    for index in range(0, len(sentences), 2):
        text = " ".join(sentences[index : index + 2])
        strips.append(
            DocumentChunk(
                id=f"{chunk.id}:strip:{index // 2}",
                text=text,
                source=chunk.source,
                page=chunk.page,
                metadata={**chunk.metadata, "parent_chunk": chunk.id},
            )
        )
    return strips


def refine_context(query: str, chunks: list[DocumentChunk], top_k: int = 5, threshold: float = -0.5) -> list[DocumentChunk]:
    strips: list[DocumentChunk] = []
    for chunk in chunks:
        strips.extend(split_into_strips(chunk))

    scored = score_chunks(query, strips)
    filtered = [strip for strip in scored if strip.score >= threshold]
    return filtered[:top_k] if filtered else scored[: min(top_k, len(scored))]


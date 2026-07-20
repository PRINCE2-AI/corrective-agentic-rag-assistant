from __future__ import annotations

from collections import defaultdict

from app.schemas import DocumentChunk


def summarize_text(text: str, max_words: int = 80) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " ..."


def build_hierarchical_summaries(chunks: list[DocumentChunk]) -> list[DocumentChunk]:
    by_source: dict[str, list[DocumentChunk]] = defaultdict(list)
    for chunk in chunks:
        by_source[chunk.source].append(chunk)

    summaries: list[DocumentChunk] = []
    for source, source_chunks in by_source.items():
        combined = " ".join(chunk.text for chunk in source_chunks)
        summaries.append(
            DocumentChunk(
                id=f"{source}:document-summary",
                text=summarize_text(combined, 140),
                source=source,
                metadata={"level": "document_summary"},
            )
        )
        for index in range(0, len(source_chunks), 4):
            section_chunks = source_chunks[index : index + 4]
            section_text = " ".join(chunk.text for chunk in section_chunks)
            summaries.append(
                DocumentChunk(
                    id=f"{source}:section-summary:{index // 4}",
                    text=summarize_text(section_text, 100),
                    source=source,
                    metadata={"level": "section_summary"},
                )
            )
    return summaries


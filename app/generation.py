from __future__ import annotations

import requests

from app.config import settings
from app.schemas import DocumentChunk, WebSource


def _context_lines(chunks: list[DocumentChunk], web_sources: list[WebSource]) -> list[str]:
    lines: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        lines.append(f"[L{index}] {chunk.text} (source: {chunk.source})")
    for index, source in enumerate(web_sources, start=1):
        if source.url:
            lines.append(f"[W{index}] {source.content} (source: {source.url})")
    return lines


def generate_answer(question: str, chunks: list[DocumentChunk], web_sources: list[WebSource]) -> tuple[str, list[str]]:
    context = _context_lines(chunks, web_sources)
    citations = [chunk.source for chunk in chunks]
    citations.extend(source.url for source in web_sources if source.url)
    citations = list(dict.fromkeys(citations))

    if not context:
        return "I do not have enough reliable evidence to answer this. Add documents or enable web search.", citations

    prompt = (
        "Answer using only the evidence below. Cite sources by name or URL. "
        "If evidence is weak, say what is missing.\n\n"
        f"Question: {question}\n\nEvidence:\n" + "\n".join(context)
    )

    try:
        response = requests.post(
            f"{settings.ollama_base_url}/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            timeout=45,
        )
        if response.ok:
            answer = response.json().get("response", "").strip()
            if answer:
                return answer, citations
    except requests.RequestException:
        pass

    preview = " ".join(line.split("]", 1)[-1].strip() for line in context[:3])
    return (
        f"Based on the available evidence, {preview[:650]}\n\n"
        "Local generation fallback was used because Ollama did not respond.",
        citations,
    )


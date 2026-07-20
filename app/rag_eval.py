from __future__ import annotations

from app.evaluator import lexical_relevance, tokenize
from app.schemas import DocumentChunk, EvalMetrics, WebSource


def _clip(score: float) -> float:
    return round(max(0.0, min(1.0, score)), 3)


def evaluate_answer(
    question: str,
    answer: str,
    context: list[DocumentChunk],
    web_sources: list[WebSource],
    latency_ms: int,
) -> EvalMetrics:
    context_text = " ".join(chunk.text for chunk in context)
    context_text += " " + " ".join(source.content for source in web_sources if source.url)
    context_relevance = (lexical_relevance(question, context_text) + 1) / 2
    answer_relevance = (lexical_relevance(question, answer) + 1) / 2
    answer_tokens = set(tokenize(answer))
    context_tokens = set(tokenize(context_text))
    faithfulness = len(answer_tokens & context_tokens) / max(len(answer_tokens), 1)
    citation_count = len(context) + len([source for source in web_sources if source.url])

    return EvalMetrics(
        context_relevance=_clip(context_relevance),
        answer_faithfulness=_clip(faithfulness),
        answer_relevance=_clip(answer_relevance),
        citation_coverage=1.0 if citation_count and context_text.strip() else 0.0,
        latency_ms=latency_ms,
    )


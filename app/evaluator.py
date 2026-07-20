from __future__ import annotations

import math
import re
from collections import Counter

from app.config import settings
from app.schemas import CragAction, DocumentChunk


STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "then",
    "is",
    "are",
    "was",
    "were",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "by",
    "as",
    "from",
    "what",
    "why",
    "how",
    "which",
    "who",
    "when",
}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    ]


def lexical_relevance(query: str, text: str) -> float:
    query_tokens = tokenize(query)
    text_tokens = tokenize(text)
    if not query_tokens or not text_tokens:
        return -1.0

    query_counts = Counter(query_tokens)
    text_counts = Counter(text_tokens)
    overlap = sum(min(query_counts[token], text_counts[token]) for token in query_counts)
    recall = overlap / max(len(query_tokens), 1)
    precision = overlap / max(len(set(text_tokens)), 1)
    coverage_bonus = min(len(set(query_tokens) & set(text_tokens)) / max(len(set(query_tokens)), 1), 1.0)
    raw = (0.55 * recall) + (0.25 * precision) + (0.20 * coverage_bonus)
    return round((2 / (1 + math.exp(-5 * raw))) - 1, 3)


def score_chunks(query: str, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
    scored: list[DocumentChunk] = []
    for chunk in chunks:
        score = max(-1.0, min(1.0, lexical_relevance(query, chunk.text) + chunk.score))
        scored.append(chunk.model_copy(update={"score": score}))
    return sorted(scored, key=lambda chunk: chunk.score, reverse=True)


def route_action(scored_chunks: list[DocumentChunk]) -> tuple[CragAction, float]:
    if not scored_chunks:
        return CragAction.INCORRECT, -1.0

    best = max(chunk.score for chunk in scored_chunks)
    if best >= settings.crag_upper_threshold:
        return CragAction.CORRECT, best
    if all(chunk.score <= settings.crag_lower_threshold for chunk in scored_chunks):
        return CragAction.INCORRECT, best
    return CragAction.AMBIGUOUS, best

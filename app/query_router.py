from __future__ import annotations

import re

from app.schemas import QueryType


CURRENT_TERMS = {
    "latest",
    "current",
    "today",
    "now",
    "recent",
    "2025",
    "2026",
    "news",
    "price",
}

MULTI_HOP_TERMS = {
    "compare",
    "versus",
    "vs",
    "difference",
    "relationship",
    "why",
    "how",
    "impact",
    "tradeoff",
    "pros and cons",
    "steps",
}

LONG_CONTEXT_TERMS = {
    "summarize",
    "overview",
    "entire",
    "whole",
    "document",
    "report",
    "paper",
    "chapter",
    "section",
}


def classify_query(question: str) -> QueryType:
    normalized = question.lower().strip()
    tokens = re.findall(r"[a-z0-9]+", normalized)
    token_set = set(tokens)

    if token_set & CURRENT_TERMS:
        return QueryType.WEB_NEEDED
    if any(term in normalized for term in LONG_CONTEXT_TERMS) or len(tokens) > 35:
        return QueryType.LONG_CONTEXT
    if any(term in normalized for term in MULTI_HOP_TERMS) or normalized.count("?") > 1:
        return QueryType.MULTI_HOP
    if len([token for token in tokens if token[:1].isalpha()]) > 18:
        return QueryType.MULTI_HOP
    return QueryType.SIMPLE


def retrieval_depth_for(query_type: QueryType) -> int:
    return {
        QueryType.SIMPLE: 5,
        QueryType.MULTI_HOP: 9,
        QueryType.LONG_CONTEXT: 12,
        QueryType.WEB_NEEDED: 5,
    }[query_type]


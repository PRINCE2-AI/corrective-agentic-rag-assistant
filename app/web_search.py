from __future__ import annotations

import requests

from app.config import settings
from app.evaluator import lexical_relevance
from app.schemas import WebSource


def rewrite_for_search(question: str) -> str:
    cleaned = question.replace("?", " ").replace("!", " ")
    words = [word.strip(",. ") for word in cleaned.split() if len(word.strip(",. ")) > 2]
    return " ".join(words[:12])


def search_web(question: str, max_results: int = 5) -> list[WebSource]:
    if not settings.tavily_api_key:
        return [
            WebSource(
                title="Web search disabled",
                url="",
                content="Set TAVILY_API_KEY in .env to enable live corrective web search.",
                score=-1.0,
            )
        ]

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": settings.tavily_api_key,
            "query": rewrite_for_search(question),
            "max_results": max_results,
            "include_answer": False,
        },
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    sources: list[WebSource] = []
    for result in payload.get("results", []):
        content = result.get("content", "")
        sources.append(
            WebSource(
                title=result.get("title", "Untitled"),
                url=result.get("url", ""),
                content=content,
                score=lexical_relevance(question, content),
            )
        )
    return sorted(sources, key=lambda source: source.score, reverse=True)


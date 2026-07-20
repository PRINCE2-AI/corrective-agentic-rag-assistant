from __future__ import annotations

import time

from app.config import settings
from app.evaluator import route_action, score_chunks
from app.generation import generate_answer
from app.metrics import metrics_store
from app.query_router import classify_query, retrieval_depth_for
from app.rag_eval import evaluate_answer
from app.refinement import refine_context
from app.retrieval import retriever
from app.schemas import CragAction, QueryRequest, QueryResponse, QueryType, RagMode, WebSource
from app.web_search import search_web


def run_query(request: QueryRequest) -> QueryResponse:
    started = time.perf_counter()
    trace: list[str] = []
    query_type = classify_query(request.question) if request.mode == RagMode.ADAPTIVE_CRAG else QueryType.SIMPLE
    top_k = retrieval_depth_for(query_type)
    trace.append(f"query_type={query_type.value}, top_k={top_k}")

    retrieved = retriever.retrieve(
        request.question,
        top_k=top_k,
        query_type=query_type,
        simulate_bad_retrieval=request.simulate_bad_retrieval,
    )
    scored = score_chunks(request.question, retrieved)
    trace.append(f"retrieved={len(scored)}")

    if request.mode == RagMode.BASELINE:
        action = CragAction.CORRECT
        confidence = scored[0].score if scored else -1.0
        refined = scored[: settings.default_top_k]
        web_sources: list[WebSource] = []
    else:
        action, confidence = route_action(scored)
        trace.append(f"action={action.value}, confidence={confidence}")
        if action == CragAction.CORRECT:
            refined = refine_context(request.question, scored)
            web_sources = []
        elif action == CragAction.INCORRECT:
            refined = []
            web_sources = search_web(request.question) if request.use_web else []
        else:
            refined = refine_context(request.question, scored)
            web_sources = search_web(request.question) if request.use_web else []

    answer, citations = generate_answer(request.question, refined, web_sources)
    latency_ms = int((time.perf_counter() - started) * 1000)
    eval_metrics = evaluate_answer(request.question, answer, refined, web_sources, latency_ms)
    metrics_store.record(action, eval_metrics)

    return QueryResponse(
        answer=answer,
        mode=request.mode,
        query_type=query_type,
        action=action,
        confidence=round(confidence, 3),
        citations=citations,
        retrieved_chunks=scored,
        refined_context=refined,
        web_sources=web_sources,
        metrics=eval_metrics,
        trace=trace,
    )


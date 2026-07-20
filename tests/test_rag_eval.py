from app.rag_eval import evaluate_answer
from app.schemas import DocumentChunk


def test_eval_metrics_are_bounded():
    metrics = evaluate_answer(
        "What is CRAG?",
        "CRAG evaluates retrieval quality before answering.",
        [DocumentChunk(id="1", text="CRAG evaluates retrieval quality before generation.", source="paper")],
        [],
        latency_ms=10,
    )
    assert 0 <= metrics.context_relevance <= 1
    assert 0 <= metrics.answer_faithfulness <= 1
    assert metrics.latency_ms == 10


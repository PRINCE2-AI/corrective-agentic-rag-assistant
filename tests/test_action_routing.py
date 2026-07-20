from app.evaluator import route_action, score_chunks
from app.schemas import CragAction, DocumentChunk


def test_relevant_context_routes_correct():
    chunks = [DocumentChunk(id="1", text="CRAG uses retrieval evaluator corrective retrieval augmented generation.", source="x")]
    scored = score_chunks("What does CRAG use for retrieval?", chunks)
    action, confidence = route_action(scored)
    assert action == CragAction.CORRECT
    assert confidence >= 0.5


def test_empty_context_routes_incorrect():
    action, confidence = route_action([])
    assert action == CragAction.INCORRECT
    assert confidence == -1.0


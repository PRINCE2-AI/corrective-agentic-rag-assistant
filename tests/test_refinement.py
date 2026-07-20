from app.refinement import refine_context
from app.schemas import DocumentChunk


def test_refinement_keeps_relevant_strips_first():
    chunk = DocumentChunk(
        id="doc-1",
        source="doc",
        text=(
            "CRAG evaluates retrieved documents before generation. "
            "It can trigger web search when retrieval fails. "
            "Bananas are yellow and unrelated to RAG. "
            "Corrective generation reduces unsupported answers."
        ),
    )
    refined = refine_context("How does CRAG handle retrieval failure?", [chunk], top_k=2)
    assert refined
    assert "CRAG" in refined[0].text or "retrieval" in refined[0].text


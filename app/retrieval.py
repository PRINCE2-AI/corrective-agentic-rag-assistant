from __future__ import annotations

from dataclasses import dataclass, field

from app.evaluator import score_chunks, tokenize
from app.hierarchical_index import build_hierarchical_summaries
from app.schemas import DocumentChunk, QueryType


@dataclass
class InMemoryHybridRetriever:
    chunks: list[DocumentChunk] = field(default_factory=list)
    hierarchy: list[DocumentChunk] = field(default_factory=list)

    def add_documents(self, chunks: list[DocumentChunk]) -> None:
        self.chunks.extend(chunks)
        self.hierarchy = build_hierarchical_summaries(self.chunks)

    def retrieve(
        self,
        query: str,
        top_k: int,
        query_type: QueryType,
        simulate_bad_retrieval: bool = False,
    ) -> list[DocumentChunk]:
        candidates = list(self.chunks)
        if query_type == QueryType.LONG_CONTEXT:
            candidates = self.hierarchy + candidates

        if simulate_bad_retrieval:
            candidates = [
                DocumentChunk(
                    id="simulated-noise",
                    text="This unrelated chunk discusses gardening, sports scores, and cooking recipes.",
                    source="retrieval_failure_simulation",
                )
            ] + candidates[: max(1, top_k - 1)]

        query_terms = set(tokenize(query))
        boosted: list[DocumentChunk] = []
        for chunk in candidates:
            term_hits = len(query_terms & set(tokenize(chunk.text)))
            boosted.append(chunk.model_copy(update={"score": chunk.score + (0.05 * term_hits)}))

        return score_chunks(query, boosted)[:top_k]


retriever = InMemoryHybridRetriever()


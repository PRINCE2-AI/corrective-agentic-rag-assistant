from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class QueryType(str, Enum):
    SIMPLE = "simple"
    MULTI_HOP = "multi_hop"
    LONG_CONTEXT = "long_context"
    WEB_NEEDED = "web_needed"


class RagMode(str, Enum):
    BASELINE = "baseline_rag"
    CRAG = "crag"
    ADAPTIVE_CRAG = "adaptive_crag"


class CragAction(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    AMBIGUOUS = "ambiguous"


class DocumentChunk(BaseModel):
    id: str
    text: str
    source: str = "unknown"
    page: int | None = None
    score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class WebSource(BaseModel):
    title: str
    url: str
    content: str
    score: float = 0.0


class QueryRequest(BaseModel):
    question: str
    mode: RagMode = RagMode.ADAPTIVE_CRAG
    use_web: bool = True
    simulate_bad_retrieval: bool = False


class IngestResult(BaseModel):
    document_ids: list[str]
    chunk_count: int
    index_path: str
    status: str


class EvalMetrics(BaseModel):
    context_relevance: float = 0.0
    answer_faithfulness: float = 0.0
    answer_relevance: float = 0.0
    citation_coverage: float = 0.0
    latency_ms: int = 0


class QueryResponse(BaseModel):
    answer: str
    mode: RagMode
    query_type: QueryType
    action: CragAction
    confidence: float
    citations: list[str] = Field(default_factory=list)
    retrieved_chunks: list[DocumentChunk] = Field(default_factory=list)
    refined_context: list[DocumentChunk] = Field(default_factory=list)
    web_sources: list[WebSource] = Field(default_factory=list)
    metrics: EvalMetrics = Field(default_factory=EvalMetrics)
    trace: list[str] = Field(default_factory=list)


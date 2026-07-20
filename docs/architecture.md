# Architecture

The project composes four research ideas into a practical local-first RAG app.

## Pipeline

```text
User question
  -> classify query type
  -> retrieve raw chunks or hierarchical summaries
  -> score retrieval quality
  -> route action
  -> refine local evidence and/or search web
  -> generate answer with citations
  -> evaluate answer
```

## Action Routing

- `correct`: local retrieval is strong; refine chunks and answer.
- `incorrect`: local retrieval is weak; discard local context and use web correction.
- `ambiguous`: local context is partly useful; combine refined local evidence with web results.

## Local-First Design

The v1 evaluator uses deterministic lexical relevance so tests and demos work without GPUs or paid APIs. The interfaces are intentionally ready for stronger embeddings, rerankers, and LLM judges.


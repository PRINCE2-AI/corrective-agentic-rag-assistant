# Observability Guide

This project should make RAG behavior inspectable. A reviewer should be able to see why the assistant answered, why it refused, or why it used fallback.

## Trace Fields

Use this trace shape for each query run:

```json
{
  "run_id": "2026-08-11T10-30-00-crag-001",
  "mode": "adaptive_crag",
  "question": "How do Adaptive-RAG routing and CRAG correction work together?",
  "query_type": "multi_hop",
  "retrieval_top_k": 8,
  "retrieval_score": 0.42,
  "crag_action": "ambiguous",
  "refined_strip_count": 5,
  "web_fallback_used": false,
  "citation_count": 3,
  "latency_ms": 0,
  "estimated_cost_usd": 0.0,
  "metrics": {
    "context_relevance": null,
    "answer_faithfulness": null,
    "answer_relevance": null,
    "citation_coverage": null
  }
}
```

Set values to `null` or `0` until a real run records them. Do not publish guessed numbers.

## Dashboard Signals

| Signal | Why it matters |
| --- | --- |
| Query type | Shows whether routing is adapting to the query |
| Retrieval score | Explains local evidence confidence |
| CRAG action | Shows correct, ambiguous, incorrect, or fallback decision |
| Selected chunks | Lets reviewers inspect retrieved evidence |
| Refined strips | Shows noisy context removal |
| Web fallback sources | Shows current-source correction when enabled |
| Citation coverage | Detects unsupported answer claims |
| Latency | Shows cost of adaptive routing and fallback |

## Failure Types

Track these failure categories:

| Failure type | Example |
| --- | --- |
| No evidence | Local index has no relevant document |
| Related but not answerable | Retrieved text is similar but lacks decisive evidence |
| Stale context | Local document is outdated for a current question |
| Conflicting evidence | Retrieved chunks disagree |
| Low citation coverage | Answer contains claims without sources |
| Web disabled | Query needs current information but Tavily is unavailable |

## Cost and Latency Table

| Mode | Avg latency | p95 latency | Avg estimated cost | Notes |
| --- | --- | --- | --- | --- |
| Baseline RAG | TBD | TBD | TBD | Local retrieval only |
| CRAG | TBD | TBD | TBD | Adds retrieval scoring and correction |
| Adaptive CRAG | TBD | TBD | TBD | Adds query routing and hierarchical retrieval |
| Adaptive CRAG + web | TBD | TBD | TBD | Uses Tavily only when configured |

## Next Upgrade

Add a trace writer that stores each run as JSONL in `outputs/traces.jsonl`, then summarize it in the Streamlit dashboard.

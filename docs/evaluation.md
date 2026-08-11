# Evaluation Guide

Corrective Agentic RAG Assistant includes a 30-question evaluation set at [`data/eval_questions.json`](../data/eval_questions.json). The set is designed to test retrieval quality, query routing, corrective actions, citation grounding, and graceful uncertainty.

## Evaluation Goals

| Goal | What to inspect |
| --- | --- |
| Query routing | Whether the router identifies `simple`, `multi_hop`, `long_context`, `web_needed`, or `out_of_domain` queries |
| Retrieval quality | Whether retrieved chunks contain decisive evidence instead of merely related text |
| CRAG action quality | Whether the system chooses `correct`, `ambiguous`, `incorrect`, or web fallback appropriately |
| Faithfulness | Whether final claims are supported by selected context |
| Citation coverage | Whether answer claims point back to local chunks or web sources |
| Safety | Whether unsupported or private-data-style questions are refused or marked uncertain |

## Dataset Shape

Each item contains:

```json
{
  "id": "crag_multi_005",
  "question": "How do Adaptive-RAG routing and CRAG correction work together?",
  "query_type": "multi_hop",
  "expected_route": "ambiguous",
  "expected_evidence": ["query router", "retrieval evaluator", "corrective action"],
  "quality_checks": ["answer_explains_pipeline", "answer_uses_citations"]
}
```

## Suggested Scoring

| Metric | Simple scoring rule |
| --- | --- |
| Router accuracy | 1 if predicted query type matches expected type, else 0 |
| Route accuracy | 1 if selected action matches or is compatible with expected route, else 0 |
| Evidence hit rate | Fraction of expected evidence terms present in selected context |
| Faithfulness | 1 if answer claims are supported by context, 0.5 if partly supported, 0 if unsupported |
| Citation coverage | Fraction of key claims with citations |
| Refusal safety | 1 if unsupported/private/out-of-domain questions are not hallucinated |

## Recommended Report Table

| Run | Router accuracy | Route accuracy | Evidence hit rate | Faithfulness | Citation coverage | Fallback rate | Avg latency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline RAG | TBD | TBD | TBD | TBD | TBD | N/A | TBD |
| Adaptive CRAG | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

Do not fill the table with guessed numbers. Run the evaluator, save outputs, and only publish observed results.

## Acceptance Targets

For a portfolio demo, target:

- Router accuracy >= 80% on the 30-question set.
- Adaptive CRAG improves evidence hit rate over baseline RAG.
- Unsupported/out-of-domain questions produce uncertainty or refusal instead of invented answers.
- Citation coverage is reported for every generated answer.

## Next Upgrade

Add an executable benchmark script that loads `data/eval_questions.json`, runs baseline RAG and Adaptive CRAG, then writes `outputs/eval_report.json` and `outputs/eval_report.csv`.

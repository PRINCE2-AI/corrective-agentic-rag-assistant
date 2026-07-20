from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from app.schemas import CragAction, EvalMetrics


@dataclass
class MetricsStore:
    actions: Counter[str] = field(default_factory=Counter)
    evals: list[EvalMetrics] = field(default_factory=list)

    def record(self, action: CragAction, metrics: EvalMetrics) -> None:
        self.actions[action.value] += 1
        self.evals.append(metrics)

    def snapshot(self) -> dict[str, object]:
        total = sum(self.actions.values())
        fallback_count = self.actions.get(CragAction.INCORRECT.value, 0) + self.actions.get(CragAction.AMBIGUOUS.value, 0)
        avg_latency = sum(metric.latency_ms for metric in self.evals) / max(len(self.evals), 1)
        avg_faithfulness = sum(metric.answer_faithfulness for metric in self.evals) / max(len(self.evals), 1)
        return {
            "total_queries": total,
            "action_counts": dict(self.actions),
            "fallback_rate": round(fallback_count / max(total, 1), 3),
            "average_latency_ms": round(avg_latency, 1),
            "average_faithfulness": round(avg_faithfulness, 3),
        }


metrics_store = MetricsStore()


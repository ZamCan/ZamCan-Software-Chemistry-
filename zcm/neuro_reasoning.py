"""Offline evidence-aware inference. Scores are heuristic, not probabilities."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Evidence:
    key: str
    source: str
    score: float
    status: str
    def __post_init__(self):
        if not self.key or not self.source or not isfinite(self.score) or not 0 <= self.score <= 1:
            raise ValueError("Invalid evidence")
        if self.status not in {"observed", "calculated", "predicted", "hypothesized"}:
            raise ValueError("Invalid evidence status")

@dataclass(frozen=True)
class Rule:
    name: str
    premises: tuple[str, ...]
    conclusion: str
    weight: float = 1.0
    def __post_init__(self):
        if not self.name or not self.premises or not self.conclusion or not 0 <= self.weight <= 1:
            raise ValueError("Invalid rule")

@dataclass(frozen=True)
class Inference:
    key: str
    score: float
    status: str
    sources: tuple[str, ...]
    trace: tuple[str, ...]

class ScientificReasoner:
    """Bounded forward chaining; no inference is promoted to observation."""
    def __init__(self, rules=()):
        self.rules = tuple(rules)

    def infer(self, evidence, max_rounds=32):
        if not 1 <= max_rounds <= 256:
            raise ValueError("Invalid iteration bound")
        known = {}
        for e in evidence:
            if e.key in known:
                raise ValueError("Duplicate evidence key; resolve conflicts explicitly")
            known[e.key] = Inference(e.key, e.score, e.status, (e.source,), ())
        for _ in range(max_rounds):
            changed = False
            for r in self.rules:
                if r.conclusion in known or not all(p in known for p in r.premises):
                    continue
                parents = [known[p] for p in r.premises]
                known[r.conclusion] = Inference(
                    r.conclusion, min(p.score for p in parents)*r.weight,
                    "predicted", tuple(sorted({s for p in parents for s in p.sources})),
                    tuple(dict.fromkeys(t for p in parents for t in p.trace)) + (r.name,))
                changed = True
            if not changed:
                return known
        if any(r.conclusion not in known and all(p in known for p in r.premises) for r in self.rules):
            raise RuntimeError("Inference iteration limit exceeded")
        return known

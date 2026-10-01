from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PredictionStatus(str, Enum):
    PREDICTED = "predicted"
    CONDITION_DEPENDENT = "condition_dependent"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass(frozen=True)
class ProductPrediction:
    status: PredictionStatus
    products: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReactionRule:
    reactants: frozenset[str]
    products: tuple[str, ...]
    reason: str
    condition_dependent: bool = True
    evidence: tuple[str, ...] = ()


_DEFAULT_RULES = (
    ReactionRule(
        reactants=frozenset({"H2", "O2"}),
        products=("H2O",),
        reason="Hydrogen and oxygen form water in a chemically established combination reaction; the actual rate and operating regime depend on conditions.",
        evidence=("established chemical reaction",),
    ),
)


class ProductPredictionEngine:
    name = "product_prediction"

    def __init__(self, rules: tuple[ReactionRule, ...] = _DEFAULT_RULES):
        self.rules = tuple(rules)

    def predict(
        self,
        reactants: tuple[str, ...],
        conditions: tuple[str, ...] = (),
    ) -> ProductPrediction:
        if not reactants:
            raise ValueError("at least one reactant is required")

        normalized = frozenset(item.strip() for item in reactants)
        for rule in self.rules:
            if normalized == rule.reactants:
                return ProductPrediction(
                    status=(
                        PredictionStatus.CONDITION_DEPENDENT
                        if rule.condition_dependent
                        else PredictionStatus.PREDICTED
                    ),
                    products=rule.products,
                    reasons=(rule.reason,),
                    conditions=conditions,
                    evidence=rule.evidence,
                )

        return ProductPrediction(
            status=PredictionStatus.INSUFFICIENT_DATA,
            reasons=(
                "No registered reaction rule matches the supplied reactant set. Product prediction requires an applicable rule, mechanism, thermodynamic basis, kinetic basis, or experimental evidence.",
            ),
            conditions=conditions,
        )


product_prediction_engine = ProductPredictionEngine()

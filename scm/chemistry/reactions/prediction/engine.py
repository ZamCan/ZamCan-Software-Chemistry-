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


class ProductPredictionEngine:
    name = "product_prediction"

    def predict(
        self,
        reactants: tuple[str, ...],
        conditions: tuple[str, ...] = (),
    ) -> ProductPrediction:
        if not reactants:
            raise ValueError("at least one reactant is required")

        return ProductPrediction(
            status=PredictionStatus.INSUFFICIENT_DATA,
            reasons=(
                "Products cannot be established from reactant formulas alone without an applicable chemical reaction rule, mechanism, thermodynamic basis, kinetic basis, or experimental evidence.",
            ),
            conditions=conditions,
        )


product_prediction_engine = ProductPredictionEngine()

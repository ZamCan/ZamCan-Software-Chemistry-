from __future__ import annotations

from scm.core import Quantity
from scm.chemistry.engine import ChemistryModule
from scm.chemistry.engine import CalculationResult, ResultStatus


class ChemistryCalculator(ChemistryModule):
    name = "calculator"

    def capabilities(self) -> frozenset[str]:
        return frozenset({
            "calculation",
            "quantity_arithmetic",
            "unit_aware_calculation",
        })

    def add(self, left: Quantity, right: Quantity) -> Quantity:
        return left + right

    def subtract(self, left: Quantity, right: Quantity) -> Quantity:
        return left - right

    def multiply(self, left: Quantity, right: Quantity) -> Quantity:
        return left * right

    def divide(self, left: Quantity, right: Quantity) -> Quantity:
        return left / right

    def calculate_addition(
        self,
        left: Quantity,
        right: Quantity,
    ) -> CalculationResult[Quantity]:
        try:
            value = self.add(left, right)
        except (TypeError, ValueError) as exc:
            return CalculationResult(
                status=ResultStatus.FAILURE,
                message=str(exc),
            )

        return CalculationResult(
            status=ResultStatus.SUCCESS,
            value=value,
        )


chemistry_calculator = ChemistryCalculator()

__all__ = [
    "ChemistryCalculator",
    "chemistry_calculator",
]

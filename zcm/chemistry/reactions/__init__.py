from __future__ import annotations

from scm.chemistry.engine import ChemistryModule
from scm.chemistry.engine import CalculationResult, ResultStatus
from scm.chemistry.reactions import (
    ChemicalEquation,
    ReactionAssessment,
    balance_equation,
    assess_reaction,
)


class ReactionWorkspace(ChemistryModule):
    name = "reactions"

    def capabilities(self) -> frozenset[str]:
        return frozenset({
            "equation_balancing",
            "reaction_assessment",
            "reaction_reasoning",
            "product_analysis",
        })

    def balance(
        self,
        reactants: tuple[str, ...],
        products: tuple[str, ...],
    ):
        equation = ChemicalEquation.from_formulas(
            reactants,
            products,
        )

        return balance_equation(equation)

    def assess(
        self,
        reactants: tuple[str, ...],
        products: tuple[str, ...] | None = None,
        conditions: tuple[str, ...] = (),
    ) -> ReactionAssessment:
        return assess_reaction(
            reactants=reactants,
            products=products,
            conditions=conditions,
        )

    def evaluate(
        self,
        reactants: tuple[str, ...],
        products: tuple[str, ...] | None = None,
        conditions: tuple[str, ...] = (),
    ) -> CalculationResult[ReactionAssessment]:
        assessment = self.assess(
            reactants=reactants,
            products=products,
            conditions=conditions,
        )

        if assessment.reasons:
            return CalculationResult(
                status=ResultStatus.WARNING,
                value=assessment,
                message=assessment.primary_reason.statement
                if assessment.primary_reason
                else None,
                reasons=tuple(
                    reason.statement
                    for reason in assessment.reasons
                ),
            )

        return CalculationResult(
            status=ResultStatus.SUCCESS,
            value=assessment,
        )


reaction_workspace = ReactionWorkspace()

__all__ = [
    "ReactionWorkspace",
    "reaction_workspace",
]

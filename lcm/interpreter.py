from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from scm.chemistry.reactions import balance_equation, assess_reaction, ChemicalEquation
from zcm.catalog.elements import element_catalog

from .intent import ChemicalIntent, IntentKind


@dataclass(frozen=True)
class Interpretation:
    intent: ChemicalIntent
    result: Any = None
    message: str | None = None

    @property
    def successful(self) -> bool:
        return self.result is not None


def interpret(intent: ChemicalIntent) -> Interpretation:
    if not isinstance(intent, ChemicalIntent):
        raise TypeError("intent must be a ChemicalIntent")

    if intent.kind is IntentKind.ELEMENT_LOOKUP:
        if intent.target is None:
            return Interpretation(intent, message="Element target is missing.")
        try:
            return Interpretation(intent, result=element_catalog.get(intent.target))
        except (KeyError, ValueError, TypeError) as exc:
            return Interpretation(intent, message=str(exc))

    if intent.kind is IntentKind.BALANCE_EQUATION:
        equation = ChemicalEquation.from_formulas(
            intent.reactants,
            intent.products,
        )
        return Interpretation(intent, result=balance_equation(equation))

    if intent.kind is IntentKind.REACTION_ASSESSMENT:
        return Interpretation(
            intent,
            result=assess_reaction(
                reactants=intent.reactants,
                products=intent.products or None,
                conditions=intent.conditions,
            ),
        )

    return Interpretation(
        intent,
        message="The language layer did not resolve a supported chemical intent.",
    )


__all__ = ["Interpretation", "interpret"]

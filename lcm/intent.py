from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IntentKind(str, Enum):
    ELEMENT_LOOKUP = "element_lookup"
    BALANCE_EQUATION = "balance_equation"
    REACTION_ASSESSMENT = "reaction_assessment"
    OXIDATION_STATE = "oxidation_state"
    MOLAR_MASS = "molar_mass"
    TITRATION = "titration"
    EQUILIBRIUM = "equilibrium"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ChemicalIntent:
    kind: IntentKind
    raw_text: str
    target: str | None = None
    reactants: tuple[str, ...] = ()
    products: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    confidence: float = 1.0
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.raw_text, str) or not self.raw_text.strip():
            raise ValueError("raw_text must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    @property
    def is_resolved(self) -> bool:
        return self.kind is not IntentKind.UNKNOWN

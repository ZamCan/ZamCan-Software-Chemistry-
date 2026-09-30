from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReactionOutcome(str, Enum):
    POSSIBLE = "possible"
    CONDITION_DEPENDENT = "condition_dependent"
    UNDETERMINED = "undetermined"
    NOT_SUPPORTED = "not_supported"


class ReactionReasonCode(str, Enum):
    THERMODYNAMIC = "thermodynamic"
    KINETIC = "kinetic"
    ELECTRONIC_STRUCTURE = "electronic_structure"
    NOBLE_GAS_STABILITY = "noble_gas_stability"
    OXIDATION_STATE = "oxidation_state"
    STOICHIOMETRIC = "stoichiometric"
    EQUILIBRIUM = "equilibrium"
    SOLUBILITY = "solubility"
    ACID_BASE = "acid_base"
    REDOX = "redox"
    CONDITION = "condition"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass(frozen=True)
class ReactionReason:
    code: ReactionReasonCode
    statement: str
    confidence: float | None = None


@dataclass(frozen=True)
class ReactionAssessment:
    outcome: ReactionOutcome
    reasons: tuple[ReactionReason, ...] = ()
    conditions: tuple[str, ...] = ()

    @property
    def primary_reason(self) -> ReactionReason | None:
        return self.reasons[0] if self.reasons else None


def assess_reaction(
    *,
    reactants: tuple[str, ...],
    products: tuple[str, ...] | None = None,
    conditions: tuple[str, ...] = (),
) -> ReactionAssessment:
    normalized = {
        item.strip().casefold()
        for item in reactants
    }

    noble_gases = {
        "he",
        "ne",
        "ar",
        "kr",
        "xe",
        "rn",
        "og",
    }

    present_noble_gases = normalized & noble_gases

    if present_noble_gases:
        return ReactionAssessment(
            outcome=ReactionOutcome.CONDITION_DEPENDENT,
            reasons=(
                ReactionReason(
                    ReactionReasonCode.NOBLE_GAS_STABILITY,
                    "The reactant set contains a noble gas. Its closed-shell electronic structure generally gives it very low chemical reactivity under ordinary conditions; any reaction claim requires examination of the specific partner and intensive conditions.",
                ),
            ),
            conditions=conditions,
        )

    if products is None:
        return ReactionAssessment(
            outcome=ReactionOutcome.UNDETERMINED,
            reasons=(
                ReactionReason(
                    ReactionReasonCode.INSUFFICIENT_DATA,
                    "Products cannot be established from reactants alone without a reaction-rule, mechanism, thermodynamic, kinetic, or experimental basis.",
                ),
            ),
            conditions=conditions,
        )

    return ReactionAssessment(
        outcome=ReactionOutcome.UNDETERMINED,
        reasons=(
            ReactionReason(
                ReactionReasonCode.INSUFFICIENT_DATA,
                "A balanced equation does not by itself establish that a reaction occurs. Chemical feasibility requires additional evidence such as thermodynamics, kinetics, mechanism, equilibrium, conditions, or experimental evidence.",
            ),
        ),
        conditions=conditions,
    )

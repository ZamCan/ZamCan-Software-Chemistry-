from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ValenceEvidence(str, Enum):
    ELECTRON_CONFIGURATION = "electron_configuration"
    COMMON_CHEMISTRY = "common_chemistry"
    OXIDATION_STATE = "oxidation_state"
    STRUCTURAL = "structural"
    INSUFFICIENT = "insufficient"


@dataclass(frozen=True)
class ValenceProfile:
    symbol: str
    valence_electrons: int | None
    common_valences: tuple[int, ...]
    common_oxidation_states: tuple[int, ...]
    evidence: tuple[ValenceEvidence, ...]
    explanation: str


# These are deliberately common-valence profiles, not universal maximum
# valence rules. Transition metals, hypervalent molecules, radicals and
# unusual coordination environments require deeper electronic structure.
COMMON_VALENCE: dict[str, ValenceProfile] = {
    "H": ValenceProfile("H", 1, (1,), (-1, 1), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "One valence electron; one conventional covalent bond commonly completes its 1s shell."),
    "C": ValenceProfile("C", 4, (4,), (-4, 2, 4), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Four valence electrons; tetravalent covalent bonding is common, with bonding governed by orbital and electronic structure."),
    "N": ValenceProfile("N", 5, (3, 5), (-3, 3, 5), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Five valence electrons; three covalent bonds with a lone pair are common, while multiple oxidation states occur."),
    "O": ValenceProfile("O", 6, (2,), (-2, 0, 1, 2), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Six valence electrons; two conventional covalent bonds commonly complete the valence-shell pattern."),
    "F": ValenceProfile("F", 7, (1,), (-1,), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Seven valence electrons; one conventional bond is common."),
    "Cl": ValenceProfile("Cl", 7, (1,), (-1, 1, 3, 5, 7), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Seven valence electrons; one covalent bond is common, with broader oxidation-state chemistry."),
    "Br": ValenceProfile("Br", 7, (1,), (-1, 1, 3, 5, 7), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Seven valence electrons; one conventional bond is common."),
    "I": ValenceProfile("I", 7, (1,), (-1, 1, 3, 5, 7), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Seven valence electrons; one conventional bond is common."),
    "S": ValenceProfile("S", 6, (2, 4, 6), (-2, 0, 2, 4, 6), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Six valence electrons; divalent bonding is common, while expanded and hypervalent descriptions occur in appropriate compounds."),
    "P": ValenceProfile("P", 5, (3, 5), (-3, 3, 5), (ValenceEvidence.ELECTRON_CONFIGURATION, ValenceEvidence.COMMON_CHEMISTRY), "Five valence electrons; three and five-coordinate covalent patterns occur in established chemistry."),
}


def valence_electron_count(symbol: str) -> int | None:
    profile = COMMON_VALENCE.get(symbol.strip())
    return None if profile is None else profile.valence_electrons


def get_valence_profile(symbol: str) -> ValenceProfile | None:
    return COMMON_VALENCE.get(symbol.strip())


def explain_bond_possibility(
    symbol_a: str,
    symbol_b: str,
    *,
    proposed_order: int = 1,
    electronegativity_difference: float | None = None,
) -> tuple[str, ...]:
    """Return a conservative, explainable screening rationale.

    This is a screening layer, not a universal reaction/bond predictor.
    A positive answer means the proposed bonding pattern is chemically
    plausible enough to send to a deeper electronic-structure model.
    """
    if proposed_order < 1:
        raise ValueError("proposed_order must be positive")

    a = get_valence_profile(symbol_a)
    b = get_valence_profile(symbol_b)
    reasons: list[str] = []

    if a is None or b is None:
        return (
            "At least one element lacks a registered valence profile.",
            "Electronic-structure, oxidation-state and experimental evidence are required.",
        )

    if proposed_order in a.common_valences or proposed_order in b.common_valences:
        reasons.append("The proposed bond order is compatible with at least one registered common-valence pattern.")
    else:
        reasons.append("The proposed bond order is outside the registered common-valence patterns and requires deeper electronic-structure evidence.")

    if electronegativity_difference is not None:
        if electronegativity_difference < 0:
            raise ValueError("electronegativity_difference must be nonnegative")
        if electronegativity_difference == 0:
            reasons.append("Equal electronegativity supports a nonpolar covalent description.")
        else:
            reasons.append("Electronegativity difference predicts unequal electron density; this changes polarity and ionic character continuously rather than imposing a hard bond-type boundary.")

    reasons.extend((
        "Orbital compatibility, electron count, geometry, charge, spin state and total-energy stabilization determine whether the bond actually forms.",
        "A valence count alone cannot prove a bond is possible or impossible.",
    ))
    return tuple(reasons)

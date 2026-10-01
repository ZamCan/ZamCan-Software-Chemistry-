"""Conservative oxidation-state assignment utilities.

Oxidation state is a formal bookkeeping concept and is intentionally kept
separate from formal charge and valence. Ambiguous cases are returned as
ambiguous instead of guessed.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence
import re

class OxidationStatus(str, Enum):
    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    INSUFFICIENT_DATA = "insufficient_data"

@dataclass(frozen=True)
class OxidationAssignment:
    symbol: str
    state: int | None
    status: OxidationStatus
    reason: str

@dataclass(frozen=True)
class OxidationStateResult:
    formula: str
    assignments: tuple[OxidationAssignment, ...]
    status: OxidationStatus
    charge: int = 0
    reason: str = ""

_COMMON = {
    "F": (-1,), "O": (-2,), "H": (1,), "Li": (1,), "Na": (1,), "K": (1,),
    "Rb": (1,), "Cs": (1,), "Mg": (2,), "Ca": (2,), "Sr": (2,), "Ba": (2,),
    "Al": (3,), "Zn": (2,), "Ag": (1,),
}

def _parse(formula: str) -> list[tuple[str,int]]:
    tokens = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    if not tokens or "".join(s + (str(n) if n != "" else "") for s,n in tokens) != formula:
        raise ValueError(f"Unsupported formula: {formula}")
    return [(s, int(n or 1)) for s,n in tokens]

def assign_oxidation_states(formula: str, charge: int = 0) -> OxidationStateResult:
    parts = _parse(formula)
    fixed: dict[str,int] = {}
    for s,_ in parts:
        if s in _COMMON and s not in fixed:
            fixed[s] = _COMMON[s][0]
    # H/O exceptions are handled conservatively for compounds containing metals.
    if "H" in fixed and any(s in parts for s in ("F","O")):
        fixed["H"] = 1
    unknown = [(s,n) for s,n in parts if s not in fixed]
    if not unknown:
        total = sum(n*fixed[s] for s,n in parts)
        if total != charge:
            return OxidationStateResult(formula, tuple(
                OxidationAssignment(s, fixed[s], OxidationStatus.AMBIGUOUS,
                                    "Fixed-rule sum conflicts with specified charge")
                for s,_ in parts), OxidationStatus.AMBIGUOUS, charge,
                "No oxidation-state assignment satisfies the specified charge.")
        return OxidationStateResult(formula, tuple(
            OxidationAssignment(s, fixed[s], OxidationStatus.RESOLVED, "Standard bookkeeping rule")
            for s,_ in parts), OxidationStatus.RESOLVED, charge, "Resolved from standard rules.")
    if len({s for s,_ in unknown}) == 1:
        s = unknown[0][0]
        n = sum(c for x,c in parts if x == s)
        remainder = sum(c*fixed[x] for x,c in parts if x != s)
        if n and (charge-remainder) % n == 0:
            state = (charge-remainder)//n
            return OxidationStateResult(formula, tuple(
                OxidationAssignment(x, state if x == s else fixed[x], OxidationStatus.RESOLVED,
                                    "Charge balance with standard fixed states")
                for x,_ in parts), OxidationStatus.RESOLVED, charge,
                "One unknown oxidation state resolved by charge balance.")
    return OxidationStateResult(formula, tuple(
        OxidationAssignment(s, fixed.get(s), OxidationStatus.AMBIGUOUS if s in fixed else OxidationStatus.INSUFFICIENT_DATA,
                            "Multiple oxidation-state solutions or insufficient chemical context")
        for s,_ in parts), OxidationStatus.AMBIGUOUS, charge,
        "Oxidation states require additional structural/contextual evidence.")

def oxidation_state_sum(formula: str, assignments: Mapping[str,int]) -> int:
    return sum(n*assignments[s] for s,n in _parse(formula))

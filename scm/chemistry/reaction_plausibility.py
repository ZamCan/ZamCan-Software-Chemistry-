"""Evidence-aware reaction checks; never claim products from element names alone."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Mapping

class PlausibilityStatus(str,Enum): PLAUSIBLE='plausible'; CONDITION_DEPENDENT='condition_dependent'; CONTRADICTED='contradicted'; INSUFFICIENT_DATA='insufficient_data'
@dataclass(frozen=True)
class ReactionAssessment:
    status:PlausibilityStatus
    checks:tuple[tuple[str,bool|None,str],...]
    explanation:str

def assess_reaction(*, atom_balance: bool|None, charge_balance: bool|None, evidence_available: bool=False, conditions_known: bool=False, energetic_support: bool|None=None, kinetic_support: bool|None=None)->ReactionAssessment:
    checks=(('atom_balance',atom_balance,'Elemental conservation'),('charge_balance',charge_balance,'Net-charge conservation'),('energetics',energetic_support,'Thermodynamic support'),('kinetics',kinetic_support,'Kinetic feasibility'))
    if atom_balance is False or charge_balance is False:
        return ReactionAssessment(PlausibilityStatus.CONTRADICTED,checks,'Conservation check failed; reaction representation must be corrected.')
    if atom_balance is not True or charge_balance is not True:
        return ReactionAssessment(PlausibilityStatus.INSUFFICIENT_DATA,checks,'Atom and charge conservation must both be verified.')
    if energetic_support is False:
        return ReactionAssessment(PlausibilityStatus.CONDITION_DEPENDENT,checks,'Energetic support is absent under the supplied model; consider conditions and model limitations.')
    if not evidence_available or energetic_support is None or kinetic_support is None:
        return ReactionAssessment(PlausibilityStatus.INSUFFICIENT_DATA,checks,'Balanced equations alone do not establish that a reaction occurs.')
    if kinetic_support is False:
        return ReactionAssessment(PlausibilityStatus.CONDITION_DEPENDENT,checks,'The supplied kinetic evidence does not support an appreciable rate under these conditions.')
    if not conditions_known:
        return ReactionAssessment(PlausibilityStatus.CONDITION_DEPENDENT,checks,'Evidence supports further consideration, but conditions are unspecified.')
    return ReactionAssessment(PlausibilityStatus.PLAUSIBLE,checks,'Available evidence supports plausibility; this is not proof of experimental occurrence.')

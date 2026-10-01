from dataclasses import dataclass
from enum import Enum
class SafetyLevel(str,Enum): INFORMATIONAL='informational'; CAUTION='caution'; BLOCKED='blocked'
@dataclass(frozen=True)
class SafetyDecision:
    level:SafetyLevel
    reason:str
    requires_human_review:bool=True
def assess_operation(operation,known_hazards=()):
    if known_hazards: return SafetyDecision(SafetyLevel.CAUTION,'Known hazards require human review.')
    return SafetyDecision(SafetyLevel.INFORMATIONAL,'No hazard records were supplied; absence of data is not proof of safety.')

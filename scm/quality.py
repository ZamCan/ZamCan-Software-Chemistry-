from dataclasses import dataclass
from enum import Enum
import math
class QualityStatus(str,Enum): ACCEPTED='accepted'; WARNING='warning'; REJECTED='rejected'
@dataclass(frozen=True)
class ValidationIssue:
    code:str
    message:str
    severity:QualityStatus
@dataclass(frozen=True)
class ValidationReport:
    issues:tuple[ValidationIssue,...]
    @property
    def accepted(self): return not any(x.severity is QualityStatus.REJECTED for x in self.issues)
def validate_finite(value,name):
    if not math.isfinite(value): return ValidationIssue('nonfinite',f'{name} is not finite',QualityStatus.REJECTED)
    return None

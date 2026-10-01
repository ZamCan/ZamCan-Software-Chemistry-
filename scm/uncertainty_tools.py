from dataclasses import dataclass
import math
@dataclass(frozen=True)
class UncertaintyResult:
    value:float
    standard_uncertainty:float
def propagate_independent_sum(values,uncertainties):
    if len(values)!=len(uncertainties): raise ValueError('length mismatch')
    if any(u<0 for u in uncertainties): raise ValueError('uncertainty must be nonnegative')
    return UncertaintyResult(sum(values),math.sqrt(sum(u*u for u in uncertainties)))
def propagate_product(value,relative_uncertainties):
    if value==0: raise ValueError('value must be nonzero')
    if any(u<0 for u in relative_uncertainties): raise ValueError('uncertainty must be nonnegative')
    return UncertaintyResult(value,abs(value)*math.sqrt(sum(u*u for u in relative_uncertainties)))

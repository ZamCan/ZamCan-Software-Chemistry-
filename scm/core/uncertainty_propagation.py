"""First-order uncertainty propagation for independent measured inputs."""
from __future__ import annotations
from dataclasses import dataclass
import math
from collections.abc import Callable, Sequence

@dataclass(frozen=True)
class UncertainValue:
    value: float
    standard_uncertainty: float
    def __post_init__(self):
        if not math.isfinite(self.value): raise ValueError('value must be finite')
        if not math.isfinite(self.standard_uncertainty) or self.standard_uncertainty < 0: raise ValueError('standard uncertainty must be finite and nonnegative')

@dataclass(frozen=True)
class PropagationResult:
    value: float
    standard_uncertainty: float
    method: str = 'first-order independent-input propagation'

def propagate_independent(function: Callable[..., float], inputs: Sequence[UncertainValue], *, relative_step: float = 1e-6) -> PropagationResult:
    if not inputs: raise ValueError('at least one uncertain input is required')
    if relative_step <= 0 or not math.isfinite(relative_step): raise ValueError('relative_step must be finite and positive')
    x=[item.value for item in inputs]
    y=float(function(*x))
    if not math.isfinite(y): raise ValueError('function result must be finite')
    variance=0.0
    for i,item in enumerate(inputs):
        if item.standard_uncertainty == 0: continue
        h=max(abs(x[i])*relative_step,relative_step)
        plus=x.copy(); minus=x.copy(); plus[i]+=h; minus[i]-=h
        fp=float(function(*plus)); fm=float(function(*minus))
        if not math.isfinite(fp) or not math.isfinite(fm): raise ValueError('function must remain finite near each input')
        derivative=(fp-fm)/(2*h)
        variance+=(derivative*item.standard_uncertainty)**2
    return PropagationResult(y,math.sqrt(variance))
